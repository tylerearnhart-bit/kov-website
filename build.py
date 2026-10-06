#!/usr/bin/env python3
"""Assembles the KÖV site pages from shared header/footer parts."""
import os, re

OUT = os.path.dirname(os.path.abspath(__file__))

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n'
         '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
         'family=Newsreader:opsz,wght@6..72,300;6..72,400;6..72,500;6..72,600'
         '&family=Figtree:wght@300;400;500;600;700'
         '&family=Archivo+Narrow:wght@600;700&display=swap">')


SITE = "https://kovinteriors.com"


def head(title, desc, canonical="/", jsonld=""):
    ld = f'\n<script type="application/ld+json">{jsonld}</script>' if jsonld else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#577693">
<link rel="canonical" href="{SITE}{canonical}">

<link rel="icon" href="assets/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="assets/favicon-16x16.png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">

<meta property="og:site_name" content="K&Ouml;V Simply Interiors">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{canonical}">
<meta property="og:image" content="{SITE}/assets/og-image.jpg">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/assets/og-image.jpg">
{FONTS}
<link rel="stylesheet" href="assets/styles.css">{ld}
</head>
<body>
<script>document.documentElement.classList.add('js');</script>
<a class="skip-link" href="#main">Skip to content</a>
"""


def header(active=""):
    def cur(name):
        return ' aria-current="page"' if active == name else ''
    home = 'index.html'
    return f"""
<header class="site-header">
  <div class="shell header-inner">
    <a class="lockup" href="{home}" aria-label="KÖV Simply Interiors, home">
      <img src="assets/kov-logo.png" alt="KÖV Simply Interiors" width="900" height="196">
    </a>

    <nav class="nav" id="primary-nav" aria-label="Primary">
      <a href="{home}#offerings">What We Finish</a>
      <a href="{home}#approach">Our Approach</a>
      <a href="gallery.html"{cur('gallery')}>Gallery</a>
      <div class="nav-item">
        <button class="nav-toggle" type="button" aria-expanded="false" aria-haspopup="true">
          Locations <span class="caret" aria-hidden="true"></span>
        </button>
        <ul class="nav-menu">
          <li><a href="houghton-lake.html"{cur('houghton')}>Houghton Lake</a></li>
          <li><a href="paris.html"{cur('paris')}>Paris</a></li>
        </ul>
      </div>
    </nav>

    <div class="header-cta">
      <a class="btn btn-solid" href="{home}#consult"><span class="cta-long">Request a Free Consultation</span><span class="cta-short">Free Consult</span></a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="primary-nav" aria-label="Menu">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
  <div class="scroll-progress" aria-hidden="true"><span></span></div>
</header>
"""


FOOTER = """
<footer class="site-footer tone-dark">
  <div class="shell">
    <div class="footer-top">
      <div>
        <img src="assets/kov-logo-white.png" alt="KÖV Simply Interiors" width="900" height="196" style="height:46px;width:auto;display:block;">
        <p class="footer-tag">Every Surface. Every Space.</p>
        <p class="footer-blurb">A Michigan-born studio finishing houses so they feel like home &mdash; flooring, cabinetry, tile and window coverings, under one roof.</p>
      </div>
      <div class="footer-col">
        <h4>What We Finish</h4>
        <ul>
          <li><a href="index.html#offerings">Flooring</a></li>
          <li><a href="index.html#offerings">Cabinetry</a></li>
          <li><a href="index.html#offerings">Tile &amp; Stone</a></li>
          <li><a href="index.html#offerings">Window Coverings</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Studio</h4>
        <ul>
          <li><a href="index.html#approach">Our Approach</a></li>
          <li><a href="gallery.html">Gallery</a></li>
          <li><a href="index.html#consult">Request a Free Consultation</a></li>
        </ul>
      </div>
      <div class="footer-col">
        <h4>Visit</h4>
        <ul>
          <li><a href="houghton-lake.html">Houghton Lake</a><br><a href="tel:+19894223545">989.422.3545</a></li>
          <li><a href="paris.html">Paris</a><br><a href="tel:+12317960330">231.796.0330</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 K&Ouml;V Simply Interiors. All rights reserved.</span>
      <span class="legal-todo">Privacy policy and terms of service to be added before launch.</span>
    </div>
  </div>
</footer>

