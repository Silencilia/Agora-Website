import { defineCollection, z } from "astro:content";
import { glob } from "astro/loaders";

/**
 * Each project lives in its own folder under src/content/projects/<slug>/
 * with an index.md (frontmatter + narrative) and its images alongside it.
 * The folder name becomes the URL slug: /projects/<slug>/
 */
const projects = defineCollection({
  loader: glob({
    pattern: "*/index.md",
    base: "./src/content/projects",
    generateId: ({ entry }) => entry.replace(/[\\/]index\.md$/, ""),
  }),
  schema: ({ image }) =>
    z.object({
      title: z.string(),
      subtitle: z.string().optional(),
      category: z.enum(["professional", "academic", "personal", "research"]),
      year: z.string().optional(),
      location: z.string().optional(),
      /** e.g. Built, Competition, Concept, Installation */
      status: z.string().optional(),
      role: z.string().optional(),
      collaborators: z.string().optional(),
      awards: z.array(z.string()).default([]),
      /** Index image shown in the gallery and as the page hero */
      cover: image(),
      /** Shown in the selected-works grid on the main page */
      featured: z.boolean().default(false),
      /** Sort key for the gallery; lower comes first */
      order: z.number().default(999),
      draft: z.boolean().default(false),
      /**
       * Supplemental text inserted between gallery images. `after` is the
       * 1-indexed gallery image the text should follow; `body` may contain
       * multiple paragraphs separated by blank lines.
       */
      interludes: z
        .array(
          z.object({
            after: z.number(),
            heading: z.string().optional(),
            body: z.string(),
          }),
        )
        .default([]),
    }),
});

export const collections = { projects };
