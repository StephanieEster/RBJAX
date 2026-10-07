# Rio Cleaning Services — novo site (riocleanings.com)

Site estático completo, em inglês americano, para a Rio Cleaning Services LLC (Philadelphia, PA).
Foco: limpeza residencial recorrente (prioridade **biweekly**), ligação telefônica como conversão
principal e SEO local para uma *service area business* (sem endereço publicado).

## Estrutura

```
rio-cleaning/
├── build/content.py   ← dados da empresa, textos, serviços, FAQs, IDs de tracking (edite aqui)
├── build/build.py     ← componentes e templates das páginas, JSON-LD, sitemap, redirects
├── build/images.py    ← pipeline das fotos (WebP responsivo, imagens OG, logo, favicons)
├── site/              ← site pronto para publicar (gerado)
└── vercel.json        ← configuração da Vercel (gerado)
```

Para alterar textos, FAQ, horários, avaliações ou cidades: edite `build/content.py` e rode

```bash
cd rio-cleaning && python3 build/build.py
```

Os `.html`, `sitemap.xml`, `robots.txt`, `.htaccess` e `vercel.json` são gerados; não edite à mão.
CSS e JS ficam em `site/assets/css/style.css` e `site/assets/js/main.js` (edição direta).

## Páginas

| URL | Intenção |
|---|---|
| `/` | Marca + conversão (hero, confiança, serviços, biweekly, incluso, processo, história, área, FAQ, formulário) |
| `/residential-cleaning/` | Hub comercial: todos os serviços, "qual serviço eu preciso", critérios de escolha |
| `/recurring-cleaning/` | Weekly / biweekly / monthly, com tabela de frequências e destaque biweekly |
| `/deep-cleaning/` | Deep / first-time cleaning, regular vs. deep |
| `/move-in-move-out-cleaning/` | Move-in e move-out |
| `/carpet-cleaning/` | Carpet cleaning |
| `/service-areas/` | Área atendida (Philadelphia + comunidades próximas em PA, NJ e DE) |
| `/about/` | História da Marcia, fatos, valores |
| `/reviews/` | Relacionamentos de longo prazo + links oficiais (avaliações reais entram aqui) |
| `/faq/` | 18 perguntas em 4 grupos |
| `/contact/` | Telefone, e-mail, horário, pagamento e formulário |
| `/privacy-policy/`, `/terms-and-conditions/`, `404.html` | Institucional |

Cada página tem title e description únicos, H1 único, canonical, Open Graph/Twitter, breadcrumb
(visível + `BreadcrumbList`), `LocalBusiness` com `@id` estável, `Service` nas páginas de serviço e
`FAQPage` idêntico às perguntas visíveis. Não há `AggregateRating`/`Review` no schema.

## Publicação

### Vercel
1. Novo projeto apontando para este repositório, **Root Directory = `rio-cleaning`**,
   Framework Preset = *Other*, sem comando de build.
2. O `vercel.json` já define a pasta `site`, URLs com barra final, cache de `/assets/`,
   cabeçalhos de segurança e os redirects 301 do site antigo.
3. Conectar o domínio `riocleanings.com`.

### Hostinger (ou qualquer hospedagem Apache)
Envie o **conteúdo** de `site/` para `public_html` (ative "mostrar arquivos ocultos" para incluir o
`.htaccess`). O `.htaccess` força HTTPS, remove `www`, aplica os redirects 301 e o cache.

### Depois de publicar
- Envie `https://riocleanings.com/sitemap.xml` no Google Search Console.
- **Ative o formulário** (abaixo) com um envio de teste.
- Teste o botão de ligação no celular.

## Formulário de orçamento

Envio real via **FormSubmit** (formsubmit.co) para `riocleaningservices.m@gmail.com`, sem backend.
- Validação no navegador (nome, telefone dos EUA com 10 dígitos, ZIP de 5 dígitos, tipo de limpeza;
  e-mail obrigatório só se "Email" for o contato preferido), mensagens de erro acessíveis,
  estado de carregamento, bloqueio de envio duplicado, honeypot + tempo mínimo anti-spam e
  mensagem de sucesso. Sem JavaScript, o formulário envia normalmente e volta para `/contact/?sent=1`.
- **Ativação obrigatória:** no primeiro envio o FormSubmit manda um e-mail de confirmação para
  `riocleaningservices.m@gmail.com`. Clique em "Activate Form". Só depois disso os pedidos chegam.
- Se a empresa passar a usar um CRM/webhook, troque `FORM_ENDPOINT` em `content.py`.
- Não há consentimento de SMS (o fluxo de SMS marketing não existe).

