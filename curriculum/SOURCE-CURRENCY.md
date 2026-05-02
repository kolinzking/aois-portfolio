# AOIS Source Currency

Fast-moving AI infrastructure topics must be checked against official or primary sources during authoring.

This file records the baseline source families to use. Individual lessons should add narrower source notes when authored.

## Baseline Official Sources

| Domain | Source |
|---|---|
| Kubernetes workloads, probes, resources, and cluster behavior | <https://kubernetes.io/docs/> |
| OpenTelemetry traces, metrics, logs, collector, and semantic concepts | <https://opentelemetry.io/docs/> |
| vLLM serving, metrics, batching, and runtime behavior | <https://docs.vllm.ai/> |
| NVIDIA GPU Operator and Kubernetes GPU node management | <https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/> |
| NVIDIA Triton Inference Server | <https://docs.nvidia.com/deeplearning/triton-inference-server/> |
| Model Context Protocol specification and server primitives | <https://modelcontextprotocol.io/specification/> |
| Temporal durable execution and workflow model | <https://docs.temporal.io/> |
| LangGraph durable execution, persistence, and agent orchestration | <https://docs.langchain.com/oss/python/langgraph/> |
| OpenAI API, model behavior, structured outputs, tools, and safety guidance | <https://platform.openai.com/docs/> |

## Authoring Rule

When a lesson depends on current behavior, add a `Source Notes` section to `notes.md` with:

- source name
- URL
- date checked
- what claim the source supports

## Durable Principle Rule

When possible, teach durable principles first:

- what problem the tool solves
- where it sits in AOIS
- what operational failure it introduces
- how to observe and constrain it

Then teach tool-specific commands or APIs.
This keeps the curriculum useful even when specific tools change.
<!-- AOIS-NAV-START -->
---

## Navigation

- Reading order: [AOIS Reading Order](READING-ORDER.md)
- Previous: [AOIS Codex Live Teacher Mode](CODEX-GUIDE-MODE.md)
- Next: [AOIS Repository Blueprint](REPO-BLUEPRINT.md)
<!-- AOIS-NAV-END -->
