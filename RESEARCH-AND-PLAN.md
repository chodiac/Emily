# Salon Emilly — istraživanje, popis sadržaja i plan redizajna

Research date: 2026-09-23. Sources: https://kozmetickisalonemilly.rs (all pages fetched and read) and https://www.ever.co.id (inspected in a real browser, including its GSAP/Lenis scripts and its Webflow IX2 interaction data).

---

## 1. Emilly: map of pages and content

| Original URL | Content found | In the redesign |
|---|---|---|
| `/` Početna | H1 "Kozmetički salon u Beogradu – Salon Emilly", intro text (Voždovac, Ustanička 84b, Emilija Bojić), 8 service cards with short descriptions, 6-photo gallery, **Poklon vaučer** text, **19 client reviews** (Google + Sredi me links), CTA "Zakažite termin već danas" | `/` |
| `/o-nama/` | Salon story in the first person (Emilija Bojić, decades of experience, work with teenagers, anti-age care), **partner brands** (Dr. med. Christine Schrammek – Green Peel, Ericson Laboratoire, Biodroga, Physio Natura, MCCM Medical Cosmetic, Esthemax), **awards** (Factor Estetic; Top salon on Sredi me), mission. 2 photos of the owner | `/o-nama/` |
| "Usluge" (dropdown only, no overview page) | 11 categories | new overview page `/usluge/` + full price list |
| `/higijenski-tretmani-lica/` | 4 text blocks, **5 prices**, 3 FAQ | same URL |
| `/ultrazvucno-ciscenje-lica/` | 4 blocks, **4 prices**, 3 FAQ | same URL |
| `/beauty-tretmani/` | 4 blocks, **9 prices**, 3 FAQ | same URL |
| `/revitalizujuci-tretmani/` | 4 blocks, **16 prices**, 3 FAQ | same URL |
| `/lux-tretmani/` | 4 blocks, **2 Spa day packages**, 3 FAQ | same URL |
| `/green-peel-tretmani/` | 4 blocks, **6 prices**, 3 FAQ | same URL |
| `/higijenski-tretmani-ledja/` | 4 blocks, **5 prices**, 3 FAQ | same URL |
| `/dodaci-tretmanima/` | 4 blocks, **15 prices**, 3 FAQ | same URL |
| `/masaze/` | 4 blocks, **8 prices**, 3 FAQ | same URL |
| `/madero-masaze/` | 4 blocks, **7 prices**, 3 FAQ | same URL |
| `/anticelulit-masaze/` (menu: "Anticelulit program") | 4 blocks, **8 prices**, 3 FAQ | same URL |
| `/galerija/` | 33 photos (mostly before/after, no captions) | `/galerija/` |
| `/kontakt/` | email, phone, WhatsApp/Viber icons, hours, address, transit lines, Google map, Google rating 4.9, Sredi me "Top salon", counters (3+ decades, 100+ treatments, 7500+ clients), contact form | `/kontakt/` |
| `/kozmeticki-salon-vozdovac/`, `/kozmeticki-salon-dusanovac/`, `/kozmeticki-salon-sumice/` | Local SEO pages (not in the menu; linked from text and the footer) | kept at the same URLs |

**Contact details (unchanged):** Ustanička 84b, Voždovac, 11000 Beograd · 064/11-62-333 · salonemilly7@gmail.com · Mon–Fri 12–20, Sat 09–17, Sun closed · Lines 17, 25, 25p, 26, 30, 31 · Instagram `salon_emilly_`, Facebook, TikTok `@salonemilly`, Google profile (share.google link).

**Booking path on the original:** every "Zakaži termin" button leads to `/kontakt/`.

