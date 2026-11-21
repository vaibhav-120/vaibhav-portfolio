---
title: Emnaar
summary: An on-premise telephony voice assistant that holds customer conversations in English, Hindi, and Hinglish.
order: 2
featured: true
period: Jan 2026 – Present
metric:
  value: "~800 ms"
  label: from the end of a caller’s turn to the first spoken response
stack: [Voice AI, STT, LLM, TTS, RAG, On-premise deployment, Multilingual NLP]
confidentiality: Client project. The client and their product branding aren’t shown.
---

## The problem

Customers call in and speak the way they actually speak: in English, in Hindi, and often in Hinglish, switching languages mid-sentence. The assistant has to understand them, answer from the business’s own knowledge, and reply fast enough that the call feels natural.

It also has to run entirely on the client’s own server, so hosted speech and model APIs were off the table.

## What I built

An end-to-end, RAG-based telephony voice assistant. Every stage is an open-source model deployed on-premise:

- **Speech to text** turns the caller’s turn into text, including code-switched Hindi and English.
- **The LLM with retrieval** answers from the client’s knowledge base.
- **Text to speech** speaks the answer back on the call.

## Latency

On a phone call, silence reads as failure. The pipeline reaches the first spoken audio about 800 ms after the caller finishes speaking.

## Why multilingual is the hard part

Hinglish isn’t a third language with its own clean dataset. It’s two languages, two scripts, and a lot of mixing inside one sentence. Every stage of the pipeline, from recognition to retrieval to generation to speech, has to handle that without falling back to one language.
