# 对话历史记录

这个目录用于存储与AI助手的重要开发会话记录，帮助在不同机器或不同会话中延续上下文。

## 📁 文件组织

```
chat_history/
├── README.md                           # 本文件
├── 2025-01-24_ci_fix_session.md      # CI修复会话记录
└── [future sessions...]
```

## 🎯 用途

1. **上下文延续** - 在新机器或新会话中快速了解之前的工作
2. **问题追溯** - 记录问题诊断和解决过程
3. **知识沉淀** - 保存技术要点和最佳实践
4. **团队协作** - 分享开发决策和思路

## 📝 如何使用

### 在新机器上继续开发

1. **克隆仓库**
   ```bash
   git clone <repo-url>
   cd zxtMaya_Suite
   git submodule update --init --recursive
   ```

2. **阅读最近的会话记录**
   ```bash
   # 查看所有会话记录
   ls docs/chat_history/
   
   # 阅读最新的会话
   cat docs/chat_history/2025-01-24_ci_fix_session.md
   ```

3. **与AI助手继续对话**
   - 在Cursor中打开项目
   - 告诉AI："我想继续之前的[主题]工作，请先阅读 `docs/chat_history/[日期]_[主题].md`"
   - AI会根据记录了解上下文并继续工作

### 记录新会话

当完成重要开发工作后：

1. **创建会话记录**
   ```bash
   # 命名格式：YYYY-MM-DD_topic_session.md
   touch docs/chat_history/2025-01-25_feature_implementation.md
   ```

2. **记录内容建议**
   - 会话日期和主题
   - 解决的问题
   - 做出的决策
   - 修改的文件
   - 提交记录
   - 技术要点
   - 下一步计划

3. **提交到仓库**
   ```bash
   git add docs/chat_history/
   git commit -m "docs: add [topic] session history"
   git push
   ```

## 📋 会话记录模板

```markdown
# [主题]开发会话记录
**日期**: YYYY-MM-DD  
**主题**: 简短描述

## 会话概览
[本次会话主要做了什么]

## 问题与解决
### 问题1
- **现象**: 
- **原因**: 
- **解决**: 

## 提交记录
- `hash` - commit message

## 技术要点
[关键知识点]

## 下一步
[未完成的工作或后续计划]
```

## 🔗 相关文档

- [AGENTS.md](../AGENTS.md) - 开发指南
- [session_notes.md](../session_notes.md) - 项目进度
- [dev_workflow.md](../dev_workflow.md) - 开发流程

## ⚠️ 注意事项

1. **不要包含敏感信息** - 密码、token、个人路径等
2. **保持简洁** - 记录关键信息，不是完整对话
3. **及时更新** - 重要会话结束后立即记录
4. **使用Markdown** - 便于阅读和版本控制

---

💡 **提示**: 这个目录的存在，让你可以在任何地方、任何时间无缝继续你的开发工作！

