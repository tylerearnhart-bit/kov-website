# KÖV Simply Interiors — website

Static marketing site for KÖV Simply Interiors (Houghton Lake & Paris, Michigan).
No build step, no framework, no dependencies — the HTML in this repo is what ships.

Built and maintained by OptSpot.

---

## What's here

```
index.html            Home
gallery.html          Full project gallery (59 photos)
houghton-lake.html    Showroom: address, hours, socials, team
paris.html            Showroom: address, hours, socials, team
404.html              Branded not-found page

assets/styles.css     All styling
assets/site.js        Nav, scroll reveals, lightbox, contact form
assets/gallery/       Project photography
assets/team/          Staff headshots
assets/*.png|.jpg     Logos, icons, hero, social preview

robots.txt            Search engine directives
sitemap.xml           Four pages, for Search Console
_headers              Cloudflare Pages: caching + security headers

build.py              Regenerates the four HTML pages (optional — see below)
build_single.py       Bundles everything into one portable .html file
```

### About `build.py`

The HTML files are committed and deployable as-is. `build.py` is the generator
they came from — it keeps the shared header, footer and nav in sync across pages.

- **Editing text or layout:** change `build.py`, run `python3 build.py`, commit both.
- **Editing by hand instead:** fine, but repeat shared changes in all five HTML files,
  and know that re-running `build.py` would overwrite them.

Python 3 only. No packages to install.

---

## Deploying to Cloudflare Pages

**1. Push this folder to a GitHub repo.**

```bash
cd kov
git init
git add .
git commit -m "KÖV Simply Interiors website"
git branch -M main
git remote add origin https://github.com/YOUR-ORG/kov-website.git
git push -u origin main
```

**2. Connect it in Cloudflare.**

Cloudflare Dashboard → Workers & Pages → Create → Pages → Connect to Git →
pick the repo.

Build settings — leave these **empty**, this is a static site:

| Setting | Value |
|---|---|
| Framework preset | None |
| Build command | *(blank)* |
| Build output directory | `/` |

Save and Deploy. First build takes under a minute and you get a
`kov-website.pages.dev` URL.

**3. Point the domain.**

Pages project → Custom domains → Set up a custom domain → `kovinteriors.com`.
Add `www.kovinteriors.com` too and let Cloudflare redirect it to the apex.
If the domain's DNS is already on Cloudflare, records are added automatically.

Every push to `main` redeploys. Pull requests get their own preview URL.

---

## The contact form

Submissions run through [Web3Forms](https://web3forms.com). The form posts as
JSON so the confirmation appears in place without a page reload; if JavaScript
fails it falls back to a normal form POST to the same endpoint.

The access key lives in `index.html` as `name="access_key"`. It is designed to be
public — it only identifies the destination inbox and cannot read past
submissions. Rotate it from the Web3Forms dashboard if it ever gets abused.

**Fields sent:** `first_name`, `last_name`, `email`, `phone`,
`preferred_showroom`, `project_scope`, `message`, plus a combined `name`.

**Spam protection:** a hidden `botcheck` honeypot. Turn on reCAPTCHA or Turnstile
in the Web3Forms dashboard if spam gets through.

### Routing leads by showroom

One Web3Forms access key sends to one inbox. To split Houghton Lake and Paris,
create a second form in Web3Forms and pick the key at submit time in
`assets/site.js`:

```js
var KEYS = {
  'Houghton Lake, MI': 'HOUGHTON-LAKE-KEY',
  'Paris, MI':         'PARIS-KEY'
};
data.access_key = KEYS[data.preferred_showroom] || data.access_key;
```

The showroom field is required, so every submission carries one of those two values.

---

## Still outstanding

- [ ] Privacy policy and terms of service (footer links to them as pending)
- [ ] Second Web3Forms key, to route leads per showroom
- [ ] Confirm the Houghton Lake address against the sign out front
- [ ] Submit `sitemap.xml` in Google Search Console after launch
- [ ] Verify the real Facebook and Instagram handles on both showroom pages

---

## Notes for whoever picks this up next

**Internal links keep their `.html` endings** so the site also works when opened
straight from disk — useful for client review without hosting. Cloudflare Pages
serves these at clean URLs (`/gallery`) and redirects the `.html` form to match,
which is where the canonical tags point. Dropping the extensions from the `href`s
would remove one redirect per click, at the cost of local file browsing.

**Photos are pre-sized** to 1600px wide at ~78% JPEG quality and lazy-load below
the fold. Run new photography through the same treatment before committing it —
dropping in 5MB camera files will sink the page on mobile.

**Accessibility:** the site honors `prefers-reduced-motion`, keeps visible focus
rings, uses real labels on every form field, and ships alt text on every photo.
Keep that up when adding content.
