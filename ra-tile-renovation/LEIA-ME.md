# R.A Tile Renovation — Website (HTML/PHP para Hostinger)

Site institucional + captação de leads para a **R.A Tile Renovation** (Manchester, NH), em inglês (público americano), com a identidade visual do brandbook (azul-marinho, dourado metálico e prata; Archivo Black nos títulos e Poppins no texto).

## Páginas

| URL | Arquivo | Conteúdo |
|---|---|---|
| `/` | `index.php` | Home: hero com formulário, serviços, destaque banheiros, diferenciais, processo, galeria, sobre, áreas, FAQ, CTA |
| `/bathroom-shower-remodeling` | `bathroom-shower-remodeling.php` | Showers & Bathrooms (carro-chefe) |
| `/tile-flooring` | `tile-flooring.php` | Pisos de tile (+ menção a LVP) |
| `/kitchen-backsplash` | `kitchen-backsplash.php` | Backsplash de cozinha |
| `/fireplace-tile` | `fireplace-tile.php` | Fireplace |
| `/about` | `about.php` | História do Renato e Anderson |
| `/service-areas` | `service-areas.php` | Cidades de NH (sem MA/ME) + mapa |
| `/contact` | `contact.php` | SMS / ligação / e-mail / Instagram + formulário |
| `/thank-you` | `thank-you.php` | Página de conversão (noindex, dispara eventos de Ads/Pixel) |
| `/privacy-policy` | `privacy-policy.php` | Política de privacidade (inclui consentimento SMS) |
| `/sitemap.xml`, `/robots.txt` | `sitemap.php`, `robots.php` | Gerados automaticamente a partir do domínio configurado |

As 4 páginas de serviço usam o mesmo template (`includes/service-template.php`); os textos ficam em `includes/data.php`.

## Como publicar na Hostinger

1. **hPanel → Sites → Gerenciador de Arquivos → `public_html`**.
2. Apague o `default.php` da Hostinger (se existir).
3. Envie o arquivo **`ra-tile-renovation-hostinger.zip`** e clique em **Extrair** dentro de `public_html`
   (ou envie o *conteúdo* da pasta `public_html/` deste projeto — incluindo os arquivos ocultos `.htaccess`).
4. **hPanel → Segurança → SSL**: ative o SSL (o `.htaccess` já força HTTPS e remove o `www`).
5. Abra `includes/config.php` e ajuste (veja abaixo).
6. Teste o formulário e confira se o lead chegou no e-mail.

> PHP 7.4+ (recomendado 8.1+). Nenhum banco de dados é necessário.

## Prévia no Vercel (enquanto não há Hostinger)

O Vercel **não executa PHP** — se você subir a pasta `public_html`, ele entrega o `index.php` como arquivo e o navegador faz download. Por isso existe uma **versão estática** pronta na pasta **`vercel/`** (e no arquivo `ra-tile-renovation-vercel.zip`):

1. Descompacte `ra-tile-renovation-vercel.zip` (ou use a pasta `vercel/`).
2. No Vercel, arraste a **pasta** para o projeto (Vercel Drop / "drop your project"), ou rode `vercel --prod` dentro dela.
3. O formulário, nessa versão, envia pelo **FormSubmit** (grátis, sem servidor). No **primeiro envio**, o FormSubmit manda um e-mail de ativação para `tilerenovationpro@gmail.com` — clique em **Activate Form** uma única vez; depois os leads chegam direto no Gmail.

Para regenerar a versão estática depois de editar textos/imagens (precisa de PHP instalado):

```bash
php tools/build-static.php https://ra-tile-renovation.vercel.app vercel
```

Troque a URL se o domínio do Vercel for outro (ela vira o canonical e o sitemap). Quando migrar para a Hostinger, use a pasta `public_html` normalmente — lá o formulário volta a usar o `send.php` (SMTP + backup CSV).

## Configuração — `includes/config.php`

Tudo o que muda fica nesse arquivo:

- `SITE_URL` → **troque pelo domínio real** (ex.: `https://ratilerenovation.com`). É usado no canonical, sitemap, Open Graph e schema.
- Telefone, e-mail, Instagram, Facebook e Google Business (preencher Facebook/GMB quando existirem).
- `LEAD_TO` → e-mail que recebe os leads (padrão: `tilerenovationpro@gmail.com`).
- `MAIL_FROM` → **precisa ser uma caixa de e-mail do próprio domínio** (crie em hPanel → E-mails, ex.: `no-reply@seudominio.com`). A Hostinger bloqueia envio com remetente de outro domínio (ex.: Gmail).
- **SMTP (recomendado)**: `SMTP_ENABLED = true`, `SMTP_USER` = a caixa criada, `SMTP_PASS` = senha dela. Host `smtp.hostinger.com`, porta `465`, `ssl`. Sem SMTP o site usa o `mail()` do PHP como alternativa.
- `LEAD_WEBHOOK_URL` → opcional, envia cada lead em JSON para o CRM / Zapier / Make.
- `GA4_ID`, `GOOGLE_ADS_ID` + `GOOGLE_ADS_LEAD_LABEL`, `META_PIXEL_ID`, `GOOGLE_SITE_VERIFICATION` → rastreamento (vazio = desativado). A conversão de lead dispara na `/thank-you`; cliques em "Text Us"/"Call" viram eventos `sms_click`/`phone_click`.
- `FORM_SECRET` → se deixar o padrão, o site gera um segredo aleatório automaticamente em `data/.secret`.

