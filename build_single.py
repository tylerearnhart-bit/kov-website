#!/usr/bin/env python3
"""Bundles the four-page KÖV site into ONE self-contained .html file.

Everything is inlined — stylesheet, script, and every photo as a data URI —
and the four pages become hash-routed views, so the file works anywhere:
double-clicked from a desktop, emailed, or dropped in Drive.
"""
import base64, mimetypes, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "/mnt/user-data/outputs/KOV-Simply-Interiors.html"

PAGES = [("home", "index.html"), ("gallery", "gallery.html"),
         ("houghton-lake", "houghton-lake.html"), ("paris", "paris.html")]


def read(p):
    return open(os.path.join(HERE, p), encoding="utf-8").read()


def grab(html, tag_open, tag_close):
    i = html.index(tag_open)
    j = html.index(tag_close, i) + len(tag_close)
    return html[i:j]


# ---------------------------------------------------------------- assets
def data_uri(rel):
    path = os.path.join(HERE, rel)
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    return "data:%s;base64,%s" % (mime, base64.b64encode(open(path, "rb").read()).decode())


_cache = {}


def inline_assets(html):
    def sub(m):
        rel = m.group(2)
        if rel not in _cache:
            _cache[rel] = data_uri(rel)
        return '%s="%s"' % (m.group(1), _cache[rel])
    return re.sub(r'(src)="(assets/[^"]+)"', sub, html)


# ---------------------------------------------------------------- links
def rewrite_links(html):
    for a, b in [
        ('href="index.html#', 'href="#'),
        ('href="index.html"', 'href="#/home"'),
        ('href="gallery.html"', 'href="#/gallery"'),
        ('href="houghton-lake.html"', 'href="#/houghton-lake"'),
        ('href="paris.html"', 'href="#/paris"'),
    ]:
        html = html.replace(a, b)
    return html


# ---------------------------------------------------------------- build
home = read("index.html")
header = grab(home, "<header class=\"site-header\">", "</header>")
footer = grab(home, "<footer class=\"site-footer", "</footer>")

views = []
for name, fname in PAGES:
    main = grab(read(fname), "<main", "</main>")
    main = main.replace('<main id="main"', "<main", 1).replace("<main>", "<main>", 1)
    views.append(
        '<div class="page" data-page="%s"%s>\n%s\n</div>'
        % (name, "" if name == "home" else " hidden", main)
    )

css = read("assets/styles.css")
js = read("assets/site.js")

# the lightbox scopes itself to the page the photo lives on
js = js.replace(
    "var shots = Array.prototype.slice.call(document.querySelectorAll('[data-shot]'));",
    "var shots = Array.prototype.slice.call(document.querySelectorAll('[data-shot]'));\n"
    "  function pageShots(el) {\n"
    "    var scope = el.closest ? el.closest('.page') : null;\n"
    "    return Array.prototype.slice.call((scope || document).querySelectorAll('[data-shot]'));\n"
    "  }"
)
js = js.replace(
    "    shots.forEach(function (s, i) {\n      s.addEventListener('click', function () { open(i); });\n    });",
    "    shots.forEach(function (s) {\n"
    "      s.addEventListener('click', function () {\n"
    "        shots = pageShots(s);\n"
    "        open(shots.indexOf(s));\n"
    "      });\n"
    "    });"
)

ROUTER = """
/* ---------- Hash router: four pages inside one file ---------- */
(function () {
  var pages = {};
  Array.prototype.forEach.call(document.querySelectorAll('.page'), function (el) {
    pages[el.getAttribute('data-page')] = el;
  });

  function setActive(name) {
    Object.keys(pages).forEach(function (k) { pages[k].hidden = (k !== name); });
    Array.prototype.forEach.call(document.querySelectorAll('.nav a[href^="#/"]'), function (a) {
      if (a.getAttribute('href').slice(2) === name) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    });
    var nav = document.getElementById('primary-nav');
    var menuBtn = document.querySelector('.menu-btn');
    if (nav) nav.classList.remove('open');
    if (menuBtn) menuBtn.setAttribute('aria-expanded', 'false');
    Array.prototype.forEach.call(document.querySelectorAll('.nav-item'), function (i) {
      i.classList.remove('open');
      var t = i.querySelector('.nav-toggle');
      if (t) t.setAttribute('aria-expanded', 'false');
    });
  }

  function route() {
    var h = location.hash || '';
    if (h.indexOf('#/') === 0) {
      var name = h.slice(2) || 'home';
      setActive(pages[name] ? name : 'home');
      window.scrollTo(0, 0);
    } else if (h.length > 1) {
      setActive('home');
      var target = document.getElementById(h.slice(1));
      if (target) target.scrollIntoView();
    } else {
      setActive('home');
      window.scrollTo(0, 0);
    }
  }

  window.addEventListener('hashchange', route);
  route();
})();
"""

doc = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>KÖV Simply Interiors</title>
<meta name="description" content="A Michigan-born design &amp; interiors studio finishing houses so they feel like home. Flooring, cabinetry, tile, countertops and window coverings under one roof.">
<meta name="theme-color" content="#577693">
<meta property="og:title" content="KÖV Simply Interiors">
<meta property="og:description" content="Every Surface. Every Space.">
<meta property="og:type" content="website">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,300;6..72,400;6..72,500;6..72,600&family=Figtree:wght@300;400;500;600;700&family=Archivo+Narrow:wght@600;700&display=swap">
<style>
:root{ padding-top: env(safe-area-inset-top, 0px); padding-bottom: env(safe-area-inset-bottom, 0px); }
html, body{ margin: 0; }
[hidden]{ display: none !important; }
__CSS__
</style>
</head>
<body>
<script>document.documentElement.classList.add('js');</script>
<a class="skip-link" href="#/home">Skip to content</a>
__HEADER__
<div id="main">
__VIEWS__
</div>
__FOOTER__
<script>
__JS__
__ROUTER__
</script>
</body>
</html>
"""

doc = (doc.replace("__CSS__", css)
          .replace("__HEADER__", header)
          .replace("__VIEWS__", "\n".join(views))
          .replace("__FOOTER__", footer)
          .replace("__JS__", js)
          .replace("__ROUTER__", ROUTER))

doc = rewrite_links(doc)
doc = inline_assets(doc)

os.makedirs(os.path.dirname(OUT), exist_ok=True)
open(OUT, "w", encoding="utf-8").write(doc)
print("wrote %s  —  %.1f MB" % (OUT, os.path.getsize(OUT) / 1024 / 1024))
