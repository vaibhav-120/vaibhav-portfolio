# Vaibhav Shrivastava · Portfolio

Portfolio built with [Astro](https://astro.build) 5, plus a FastAPI voice agent that answers questions about my work. The site ships almost no JavaScript, works in light and dark mode, and the whole project deploys free on Vercel.

## Run it locally

Requires Node.js 18.20+ (20 or 22 recommended).

```bash
npm install
npm run dev        # site only, http://localhost:4321
npm run build      # production build into dist/
```

### Run the voice agent locally

One-time setup:

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt python-dotenv
cp .env.example .env             # then put your Groq key in .env
sh scripts/download-voice.sh     # Piper voice, ~60 MB (Windows: run in Git Bash)
```

Then, in two terminals:

```bash
uvicorn index:app --app-dir api --env-file .env --port 8000 --reload   # agent backend
npm run dev                                                           # site, http://localhost:4321
```

`npm run dev` forwards `/api` to the backend (see `astro.config.mjs`). The agent panel always shows during local development so you can test it. Backend errors, such as a bad key or a retired model name, are printed in the uvicorn terminal as `[agent] ...` lines.

Alternatively, `vercel dev` runs both together at http://localhost:3000, after a one-time `vercel login`.

## Deploy on Vercel (free)

1. Push this folder to a new GitHub repository.
2. Go to [vercel.com/new](https://vercel.com/new) and import the repository. Vercel detects Astro automatically; keep the default settings.
3. Before deploying, open **Environment Variables** and add `GROQ_API_KEY` (and `BLOCKED_TERMS`, see below). The full list is in `.env.example`.
4. Click **Deploy**. Every push to `main` redeploys.
4. To use a custom domain, add it under **Project → Settings → Domains**, then set `site` in `astro.config.mjs` to that domain.

## Where to edit things

| What | File |
| --- | --- |
| Name, headline, intro, links, résumé, GitHub | `src/data/profile.ts` |
| Experience, education, skills | `src/data/profile.ts` |
| Case study text and metrics | `src/content/work/*.md` |
| Architecture diagrams | `src/data/diagrams.ts` |
| Latency chart on the home page | `src/components/LatencyCard.astro` |
| Notes / blog posts | `src/content/notes/*.md` |
| What the voice agent knows | `api/_data/knowledge.md` |
| Voice agent rules and models | `api/_lib/agent.py` |
| Voice agent widget | `src/components/AskAgent.astro` |
| Colors and type | `src/styles/global.css` (tokens at the top) |

Empty values hide their UI. For example, the résumé button appears only once `links.resume` has a URL, and the Notes link appears only once a note has `draft: false`.

To hide a case study until it's cleared, add `draft: true` to its front matter.

### Adding a case study

Create `src/content/work/my-project.md`:

```md
---
title: My project
summary: One sentence on what it is.
order: 6
featured: false
stack: [LangGraph, RAG]
---

## The problem
...
```

Then optionally add a diagram under the same key (`'my-project'`) in `src/data/diagrams.ts`.

## Before you publish

From the open items in the brief:

- [ ] **AI wallet layer** (`ai-wallet-layer.md`): confirm whether "LXX DAO" can be named. It's currently described by approach only.
- [ ] **Agentic RAG platform**: if any part can be open-sourced, add `repo: https://github.com/...` to its front matter to show a code link.
- [ ] **AI-powered LMS**: confirm there's no client name that needs to stay private.
- [ ] **Résumé**: add the public PDF link to `links.resume` in `src/data/profile.ts`.
- [ ] **GitHub**: add your profile URL to `links.github` if you want it shown.
- [ ] **Accuracy pass**: read every case study once. The copy sticks to the brief, but a few lines are written as framing. Change anything that isn't exactly right.
- [ ] **Groq key**: add `GROQ_API_KEY` in Vercel, and list client names in `BLOCKED_TERMS`.
- [ ] **Voice agent**: test locally with `vercel dev`, run the evals, then set `askAgentEnabled: true`.

Worth adding when you have time, because these are the strongest parts of each case study:

- [ ] **HealthAera**: what in the architecture and code changed to cut time to first token, what it cost, and what you'd do differently. The draft note `src/content/notes/healthcare-agent-latency.md` already has this outline.
- [ ] **Emnaar**: how the pipeline reaches ~800 ms, and how you handled code-switched Hindi and English.
- [ ] **Old site**: once this is live, take down or redirect the Streamlit app so recruiters don't find the retired projects.

## The voice agent

```
Browser speech recognition → /api/ask (FastAPI on Vercel) → Groq: gpt-oss-20b, falls back to llama-3.1-8b-instant
                                                          → Piper speaks each sentence as soon as it's written
```

- **How a conversation works:** the visitor presses Start conversation once. The mic stays on and the agent answers each question until they press Stop. Speaking while the agent talks interrupts it: audio stops at once, the transcript keeps only what was actually heard, and the agent listens to the new question.
- **Echo handling:** with speakers, the mic can hear the agent's own voice. Speech that mostly repeats what the agent just said is ignored, so the agent doesn't interrupt itself. Headphones avoid the problem entirely, which the widget suggests.
- **Browser support:** voice input needs the Web Speech API, available in Chrome, Edge, and Safari. In other browsers the panel explains this instead of starting.

- **Turning it on for the live site:** set `askAgentEnabled: true` in `src/data/profile.ts` once you're happy with it locally.
- **Keys and secrets:** `GROQ_API_KEY` lives only in `.env` (local, never committed) and in Vercel's environment variables. It never reaches the browser.
- **Client names:** put every name the agent must never say in `BLOCKED_TERMS`, comma-separated. Any sentence containing one is replaced before it leaves the server. This is a backstop: the real protection is that `knowledge.md` contains no client names.
- **Knowledge:** `api/_data/knowledge.md` is the agent's entire world. Edit it when your site changes, and keep it short, since every question sends the whole file to Groq.
- **Free-tier limits:** Groq's limits are the hard ceiling. When they're hit, the agent falls back to the next model, then replies with a "try again or message me on LinkedIn" line. There's no card on the account, so there's no bill. Each visitor is also limited to 20 questions per 10 minutes (`RATE_LIMIT_MAX`, `RATE_LIMIT_WINDOW`).
- **Voice:** if the Piper voice file is missing, the browser's built-in voice is used instead. To try another voice, pass its name to `scripts/download-voice.sh` and set `PIPER_VOICE`.
- **Licence note:** the `piper-tts` package is GPL-3.0. Running it on your server is fine; keep that in mind if you ever distribute this code as a product.

### Evals

`evals/promptfooconfig.yaml` checks the agent's facts and guardrails: correct latency numbers, no client names, no invented metrics, salary questions sent to LinkedIn, and resistance to prompt injection.

```bash
# with the backend running (uvicorn on port 8000)
BLOCKED_TERMS="name one,name two" npx promptfoo@latest eval -c evals/promptfooconfig.yaml
```

Run it after every change to `knowledge.md` or the agent's prompt.

### After the first deploy

In the Vercel dashboard, open **Deployments → your deployment → Functions** and check that `api/index.py` is listed. Then visit `/api/health`: it should return `"voice": true` once the Piper voice is committed.