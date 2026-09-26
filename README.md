# AGORA — website

Portfolio website of AGORA, the architecture practice of Minquan Wang.
Built with [Astro 5](https://astro.build) and [Tailwind CSS 4](https://tailwindcss.com); fully static output.

## Commands

Run from the repository root (`E:\_AGORA\_Website`):

| Command                    | Action                                             |
| :------------------------- | :------------------------------------------------- |
| `npm install`              | Install dependencies                               |
| `npm run dev`              | Dev server at `http://localhost:4321`              |
| `npm run build`            | Production build to `./dist/`                      |
| `npm run preview`          | Preview the production build                       |
| `npm run import:projects`  | Re-import project index images (see below)         |

## Structure

```
_Website/                       ← repo root = Astro project root
├── Projects/ Background/ Index images/   ← raw asset archive (git-ignored, local only)
├── Header and logo/ Icon/      ← branding sources
├── public/
│   ├── fonts/                  ← empty; fonts load from Google Fonts (see Fonts)
│   ├── favicon.svg             ← AGORA mark
│   └── Minquan_Wang_CV.pdf     ← linked from the Contact page
├── scripts/
│   └── import_projects.py      ← builds web-sized index images from Projects/
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

## Fonts — Hanken Grotesk

Hanken Grotesk is the site's primary typeface. It is **open source** (SIL Open
Font License), so nothing needs to be licensed or committed. It is loaded from
Google Fonts by the `<link>` in `src/layouts/Base.astro`:

```
https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@300..900&display=swap
```

That request pulls the variable font covering weights 300-900, which is the
range the site uses (300 light, 400 regular, 700 bold, 900 black). No italics
are used, so none are requested.

### Self-hosting instead

To drop the third-party request, download the family from
<https://fonts.google.com/specimen/Hanken+Grotesk>, put the `.woff2` files in
`public/fonts/`, remove the Google Fonts `<link>` from `Base.astro`, and add
`@font-face` rules to `global.css` pointing at them.

## Brand tokens

Derived from `Header and logo/AGORA_LOGO_light.ai`:

- Vermilion `#EA3B2E` (`--color-brand`) — mark, wordmark, accents
- Near-black `#171717` (`--color-ink`) on white (`--color-paper`)
- Hairlines `#E6E6E4` (`--color-line`), image wells `#F4F4F3` (`--color-mist`)
- Wordmark letterspacing `0.45em`; labels/nav `0.28em`

## Before deploying

- Set the production domain in `astro.config.mjs` (`site`).
- Fill the `TODO` narratives in several `src/content/projects/*/index.md`.
