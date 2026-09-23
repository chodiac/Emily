# Salon Emilly — redizajn sajta

Statički sajt (HTML + CSS + JS, GSAP + ScrollTrigger + Lenis). Gotov sajt je u **glavnom folderu** (`index.html` je u korenu), tako da ga GitHub Pages može direktno objaviti.

## Objava na GitHub Pages
1. Ceo sadržaj ovog foldera stavite u koren repozitorijuma (`index.html` mora biti na vrhu).
2. Na GitHubu otvorite **Settings → Pages → Build and deployment**, izaberite **Deploy from a branch**, zatim `main` i folder `/ (root)`.
3. Svi linkovi su relativni, pa sajt radi i na `korisnik.github.io` i na `korisnik.github.io/ime-repozitorijuma/`.
4. Fajl `.nojekyll` je već prisutan.

Napomena: stranica `404.html` učitava stilove ispravno samo na adresama prvog nivoa (npr. `/nepostojeca-strana`). Na domenu sa korena ovo nije problem.

## Struktura
| Putanja | Šta je |
|---|---|
| `index.html`, `o-nama/`, `usluge/`, `galerija/`, `kontakt/`, 11 stranica tretmana, 3 lokacijske stranice, `404.html` | **generisane** stranice (ne menjati ručno) |
| `assets/css/main.css` | generisan iz `src/css/*.css` |
| `assets/js/` | JavaScript (ES moduli), menja se direktno |
| `assets/img/` | optimizovane WebP slike, generisane iz `source-assets/original-images` |
| `assets/vendor/` | GSAP, ScrollTrigger, Lenis |
| `content/site.json` | uređeni sadržaj (kontakt, usluge, slike, brendovi) |
| `content/extracted/*.json` | doslovni tekst, cene i FAQ preuzeti sa originalnog sajta |
| `builder/` | Python šabloni stranica |
| `tools/` | izvlačenje sadržaja, optimizacija slika, lokalni server |
| `RESEARCH-AND-PLAN.md` | popis sadržaja, analiza EVER sajta, plan |

## Izmene
```bash
python build.py                    # ponovo generiše sve stranice i main.css
python tools/optimize_images.py    # samo kada se menjaju slike
python tools/serve.py              # lokalni pregled na http://localhost:5184/
```

Razvojne opcije u adresi:
- Animacije su uvek uključene. Posetilac ih može isključiti prekidačem „Animacije“ u footeru (izbor se pamti), a isto radi i `?motion=reduce`.
- `&raw` — isključuje Lenis (obično skrolovanje).
