---
title: HealthAera
summary: Multi-agent AI workflows for a HIPAA-aligned US healthcare platform, grounded in each patient’s reports and FHIR data.
order: 1
featured: true
period: Oct 2025 – Present
metric:
  value: "~12 s → ~2 s"
  label: time to first token after re-architecting the system
stack: [LangGraph, MCP, RAG, FHIR, Multi-agent systems, Latency optimization, LLM evals]
confidentiality: Client work under NDA. The client isn’t named, and no product UI or patient data is shown. The system design is my own engineering work.
---

## The problem

The platform needed to answer patients with responses grounded in their own medical context: their reports and their FHIR records. Requests fall into different kinds of work, from medical questions to navigation to managing plans and tasks, and each kind needs different context and different actions.

## What I built

I built AI workflows that read patient reports and FHIR data and hand each request to a specialized agent:

- a **medical agent** for health questions grounded in the patient’s own records,
- a **navigation agent**,
- a **plan and task agent** that can create tasks through MCP-based tool integration.

## Re-architecting for latency

The first version took roughly 12 seconds to produce its first token. Swapping one framework for another wasn’t going to fix that, so I re-architected the system: how the workflows are orchestrated, how the agents are structured, and the code behind them. The new design runs on LangGraph, with task creation handled through MCP.

Time to first token dropped to roughly 2 seconds. In a patient-facing product, that’s the difference between a response that feels broken and one that feels like a conversation.

## Evaluation

Healthcare responses have to be correct, not just fluent. The workflows are evaluated with Ragas, LangSmith, and Promptfoo to keep response quality measurable as they change.
