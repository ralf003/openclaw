# AI Contributions Clarification

## Question: Is "claude" a contributor from Anthropic, or is it the AI tool?

### Short Answer

In the context of OpenClaw contributions, when you see references to "claude" or AI-assisted contributions, these typically refer to **the Claude AI tool by Anthropic** being used to assist human developers, **not** an employee from Anthropic company directly submitting code.

### Understanding AI-Assisted Contributions

OpenClaw explicitly welcomes AI-assisted contributions as documented in [CONTRIBUTING.md](../../CONTRIBUTING.md):

> **AI/Vibe-Coded PRs Welcome! 🤖**
> 
> Built with Codex, Claude, or other AI tools? **Awesome - just mark it!**

### How to Identify Different Types of Contributors

#### 1. **Human Contributors**
- Regular GitHub users with human names
- Example: `Peter Steinberger` (steipete@gmail.com)
- These are actual people who may or may not use AI tools

#### 2. **AI-Assisted Human Contributions**
- Human developers using AI tools (Claude, Codex, GitHub Copilot, etc.)
- The human is the contributor of record
- AI tools are assistants, not the actual authors
- Should be marked in PR descriptions as AI-assisted

#### 3. **Bot Accounts**
- Automated tools with `[bot]` suffix
- Example: `copilot-swe-agent[bot]`
- These are automation tools that may use AI under the hood

### The Anthropic Connection

- **Anthropic** is the company that created Claude AI
- **Claude** is the AI assistant tool made by Anthropic
- When PRs mention being created with "Claude", it means:
  - A human developer used the Claude AI tool to help write code
  - The human is still the contributor and responsible party
  - Anthropic (the company) is not directly contributing to OpenClaw
  - The human developer is leveraging Claude as a coding assistant

### Attribution Guidelines

According to OpenClaw's contribution guidelines, AI-assisted PRs should:

- ✅ Mark as AI-assisted in the PR title or description
- ✅ Note the degree of testing (untested / lightly tested / fully tested)
- ✅ Include prompts or session logs if possible
- ✅ Confirm the contributor understands what the code does

### Example Scenarios

#### Scenario 1: "PR created with Claude"
- **Meaning**: A human developer used Claude AI to help write the code
- **Attribution**: The human developer is the contributor
- **Anthropic's role**: Provider of the AI tool, not the actual contributor

#### Scenario 2: GitHub user named "claude"
- **If found**: Would be a human who chose that username
- **Not found**: No such user exists in most cases
- **Actual usage**: References to "claude" in OpenClaw context typically mean the AI tool

#### Scenario 3: "1577 Anthropic PRs"
- **Likely meaning**: 1,577 PRs that were assisted by Claude AI (Anthropic's product)
- **Not meaning**: 1,577 PRs from Anthropic employees
- **Reality**: These are community contributions enhanced by AI tools

### Summary

In the OpenClaw ecosystem:

1. **"Claude" references** → The AI tool by Anthropic, not a person
2. **AI-assisted contributions** → Humans using AI tools, with humans as the contributors
3. **Anthropic's role** → AI tool provider, not direct code contributor
4. **Transparency** → OpenClaw encourages marking AI-assisted work clearly

The project embraces AI as a productivity tool while maintaining human responsibility and oversight for all contributions.

---

## Related Documentation

- [CONTRIBUTING.md](../../CONTRIBUTING.md) - Full contribution guidelines
- [Models](../concepts/models.md) - Supported AI models including Claude
- [GitHub Discussions](https://github.com/openclaw/openclaw/discussions) - Community discussion

---

*Last updated: 2026-02-10*
