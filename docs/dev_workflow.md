# 开发流程速览

以下流程用于日常维护 zxtMaya_* 系列仓库（包含 zxtMaya_Validate 等）及主套件 zxtMaya_Suite：

1. **同步主仓与子模块**  
   - git pull 更新 zxtMaya_Suite。  
   - git submodule update --init --recursive 保证子模块在本地存在。  
   - 如果只计划改某个子仓，例如 	ools/zxtMaya_Validate，进入对应目录再执行 git pull origin main，无需同时更新所有子模块。

2. **在目标子仓开发**  
   - 在子仓内完成代码修改、运行脚本或测试。  
   - git status 确认变更，使用 git commit、git push origin main 将该仓的改动推送到 GitHub。

3. **回到套件更新引用**  
   - 返回 zxtMaya_Suite 根目录，git status 会显示子模块指针已更新。  
   - 若需要调整 suite_manifest.json、modules/maya2024/MyMayaSuite.mod、docs/integration_plan.md 等文件，请在主仓完成修改，并运行：  
     - python tools/generate_mod.py --validate  
     - python tools/generate_mod.py --maya 2024（或其他版本）
   - git commit -am "<说明>" 记录子模块指针及相关文件的更新，最后 git push origin main。

4. **循环上述步骤**  
   - 每次迭代都先同步主仓，再进入具体工具仓开发，最后回到主仓更新指针和文档，保持各仓历史清晰独立。

> 提示：只有在需要查看或修改时，才拉取其他 zxtMaya_* 子仓。这样可减少不必要的冲突与更新量。