<script src="assets/site.js"></script>
</body>
</html>
"""


def ph(label, note="", cls=""):
    n = f'\n        <span class="ph-note">{note}</span>' if note else ''
    return f"""<div class="ph{(' ' + cls) if cls else ''}">
        <span class="ph-mark" aria-hidden="true"></span>
        <span class="ph-label">{label}</span>{n}
      </div>"""


def shot(slug, alt, caption, fixed=False, span=2):
    """A clickable project photo. `fixed` is the home grid; otherwise a gallery cell."""
    cls = "shot-fixed" if fixed else ("shot span-%d" % span)
    return (f'<button class="{cls}" type="button" data-shot data-caption="{caption}" '
            f'aria-label="Enlarge: {caption}">'
            f'<img src="assets/gallery/{slug}.jpg" alt="{alt}" loading="lazy" decoding="async">'
            f'</button>')


# --------------------------------------------------------------------------
# HOME
# --------------------------------------------------------------------------
HOME_MAIN = f"""
<main id="main">

  <!-- HERO -->
  <section class="hero tone-dark">
    <div class="hero-media" aria-hidden="true">
      <img src="assets/hero-kitchen.jpg" alt="" width="1800" height="1013">
    </div>
    <div class="shell hero-inner">
      <div class="hero-copy">
        <span class="eyebrow"><span class="dots gold" aria-hidden="true"><i></i><i></i></span> Michigan-Born Design &amp; Interiors Studio</span>
        <h1>You bring the house. We'll make it <em>home</em>.</h1>
        <p class="lede">Stop juggling showrooms, suppliers and installers. K&Ouml;V brings every interior finish together in one place, so your cabinetry, countertops, tile, flooring, fixtures and window coverings work together from the start. Whether it's one room or every room, we design it, sequence it and install it right. Just for you.</p>
        <div class="hero-actions">
          <a class="btn btn-solid" href="#consult">Request a Free Consultation <span class="btn-arrow" aria-hidden="true">&rarr;</span></a>
          <a class="btn btn-ghost" href="#work">See Recent Work <span class="btn-arrow" aria-hidden="true">&rarr;</span></a>
        </div>
      </div>
    </div>
  </section>

  <!-- OFFERINGS -->
  <section class="band" id="offerings">
    <div class="shell">
      <div class="sec-head wide">
        <span class="eyebrow"><span class="dots gold" aria-hidden="true"><i></i><i></i></span> Every Surface. Every Space.</span>
        <h2>Every finish. One team. Your whole home.</h2>
        <p>From the floors beneath your feet to the fixtures in your hands, K&Ouml;V's designers finish everything inside your home. Kitchens, bathrooms, bedrooms, or the whole home &mdash; we select, coordinate and install your flooring, tile and stone, cabinetry, countertops, window coverings and plumbing fixtures &mdash; all under one roof, with one team that sees it through.</p>
      </div>

      <div class="offerings">
        <article class="offer">
          <span class="num">01</span>
          <h3>Flooring</h3>
          <p>Hardwood, luxury vinyl, carpet and specialty runs &mdash; specified for how the room actually gets used.</p>
          <p class="tags">Hardwood &middot; LVP &middot; Carpet</p>
        </article>
        <article class="offer">
          <span class="num">02</span>
          <h3>Cabinetry</h3>
          <p>Semi-custom and custom kitchens, baths, mudrooms and built-ins. Miter joints we're happy to have inspected.</p>
          <p class="tags">Kitchen &middot; Bath &middot; Built-ins</p>
        </article>
        <article class="offer">
          <span class="num">03</span>
          <h3>Tile &amp; Stone</h3>
          <p>Showers, backsplashes, entries and fireplace surrounds &mdash; layout drawn before the first sheet is cut.</p>
          <p class="tags">Porcelain &middot; Stone &middot; Mosaic</p>
        </article>
        <article class="offer">
          <span class="num">04</span>
          <h3>Window Coverings</h3>
          <p>Blinds, shades, shutters and motorized systems, measured and hung by professionals who know their craft.</p>
          <p class="tags">Shades &middot; Shutters &middot; Motorized</p>
        </article>
      </div>
    </div>
  </section>

  <!-- APPROACH -->
  <section class="band band-ink tone-dark" id="approach">
    <div class="shell ethos-grid">
      <div>
        <span class="eyebrow"><span class="dots gold" aria-hidden="true"><i></i><i></i></span> A Harbor for the Home</span>
        <p class="pull">K&Ouml;V is named for the cove &mdash; a harbor that holds when the weather turns.</p>
        <div class="ethos-body">
          <p>Plenty of people can build a house. Far fewer know how to finish one so it actually feels like home. We're not a big-box store where you're a line on an order. We're a studio that handles everything from the floors you walk on to the cabinets in your kitchen.</p>
          <p>Our two dots are the signature: a promise that we care about the miter joints and the textures as much as you do. Lakefront estate or a mudroom refresh &mdash; same standard, same stock, same crew.</p>
        </div>
        <img class="ethos-mark" src="assets/kov-icon.png" alt="" width="231" height="293">
      </div>

      <div class="values">
        <article class="value">
          <span class="dots" aria-hidden="true"><i></i><i></i></span>
          <div>
            <h3>No-Drama Precision</h3>
            <p>Quiet professionals. We manage the project with surgical focus so the only thing you feel is the finished product &mdash; never the noise of getting there.</p>
          </div>
        </article>
        <article class="value">
          <span class="dots" aria-hidden="true"><i></i><i></i></span>
          <div>
            <h3>Unfiltered Authenticity</h3>
            <p>Truthfulness over corporate fluff. If a selection won't hold up in your space, you'll hear it from us early &mdash; not from the installer on day one.</p>
          </div>
        </article>
        <article class="value">
          <span class="dots" aria-hidden="true"><i></i><i></i></span>
          <div>
            <h3>Relentless Problem-Solving</h3>
            <p>When a project feels overwhelmed, we're the fixers. Craftsmanship plus a can-do streak, until every expectation is met on the install.</p>
          </div>
        </article>
        <article class="value">
          <span class="dots" aria-hidden="true"><i></i><i></i></span>
          <div>
            <h3>Radically Relationship-Driven</h3>
            <p>Built on trust and a deep connection to our community. Every client is treated like our only client, start to reveal.</p>
          </div>
        </article>
      </div>
    </div>
  </section>

  <!-- PROCESS -->
  <section class="band">
    <div class="shell">
      <div class="sec-head wide">
        <span class="eyebrow"><span class="dots" aria-hidden="true"><i></i><i></i></span> How a Project Runs</span>
        <h2>Three stages, and you always know which one you're in.</h2>
      </div>
      <div class="steps">
        <article class="step">
          <span class="num">Stage One</span>
          <h3>Consultation</h3>
          <p>We walk the space, take measurements and talk budget honestly. You leave with a scope and a realistic lead time &mdash; not a ballpark.</p>
        </article>
        <article class="step">
          <span class="num">Stage Two</span>
          <h3>Selection</h3>
          <p>Sit down with a design consultant in the showroom. Floors, cabinets, tile and coverings get chosen together so the palette reads as one room.</p>
        </article>
        <article class="step">
          <span class="num">Stage Three</span>
          <h3>White-Glove Install</h3>
          <p>Our crews sequence the trades, protect the site and hand the space back styled and clean. Milestones land in your inbox as they clear.</p>
        </article>
      </div>
    </div>
  </section>

  <!-- WORK -->
  <section class="band band-deep tone-dark" id="work">
    <div class="shell">
      <div class="sec-head wide">
        <span class="eyebrow"><span class="dots gold" aria-hidden="true"><i></i><i></i></span> Recent Work</span>
        <h2>Finished spaces across Central and Northern Michigan.</h2>
        <p>Here's a few highlights. See more in our <a href="gallery.html">Gallery</a>.</p>
      </div>

      <div class="work-grid">
        <div class="work-item feature">
          {shot('kitchen-walnut-island', 'White kitchen with a walnut island, quartz waterfall top and brass pendant lighting', 'Walnut Island Kitchen', fixed=True)}
          <div class="work-cap"><h3>Walnut Island Kitchen</h3><span>Cabinetry &middot; Countertops &middot; Flooring</span></div>
        </div>
        <div class="work-item portrait">
          {shot('kitchen-olive-dining', 'Olive green kitchen with a marble island, leather stools and a pro range', 'Olive Kitchen &amp; Dining', fixed=True)}
          <div class="work-cap"><h3>Olive Kitchen</h3><span>Cabinetry</span></div>
        </div>
        <div class="work-item">
          {shot('bath-primary-suite', 'Primary bath with a marble-tile shower, double vanity and brushed brass sconces', 'Primary Bath Suite', fixed=True)}
          <div class="work-cap"><h3>Primary Bath</h3><span>Tile &middot; Cabinetry</span></div>
        </div>
        <div class="work-item">
          {shot('living-stone-fireplace', 'Great room with a stone fireplace, vaulted wood ceiling and navy built-in cabinets', 'Great Room Fireplace', fixed=True)}
          <div class="work-cap"><h3>Great Room</h3><span>Cabinetry &middot; Flooring</span></div>
        </div>
        <div class="work-item">
          {shot('pantry-butlers', "Butler's pantry with a walnut counter, white cabinetry and navy arabesque tile", "Butler's Pantry", fixed=True)}
          <div class="work-cap"><h3>Butler's Pantry</h3><span>Cabinetry &middot; Tile</span></div>
        </div>
      </div>

      <div class="btn-row">
        <a class="btn btn-solid btn-wide" href="gallery.html">View More <span class="btn-arrow" aria-hidden="true">&rarr;</span></a>
      </div>
    </div>
  </section>

  <!-- CONSULTATION -->
  <section class="band band-tint" id="consult">
    <div class="shell consult-grid">
      <div>
        <span class="eyebrow"><span class="dots gold" aria-hidden="true"><i></i><i></i></span> Start Here</span>
        <h2>Tell us what you're finishing.</h2>
        <ul class="promise">
          <li><span class="dots" aria-hidden="true"><i></i><i></i></span><span>A real person reads every request &mdash; usually back to you the same business day.</span></li>
          <li><span class="dots" aria-hidden="true"><i></i><i></i></span><span>No pressure, no quote-by-guess. We give you a scope and a lead time.</span></li>
          <li><span class="dots" aria-hidden="true"><i></i><i></i></span><span>Builders and designers welcome &mdash; ask about trade scheduling.</span></li>
        </ul>
      </div>

      <div class="form-card tone-light" id="consultCard">
        <form class="form-body" id="consultForm" action="https://api.web3forms.com/submit" method="POST" novalidate>
          <input type="hidden" name="access_key" value="4b04a78e-1222-40c4-ba0d-5f8aaee83861">
          <input type="hidden" name="subject" value="New consultation request &mdash; K&Ouml;V website">
          <input type="hidden" name="from_name" value="K&Ouml;V Simply Interiors Website">
          <input type="checkbox" name="botcheck" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
          <div class="field-row">
            <div class="field">
              <label for="fname">First Name</label>
              <input id="fname" name="first_name" type="text" autocomplete="given-name" required>
            </div>
            <div class="field">
              <label for="lname">Last Name</label>
              <input id="lname" name="last_name" type="text" autocomplete="family-name" required>
            </div>
          </div>
          <div class="field-row">
            <div class="field">
              <label for="email">Email</label>
              <input id="email" name="email" type="email" autocomplete="email" required>
            </div>
            <div class="field">
              <label for="phone">Phone</label>
              <input id="phone" name="phone" type="tel" autocomplete="tel">
            </div>
          </div>
          <div class="field-row">
            <div class="field">
              <label for="showroom">Preferred Showroom</label>
              <select id="showroom" name="preferred_showroom" required>
                <option value="" disabled selected>Choose a showroom</option>
                <option>Houghton Lake, MI</option>
                <option>Paris, MI</option>
              </select>
            </div>
            <div class="field">
              <label for="scope">Project Scope</label>
              <select id="scope" name="project_scope">
                <option>Flooring</option>
                <option>Cabinetry</option>
                <option>Tile &amp; Stone</option>
                <option>Window Coverings</option>
                <option>Whole-home finish</option>
                <option>Kitchen</option>
                <option>Bathroom</option>
                <option>Not sure yet</option>
              </select>
            </div>
          </div>
          <div class="field">
            <label for="details">Project Details</label>
            <textarea id="details" name="message" placeholder="Rooms involved, rough timeline, anything already selected."></textarea>
          </div>
          <div class="form-foot">
            <button class="btn btn-solid" type="submit">Send Request <span class="btn-arrow" aria-hidden="true">&rarr;</span></button>
            <span class="fine">We'll follow up by email or phone, whichever you prefer.</span>
          </div>
          <p class="form-error" id="formError" role="alert" hidden>Something went wrong sending that. Please try again, or call the showroom nearest you.</p>
        </form>

        <div class="form-success" id="consultSuccess" role="status">
          <span class="dots gold" aria-hidden="true" style="justify-content:center;"><i></i><i></i></span>
          <h3>Request received.</h3>
          <p>Thanks &mdash; your request is on its way to the K&Ouml;V team. We'll be in touch shortly to set up your consultation.</p>
        </div>
      </div>
    </div>
  </section>
