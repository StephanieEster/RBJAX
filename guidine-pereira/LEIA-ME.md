# Site — Guidine Pereira Construction LLC

Site em PHP/HTML, pronto para a Hostinger (opção **"Site PHP/HTML personalizado"** no hPanel).
Em inglês (público americano), otimizado para SEO local em Myrtle Beach, SC.

## Como publicar na Hostinger

1. No hPanel, abra **Sites > Gerenciar > Gerenciador de Arquivos** e entre em `public_html`.
2. Apague o `default.php` (ou `index.html`) padrão da Hostinger, se houver.
3. Envie o arquivo `guidine-pereira-hostinger.zip` para dentro de `public_html` e use **Extrair**.
   Os arquivos (`index.php`, `.htaccess`, `assets/`...) precisam ficar direto em `public_html`, sem subpasta.
4. Ative o SSL (hPanel > Segurança > SSL) e depois ative **Forçar HTTPS** no hPanel
   (ou descomente as 2 linhas de HTTPS no início do `.htaccess`).
5. Abra `includes/config.php` e revise (explicado abaixo).
6. Teste o formulário em `/contact` e confira se o e-mail chegou.
7. Envie `https://SEUDOMINIO.com/sitemap.xml` no Google Search Console.

## Configuração (`includes/config.php`)

É o único arquivo que normalmente precisa ser editado.

| Campo | O que colocar |
|---|---|
| `SITE_URL` | Domínio final, ex.: `https://guidinepereiraconstruction.com`. Se ficar vazio, o site detecta sozinho. Recomendado preencher. |
| `LEAD_TO` | E-mail que recebe os pedidos de orçamento (já está o Gmail do cliente). |
| `MAIL_FROM` | Remetente. Na Hostinger precisa ser um e-mail do próprio domínio, ex.: `contato@dominio.com`. Vazio = `no-reply@dominio`. |
| `SMTP_*` | Opcional, **recomendado** para não cair em spam. Crie uma conta de e-mail no hPanel e preencha: `smtp.hostinger.com`, porta `465`, `ssl`, usuário = e-mail completo, senha da conta. |
| `GOOGLE_BUSINESS_URL` | Link do Perfil da Empresa no Google quando estiver verificado (aparece no rodapé e no schema). |
| `GTM_ID`, `GA4_ID`, `GOOGLE_ADS_ID`, `GOOGLE_ADS_LEAD_LABEL`, `META_PIXEL_ID` | IDs de rastreamento. Só são carregados quando preenchidos. |

## Formulário de orçamento

- Na home e nas 4 páginas de serviço o formulário fica **na hero** (versão curta: nome, telefone, e-mail, cidade, serviço e detalhes opcionais).
  Nas páginas de serviço o serviço já vem selecionado. Os botões "Free Estimate" do topo e da barra do celular levam direto a ele.
- A versão completa continua no fim das páginas e em `/contact`.
- Envio via AJAX, sem recarregar a página; depois redireciona para `/thank-you`.
- Validação no navegador e no servidor, máscara de telefone americano.
- Antispam: campo invisível (honeypot), tempo mínimo de preenchimento e limite de 5 envios a cada 10 min por IP.
- Captura `utm_source`, `utm_medium`, `utm_campaign`, `utm_term`, `gclid` e `fbclid` e envia junto no e-mail.
- **Backup:** todo pedido também é salvo em `leads/leads.csv` (pasta bloqueada ao público). Se o e-mail falhar,
  o lead não se perde; as falhas ficam em `leads/mail-errors.log`.

## Conversões (tráfego pago)

- `/thank-you` dispara: conversão do Google Ads (se `GOOGLE_ADS_ID` + `GOOGLE_ADS_LEAD_LABEL`), evento `generate_lead` no GA4,
  `Lead` no Meta Pixel e `estimate_form_submit` no dataLayer (para GTM). A página tem `noindex`.
- Cliques em ligar, SMS e e-mail disparam `contact_click` (dataLayer/GA4) e `Contact` (Meta Pixel).

## Páginas

| URL | Arquivo |
|---|---|
| `/` | `index.php` |
| `/shower-bathroom-remodeling` | `shower-bathroom-remodeling.php` |
| `/tile-flooring-installation` | `tile-flooring-installation.php` |
| `/wall-tile-installation` | `wall-tile-installation.php` |
| `/backsplash-installation` | `backsplash-installation.php` |
| `/projects` | `projects.php` (galeria com filtros e lightbox) |
| `/about` | `about.php` |
| `/service-areas` | `service-areas.php` |
| `/contact` | `contact.php` |
| `/thank-you` | `thank-you.php` |
| `/privacy-policy` | `privacy-policy.php` |
| `/sitemap.xml`, `/robots.txt` | gerados por `sitemap.php` e `robots.php` |

Textos dos serviços, FAQ e cidades atendidas ficam em `includes/data.php`.
As fotos da galeria ficam listadas em `includes/gallery-data.php` (arquivos em `assets/img/work/`).

## SEO incluído

- Title, meta description, canonical, Open Graph e Twitter Card em todas as páginas.
- Schema.org: `HomeAndConstructionBusiness` (área de atendimento, telefone, pagamentos, redes), `Service`,
  `FAQPage` e `BreadcrumbList`.
- URLs limpas (sem `.php`), sitemap com imagens, robots.txt, 404 personalizada.
- 59 fotos reais do cliente convertidas para WebP em 2 tamanhos (480 e 900 px) com `srcset`,
  `width/height` definidos (sem salto de layout), lazy-load e textos alternativos descritivos.
- Fonte da marca (Anek Devanagari) hospedada localmente e pré-carregada; cache e compressão no `.htaccess`.

## Pontos para confirmar com o cliente

- Prazos citados no FAQ (backsplash 1–2 dias, piso alguns dias, banheiro/box 1–3 semanas). O briefing
  apontou "prazo de entrega" como dúvida frequente, mas não informou números. Ajuste em `includes/data.php`.
- A página About cita o Adeildo pelo primeiro nome. Confirmar se ele concorda.
- Não há depoimentos no site (o cliente ainda não tem avaliações). Quando o Perfil da Empresa no Google tiver
  avaliações, vale incluir uma seção de reviews.
