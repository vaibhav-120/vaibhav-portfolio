import { defineConfig } from 'astro/config';

// Set `site` to your final domain once you have one (used for canonical URLs).
export default defineConfig({
  site: 'https://vaibhav-portfolio-khaki.vercel.app',
  // Local development: `npm run dev` forwards /api requests to the FastAPI
  // server started with uvicorn on port 8000. On Vercel, vercel.json routes /api.
  vite: {
    server: {
      proxy: { '/api': 'http://127.0.0.1:8000' },
    },
  },
});