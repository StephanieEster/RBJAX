# Guardians Home Health Care — Hostinger

## Resumo rápido (PT-BR)

1. No hPanel da Hostinger, abra **Gerenciador de Arquivos → public_html**, apague o conteúdo padrão (ex.: `default.php`) e envie o ZIP. Extraia **direto** em `public_html` (o `index.html` e o `.htaccess` precisam ficar na raiz, não dentro de uma subpasta).
2. Ative o **SSL** do domínio (hPanel → Segurança → SSL). O `.htaccess` já força HTTPS.
3. **E-mail confiável (recomendado):** crie uma conta de e-mail no domínio (ex.: `website@guardianshomehelphllc.com`), copie `guardian-mail-config.sample.php` para **uma pasta acima** de `public_html` com o nome `guardian-mail-config.php` e preencha usuário/senha. Sem esse arquivo o site usa o `mail()` do PHP, que costuma cair no spam do Gmail.
4. O site já está configurado para **guardianshomehelphllc.com** (sem www; o www redireciona). Por segurança, o formulário só aceita envios vindos desse domínio: se quiser testar no domínio temporário da Hostinger, deixe `SITE_DOMAIN = ''` no topo de `send-form.php` e volte depois.
5. Teste os 3 formulários (topo da home, página de contato e popup) e confira a caixa de entrada **e o spam** de `guardianshomehealthllc@gmail.com`. Espere 1 minuto entre testes (anti-spam).
6. Abra `/robots.txt` e `/sitemap.xml` e envie o sitemap no Google Search Console.
7. Se editar `assets/styles.css` ou `assets/site.js`, troque `?v=20261008` nas páginas HTML por um novo valor (ex.: a data), senão os visitantes continuam com a versão em cache.

---

## Full installation (EN)

1. Create the Hostinger project using **Custom PHP/HTML website**. Select PHP 8.1 or newer (7.4+ also works).
2. Extract this ZIP directly into `public_html`. `index.html`, `send-form.php`, `.htaccess` and `assets` must be immediately inside that folder.
3. Connect the real domain and enable SSL/HTTPS in Hostinger. Choose one preferred host (www or non-www) and set the hosting redirect to it.
4. `SITE_DOMAIN` at the top of `send-form.php` is set to `guardianshomehelphllc.com` (www is redirected to it by `.htaccess`). Requests from any other host are rejected; set it to `''` temporarily to test on a Hostinger preview domain. `site_domain` in the private config overrides it. Never set it to the recipient's Gmail domain. The sender will be `website@YOUR_REAL_DOMAIN` (or the SMTP mailbox), and the visitor's email is used only in Reply-To.
5. Forms send only to `guardianshomehealthllc@gmail.com`. This final briefing address supersedes the earlier `homehelph` spelling. Browser values cannot change the recipient, subject or sender company name.
6. Perform a real submission from the published site. Check the inbox **and spam folder**. Confirm name, phone, email, care interest, optional message/city and consent record arrived. Test hero, contact and popup forms. There is a 60-second rate limit between valid submissions from one network address.
7. **SMTP (recommended).** Create a mailbox for the domain in hPanel → Emails (e.g. `website@YOUR_REAL_DOMAIN`). Copy `guardian-mail-config.sample.php` to the folder **above** `public_html` (e.g. `domains/YOUR_REAL_DOMAIN/guardian-mail-config.php`) and fill in `smtp_user`/`smtp_pass` (Hostinger: `smtp.hostinger.com`, port 465 + `ssl`, or 587 + `tls`). `send-form.php` then sends through authenticated SMTP with TLS certificate verification, and automatically falls back to PHP `mail()` if SMTP is unreachable. A copy placed inside `public_html` also works and is blocked by `.htaccess`, but outside is safer. No library (PHPMailer/Composer) is needed. In hPanel → Emails → DNS, make sure SPF, DKIM and DMARC are active for the domain. A success response means the mail server accepted the message, not that Gmail delivered it to the inbox.
8. Verify `/robots.txt` and `/sitemap.xml` open after upload. Both are generated using the published domain by the included PHP files and rewrite rules. Relative canonical links resolve to the published host. Submit `/sitemap.xml` in Google Search Console. Canonical links, `og:url`, the social preview image (`assets/images/og-image.jpg`, 1200×630) and the structured data use `https://guardianshomehelphllc.com`; robots.txt and sitemap.xml use the same fixed URL. Test the preview at https://developers.facebook.com/tools/debug/ and the structured data at https://search.google.com/test/rich-results.
9. Verify menu and service dropdown on mobile, image proportions, footer logo and popup closing by button, backdrop and Esc. The scroll popup appears once per browser session and is suppressed after a form field is focused. To repeat a test, use a new private window/session.
10. Review the published privacy/terms copy against the company's actual processes. Confirm final non-medical service tasks and licensing/authorization status before advertising or starting any care arrangements. The supplied briefing says the company is newly opened and is preparing its licensing application; no active US license, insurance or integrative medical service is claimed. Per the client (Oct 2026), daytime, overnight and round-the-clock care can be arranged, and the services list on the home and Services pages (24 Hour, Alzheimer’s, Companion, Dementia, End-of-Life, Live-In, Palliative, Parkinson’s, Personal, Respite, Transition to Home and Veterans In-Home Care) was added at the client’s request; confirm each service is authorized before advertising it.
11. Social profiles, testimonials, prices and clinical services were not added without confirmed information. The website includes service-interest pages based on the briefing and brandbook; scope is discussed individually.

