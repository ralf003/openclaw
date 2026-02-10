# AI 贡献说明

## 问题：openclaw 的贡献者中叫 "claude" 的是属于 Anthropic 公司的人吗？还是它只是一个 AI 工具直接提交代码？

### 简短回答

在 OpenClaw 的贡献背景下，当你看到 "claude" 或 AI 辅助贡献的引用时，这些通常指的是 **Anthropic 公司开发的 Claude AI 工具**被用来协助人类开发者，**而不是** Anthropic 公司的员工直接提交代码。

### 理解 AI 辅助贡献

OpenClaw 在 [CONTRIBUTING.md](../../CONTRIBUTING.md) 中明确欢迎 AI 辅助的贡献：

> **AI/Vibe-Coded PRs Welcome! 🤖**
> 
> Built with Codex, Claude, or other AI tools? **Awesome - just mark it!**

### 如何识别不同类型的贡献者

#### 1. **人类贡献者**
- 拥有人类名字的普通 GitHub 用户
- 例如：`Peter Steinberger` (steipete@gmail.com)
- 这些是真实的人，可能使用也可能不使用 AI 工具

#### 2. **AI 辅助的人类贡献**
- 使用 AI 工具（Claude、Codex、GitHub Copilot 等）的人类开发者
- 人类是记录在案的贡献者
- AI 工具是辅助工具，不是实际作者
- 应在 PR 描述中标记为 AI 辅助

#### 3. **机器人账户**
- 带有 `[bot]` 后缀的自动化工具
- 例如：`copilot-swe-agent[bot]`
- 这些是可能在底层使用 AI 的自动化工具

### Anthropic 的关联

- **Anthropic** 是创建 Claude AI 的公司
- **Claude** 是 Anthropic 制作的 AI 助手工具
- 当 PR 提到使用 "Claude" 创建时，意味着：
  - 人类开发者使用 Claude AI 工具来帮助编写代码
  - 人类仍然是贡献者和负责方
  - Anthropic（公司）并没有直接向 OpenClaw 贡献代码
  - 人类开发者将 Claude 作为编码助手来利用

### 归属指南

根据 OpenClaw 的贡献指南，AI 辅助的 PR 应该：

- ✅ 在 PR 标题或描述中标记为 AI 辅助
- ✅ 注明测试程度（未测试/轻度测试/完全测试）
- ✅ 如果可能，包含提示词或会话日志
- ✅ 确认贡献者理解代码的作用

### 示例场景

#### 场景 1："使用 Claude 创建的 PR"
- **含义**：人类开发者使用 Claude AI 帮助编写代码
- **归属**：人类开发者是贡献者
- **Anthropic 的角色**：AI 工具的提供者，而不是实际贡献者

#### 场景 2：GitHub 用户名为 "claude"
- **如果找到**：会是一个选择该用户名的人类
- **未找到**：在大多数情况下不存在这样的用户
- **实际用法**：OpenClaw 上下文中对 "claude" 的引用通常指 AI 工具

#### 场景 3："1577 个 Anthropic PR"
- **可能含义**：1577 个由 Claude AI（Anthropic 的产品）辅助的 PR
- **不是指**：来自 Anthropic 员工的 1577 个 PR
- **实际情况**：这些是由 AI 工具增强的社区贡献

### 总结

在 OpenClaw 生态系统中：

1. **"Claude" 引用** → Anthropic 的 AI 工具，不是一个人
2. **AI 辅助贡献** → 使用 AI 工具的人类，人类是贡献者
3. **Anthropic 的角色** → AI 工具提供者，不是直接代码贡献者
4. **透明度** → OpenClaw 鼓励清楚地标记 AI 辅助的工作

该项目将 AI 作为生产力工具来接受，同时保持人类对所有贡献的责任和监督。

---

## 相关文档

- [CONTRIBUTING.md](../../CONTRIBUTING.md) - 完整的贡献指南
- [Models](../concepts/models.md) - 支持的 AI 模型（包括 Claude）
- [GitHub Discussions](https://github.com/openclaw/openclaw/discussions) - 社区讨论

---

*最后更新：2026-02-10*
