// @ts-check
import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  // TODO: set the final production domain before deploying
  site: "https://minquanwang.net",
  vite: {
    plugins: [tailwindcss()],
  },
});
