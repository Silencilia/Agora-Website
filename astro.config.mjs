// @ts-check
import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  // TODO: set the final production domain before deploying
  site: "https://minquanwang.net",
  // Old project URLs kept alive after renames
  redirects: {
    "/projects/contentious-city": "/projects/gloucester-maritime-trade-campus",
  },
  vite: {
    plugins: [tailwindcss()],
  },
});