## Formulários

- Validação no navegador (máscara de telefone US, campos obrigatórios) **e** no servidor (`send.php`).
- Envio via AJAX com redirecionamento para `/thank-you`; funciona também sem JavaScript.
- Anti-spam: honeypot, token assinado com tempo mínimo de preenchimento e limite de 5 envios / 10 min por IP.
- **Backup**: todo lead é salvo em `data/leads.csv` (bloqueado para acesso público). Se o e-mail falhar, o lead não se perde — baixe o CSV pelo Gerenciador de Arquivos.
- Captura UTM / `gclid` / `fbclid` (primeiro toque) e envia junto com o lead ("Lead source").
- Resposta automática para o cliente quando ele informa e-mail.

## CTA por SMS

Conforme o briefing (barreira do inglês), os botões principais abrem o **SMS** para +1 978-331-6200 com uma mensagem pré-preenchida. Há barra fixa no rodapé do celular ("Text Us" + "Free Estimate"). O número/texto ficam em `config.php`.

## Imagens (banco de imagens)

As fotos vêm do **Pexels** (uso comercial gratuito, sem atribuição), carregadas direto do CDN deles em tamanhos responsivos (`srcset`), sempre recortadas na proporção certa (4:3, 4:5, 16:9) — nada distorce nem "pula" durante o carregamento. Se alguma foto falhar, aparece um fundo azul-marinho com o ícone da marca.

Para trocar por fotos reais dos trabalhos (recomendado assim que o Renato enviar pelo Drive):

1. Envie as fotos para `assets/img/projects/` (mín. 1600 px de largura, JPG/WebP).
2. Em `includes/data.php`, na lista `$IMAGES`, troque por exemplo:
   ```php
   'shower-1' => ['src' => 'assets/img/projects/shower-01.jpg', 'alt' => 'Walk-in tile shower in Bedford, NH'],
   ```
3. Quando houver fotos reais, a galeria "Tile Styles We Install" pode virar "Our Recent Projects".

> As fotos de banco são apresentadas como **inspiração/estilos**, não como obras da empresa — o site não afirma que são trabalhos deles. Também **não há depoimentos inventados**: adicione reviews reais quando o GMB estiver verificado.

## SEO incluído

- Title/description únicos por página, canonical, Open Graph/Twitter com imagem própria (`assets/img/og-image.jpg`).
- Schema.org: `HomeAndConstructionBusiness` (service-area business, **sem endereço de rua**), `Service`, `FAQPage`, `BreadcrumbList`.
- `sitemap.xml` com imagens, `robots.txt`, URLs limpas (sem `.php`, 301 automático), página 404 própria.
- HTML semântico, 1 H1 por página, `alt` em todas as imagens, `width/height` + `aspect-ratio` (sem CLS), fontes locais com `font-display: swap`, lazy-loading, cache e compressão no `.htaccess`.
- Após publicar: cadastre o site no **Google Search Console** e envie `https://SEU-DOMINIO/sitemap.xml`.

## Pendências de conteúdo (do briefing)

- Domínio definitivo → `SITE_URL`.
- Página do Facebook e link do Google Business → `config.php`.
- Fotos/vídeos reais dos trabalhos e foto da equipe uniformizada.
- Reviews reais do GMB.
- O logo original tem um segundo telefone ((603) 351-0749); o site usa apenas o celular do Renato, conforme o briefing.

## Estrutura

```
public_html/
├── .htaccess              HTTPS, URLs limpas, cache, segurança
├── index.php, about.php, contact.php, service-areas.php, ...
├── send.php               processa o formulário
├── sitemap.php, robots.php, site.webmanifest, favicon.ico
├── includes/              config, dados, template, header/footer, mailer (bloqueado ao público)
├── data/                  leads.csv e arquivos de runtime (bloqueado ao público)
└── assets/
    ├── css/style.css
    ├── js/main.js         menu mobile, validação/envio, animações, rastreamento
    ├── fonts/             Archivo Black + Poppins (woff2)
    └── img/               logos (dourado/branco), favicons, og-image
```
