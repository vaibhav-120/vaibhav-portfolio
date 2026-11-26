// Single place to edit everything about you that isn't a case study.
// Empty strings hide the related UI, so nothing half-finished ships.

export const profile = {
  name: 'Vaibhav Shrivastava',
  role: 'AI Engineer at Antier Solutions',
  location: 'Jalandhar, Punjab, India',
  headline: 'I build AI that talks, reasons, and acts\u00A0— in production, not just in demos.',
  intro: [
    'I work on large language models, agentic systems, and real-time voice AI. Most of my time goes into LangGraph orchestration, MCP-based tool integration, retrieval-augmented generation, and STT → LLM → TTS voice pipelines.',
    'Prototypes are the easy part. I focus on what comes after: keeping LLM systems reliable, fast, and correct when they talk to real customers or handle real healthcare data.',
  ],
  links: {
    linkedin: 'https://www.linkedin.com/in/vaibhav-shrivastava120/',
    resume: 'https://drive.google.com/file/d/1E-uI-h7aXXdw50F0-z-y4YCYV1OOd-32/view?usp=drivesdk',
    // Optional: add your GitHub profile URL to show it in the header and footer.
    github: '',
  },
  // Shows the voice agent on the live site. It always shows during local
  // development (npm run dev / vercel dev) so you can test it first.
  askAgentEnabled: true,
};

export const experience = [
  {
    title: 'AI Assistant Engineer',
    org: 'Antier Solutions',
    type: 'Full-time',
    period: 'Jan 2026 – Present',
    place: 'Sahibzada Ajit Singh Nagar, Punjab',
    points: [
      'Built multi-agent workflows for a HIPAA-aligned US healthcare platform, grounded in patient reports and FHIR data.',
      'Re-architected those workflows end to end, from orchestration to code, on LangGraph with MCP-based task creation, cutting time to first token from ~12 s to ~2 s.',
      'Building Emnaar, an on-premise English, Hindi, and Hinglish telephony voice assistant with ~800 ms from end of turn to first audio.',
      'Applied LLM evaluation with Ragas, LangSmith, and Promptfoo to measure response quality across production AI work.',
    ],
  },
  {
    title: 'AI Intern',
    org: 'Antier Solutions',
    type: 'Internship',
    period: 'Jul 2025 – Dec 2025',
    place: 'Mohali, Punjab',
    points: [
      'Evaluated and optimized LLM responses across projects with Ragas and Promptfoo.',
      'Moved onto the healthcare client project after three months and contributed to production features. Brought on full-time afterwards.',
    ],
  },
];

export const education = {
  school: 'DAV University, Jalandhar',
  degree: 'B.Tech, Computer Science',
  period: 'Jul 2021 – May 2025',
  grade: 'GPA 8.5+',
};

export const skills = {
  core: [
    'LangGraph',
    'Agentic AI development',
    'Retrieval-augmented generation',
    'Voice AI',
    'Tool calling',
    'LLM evals',
    'Blockchain',
    'WebSocket',
    'Back-end web development',
  ],
  supporting: [
    'LangChain',
    'Vector databases',
    'Ragas',
    'LangSmith',
    'Promptfoo',
    'FastAPI',
    'Django',
    'Django REST Framework',
    'Docker',
    'Hugging Face',
    'TensorFlow',
    'scikit-learn',
    'NLP',
    'Generative AI',
    'Machine learning',
    'Statistical modeling',
    'Python',
    'Git',
    'Regular expressions',
  ],
};
