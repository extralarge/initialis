@AGENTS.md
@CYRILLIC.md

## 1. Project

Fork of azlen/initialis (drop-cap generator). Owner: extralarge. Adds Cyrillic capitals and Russian reading passages (commit a7cb138). Keep Azlen credits. Pure static site: no build step, no package.json. Run locally with `python3 -m http.server 8000` or `start.command`. Requires WebGL2 in workers.

## 2. Remotes

origin = github.com/extralarge/initialis  
upstream = github.com/azlen/initialis  

Pull upstream changes: `git fetch upstream && git merge upstream/main`, or use GitHub "Sync fork".

## 3. Deployment

GitHub Pages from `main` branch root. Custom domain `https://initialis.extralarge.dev`, HTTPS enforced. Every push to `main` deploys automatically.

Keep in repo root — never delete: `CNAME` (contains `initialis.extralarge.dev`) and `.nojekyll`.

DNS: CNAME `initialis` → `extralarge.github.io` in Cloudflare, must stay DNS-only (grey cloud). Cloudflare proxying is throttled in Russia; the site must remain reachable from Russia.

`_headers` is ignored by GitHub Pages (Cloudflare/Netlify format kept from upstream). GitHub Pages already sends `Access-Control-Allow-Origin: *`.

Do not move hosting to the owner's Coolify server (too small) or Cloudflare Pages (blocked in Russia). Do not trigger multiple Pages builds at once — concurrent deployments cancel each other.

## 4. Rules

Do not publish built-in upstream styles as the owner's work. Do not add fonts with unclear licences; see `render/fonts/FONTS.md`.