</main>
"""


# --------------------------------------------------------------------------
# GALLERY
# --------------------------------------------------------------------------
GALLERY = [
    ("Kitchens", [
        ("kitchen-walnut-island",     "White kitchen with a walnut island, quartz waterfall top and brass pendants", "Walnut Island Kitchen"),
        ("kitchen-sage",              "Sage green kitchen with white uppers, quartz island and brass hardware", "Sage Green Kitchen"),
        ("kitchen-olive-dining",      "Olive kitchen with a marble island, leather stools and a pro range", "Olive Kitchen &amp; Dining"),
        ("kitchen-hickory-island",    "Hickory kitchen with a faceted island, quartz top and dining nook", "Hickory Island Kitchen"),
        ("kitchen-double-oven",       "White kitchen with a double oven, custom hood and walnut floating shelves", "Double Oven Wall"),
        ("kitchen-white-dark-island", "White shaker kitchen with a dark stained island and brass pulls", "Dark Island Kitchen"),
        ("kitchen-sage-island",       "Sage kitchen from the island, with black appliances and gold hardware", "Sage Kitchen Island"),
        ("kitchen-hickory-front",     "Hickory island kitchen with mason-jar pendants and wide-plank floors", "Hickory Kitchen"),
        ("kitchen-hickory-pendants",  "Hickory island under glass pendants, framed by black-trim forest windows", "Island &amp; Pendants"),
        ("kitchen-subway-potfiller",  "White subway backsplash with a pot filler over an induction range", "Range Wall &amp; Pot Filler"),
        ("kitchen-white-pantry",      "White kitchen with a walnut island, floating shelves and pantry door", "Kitchen &amp; Pantry"),
        ("kitchen-panel-fridge",      "Panel-ready refrigerator built into custom cabinetry beside a black-trim window", "Built-In Refrigeration"),
        ("kitchen-cabin-fever",        "Cabin kitchen with sage cabinets, a farmhouse sink, granite counters and exposed timber beams", "Cabin Kitchen"),
        ("kitchen-lantern-pendants",   "White kitchen with a dark island, lantern pendants and leather counter stools", "Lantern Pendant Kitchen"),
        ("kitchen-green-brick-island", "Green kitchen with a reclaimed brick island, double wall ovens and maple floors", "Brick Island Kitchen"),
        ("kitchen-white-ash-island",   "Modern white kitchen with a white oak island front and integrated appliances", "Modern White Kitchen"),
        ("kitchen-butcher-block",      "Grey shaker kitchen with a maple butcher block island and shiplap backsplash", "Butcher Block Island"),
        ("kitchen-black-brass",        "Black and brass kitchen with rift oak cabinetry, chevron tile and a granite island", "Black &amp; Brass Kitchen"),
        ("kitchen-black-brass-range",  "Range wall with a mirrored chevron backsplash, bronze hood and brass shelving", "Chevron Range Wall"),
        ("kitchen-grey-black-stainless", "Grey shaker kitchen with black stainless appliances and a marble-look tile backsplash", "Grey Shaker Kitchen"),
        ("kitchen-grey-peninsula",      "Grey kitchen with a granite peninsula, seating for four and lantern pendants", "Granite Peninsula"),
        ("kitchen-lakeview-island",     "White kitchen with a stained island, quartz top and a lake view over the sink", "Lakeview Kitchen"),
        ("kitchen-lakeview-open",       "Open lakeview kitchen with full-height pantry cabinets and a quartz island", "Lakeview Island"),
        ("kitchen-cream-subway-range",  "Range wall with cream handmade subway tile, quartz counters and brass pulls", "Cream Subway Range Wall"),
        ("kitchen-forest-butcher-block","Forest green kitchen with a butcher block island and a two-storey shiplap hood", "Forest Green Kitchen"),
    ]),
    ("Baths", [
        ("bath-primary-suite",   "Primary bath with a marble-tile shower, double vanity and brass sconces", "Primary Bath Suite"),
        ("bath-spa-suite",       "Spa bath with a glass shower enclosure, soaking tub and forest views", "Spa Bath"),
        ("bath-navy-vanity",     "Bath with a navy vanity, black quartz top and marble-tile shower", "Navy Vanity Bath"),
        ("bath-grey-curbless",   "Grey vanity bath with a curbless shower and mosaic shower floor", "Curbless Shower Bath"),
        ("bath-hickory-vanity",  "Hickory double vanity with quartz counters, open to the primary bedroom", "Hickory Double Vanity"),
        ("bath-lower-level",     "Lower-level bath with a white vanity, gold fixtures and exposed black ceiling", "Lower Level Bath"),
        ("bath-white-hex-shower",      "White tile shower with a hexagonal mosaic accent, marble bench and niche", "Hex Accent Shower"),
        ("bath-olive-reclaimed",       "Olive bath with reclaimed wood vanities, farmhouse sinks and slate floors", "Reclaimed Wood Vanities"),
        ("bath-white-wood-vanity",     "Bright bath with a glass shower, wood vanity and marble-look quartz top", "Classic White Bath"),
        ("bath-green-woodtile",        "Green bath with a wood-look tile shower, brass fixtures and floating vanity", "Wood-Look Tile Bath"),
        ("bath-espresso-double-vanity", "Espresso double vanity with a linen tower, quartz top and brushed gold faucets", "Espresso Double Vanity"),
        ("bath-greige-double-vanity",   "Greige stained double vanity with black fixtures and charcoal tile floor", "Greige Double Vanity"),
        ("bath-freestanding-tub",       "Freestanding soaking tub beside a maple linen tower and a private toilet nook", "Freestanding Soaker"),
        ("bath-tub-linen-tower",        "Maple floor-to-ceiling linen tower next to a freestanding tub on charcoal tile", "Linen Tower &amp; Tub"),
        ("bath-marble-clawfoot",        "Marble-tile walk-in shower with a pebble floor beside a clawfoot tub", "Marble Shower &amp; Clawfoot"),
    ]),
    ("Living Spaces", [
        ("living-stone-fireplace", "Great room with a stone fireplace, vaulted wood ceiling and navy built-ins", "Great Room"),
        ("bedroom-primary",        "Primary bedroom with a linen bed, black dressers and a checkered wool rug", "Primary Bedroom"),
        ("stair-open-tread",       "Open-tread staircase with wood treads, a steel stringer and glass rail", "Open-Tread Stair"),
        ("living-fireplace-detail","Stone fireplace detail with a live-edge mantel and navy glass-front cabinets", "Fireplace &amp; Built-Ins"),
        ("stair-oak-iron",             "Oak staircase with wrought iron balusters, boxed newels and dark wide-plank floors", "Oak &amp; Iron Stair"),
        ("living-timber-truss",        "Vaulted great room with exposed timber trusses, a stone chimney and loft rail", "Timber Truss Great Room"),
        ("stair-pine-lit",             "Open-tread pine staircase with recessed step lighting and a hickory floor", "Lit Open Stair"),
        ("living-open-woodstove",      "Open living and dining space with a wood stove, white oak floors and a modern entry door", "Open Living &amp; Dining"),
        ("living-timber-loft-cabin",    "Timber-frame great room with a stone fireplace, sleeping loft and open kitchen", "Timber Frame Loft"),
    ]),
    ("Cabinetry &amp; Built-Ins", [
        ("pantry-butlers", "Butler's pantry with a walnut counter, white cabinetry and navy arabesque tile", "Butler's Pantry"),
        ("closet-walk-in", "Walk-in closet in hickory with adjustable shelving, hanging rods and drawers", "Walk-In Closet"),
        ("mudroom-log-wall",           "Mudroom with white cubby lockers, a stacked log feature wall and patterned tile floor", "Mudroom Lockers"),
        ("bar-coffee-wine",             "Coffee and wine bar with glass-front uppers, granite counter and marble tile backsplash", "Coffee &amp; Wine Bar"),
    ]),
    ("Details", [
        ("detail-cooktop-counter",   "Quartz countertop detail beside an induction cooktop with copper knobs", "Quartz &amp; Copper"),
        ("detail-dark-pulls",        "Dark stained drawer fronts with square brushed brass pulls", "Brass on Dark Oak"),
        ("detail-navy-butcherblock", "Navy island with a butcher block top and hammered nickel pulls", "Butcher Block Island"),
        ("detail-black-faucet",      "Matte black widespread faucet on a quartz vanity below a brass mirror", "Black &amp; Brass"),
    ]),
    ("Design Renderings", [
        ("rendering-kitchen", "3D rendering of a vaulted kitchen with an island, farmhouse sink and open shelving", "Kitchen Rendering"),
        ("rendering-living",  "3D rendering of an open great room with a linear fireplace and vaulted ceiling", "Great Room Rendering"),
    ]),
]


def gallery_group(title, items):
    """Last row widens to fill the width, so a section never ends ragged."""
    n = len(items)
    rem = n % 3
    out = []
    for i, (slug, alt, cap) in enumerate(items):
        span = 2
        if rem == 1 and i == n - 1:
            span = 6
        elif rem == 2 and i >= n - 2:
            span = 3
        out.append(shot(slug, alt, cap, span=span))
    cells = "\n        ".join(out)
    odd_cls = " fill-two" if n % 2 else ""   # two-up layouts need the last row filled too
    return f"""
    <div class="gallery-group">
      <div class="gallery-head">
        <h2>{title}</h2>
      </div>
      <div class="gallery-grid{odd_cls}">
        {cells}
      </div>
    </div>"""


_groups = "\n".join(gallery_group(t, items) for t, items in GALLERY)
_total = sum(len(i) for _, i in GALLERY)

GALLERY_MAIN = f"""
<main id="main">
  <section class="page-hero tone-dark">
    <div class="shell">
      <p class="crumbs"><a href="index.html">Home</a> &nbsp;/&nbsp; Gallery</p>
      <span class="eyebrow"><span class="dots gold" aria-hidden="true"><i></i><i></i></span> Gallery</span>
      <h1>Every surface, every space &mdash; finished.</h1>
      <p>Projects from across Central and Northern Michigan. Click any photo to enlarge.</p>
    </div>
  </section>

  <section class="band">
    <div class="shell">
      {_groups}
    </div>
  </section>

  <section class="band band-slate tone-dark">
    <div class="shell" style="text-align:center;">
      <span class="eyebrow" style="justify-content:center;"><span class="dots gold" aria-hidden="true"><i></i><i></i></span> Planning Something?</span>
      <h2 style="font-size:clamp(1.9rem,3.4vw,2.7rem);margin-top:1rem;">Bring us the room. We'll finish it.</h2>
      <div class="btn-row">
        <a class="btn btn-solid btn-wide" href="index.html#consult">Request a Free Consultation <span class="btn-arrow" aria-hidden="true">&rarr;</span></a>
      </div>
    </div>
  </section>
