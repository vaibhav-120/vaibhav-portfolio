import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const work = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/work' }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    order: z.number(),
    featured: z.boolean().default(false),
    period: z.string().optional(),
    // Headline number for cards and the case study header.
    metric: z.object({ value: z.string(), label: z.string() }).optional(),
    stack: z.array(z.string()),
    // Shown at the top of the case study for client or NDA work.
    confidentiality: z.string().optional(),
    repo: z.string().url().optional(),
    // Set to true to hide a case study until it's cleared for publishing.
    draft: z.boolean().default(false),
  }),
});

const notes = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/notes' }),
  schema: z.object({
    title: z.string(),
    summary: z.string(),
    date: z.coerce.date(),
    draft: z.boolean().default(true),
  }),
});

export const collections = { work, notes };
