// @ts-check
import { defineConfig } from "astro/config";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  // TODO: set the final production domain before deploying
  site: "https://minquanwang.net",
  // Old project URLs kept alive after renames
  redirects: {
    "/projects/contentious-city": "/projects/gloucester-maritime-trade-campus",
    "/projects/eisenman-studio": "/projects/oak-street-connector-redevelopment",
    "/projects/international-land-sea-center": "/projects/chongqing-international-land-sea-center",
    "/projects/miami-studio": "/projects/detournement-of-allure",
    "/projects/minsheng-wharf": "/projects/minsheng-wharf-masterplan",
    "/projects/nio-house": "/projects/nio-house-beijing-huaxi-live",
    "/projects/pita-bloom": "/projects/easy-office",
    "/projects/rama": "/projects/ram-assembles",
  },
  vite: {
    plugins: [tailwindcss()],
  },
});
