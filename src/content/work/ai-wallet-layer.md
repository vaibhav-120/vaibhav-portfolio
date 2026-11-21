---
title: AI wallet layer
summary: A natural-language interface for wallet and blockchain operations, with blockchain APIs exposed to an agent through an MCP server.
order: 3
featured: false
stack: [Tool calling, MCP servers, Agentic AI, Blockchain, Natural-language interfaces]
confidentiality: Web3 client work. Described by approach; the client isn’t named.
---

## The problem

Wallet and on-chain operations are powerful but unforgiving. Users have to understand gas, slippage, and order mechanics before they can act safely.

## What I built

A natural-language layer where users say what they want and an agent works out how to do it. Blockchain APIs are integrated as agent tools through an MCP server, so the agent turns intent into tool calls instead of just generating text.

Supported workflows:

- portfolio queries,
- transaction guidance,
- gas and slippage checks,
- conditional orders,
- price alerts.

## Why it’s interesting

Most agent work is RAG and chat. Here the agent’s job is to act: pick the right tool, check the conditions, and guide an on-chain action. It’s agentic tool calling outside the usual chatbot pattern.
