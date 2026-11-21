---
title: Agentic RAG platform
summary: A reusable framework for shipping document-grounded assistants, with routing, retrieval, tools, and short- and long-term memory built in.
order: 4
featured: false
stack: [LangGraph, RAG, Agentic AI, Tool calling, Agent memory, Framework design]
---

## The problem

Every new document-grounded assistant needs the same parts: deciding what a question needs, retrieving the right context, calling tools, and remembering the conversation. Rebuilding them per project is slow and makes quality inconsistent.

## What I built

A reusable agentic RAG framework with:

- **routing** to decide how each request should be handled,
- **retrieval** and **tool execution** as interchangeable steps,
- **conditional workflow orchestration** to branch on what each step returns.

## Memory

Assistants built on the framework keep two kinds of memory:

- **short-term memory** for context within the current conversation,
- **long-term memory** that carries context across conversations.

## Registries

**Configurable prompt and tool registries** let a new assistant be assembled from configuration instead of new code: pick the prompts, register the tools, and deploy.

## The result

New document-grounded assistants can be deployed quickly on a common foundation.
