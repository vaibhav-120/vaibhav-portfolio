# Vaibhav Shrivastava

<!--
This file is everything the voice agent knows. Keep it to public facts only.
Never add client company names or anything under NDA: if it isn't here, the
agent can't say it. Keep it short, since every question sends the whole file.
-->

AI Engineer at Antier Solutions, based in Jalandhar, Punjab, India. Works on large language models, agentic systems, and real-time voice AI. Day to day: LangGraph and agentic orchestration, MCP-based tool integration, retrieval-augmented generation, real-time voice pipelines (speech to text, LLM, text to speech), LLM evaluation with Ragas, LangSmith, and Promptfoo, latency optimization, and backends in FastAPI and Django. Focus: autonomous, scalable AI agents that make decisions and take useful action, not just generate text. Contact: LinkedIn (Vaibhav Shrivastava). Most of his work is client work under NDA, so client companies are never named.

## Experience
- AI Assistant Engineer, Antier Solutions, full-time, January 2026 to present. Builds production AI systems across healthcare and real-time voice AI (HealthAera and Emnaar below).
- AI Intern, Antier Solutions, July to December 2025. LLM evaluation and optimization with Ragas and Promptfoo. Built a tender automation system that analyzes full tender documents to produce summaries, strengths and weaknesses, and resource gaps. After three months moved onto the HealthAera client project, then was brought on full-time.

## Education
B.Tech in Computer Science, DAV University, Jalandhar, 2021 to 2025, GPA above 8.5. Studied machine learning and deep learning, then transformer architectures, which led him to generative AI. Hands-on with Python, PyTorch, TensorFlow, Hugging Face, and vector databases like FAISS.

## Projects

HealthAera (October 2025 to present): AI workflows for a HIPAA-aligned US healthcare platform. Uses patient reports and FHIR data to give personalized responses through three specialized agents: medical, navigation, and plan and task. The plan and task agent creates tasks through MCP. He re-architected the system end to end, covering orchestration, agent structure, and code, not just the framework, and it now runs on LangGraph. Time to first token dropped from about 12 seconds to about 2 seconds.

Emnaar (January 2026 to present): a RAG-based telephony voice assistant for customer calls in English, Hindi, and Hinglish, including code-switching mid-sentence. Fully on-premise on the client's server, using open-source speech to text, LLM, and text to speech models. About 800 milliseconds from the end of the caller's turn to the first spoken response.

AI wallet layer: a natural-language interface for wallet and blockchain operations. Blockchain APIs are exposed to an agent as tools through an MCP server. Supports portfolio queries, transaction guidance, gas and slippage checks, conditional orders, and price alerts.

Agentic RAG platform: a reusable framework for building document-grounded assistants. Includes routing, retrieval, tool execution, conditional workflow orchestration, short-term memory within a conversation, long-term memory across conversations, and configurable prompt and tool registries so new assistants can be deployed quickly.

AI-powered LMS: live lectures where learners talk to an AI instructor by voice in real time over WebSockets, with live assessments that produce structured performance reports.

This assistant: runs on his portfolio. The browser converts speech to text, a FastAPI backend calls a Groq-hosted model with automatic fallback to a second model, and Piper turns the answer into speech sentence by sentence so the reply starts before it's fully written. Visitors talk to it hands-free and can interrupt it at any time.

## Skills
Core: LangGraph, agentic AI, retrieval-augmented generation, voice AI, tool calling, LLM evals, blockchain, WebSockets, backend development.
Also: LangChain, vector databases, Ragas, LangSmith, Promptfoo, FastAPI, Django, Django REST Framework, Docker, Hugging Face, TensorFlow, scikit-learn, NLP, machine learning, Python, Git.