[Skip to main content](https://docs.eigent.ai/core/models/byok#content-area)

[Eigent Documentation home page![light logo](https://mintcdn.com/eigentai-0b34069f/c5JXrpK7XMq1z3Fm/images/logo-light.png?fit=max&auto=format&n=c5JXrpK7XMq1z3Fm&q=85&s=6e834644e7f72b581b80517ded8bfd50)![dark logo](https://mintcdn.com/eigentai-0b34069f/c5JXrpK7XMq1z3Fm/images/logo-dark.png?fit=max&auto=format&n=c5JXrpK7XMq1z3Fm&q=85&s=c4746a53b606e7323688e61df33aff03)](https://www.eigent.ai/)

Search...

Ctrl K

Search...

Navigation

Models

Bring Your Own Key (BYOK)

[Documentation](https://docs.eigent.ai/get_started/welcome)

- [Download Here](https://www.eigent.ai/)

##### Get Started

- [Welcome](https://docs.eigent.ai/get_started/welcome)
- [Installation](https://docs.eigent.ai/get_started/installation)
- [Quick Start](https://docs.eigent.ai/get_started/quick_start)

##### Core

- [Concepts](https://docs.eigent.ai/core/concepts)
- [Workforce](https://docs.eigent.ai/core/workforce)
- Models

  - [Bring Your Own Key (BYOK)](https://docs.eigent.ai/core/models/byok)
  - [Models (Local Model)](https://docs.eigent.ai/core/models/local-model)
  - [Gemini](https://docs.eigent.ai/core/models/gemini)
  - [Ernie](https://docs.eigent.ai/core/models/ernie)
  - [MiniMax](https://docs.eigent.ai/core/models/minimax)
  - [Kimi](https://docs.eigent.ai/core/models/kimi)
  - [SambaNova](https://docs.eigent.ai/core/models/sambanova)
- [Tools](https://docs.eigent.ai/core/tools)
- [Workers](https://docs.eigent.ai/core/workers)
- [Agent Skills](https://docs.eigent.ai/core/agent-skills)

##### Troubleshooting

- [Support](https://docs.eigent.ai/troubleshooting/support)
- [Bug](https://docs.eigent.ai/troubleshooting/bug)

On this page

- [What is BYOK?](https://docs.eigent.ai/core/models/byok#what-is-byok)
- [OpenAI Configuration (Example)](https://docs.eigent.ai/core/models/byok#openai-configuration-example)
- [Step 1: Get Your API Key](https://docs.eigent.ai/core/models/byok#step-1-get-your-api-key)
- [Step 2: Configure in Eigent](https://docs.eigent.ai/core/models/byok#step-2-configure-in-eigent)
- [Configuration Fields](https://docs.eigent.ai/core/models/byok#configuration-fields)
- [Azure-Specific Fields](https://docs.eigent.ai/core/models/byok#azure-specific-fields)
- [Common Errors](https://docs.eigent.ai/core/models/byok#common-errors)
- [Supported Providers](https://docs.eigent.ai/core/models/byok#supported-providers)
- [Tips](https://docs.eigent.ai/core/models/byok#tips)

## [​](https://docs.eigent.ai/core/models/byok\#what-is-byok)  What is BYOK?

**Bring Your Own Key (BYOK)** allows you to use your own API keys from various AI model providers with Eigent. Instead of relying on a shared service, you connect directly to providers like OpenAI, Anthropic, or Google using your personal API credentials. This gives you:

- **Full control** over your API usage and billing
- **Direct access** to the latest models from each provider
- **Privacy** \- your requests go directly to the provider

## [​](https://docs.eigent.ai/core/models/byok\#openai-configuration-example)  OpenAI Configuration (Example)

### [​](https://docs.eigent.ai/core/models/byok\#step-1-get-your-api-key)  Step 1: Get Your API Key

1. Visit the [OpenAI API Keys page](https://platform.openai.com/api-keys)
2. Click **“Create new secret key”**
3. Copy the generated key (you won’t be able to see it again)

### [​](https://docs.eigent.ai/core/models/byok\#step-2-configure-in-eigent)  Step 2: Configure in Eigent

1. Launch Eigent and go to **Agent** \> **Models**
2. Find the **OpenAI** card in the Custom Model section

![byok_1](https://mintcdn.com/eigentai-0b34069f/c5JXrpK7XMq1z3Fm/images/byok_1.png?fit=max&auto=format&n=c5JXrpK7XMq1z3Fm&q=85&s=3c62c294c4271b1e7064fbaca6deccfe)

1. Fill in the following fields:

| Field | Value | Example |
| --- | --- | --- |
| **API Key** | Your OpenAI secret key | `sk-proj-xxxx...` |
| **API Host** | OpenAI API endpoint | `https://api.openai.com/v1` |
| **Model Type** | The model you want to use | `gpt-4o`, `gpt-4o-mini` |

4. Click **Save** to validate and store your configuration
5. Click **Set as Default** to use this provider for your agents

## [​](https://docs.eigent.ai/core/models/byok\#configuration-fields)  Configuration Fields

| Field | Description | Required |
| --- | --- | --- |
| **API Key** | Your authentication key from the provider | Yes |
| **API Host** | The API endpoint URL | Yes (pre-filled for most providers) |
| **Model Type** | The specific model variant to use | Yes |
| **External Config** | Provider-specific settings (e.g., Azure deployment name) | Only for certain providers |

### [​](https://docs.eigent.ai/core/models/byok\#azure-specific-fields)  Azure-Specific Fields

| Field | Description | Example |
| --- | --- | --- |
| **API Version** | Azure OpenAI API version | `2024-02-15-preview` |
| **Deployment Name** | Your Azure deployment name | `my-gpt4-deployment` |

## [​](https://docs.eigent.ai/core/models/byok\#common-errors)  Common Errors

When saving your configuration, Eigent validates your API key and model. Here are the errors you may encounter:

| Error | Cause | Solution |
| --- | --- | --- |
| **Invalid key. Validation failed.** | API key is incorrect, expired, or malformed | Double-check your API key. Regenerate a new key if needed. |
| **Invalid model name. Validation failed.** | The specified model does not exist or is not available for your account | Verify the model name is correct. Check if you have access to that model. |
| **You exceeded your current quota** | API quota exhausted or billing issue | Check your provider’s billing dashboard. Add credits or upgrade your plan. |

## [​](https://docs.eigent.ai/core/models/byok\#supported-providers)  Supported Providers

Eigent supports the following BYOK providers:

| Provider | Default API Host | Official Documentation |
| --- | --- | --- |
| **OpenAI** | `https://api.openai.com/v1` | [OpenAI API Docs](https://platform.openai.com/docs/api-reference) |
| **Anthropic** | `https://api.anthropic.com/` | [Anthropic API Docs](https://docs.anthropic.com/en/api/getting-started) |
| **Google Gemini** | `https://generativelanguage.googleapis.com/v1beta/openai/` | [Gemini API Docs](https://ai.google.dev/gemini-api/docs) |
| **OpenRouter** | `https://openrouter.ai/api/v1` | [OpenRouter Docs](https://openrouter.ai/docs) |
| **Qwen (Alibaba)** | `https://dashscope.aliyuncs.com/compatible-mode/v1` | [Qwen API Docs](https://help.aliyun.com/zh/dashscope/developer-reference/api-details) |
| **DeepSeek** | `https://api.deepseek.com` | [DeepSeek API Docs](https://platform.deepseek.com/api-docs) |
| **Minimax** | `https://api.minimax.io/v1` | [Minimax API Docs](https://platform.minimaxi.com/document/Announcement) |
| **Z.ai** | `https://api.z.ai/api/coding/paas/v4/` | [Z.ai Platform](https://z.ai/) |
| **Azure OpenAI** | _(user-provided)_ | [Azure OpenAI Docs](https://learn.microsoft.com/en-us/azure/ai-services/openai/reference) |
| **AWS Bedrock** | _(user-provided)_ | [AWS Bedrock Docs](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html) |
| **OpenAI Compatible** | _(user-provided)_ | For custom endpoints (e.g., xAI, local servers) |

## [​](https://docs.eigent.ai/core/models/byok\#tips)  Tips

- **Keep your API key secure** \- Never share or expose your API key publicly
- **Monitor usage** \- Check your provider’s dashboard regularly to track costs
- **Use appropriate models** \- Different models have different capabilities and pricing

[Workforce\\
\\
Previous](https://docs.eigent.ai/core/workforce) [Models (Local Model)\\
\\
Next](https://docs.eigent.ai/core/models/local-model)

Ctrl+I

![byok_1](https://mintcdn.com/eigentai-0b34069f/c5JXrpK7XMq1z3Fm/images/byok_1.png?w=840&fit=max&auto=format&n=c5JXrpK7XMq1z3Fm&q=85&s=fcf97f257fb8a33761c9ac91a5007215)