**Brand:** logo SVG (gold crown and face profile, #DEC191), petrol green #253D3F, gold #DEC292, Marcellus and DM Sans fonts.

## 2. EVER: what I observed

The source code and interaction data confirm this stack: Webflow + GSAP 3.12 + ScrollTrigger + CustomEase + Lenis + SplitType + Flickity + Lottie.

**Loader**
- Brown screen. The EVER wordmark appears through a mask.
- A progress bar along the bottom and a 0→100 counter run for 6 s on a custom "stepped" ease. On a repeat visit (sessionStorage) the counter starts at 75.
- Exit: the top bar moves down 100% (500 ms, inQuart). The logo moves up −100% and fades out (delay 300 ms). The whole loader then fades out (300 ms, inOutQuart).

**Smooth scroll**
- Lenis, duration 1.5, expo-out easing `1-2^(-10t)`.
- Turned off on touch devices (`smoothTouch:false`).

**Navigation**
- Transparent bar: hamburger on the left, logo in the centre, "MAKE AN APPOINTMENT" on the right.
- The menu is a full-screen black overlay (fade 300 ms). It has:
  - a giant "MENU" word (135 px) with social links underneath;
  - a numbered service list (001–011, 40 px) in the right column;
  - secondary links marked with "/";
  - a "FOR BOOKING" block (WhatsApp / call) and a CONTACT US button.
- Burger animation: the top and bottom lines shrink to 0 (200 ms, inQuint), then the middle lines rotate 45° and 90° (400 ms, inOutQuint) to form an X.
- Link hover: the other items dim to 0.2 opacity and a small arrow animation plays.

**Home hero**
- Full-bleed close-up portrait with a dark overlay.
- Huge lowercase serif "beauty in every detail" (Bradford).
- Small "SCROLL TO EXPLORE" at the bottom.

**Arc carousel ("tricks-slider", Flickity)**
- Wide cards on a curve: each card rotates (±6°) and shifts vertically (±60%) by its distance from the centre.
- The image inside each card has parallax (up to 49%).
- Supports drag and wrap-around, with a progress bar underneath.
- Above it, a quote revealed line by line.

**Floating images (Header 80, 2700 px, pinned)**
- A centred heading stays sticky. Two image columns rise at different speeds (−85% / −60%).
- Each image's opacity grows as it rises.

**Numbered services over one photo (Layout 468)**
- A full-bleed photo with six numbered points (01–06).
- Hovering a point shows that service's card (image and text), turns the point's text dark and changes its opacity from 0.21 to 0.8.
- On mobile the points disappear and the services become stacked cards (square image and text).

**Text marquee:** "BEAUTY IN EVER DETAILS" repeats in an endless strip.

**"PERSONALISED SERVICES"**
- The heading is split into characters that reveal on scroll.
- Beside it: a portrait video with a play control and a "CHECK ALL SERVICES" button.

**Expanding image CTA (Layout 517, 1800 px, pinned)**
- The image grows from 20%×40% to 100%×100% of the viewport (scroll 2–48%).
- The text block moves in from below (y 100%→0) and scales from 0 to 1.
- Used for the appointment CTA and for the contact form.

**Service-detail hero (Header 81, 2700 px, pinned)**
- Brown background. On the left: a small serif number "001", a 130 px serif title, a vertical "SCROLL" label with a growing line, a subtitle and body text.
- On the right: an image at 50% width and full height. It widens to 100% over the first 60% of the scroll.

**Service detail, further sections**
- A statement section.
- Floating images with "WHY…".
- A numbered list of options (001, 002…) with images.
- A testimonial.
- An expanding-image CTA ("Download pricing").
- A FAQ accordion on a textured background.

**Services page (Portfolio 22)**
- A numbered list in the right column (80 px rows) and a sticky square image on the left that changes on hover.
- Hover also dims the other rows to 0.2.

**About page**
- Statement header in large uppercase.
- An image that "shrinks into place" (width 200%→100%, 1400 ms, outQuart).
- A history section.
- A pinned section whose headline fades and scales to 0.95 while a video frame grows to 100vh.
- Two rows of image marquee in opposite directions (30 s and 70 s).
- An expanding-image contact form.

**Micro-interactions**
- Button underline fills from 0→100% (300 ms).
- Image hover scale 1.125 (680 ms, inOutQuad).
- Marquee card hover: container scales to 0.95 and the image to 1.2 (800 ms, outQuart).
- Horizontal lines grow 0→100% over 2 s (outQuart) when they scroll into view.
- Vertical "text wheel": a scroll-linked list of seven large words, each step −5 rem, with opacity 1 / 0.5 / 0.
- Stacked images: slide in 10% from the side and fade in, one after another, as you scroll.

**Mobile**
- The heaviest pinned sections are hidden or simplified; the services hotspots become cards.
- The hero heading is 52 px; native scroll is used.

**Seen only as code, not verified visually**
- The "variables-color-scroll" script (background colour changes by section).
- Details of the gfluo text presets (`data-gsap=txt/par`).
- The browser pane was hidden, so I couldn't take screenshots of every scroll position. I checked positions, transforms and opacities through the live DOM at each scroll position instead.

**Not observed on EVER:** a custom cursor, page-to-page transitions, or a lightbox gallery.

## 3. Plan by page (Emilly)

The design system:
- Colours: petrol green #253D3F, deepened for backgrounds; the logo's gold #DEC292; ivory and sand.
- Type: Instrument Serif for large lowercase headings (the role Bradford plays on EVER) and Manrope for body text.
- Logo: the original SVG.

**Global**
- EVER-style loader: petrol background, the logo revealed through a mask, the counter and bar on the same custom ease. It is shortened: about 2.4 s on the first visit, not shown on later pages in the same session.
- Lenis with EVER's parameters.
- Navigation and menu, including the burger animation and the dimming hover.
- Underline-fill buttons and growing lines.
- Background-colour transitions between sections.
- *New:* a page transition (petrol curtain). A service image expands to the position of the hero image on the detail page.
- *New:* a "Prevuci" (drag) cursor label on carousels, desktop only.

**Početna (home)**
1. Hero entrance: the image scales from 1.25 to 1 and reveals through a clip; the heading rises line by line through masks.
2. Quote from the site shown line by line, plus the **arc carousel of all 11 categories**.
3. Floating images with the salon story (Emilija Bojić) and a sticky heading.
4. **Numbered service sequence 01–08** (the home page's cards) over a full-bleed photo that changes on hover or focus. On mobile these become cards.
5. Marquee: "Salon Emilly · ritual lepote i zdravlja".
6. "Personalizovani tretmani": the heading splits into characters, next to a portrait and counters.
7. **Text wheel** listing the partner brands (scroll-linked).
8. Reviews: all 20 real ones in a draggable strip.
9. Gift voucher.
10. Expanding-image CTA "Zakažite termin već danas".

**O nama (about)**
1. Statement header.
2. Image that "shrinks into place".
3. Story with line reveals.
4. Brand list numbered 001–006, with dimming on hover.
5. Awards with growing lines.
6. Mission in a pinned section (fade and scale to 0.95).
7. Two rows of gallery marquee.
8. Expanding-image CTA.

**Usluge (new overview)**
1. Portfolio-22 layout: a sticky image beside a numbered list 001–011, split into "Lice" and "Telo".
2. *New:* an editorial price index for all 85 prices, with jumps between categories.

**Individual treatment pages (×11)**
1. Header 81: number, title, vertical "Skroluj", an image widening from 50% to 100%.
2. The four original text blocks as numbered editorial chapters, with line reveals.
3. "U ponudi": price list with numbered rows and growing lines.
4. FAQ accordion.
5. Links to related treatments (kept from the original text).
6. Expanding-image CTA.
7. A large "Sledeći tretman" block with an image that leads into the next page.

**Galerija**
1. Arc carousel of photos from the salon.
2. Grid of all 33 photos with clip and scale reveals.
3. *New:* a lightbox that grows from the thumbnail, with arrow-key, swipe and Esc support and a 01/33 counter.

**Kontakt**
1. Large heading.
2. Contact rows with fill hover: phone, WhatsApp, Viber, email.
3. Opening hours, with today highlighted (*new*).
4. Location and transit lines, and a map that loads on demand.
5. Google 4.9 and Sredi me badges, and the counters.
6. A form that prepares an email or a WhatsApp message.

**Location pages ×3:** full original content in a simpler editorial template.

**Mobile:** no pinning in the floating-images and expanding-image sections (static composition instead), cards instead of hotspots, native scroll, larger touch targets, swipe in the lightbox and carousel.

**Reduced motion:** no loader, no Lenis, no pinning or scrub; content is fully visible straight away and only short opacity transitions remain.

## 4. Unavailable or needing confirmation

- **WhatsApp and Viber on the original have no working link** (the icons have no href). The redesign uses the salon's own number: `wa.me/381641162333` and `viber://chat?number=%2B381641162333`. **The salon needs to confirm the number is on WhatsApp and Viber.**
- **Contact form:** the original uses WordPress Contact Form 7, which can't work on a static site. The redesign's form opens an email to salonemilly7@gmail.com, or a WhatsApp message, with the text already filled in. Connecting it to a server-side form service is a separate step.
- **No per-service photos:** the service pages on the original have only decorative PNGs. The redesign uses the existing real photos from the gallery and home page (assignments listed in `content/site.json`). The 4 hero-style photos on the original (`h1-slider*`) come from the theme, not from the salon; they are used only as atmospheric images.
- **The gallery has no captions or categories.** None were invented; the alt text is generic ("Rezultat tretmana u salonu Emilly").
- **The image on the Voždovac page** (`ChatGPT-Image…png`) appears to be an AI render of the storefront. It is kept only where it was on the original.
- **Videos:** Emilly has none, so EVER's video sections use photos with a slow scale.
- **TikTok and Google links** are kept exactly as found.
- **Nothing was added:** no prices, testimonials, credentials or results beyond what appears on the original site.
