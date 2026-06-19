# openclaw-dev — Claude Code 工作上下文

> 🔗 共享规则：`AGENTS.md`（本仓库项目级指令）。本文件为 CC 专用扩展，补充项目技术上下文。

## 项目简介
- **仓库用途**：OpenClaw 框架的鑫鑫智能 fork，用于向社区贡献 PR 和本地定制开发
- **上游**：`openclaw/openclaw`（GitHub 社区主仓库）
- **远程**：`git@github.com:ralf003/openclaw.git`（fork）
- **技术栈**：TypeScript + Node.js v24，npm/pnpm
- **关键依赖**：Express、SQLite（better-sqlite3）、WebSocket、Zod schema

## 构建与测试
```bash
# 安装依赖
pnpm install

# 构建
pnpm build

# 运行测试
pnpm test

# 快速验证单个文件
npx tsx src/path/to/file.ts

# 本地 lint
pnpm lint
```

**CI 关键点**：
- CI workflow：`.github/workflows/ci.yml`（上游 .github 目录）
- PR body checker 格式要求：`- **field name**: value`（bullet + bold + colon），不支持 `### heading`
- 提 PR 前必须：本地 lint + test 通过

## 关键架构决策

### 核心模块（提交 PR 相关）
| 模块 | 路径 | 职责 |
|------|------|------|
| Gateway 入口 | `src/gateway/server.impl.ts` | HTTP/WS 服务、插件加载 |
| 插件注册 | `src/gateway/plugin-registry.ts` | 插件发现、diagnostics、索引 |
| 配置解析 | `src/gateway/config/*.ts` | openclaw.json 加载/合并/验证 |
| Zod Schema | `src/gateway/schema/*.ts` | 配置/运行时数据 schema |
| 会话管理 | `src/gateway/sessions/*.ts` | Agent session lifecycle |

### 配置约定
- 生产配置：`D:\openclaw-data\openclaw.json`
- 插件目录：`D:\openclaw-data\node_modules\@openclaw\`
- SQLite 数据库：`D:\openclaw-data\state\openclaw.sqlite`
- Gateway 端口：18789（生产），使用隔离端口开发测试

### 模块边界
- **插件系统**：通过 `register()` hook 注册，`plugins.entries` 控制启用，`plugins.allow` 白名单
- **安全边界**：`sanitizeToolArgs` 是独立安全层——`redactSensitive: off` 只控制日志/transcript，不影响 tool payload 脱敏
- **Zod schema**：所有配置字段必须 v3 格式 `{ enabled: true, config: { ... } }`

## 已知技术债
- [ ] plugin diagnostics 清理不完整：卸载插件后 SQLite `diagnostics_json` 仍可能残留 "plugin path not found" 错误
- [ ] orphan diagnostic record 问题（PR #93975 已提交修复，等待社区 review）
- [ ] `allowInsecureAuth` 安全警告（低优先级）

## 当前工作
- **PR #93975**：orphan diagnostic 双补丁修复（discovery.ts 清理 + Zod schema code 字段），CI 全绿，等待社区 review
- **分支**：`fix/plugin-diagnostics-orphan-cleanup-v2`

## CC → OC 记忆回流

**每次 session 结束时**，将本 session 的关键决策/发现/编码产出增量追加到 `OC-MEMORY.md`：
1. 读取 `OC-MEMORY.md` 看上次记录截止位置
2. 追加新条目到 `## 回流日志` 下，格式：
   ```
   ### YYYY-MM-DD — session N
   - **(类型) 标题**：一句话描述
   - 关键决策/发现细节（1-3 行）
   ```
3. 更新 `> 最后更新` 时间戳
4. 不重复已有内容（基于日期+标题去重）

**回流内容类型**：
- 代码产出：修改了哪些文件、为什么
- 架构决策：选择了什么方案、为什么
- 发现：bug 根因、上游变更、新理解
- 决策：PR 提交/合并决定、技术选型

## 常见问题

### PR 提交检查清单
1. `pnpm lint` 无错误
2. `pnpm test` 全绿
3. CI workflow 已读（确认 checker 格式要求）
4. PR body 用 `- **field**: value` 格式
5. 有 real behavior proof（before/after 截图或日志）

### 隔离验证
开发时 5 个环境变量必须全设：
```powershell
$env:OPENCLAW_HOME = "D:\openclaw-data\isolated"
$env:OPENCLAW_STATE_DIR = "D:\openclaw-data\isolated\state"
$env:OPENCLAW_CONFIG_PATH = "D:\openclaw-data\isolated\openclaw.json"
$env:OPENCLAW_DISABLE_BUNDLED_PLUGINS = "1"
$env:HOME = "D:\openclaw-data\isolated\home"
```

### 不碰的生产配置
- 端口 18789 = 生产 Gateway，开发用其他端口
- `D:\openclaw-data\gateway.cmd` = 不修改
- `D:\openclaw-data\openclaw.json` = 小鑫管理，小林不直接改
