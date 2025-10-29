#!/usr/bin/env python
"""Environment resolver for zxt tool suites."""
from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

try:
    import yaml  # type: ignore
except ImportError:
    sys.stderr.write("PyYAML is required to run setup_env.py\n")
    sys.exit(1)

REPO_ROOT = Path(__file__).resolve().parents[1]
if platform.system() == "Windows":
    DEFAULT_CACHE = Path(os.environ.get("APPDATA", "")) / "zxtTools" / "bundle_cache"
else:
    DEFAULT_CACHE = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "zxtTools" / "bundle_cache"

ENV_VAR_MAP = {
    "python": "PYTHONPATH",
}


class ResolveError(RuntimeError):
    """Raised when resolving packages fails."""


def load_config(config_path: Path) -> Dict:
    if not config_path.exists():
        raise ResolveError(f"Configuration file not found: {config_path}")
    try:
        return yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise ResolveError(f"Failed to parse {config_path}: {exc}") from exc


def select_packages(config: Dict, env: str | None) -> Dict[str, List[Tuple[str, Dict]]]:
    package_defs = config.get("packages", {})
    environments = config.get("environments", {})

    selected: Dict[str, List[Tuple[str, Dict]]] = {}

    def add_package(category: str, name: str) -> None:
        category_map = package_defs.get(category)
        if not category_map:
            raise ResolveError(f"Package category {category!r} not defined for {name!r}")
        pkg = category_map.get(name)
        if not pkg:
            raise ResolveError(f"Package {name!r} not found in category {category!r}")
        selected.setdefault(category, []).append((name, pkg))

    def apply_environment(env_name: str) -> None:
        env_def = environments.get(env_name)
        if env_def is None:
            raise ResolveError(f"Environment {env_name!r} not defined in requirements config")
        inherits = env_def.get("inherits")
        if inherits:
            parents = [inherits] if isinstance(inherits, str) else inherits
            for parent in parents:
                apply_environment(parent)
        for category, names in env_def.items():
            if category == "inherits":
                continue
            for name in names or []:
                add_package(category, name)

    target_env = env or "default"
    if target_env in environments:
        apply_environment(target_env)
    else:
        for category, mapping in package_defs.items():
            for name, pkg in mapping.items():
                selected.setdefault(category, []).append((name, pkg))

    if not selected:
        raise ResolveError("No packages selected; check requirements configuration")
    return selected


def ensure_git_package(destination: Path, url: str, reference: str | None) -> Path:
    if destination.exists():
        try:
            subprocess.run(
                ["git", "-C", str(destination), "fetch", "--tags", "--prune"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as exc:
            raise ResolveError(
                f"Failed to fetch git repo at {destination}: {exc.stderr.decode()}"
            ) from exc
    else:
        try:
            subprocess.run(["git", "clone", url, str(destination)], check=True)
        except subprocess.CalledProcessError as exc:
            raise ResolveError(f"Failed to clone {url}: {exc}") from exc

    if reference:
        try:
            subprocess.run(
                ["git", "-C", str(destination), "checkout", reference],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except subprocess.CalledProcessError as exc:
            raise ResolveError(
                f"Failed to checkout {reference} in {destination}: {exc.stderr.decode()}"
            ) from exc
    return destination


def resolve_package(name: str, category: str, spec: Dict, cache_root: Path) -> Path:
    location = spec.get("location") or {}
    loc_type = (location.get("type") or "").lower()
    if not loc_type:
        raise ResolveError(f"Package {name} missing location.type")

    if loc_type == "path":
        rel_path = location.get("path")
        if not rel_path:
            raise ResolveError(f"Package {name} location.path missing")
        path = (REPO_ROOT / rel_path).resolve()
        if not path.exists():
            raise ResolveError(f"Package {name} path not found: {path}")
        return path

    cache_id = location.get("cache_id") or f"{name}-{spec.get('version', 'latest')}"
    destination = cache_root / cache_id

    if loc_type == "git":
        url = location.get("url")
        if not url:
            raise ResolveError(f"Package {name} git location missing url")
        reference = location.get("reference")
        return ensure_git_package(destination, url, reference)

    raise ResolveError(f"Unsupported location type {loc_type!r} for package {name}")


def build_env_updates(selected: Dict[str, List[Tuple[str, Dict]]], cache_root: Path) -> Dict[str, List[str]]:
    env_updates: Dict[str, List[str]] = {}
    for category, items in selected.items():
        env_var = ENV_VAR_MAP.get(category)
        if not env_var:
            continue
        for name, spec in items:
            resolved = resolve_package(name, category, spec, cache_root)
            env_updates.setdefault(env_var, []).append(str(resolved))
    return env_updates


def format_env_updates(env_updates: Dict[str, List[str]], fmt: str) -> str:
    if fmt == "json":
        return json.dumps(env_updates, indent=2)
    if fmt == "text":
        lines = [f"{key}={os.pathsep.join(paths)}" for key, paths in env_updates.items()]
        return os.linesep.join(lines)
    if fmt == "bat":
        lines = [f'set "{key}={os.pathsep.join(paths)};%{key}%"' for key, paths in env_updates.items()]
        return os.linesep.join(lines)
    if fmt == "shell":
        lines = [f'export {key}="{os.pathsep.join(paths)}:${key}"' for key, paths in env_updates.items()]
        return '\n'.join(lines)
    raise ResolveError(f"Unsupported output format: {fmt}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Resolve suite package requirements.")
    parser.add_argument("--env", help="environment name defined in requirements/environments (e.g. maya)")
    parser.add_argument("--config", default="requirements/packages.yaml", help="path to YAML config file")
    parser.add_argument("--cache", help="override bundle cache directory")
    parser.add_argument("--format", choices=["json", "text", "bat", "shell"], default="text", help="output format")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    config_path = (REPO_ROOT / args.config).resolve()
    try:
        config = load_config(config_path)
        selected = select_packages(config, args.env)
        cache_root = Path(args.cache).resolve() if args.cache else DEFAULT_CACHE
        cache_root.mkdir(parents=True, exist_ok=True)
        env_updates = build_env_updates(selected, cache_root)
        output = format_env_updates(env_updates, args.format)
        if output:
            print(output)
    except ResolveError as exc:
        sys.stderr.write(f"setup_env: {exc}\n")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