</main>
"""


# --------------------------------------------------------------------------
# LOCATION PAGES
# --------------------------------------------------------------------------
FB_ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22 12a10 10 0 1 0-11.6 9.9v-7H7.9V12h2.5V9.8c0-2.5 1.5-3.9 3.8-3.9'
           '1.1 0 2.2.2 2.2.2v2.5h-1.3c-1.2 0-1.6.8-1.6 1.6V12h2.8l-.4 2.9h-2.4v7A10 10 0 0 0 22 12z"/></svg>')
IG_ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.9.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4'
           '.2.4.3 1 .4 2.2.1 1.3.1 1.7.1 4.9s0 3.6-.1 4.9c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1 .3-2.2.4'
           '-1.3.1-1.7.1-4.9.1s-3.6 0-4.9-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.3-1-.4-2.2'
           '-.1-1.3-.1-1.7-.1-4.9s0-3.6.1-4.9c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1-.3 2.2-.4 1.3-.1 1.7-.1 4.9-.1zm0 3.1'
           'a6.7 6.7 0 1 0 0 13.4 6.7 6.7 0 0 0 0-13.4zm0 11a4.3 4.3 0 1 1 0-8.6 4.3 4.3 0 0 1 0 8.6zm8.5-11.3a1.6 1.6 0 1 1-3.2 0 1.6 1.6 0 0 1 3.2 0z"/></svg>')


def team_cards(people, two_up=False):
    """people: (name, role, photo-slug or None)."""
    cls = "team-grid two-up" if two_up else "team-grid"
    out = []
    for name, role, slug in people:
        if slug:
            media = ('<div class="team-photo">'
                     '<img src="assets/team/%s.jpg" alt="%s, %s at K&Ouml;V Simply Interiors" '
                     'width="800" height="1000" loading="lazy" decoding="async"></div>' % (slug, name, role))
        else:
            media = ph("Headshot Coming Soon!")
        out.append('<div class="team-card">%s\n          <p class="name">%s</p>\n'
                   '          <p class="role">%s</p>\n        </div>' % (media, name, role))
    return '<div class="%s">\n        %s\n      </div>' % (cls, "\n        ".join(out))


def _note(n):
    return f'<p class="todo"><strong>{n[0]}</strong><span>{n[1]}</span></p>' if n else ''


def location_page(name, address_html, map_url, phone, phone_href, handle,
                  people, two_up, addr_note, phone_note, hours, active):
    hours_rows = "".join(
        "<tr><th>{}</th><td{}>{}</td></tr>".format(
            d, ' class="closed"' if t == "Closed" else "", t)
        for d, t in hours
    )
    phone_html = (f'<a href="tel:{phone_href}">{phone}</a>' if phone_href else phone)
    addr_note_html = _note(addr_note)
    phone_note_html = _note(phone_note)
    return f"""