## Content and assets

- Brand palette: #19334c, #849872, #6b89a1, #c9b79f, #fffcf9.
- Titles: Lora. Body: Poppins, minimum 16px.
- Original brandbook logo artwork is extracted as SVG; width and height stay proportional.
- Client-supplied photography is converted to WebP; pre-existing facial obscuring is preserved.
- Two generated illustrative photographs are included in `assets/images/home-companionship.webp` and `garden-companionship.webp`. They show generic companionship scenes, not actual clients or employees.
- Pages: Home, care services, four care-interest pages, founder story, service areas, contact, privacy, terms and 404.

## Hardening included in this package

- **Client revision (Oct 2026)**: company name corrected to Guardians Home Health Care (pages, e-mails, consent text version 2026-10-08); the founder’s name kept only in the founder story; new hero with a “Where is care needed?” finder that pre-fills the city on the contact form; services grid near the top of the home page; bold Poppins headings with high-contrast text; footer brand rebuilt as a PNG icon plus text (the SVG logo rendered with a black box on some phones); name tag blurred in the family photo.

- **Visual refresh** (CSS "Design layer" in `assets/styles.css`): pill buttons and eyebrows, arch-framed portraits echoing the logo roof, card-based stats, services, steps, FAQ and contact blocks with soft shadows, overlapping highlights strip under the hero, decorative leaf motifs, a navy closing call-to-action card and a brand-gradient footer accent. Brand colors and fonts unchanged.

- **Self-hosted fonts** (Lora and Poppins, SIL Open Font License, in `assets/fonts/`): no Google Fonts request, no render-blocking `@import`, works under the strict Content-Security-Policy.
- **Images** recompressed (about 45% lighter) with 800px variants served through `srcset` on phones. The hidden photo lightbox no longer downloads a 1600px image on every page.
- **Forms** post to `send-form.php` even without JavaScript (a styled confirmation page is returned instead of leaking the data into the URL). The JavaScript handler tolerates non-JSON error pages (e.g. a host firewall page), prevents double submission and uses a text honeypot plus a minimum fill time. Client-side `_to`/`subject` fields were removed.
- **Endpoint**: works on PHP 7.4–8.3; origin check compares the host only, so it keeps working behind Hostinger CDN/Cloudflare; the rate limit is written only after a successful send and is skipped (logged) if temporary storage is unavailable, so a real inquiry is never blocked by a server folder issue; `mail()` sets the envelope sender (`-f`) for SPF alignment and retries without it if the host refuses.
- **`.htaccess`**: HTTPS redirect (CDN-safe), `/index.html` → `/`, extensionless URLs (`/about` → `about.html`), Content-Security-Policy, HSTS, COOP, cache rules (CSS/JS versioned with `?v=`), compression, correct MIME types, and blocking of dotfiles, `.md`, backups, archives and the mail config.
- **404 page** uses root-relative paths, so it renders correctly at any missing URL depth, and is marked `noindex`.
- **SEO/tech**: absolute canonical/Open Graph URLs for guardianshomehelphllc.com, 1200×630 social preview image, Organization `@id`/`url`/`logo` and WebSite structured data, home canonical is `/` (sitemap matches), sitemap has priorities and skips missing files, `apple-touch-icon` and `site.webmanifest` added.
- **Adding third-party tools later** (Google Analytics, Tag Manager, chat widget, Google Maps embed, Meta Pixel): add their domains to the `Content-Security-Policy` line in `.htaccess`, otherwise the browser will block them.

## Operational notes

The endpoint validates method, payload size, request origin, action, honeypot, field formats, allowed services, source and explicit consent. It rejects header line breaks and ignores submitted recipient/sender/subject overrides. Rate files contain only hashed identifiers and timestamps in private server temporary storage (or a hidden folder above `public_html`). Inquiry content is sent to email and not saved to a website database. No external lead-submission service is used.

This ZIP contains no SMTP password or external API credential; without the private config it uses PHP `mail()`. The website is ready for Hostinger upload, but final email delivery must be verified on the live hosting account as described above.
