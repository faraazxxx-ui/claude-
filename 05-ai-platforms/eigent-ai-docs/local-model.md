[Skip to main content](https://docs.eigent.ai/core/models/local-model#content-area)

[Eigent Documentation home page![light logo](https://mintcdn.com/eigentai-0b34069f/c5JXrpK7XMq1z3Fm/images/logo-light.png?fit=max&auto=format&n=c5JXrpK7XMq1z3Fm&q=85&s=6e834644e7f72b581b80517ded8bfd50)![dark logo](https://mintcdn.com/eigentai-0b34069f/c5JXrpK7XMq1z3Fm/images/logo-dark.png?fit=max&auto=format&n=c5JXrpK7XMq1z3Fm&q=85&s=c4746a53b606e7323688e61df33aff03)](https://www.eigent.ai/)

Search...

Ctrl K

Search...

Navigation

Models

Models (Local Model)

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

- [Self-Host Model](https://docs.eigent.ai/core/models/local-model#self-host-model)
- [API KEY Reference](https://docs.eigent.ai/core/models/local-model#api-key-reference)

## [​](https://docs.eigent.ai/core/models/local-model\#self-host-model)  **Self-Host Model**

1. Configure your self-host model

First, you need to set up your local models and expose them as an **OpenAI-Compatible Server.**

```
#Vllm https://docs.vllm.ai/en/latest/getting_started/quickstart.html#openai-compatible-server
vllm serve Qwen/Qwen2.5-1.5B-Instruct
```

```
#SGLang https://docs.sglang.ai/backend/openai_api_completions.html
from sglang.test.test_utils import is_in_ci

if is_in_ci():
    from patch import launch_server_cmd
else:
    from sglang.utils import launch_server_cmd

from sglang.utils import wait_for_server, print_highlight, terminate_process

server_process, port = launch_server_cmd(
    "python3 -m sglang.launch_server --model-path qwen/qwen2.5-0.5b-instruct --host 0.0.0.0 --mem-fraction-static 0.8"
)

wait_for_server(f"http://localhost:{port}")
print(f"Server started on http://localhost:{port}")
```

```
#Ollama https://github.com/ollama/ollama
ollama pull qwen2.5:7b
```

```
# LLaMA.cpp server https://github.com/ggml-org/llama.cpp/tree/master/tools/server
./llama-server -m /path/to/model.gguf --host 0.0.0.0 --port 8080
```

2. Setting your model

![set_local_model](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/models_local_model.png)

3. Configure the Google Search toolkit

![configure_searchtools](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/models_configure_tools.png)![configure_searchtoolsapi](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/models_configure_tools_key.png) You can refer to the following document for detailed information on how to configure **GOOGLE\_API\_KEY** and **SEARCH\_ENGINE\_ID :** [https://developers.google.com/custom-search/v1/overview](https://developers.google.com/custom-search/v1/overview)

## [​](https://docs.eigent.ai/core/models/local-model\#api-key-reference)  **API KEY Reference**

Gemini: [https://ai.google.dev/gemini-api/docs/api-key](https://ai.google.dev/gemini-api/docs/api-key)OpenAI: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)Anthropic: [https://console.anthropic.com/](https://console.anthropic.com/)Qwen: [https://www.alibabacloud.com/help/en/model-studio/get-api-key](https://www.alibabacloud.com/help/en/model-studio/get-api-key)Deepseek: [https://platform.deepseek.com/api\_keys](https://platform.deepseek.com/api_keys)AWS Bedrock: [https://github.com/aws-samples/bedrock-access-gateway/blob/main/README.md](https://github.com/aws-samples/bedrock-access-gateway/blob/main/README.md)Azure: [https://azure.microsoft.com/products/cognitive-services/openai-service/](https://azure.microsoft.com/products/cognitive-services/openai-service/)

[Bring Your Own Key (BYOK)\\
\\
Previous](https://docs.eigent.ai/core/models/byok) [Gemini\\
\\
Next](https://docs.eigent.ai/core/models/gemini)

Ctrl+I

![set_local_model](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/models_local_model.png)

![configure_searchtools](https://mintlify.s3.us-west-1.amazonaws.com/eigentai-0b34069f/images/models_configure_tools.png)