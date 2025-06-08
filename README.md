# DevOps-LLM 项目简介

这是一个用于探索和实践大语言模型（LLM）在 DevOps 场景中应用的实验性项目。本项目演示了如何使用主流 SDK 和工具调用 LLM 服务，目前主要实现了对 `openai` 和 `litellm` 接口的支持，并为后续扩展 Function Call 和 [MCP](https://github.com/autogpt-archive/multi-agent-protocol) 协议打下基础。

## 📌 功能概览

| 模块 | 功能描述 |
|------|----------|
| LLM 调用 | 已实现，支持通过 `openai` 和 `litellm` 客户端调用远程大模型服务（如阿里云 DashScope、OpenAI 等） |
| Function Call | 待实现，计划支持本地函数自动调用机制 |
| MCP 协议 | 待实现，未来将集成 Multi Capability Protocol 实现多智能体协作 |

---

## 🧩 核心功能说明

### 1. LLM 调用（OpenAI / LiteLLM）

#### 当前功能：
- 使用 `openai` Python SDK 调用兼容 OpenAI API 的模型服务（如阿里云 DashScope）
- 使用 `litellm` 进行统一接口调用，支持多种后端（OpenAI、DashScope 等）

#### 示例文件：
- [test_openai_aliyun_llm.py](file://E:\project-code\Devops-LLM\src\test\test_openai_aliyun_llm.py)
- [test_litellm_aliyun_llm.py](file://E:\project-code\Devops-LLM\src\test\test_litellm_aliyun_llm.py)

#### 特点：
- 支持 system/user/assistant 角色对话
- 可切换不同模型（如 qwen-plus, gpt-3.5-turbo）
- 支持设置额外参数（如 enable_thinking）

---

## 🔐 配置管理

本项目使用 `.secrets.toml` 文件进行敏感信息管理，位于 `src/config/` 目录下，包含阿里云 DashScope 的 API Key 和模型配置。

示例配置如下：
```toml
# src/config/.secrets.toml
[litellm_qwen_plus]
model="openai/qwen-plus"
api_base = "https://dashscope.aliyuncs.com/compatible-mode/v1"
api_key = "<你的阿里云百炼平台的token>"

[openai_qwen_plus]
model="qwen-plus"
api_base = "https://dashscope.aliyuncs.com/compatible-mode/v1"
api_key = "<你的阿里云百炼平台的token>"
```

> ⚠️ 注意：请勿将 `.secrets.toml` 提交到版本控制中，它已加入 `.gitignore`。

---

## 📦 依赖管理

本项目使用 [`uv`](https://docs.astral.sh/uv/) 作为依赖管理和构建工具，替代了传统的 Poetry 或 pipenv。

### 安装依赖

```bash
uv sync
```

### 添加新依赖

```bash
uv add <package-name>
```

### 开发模式安装

```bash
uv develop
```

---

## 📁 目录结构

```
src/
├── config/
│   ├── .secrets.toml         # 敏感配置文件（未提交）
│   └── config_loader.py      # 配置加载模块
└── test/
    ├── test_openai_aliyun_llm.py     # 使用 openai SDK 调用阿里云 LLM
    └── test_litellm_aliyun_llm.py    # 使用 litellm 调用 LLM
```

> ⚠️ 注意：MCP 模块尚未开始开发，相关目录和文件暂未创建。

---

## ✅ 快速开始

运行测试示例：

```bash
uv run src/tests/test_litellm_aliyun_llm.py
```

---

## 📬 联系我们

如果你有任何问题或建议，请提交 Issue 或联系项目维护者。