<main id="main">
  <section class="page-hero loc-hero tone-dark">
    <div class="shell">
      <p class="crumbs"><a href="index.html">Home</a> &nbsp;/&nbsp; Locations &nbsp;/&nbsp; {name}</p>
      <span class="eyebrow"><span class="dots gold" aria-hidden="true"><i></i><i></i></span> K&Ouml;V Showroom</span>
      <h1>{name}</h1>
    </div>
  </section>

  <section class="band">
    <div class="shell loc-grid">
      <div>
        <div class="info-list">
          <div class="info-block">
            <h3>Address</h3>
            <p class="big">{address_html}</p>
            <p class="map-link"><a href="{map_url}" target="_blank" rel="noopener">Get directions &rarr;</a></p>
            {addr_note_html}
          </div>
          <div class="info-block">
            <h3>Phone</h3>
            <p class="big">{phone_html}</p>
            {phone_note_html}
          </div>
          <div class="info-block">
            <h3>Follow</h3>
            <div class="social-row">
              <a class="social-chip" href="https://facebook.com/{handle}" rel="noopener">{FB_ICON} @{handle}</a>
              <a class="social-chip" href="https://instagram.com/{handle}" rel="noopener">{IG_ICON} @{handle}</a>
            </div>
          </div>
        </div>
      </div>

      <div class="loc-hours">
        <h2>Hours of Operation</h2>
        <table class="hours">
          <tbody>{hours_rows}</tbody>
        </table>
        <p class="hours-note">Showroom visits outside these hours are available by appointment &mdash; just ask when you request a consultation.</p>
      </div>
    </div>
  </section>

  <section class="band band-deep tone-dark">
    <div class="shell">
      <div class="sec-head wide">
        <span class="eyebrow"><span class="dots gold" aria-hidden="true"><i></i><i></i></span> The Team</span>
        <h2>Who you'll be working with.</h2>
      </div>
      {team_cards(people, two_up)}
    </div>
  </section>

  <section class="band band-tint">
    <div class="shell" style="text-align:center;">
      <span class="eyebrow" style="justify-content:center;"><span class="dots gold" aria-hidden="true"><i></i><i></i></span> Start Here</span>
      <h2 style="font-size:clamp(1.9rem,3.4vw,2.7rem);margin-top:1rem;">Book time with a design consultant.</h2>
      <div class="btn-row">
        <a class="btn btn-solid btn-wide" href="index.html#consult">Request a Free Consultation <span class="btn-arrow" aria-hidden="true">&rarr;</span></a>
      </div>
    </div>
  </section>