## Tracking (GA4, GTM, Google Ads, Meta Pixel)

Nada é carregado enquanto os IDs estiverem vazios em `TRACKING` (`content.py`). Ao preencher,
os scripts entram em todas as páginas. Eventos já disparados no `dataLayer` (e em `gtag`/`fbq`
se existirem):

| Evento | Quando |
|---|---|
| `phone_click` | qualquer link `tel:` (com `location`: header, hero, sticky_bar, footer...) |
| `quote_form_start` | primeira interação com o formulário |
| `quote_form_submit` | envio confirmado |
| `service_click` | cliques nos cards de serviço |
| `instagram_click`, `facebook_click` | links das redes |

Com `google_ads` + labels de conversão preenchidos, ligações e formulários viram conversões do
Google Ads; no Meta Pixel, `phone_click` → `Contact` e `quote_form_submit` → `Lead`.
`directions_click` não foi criado porque o site não publica endereço.

## Análise do site antigo (riocleanings.com)

| Informação | Decisão |
|---|---|
| Telefone (267) 694-4609, e-mail, Philadelphia PA | KEEP |
| Instagram e Facebook (`facebook.com/riodejaneirocleaningservices`, linkado no site antigo) | KEEP |
| Logo | KEEP (arquivo do brandbook, sem alteração) |
| Regular, deep e move-in/move-out cleaning | REWRITE (nova copy) |
| Commercial, office, Airbnb, post-construction, occasional cleaning | REMOVE (fora do posicionamento) |
| Oferta de 15% OFF | REMOVE |
| Consentimento de SMS com o nome "Spotless Solutions" | REMOVE (texto de outra empresa) |
| Selo "Pet Friendly" | VERIFY (não publicado até a empresa confirmar) |
| Horário Mon–Fri 7 AM–5 PM | VERIFY (publicado; confirme se bate com o Google Business Profile) |
| Fotos e imagem do carro | REMOVE (banco de imagens antigo / montagem) |
| Crédito "ROI Digital Marketing" no rodapé | REMOVE |

### Redirects 301 (já configurados no `vercel.json` e no `.htaccess`)

| Antiga | Nova |
|---|---|
| `/about-us/` | `/about/` |
| `/services/`, `/service/` | `/residential-cleaning/` |
| `/contact-us/` | `/contact/` |
| `/privacy-policy/`, `/terms-and-conditions/` | mesmas URLs |
| `/hello-world/`, `/category/uncategorized/`, `/feed/`, `/comments/feed/` | `/` |
| `/author/paulotmaqueara01gmail-com/` | `/about/` |

## Pendências — só a empresa pode fornecer

Nada foi inventado. Cada item abaixo tem lugar pronto em `build/content.py`:

1. **Google Business Profile oficial** → `GOOGLE_PROFILE` (entra no rodapé, Reviews e `sameAs`).
2. **Avaliações reais** (texto, nome, fonte e link) → `REVIEWS`. A página Reviews passa a mostrar
   a seção "See What Local Homeowners Are Saying". Não adicione nota/quantidade sem fonte.
3. **Lista de cidades confirmadas** → `CONFIRMED_CITIES` (aparece na página de áreas e no `areaServed`).
   Páginas por cidade só devem ser criadas com conteúdo próprio de cada cidade.
4. **Confirmar o horário** com o Google Business Profile (`HOURS`; `None` esconde).
5. **Oferta autorizada** (uma só: indicação de $50, primeira limpeza ou carpet até $100) → `OFFER`.
   Hoje nenhuma oferta é exibida.
6. **Fotos reais** da equipe e de trabalhos → substituir as imagens de banco (mesmos nomes de
   arquivo, ou rode `build/images.py` com as novas fotos).
7. **IDs de tracking** reais → `TRACKING`.
8. Detalhes que não foram confirmados e por isso não aparecem: "bonded", "background checked",
   garantia formal, produtos próprios, método de carpet cleaning, pet friendly.

## Imagens

Fotos de banco do **Pexels** (licença gratuita para uso comercial, sem atribuição obrigatória):
1080721, 8583748, 3875141, 6195198, 4239123, 4239037, 7203788, 9462316, 18093637, 4682120,
15580493 (`https://www.pexels.com/photo/<id>/`). Os Termos informam que algumas fotos são
ilustrativas. Nenhuma foto de pessoa é apresentada como sendo a Marcia ou a equipe.

Tipografia: Fraunces (títulos) e Montserrat (texto, do brandbook), hospedadas no próprio site.
Ícones: SVG em sprite único (`/assets/icons.svg`), estilo Lucide.
