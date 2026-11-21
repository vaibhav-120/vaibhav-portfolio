// Architecture diagrams, keyed by case study file name.
// Each case study can have one or more flows. A step is either a single node
// or a group of parallel nodes. Edit labels freely; layout is automatic.

export type Node = { label: string; note?: string; accent?: boolean };
export type Step = Node | { group: Node[]; label?: string };
export type Flow = {
  title?: string;
  boundary?: string; // draws a dashed frame, e.g. "On-premise"
  steps: Step[];
  span?: string; // measured span shown under the flow
  support?: string[]; // shared foundations shown beneath the flow
};

export const diagrams: Record<string, Flow[]> = {
  healthaera: [
    {
      steps: [
        { label: 'Patient request' },
        { label: 'Patient context', note: 'Reports and FHIR data' },
        {
          label: 'LangGraph agents',
          group: [
            { label: 'Medical agent' },
            { label: 'Navigation agent' },
            { label: 'Plan and task agent', note: 'Creates tasks via MCP', accent: true },
          ],
        },
        { label: 'Personalized response' },
      ],
      span: '~2 s to first token, down from ~12 s',
    },
  ],
  emnaar: [
    {
      steps: [
        { label: 'Caller speaks', note: 'English, Hindi, Hinglish' },
        { label: 'Speech to text', note: 'Open-source, on-premise' },
        { label: 'LLM with RAG', note: 'Open-source, on-premise', accent: true },
        { label: 'Text to speech', note: 'Open-source, on-premise' },
        { label: 'Caller hears the reply' },
      ],
      span: '~800 ms from end of turn to first audio',
    },
  ],
  'ai-wallet-layer': [
    {
      steps: [
        { label: 'User intent', note: 'Plain language' },
        { label: 'Agent', note: 'Chooses tools' },
        { label: 'MCP server', note: 'Blockchain APIs as tools', accent: true },
        {
          label: 'Workflows',
          group: [
            { label: 'Portfolio queries' },
            { label: 'Transaction guidance' },
            { label: 'Gas and slippage checks' },
            { label: 'Conditional orders' },
            { label: 'Price alerts' },
          ],
        },
      ],
    },
  ],
  'agentic-rag-platform': [
    {
      steps: [
        { label: 'Question' },
        { label: 'Routing', accent: true },
        {
          label: 'Execution',
          group: [{ label: 'Retrieval' }, { label: 'Tool execution' }],
        },
        { label: 'Conditional workflow', note: 'Branches on each result' },
        { label: 'Grounded answer' },
      ],
      support: ['Short-term memory', 'Long-term memory', 'Prompt registry', 'Tool registry'],
    },
  ],
  'ai-powered-lms': [
    {
      steps: [
        { label: 'Learner speaks' },
        { label: 'WebSocket', note: 'Real-time audio' },
        { label: 'AI instructor', note: 'Live lecture', accent: true },
        { label: 'Live assessment' },
        { label: 'Performance report' },
      ],
    },
  ],
};