</main>
"""


# --------------------------------------------------------------------------
PAGES = {
    "index.html": (
        "KÖV Simply Interiors",
        "A Michigan-born design &amp; interiors studio finishing houses so they feel like home. Flooring, cabinetry, tile and window coverings under one roof.",
        "", HOME_MAIN),
    "gallery.html": (
        "KÖV Gallery",
        "Finished kitchens, baths, flooring, cabinetry and window coverings from across Central and Northern Michigan.",
        "gallery", GALLERY_MAIN),
    "houghton-lake.html": (
        "KÖV Houghton Lake",
        "The KÖV showroom in Houghton Lake, Michigan — address, hours, and the team.",
        "houghton",
        location_page(
            "Houghton Lake",
            "2485 W Houghton Lake Drive<br>Houghton Lake, MI 48629",
            "https://www.google.com/maps/search/2485+W+Houghton+Lake+Drive+Houghton+Lake+MI+48629",
            "989.422.3545", "+19894223545", "KOVHoughtonLake",
            [("Alissa Burden", "Office Manager", "alissa-burden"),
             ("Tara Kubiak", "Designer / Sales", "tara-kubiak"),
             ("Cassidy Westdrop", "Designer / Sales", "cassidy-westdrop"),
             ("Autumn Jobson", "Sales Associate", "autumn-jobson")],
            False,
            None,
            None,
            [("Monday &ndash; Friday", "9:00 am &ndash; 5:00 pm"),
             ("Saturday", "10:00 am &ndash; 3:00 pm"),
             ("Sunday", "Closed")],
            "houghton")),
    "paris.html": (
        "KÖV Paris",
        "The KÖV showroom in Paris, Michigan — address, hours, and the team.",
        "paris",
        location_page(
            "Paris",
            "21498 Northland Drive<br>Paris, MI 49338",
            "https://www.google.com/maps/search/21498+Northland+Drive+Paris,+MI+49338",
            "231.796.0330", "+12317960330", "KOVParis",
            [("Kelli McCuaig", "Sales Manager", "kelli-mccuaig"),
             ("Madalynn Stout", "Office Manager", "madalynn-stout")],
            True,
            None,
            None,
            [("Monday &ndash; Friday", "10:00 am &ndash; 5:00 pm"),
             ("Saturday", "Closed"),
             ("Sunday", "Closed")],
            "paris")),
}

CANON = {
    "index.html": ("/", '{"@context":"https://schema.org","@type":"HomeAndConstructionBusiness","name":"KÖV Simply Interiors","url":"https://kovinteriors.com","logo":"https://kovinteriors.com/assets/kov-logo.png","image":"https://kovinteriors.com/assets/og-image.jpg","description":"A Michigan design and interiors studio finishing homes — flooring, cabinetry, tile and stone, countertops, window coverings and plumbing fixtures under one roof.","areaServed":"Central and Northern Michigan","department":[{"@type":"HomeAndConstructionBusiness","name":"KÖV Simply Interiors — Houghton Lake","url":"https://kovinteriors.com/houghton-lake","telephone":"+1-989-422-3545","address":{"@type":"PostalAddress","streetAddress":"2485 W Houghton Lake Drive","addressLocality":"Houghton Lake","addressRegion":"MI","postalCode":"48629","addressCountry":"US"},"openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"09:00","closes":"17:00"},{"@type":"OpeningHoursSpecification","dayOfWeek":"Saturday","opens":"10:00","closes":"15:00"}]},{"@type":"HomeAndConstructionBusiness","name":"KÖV Simply Interiors — Paris","url":"https://kovinteriors.com/paris","telephone":"+1-231-796-0330","address":{"@type":"PostalAddress","streetAddress":"21498 Northland Drive","addressLocality":"Paris","addressRegion":"MI","postalCode":"49338","addressCountry":"US"},"openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"10:00","closes":"17:00"}]}]}'),
    "gallery.html": ("/gallery", ""),
    "houghton-lake.html": ("/houghton-lake", '{"@context":"https://schema.org","@type":"HomeAndConstructionBusiness","name":"KÖV Simply Interiors — Houghton Lake","url":"https://kovinteriors.com/houghton-lake","telephone":"+1-989-422-3545","image":"https://kovinteriors.com/assets/og-image.jpg","parentOrganization":{"@type":"Organization","name":"KÖV Simply Interiors","url":"https://kovinteriors.com"},"address":{"@type":"PostalAddress","streetAddress":"2485 W Houghton Lake Drive","addressLocality":"Houghton Lake","addressRegion":"MI","postalCode":"48629","addressCountry":"US"},"openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"09:00","closes":"17:00"},{"@type":"OpeningHoursSpecification","dayOfWeek":"Saturday","opens":"10:00","closes":"15:00"}]}'),
    "paris.html": ("/paris", '{"@context":"https://schema.org","@type":"HomeAndConstructionBusiness","name":"KÖV Simply Interiors — Paris","url":"https://kovinteriors.com/paris","telephone":"+1-231-796-0330","image":"https://kovinteriors.com/assets/og-image.jpg","parentOrganization":{"@type":"Organization","name":"KÖV Simply Interiors","url":"https://kovinteriors.com"},"address":{"@type":"PostalAddress","streetAddress":"21498 Northland Drive","addressLocality":"Paris","addressRegion":"MI","postalCode":"49338","addressCountry":"US"},"openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"10:00","closes":"17:00"}]}'),
}

for fname, (title, desc, active, main) in PAGES.items():
    canonical, jsonld = CANON[fname]
    html = head(title, desc, canonical, jsonld) + header(active) + main + FOOTER
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", fname, len(html) // 1024, "KB")
