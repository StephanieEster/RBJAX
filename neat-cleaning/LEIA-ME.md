# Neat Cleaning — site para Hostinger

Redesign completo do site da Neat Cleaning (Natick, MA): visual premium seguindo o
brandbook (preto, dourado, marfim · Cinzel + Montserrat), SEO técnico por intenção
de busca e todas as páginas geradas a partir de um único template.

## Estrutura

```
neat-cleaning/
├── build/build.py   ← conteúdo + templates de todas as páginas (edite aqui)
└── site/            ← pasta pronta para public_html da Hostinger
```

Para alterar texto, FAQ, serviços ou cidades, edite `build/build.py` e rode:

```bash
cd neat-cleaning && python3 build/build.py
```

Os arquivos `.html` em `site/` são gerados; não edite à mão (seriam sobrescritos).
CSS e JS ficam em `site/assets/css/style.css` e `site/assets/js/main.js`.

## Publicação na Hostinger

1. No hPanel: Website → Custom PHP/HTML. Envie o **conteúdo** de `site/` (ou o ZIP
   `Neat-Cleaning-Hostinger.zip`) para `public_html` e extraia ali, sem pasta
   intermediária. Ative "mostrar arquivos ocultos" e confira o `.htaccess`.
2. Ative o SSL e abra o site em HTTPS.
3. Em `site-settings.php`, preencha `NEAT_SITE_URL` com o domínio final
   (ex.: `https://neatcleaningma.com`, sem barra no fim). Canonical, Open Graph,
   JSON-LD, sitemap e robots usam esse domínio automaticamente.
4. Envie `https://SEU-DOMINIO/sitemap.xml` no Google Search Console.
5. Teste um envio real pelo formulário (home, contato e uma página de serviço).
   O e-mail chega em `Neatcleaningservicesusa@gmail.com` (fixo no servidor).
   Se não chegar, verifique spam e configure SMTP (PHPMailer) na hospedagem.

## O que mudou

**Visual**
- Identidade do brandbook aplicada: preto profundo + dourado em fios finos e
  detalhes, marfim nas seções claras; Cinzel nos títulos, Montserrat no texto.
- Layout editorial: hero dividido com foto emoldurada, índice de serviços com
  pré-visualização da foto, tabelas de critérios, numeração romana nas seções,
  formulário com campos sublinhados, menu mobile em tela cheia, barra fixa
  "Text for a quote / Call" no celular.
- Fontes hospedadas no próprio site (mais rápido e sem requisição ao Google).
- Imagens responsivas (640/1024/1536 px) e imagens de compartilhamento 1200×630.

**SEO**
- Um H1 por página com serviço + cidade ("Regular house cleaning in Natick, MA").
- Frase definicional em destaque logo após o hero de cada página.
- Titles (≤ 62 caracteres) e descriptions (≤ 160) únicos.
- JSON-LD em `@graph`: LocalBusiness com `@id` único, área de 25 milhas
  (GeoCircle), WebSite, Service por serviço, BreadcrumbList, FAQPage idêntico às
  perguntas visíveis, AboutPage/ContactPage/CollectionPage.
- 6–7 perguntas por página de serviço e 14 na FAQ geral, respostas de 40–80
  palavras com fatos reais.
- Links contextuais entre páginas irmãs explicando a diferença entre serviços.
- Página de área com mapa esquemático e distâncias reais de 29 cidades.
- `/index.html` redireciona (301) para `/`; breadcrumbs visíveis.

## Pendências — dados que só a empresa pode fornecer ([PREENCHER])

Nada foi inventado. Estes itens aumentariam conversão e SEO quando disponíveis
(as marcações estão como comentários `PREENCHER` em `build/build.py`):

1. **Perfil do Google (Google Business Profile)** e redes sociais → adicionar em
   `sameAs` no JSON-LD e no rodapé.
2. **Avaliações reais** (nota e link do Google) → bloco de prova na home.
3. **Faixa de preço de referência datada** (ex.: "3 quartos / 2 banheiros em
   Natick, out/2026: US$ X–Y") → home e cada serviço.
4. **Horário de atendimento** e tempo médio de resposta → rodapé e contato.
5. **Foto real da Daiane** → página About e bloco "Who you will talk to".
6. Seguro/licença, se houver (não foi citado porque não foi informado).
7. Domínio final em `NEAT_SITE_URL`.

As imagens de ambientes são ilustrativas (o rodapé e os Termos informam isso).
Fotos reais de trabalhos feitos, com cidade e data, são a melhor prova possível.
