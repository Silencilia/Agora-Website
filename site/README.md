# AGORA — website

Portfolio website of AGORA, the architecture practice of Minquan Wang.
Built with [Astro 5](https://astro.build) and [Tailwind CSS 4](https://tailwindcss.com); fully static output.

## Commands

Run from this `site/` folder:

| Command                    | Action                                             |
| :------------------------- | :------------------------------------------------- |
| `npm install`              | Install dependencies                               |
| `npm run dev`              | Dev server at `http://localhost:4321`              |
| `npm run build`            | Production build to `./dist/`                      |
| `npm run preview`          | Preview the production build                       |
| `npm run import:projects`  | Re-import project index images (see below)         |

## Structure

```
site/
├── public/
│   ├── fonts/                  ← Neuzeit Grotesk .woff2 files go here (see Fonts)
│   ├── favicon.svg             ← AGORA mark
│   └── Minquan_Wang_CV.pdf     ← linked from the Contact page
├── scripts/
│   └── import_projects.py      ← builds web-sized index images from ../Projects
└── src/
    ├── components/             ← common graphics & UI components
    │   ├── Logo.astro          ← the AGORA mark (SVG, extracted from AGORA_LOGO_light.ai)
    │   ├── Wordmark.astro      ← letterspaced AGORA wordmark
    │   ├── ArrowIcon.astro     ← brand arrow (from Icon/Arrow.ai)
    │   ├── Header.astro        ← sticky top bar with page navigation
    │   ├── Footer.astro        ← footer bar with basic information
    │   └── ProjectCard.astro   ← gallery tile
    ├── content/
    │   └── projects/           ← one folder per project: images + text
    │       └── <slug>/
    │           ├── index.md    ← frontmatter (title, year, role, awards…) + narrative
    │           └── main.jpg    ← index image (web-sized derivative of MAIN)
    ├── content.config.ts       ← project schema
    ├── layouts/Base.astro      ← html shell: header / scrollable main / footer
    ├── pages/
    │   ├── index.astro         ← main page (titled "Agora")
    │   ├── projects/index.astro    ← gallery of all projects
    │   ├── projects/[slug].astro   ← individual project page
    │   ├── about.astro
    │   └── contact.astro
    └── styles/global.css       ← Tailwind theme tokens, fonts, base styles
```

## Adding or updating a project

1. Add the raw project folder (with a `MAIN` image) to `E:\_AGORA\_Website\Projects`.
2. Add its slug to `SLUGS` in `scripts/import_projects.py`, then run
   `npm run import:projects` (pass `--force` to regenerate existing images).
3. Create `src/content/projects/<slug>/index.md` — copy an existing one as a
   template. The folder name is the URL: `/projects/<slug>/`.
4. Additional page images can be dropped into the same folder and referenced
   from the markdown body (`![caption](./photo.jpg)`).

Frontmatter fields: `title`, `subtitle?`, `category` (professional | academic |
personal | research), `year?`, `location?`, `status?`, `role?`,
`collaborators?`, `awards?`, `cover`, `featured?` (main-page grid),
`order` (gallery sort), `draft?` (hide).

## Fonts — Neuzeit Grotesk

Neuzeit Grotesk is the site's primary typeface but is a **commercial font**
(URW/Monotype; also on Adobe Fonts as `neuzeit-grotesk`). Licensed files are
not committed. To activate it, add the webfont files to `public/fonts/`:

```
NeuzeitGrotesk-Light.woff2      (300)
NeuzeitGrotesk-Regular.woff2    (400)
NeuzeitGrotesk-Bold.woff2       (700)
NeuzeitGrotesk-Black.woff2      (900)
```

Until then the site falls back to a locally installed copy of the font if one
exists (e.g. activated via Adobe Fonts / Creative Cloud), then to Helvetica /
Arial. Alternatively an Adobe Fonts web-project kit can be wired into
`src/layouts/Base.astro`.

## Brand tokens

Derived from `Header and logo/AGORA_LOGO_light.ai`:

- Vermilion `#EA3B2E` (`--color-brand`) — mark, wordmark, accents
- Near-black `#171717` (`--color-ink`) on white (`--color-paper`)
- Hairlines `#E6E6E4` (`--color-line`), image wells `#F4F4F3` (`--color-mist`)
- Wordmark letterspacing `0.45em`; labels/nav `0.28em`

## Before deploying

- Set the production domain in `astro.config.mjs` (`site`).
- Provide licensed Neuzeit Grotesk webfonts (above).
- Replace the portrait placeholder on the About page.
- Fill the `TODO` narratives in several `src/content/projects/*/index.md`.
