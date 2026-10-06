# Deploying KÖV Simply Interiors

Static site. No build step, no dependencies. ~30 minutes, most of it waiting on DNS.

---

## Step 1 — GitHub

Create a new repo named `kov-website`. Leave it **empty** — no README, no .gitignore,
no license. Those files already exist here and will collide.

Then push from inside the unzipped folder:

```bash
cd kov
git init
git add .
git commit -m "KOV Simply Interiors website"
git branch -M main
git remote add origin https://github.com/YOUR-ORG/kov-website.git
git push -u origin main
```

**Why not drag-and-drop?** This site is 93 files across nested folders
(`assets/gallery/`, `assets/team/`). GitHub's web uploader can handle it, but it is
slow and drops files silently at this size. If you do use it, drag the **contents**
of the `kov` folder, never the folder itself — `index.html` must land at the repo
root or every page 404s.

---

## Step 2 — Cloudflare Pages

**Workers & Pages** → **Create** → **Pages** tab → **Connect to Git** → pick the repo.

| Setting | Value |
|---|---|
| Framework preset | None |
| Build command | *(blank)* |
| Build output directory | `/` |

**Delete anything Cloudflare pre-fills into the build command.** It guesses, and a
site with no build step fails if that guess runs. This is the most common failure here.

Save and Deploy. Under a minute later you have a `kov-website.pages.dev` URL.

---

## Step 3 — Test on the Pages URL

Before pointing the domain:

- [ ] All four pages load, nav works
- [ ] Gallery photos appear, lightbox opens and arrows move through
- [ ] Locations dropdown reaches both showroom pages
- [ ] **Submit the contact form for real** and confirm the email arrives
- [ ] Open it on an actual phone

---

## Step 4 — Domain

Pages project → **Custom domains** → add `kovinteriors.com` and `www.kovinteriors.com`.

Requires the domain already on your Cloudflare account. If DNS is already there,
records are added automatically and it is live in minutes. If the domain is
registered elsewhere, move the nameservers to Cloudflare first — up to 24 hours.

---

## Step 5 — After launch

- [ ] Google Search Console → add property → submit `https://kovinteriors.com/sitemap.xml`
- [ ] Text yourself the link, confirm the preview card renders
- [ ] Verify the Facebook and Instagram handles on both showroom pages actually resolve

---

## Making changes later

```bash
git add .
git commit -m "what changed"
git push
```

Cloudflare redeploys in ~30 seconds. Every push is a version you can roll back to
from the Pages dashboard.

---

## Troubleshooting

**Blank page / everything 404s** — `index.html` is not at the repo root. Check that
the repo shows `index.html` in its file list, not a `kov/` folder.

**Build fails** — the build command is not empty. Settings → Builds & deployments →
clear it → Retry deployment.

**Photos missing but pages load** — `assets/` did not upload completely. Re-push.

---

## Still outstanding

- Privacy policy and terms of service — footer links to them as pending. The site
  collects names, emails and phone numbers, so this needs real legal review.
- Social handles `@KOVHoughtonLake` and `@KOVParis` on the showroom pages were taken
  from the change document and have not been verified against live accounts.
- Houghton Lake street address came from the brand playbook business card.
- Lead routing: one Web3Forms key, so every submission lands in one inbox regardless
  of which showroom the visitor picks. See README.md to split it later.
