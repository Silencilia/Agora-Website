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
      /** Credit line, e.g. "As design lead for" + linked firm name */
      credit: z
        .object({
          text: z.string(),
          firm: z.string(),
          url: z.string().url(),
        })
        .optional(),
      collaborators: z.string().optional(),
      awards: z.array(z.string()).default([]),
      /** Index image shown in the gallery and as the page hero */
      cover: image(),
      /** Shown in the selected-works grid on the main page */
      featured: z.boolean().default(false),
      /**
       * Page layout. "standard": cover, then info + text, then gallery.
       * "images-first": info, then cover + gallery one per row, then text.
       */
      layout: z.enum(["standard", "images-first"]).default("standard"),
      /**
       * Text placed between gallery images, in order. `after` is the image
       * number it follows ("g05" for g05-set.jpg). `caption` sits right
       * under that image; `title` + `text` form a block after it
       * (paragraphs separated by a blank line).
       */
      notes: z
        .array(
          z.object({
            after: z.string(),
            caption: z.string().optional(),
            title: z.string().optional(),
            subtitle: z.string().optional(),
            text: z.string().optional(),
            /** Text beside the image; the image takes this share (0–1) of the width */
            beside: z.number().min(0.1).max(0.9).optional(),
            /** With `beside`: align text to the top ("start") or bottom ("end") */
            align: z.enum(["start", "end"]).optional(),
            /** Show a "-set" image at this share (0–1) of the column width */
            width: z.number().min(0.1).max(1).optional(),
            /** "-row": title/text go under that image instead of after the row */
            under: z.boolean().optional(),
            /** "-row": stack this image under the previous one, in the same column */
            stack: z.boolean().optional(),
            /** "-row": gap between the row's images, in px (at every screen size) */
            gap: z.number().min(0).optional(),
            /** Space after this image's row, in px (replaces the usual gallery spacing) */
            below: z.number().min(0).optional(),
            /** With `beside`: small image (x01.jpg …) shown in the text column */
            aside: z.string().optional(),
            /** Put the `aside` image above the text instead of below */
            asideFirst: z.boolean().optional(),
            /** The `aside` image's share (0–1) of the text column's width */
            asideWidth: z.number().min(0.1).max(1).optional(),
            /** Caption under the `aside` image */
            asideCaption: z.string().optional(),
          }),
        )
        .default([]),
      /** Sort key for the gallery; lower comes first */
      order: z.number().default(999),
      draft: z.boolean().default(false),
    }),
});

export const collections = { projects };
