# Mountain Weather — Cooling & Heating · Website

Site institucional da Mountain Weather (HVAC, Kearny, NJ). São 7 páginas públicas mais a página 404,
todas em HTML estático gerado por um build em Node, sem framework e sem dependências em produção.

| URL | Página | Intenção de busca principal |
|---|---|---|
| `/` | Home | Marca + "HVAC services Kearny NJ" |
| `/emergency-hvac-services` | Emergency HVAC Services | "Emergency HVAC services Kearny NJ" |
| `/hvac-replacement` | HVAC Replacement | "HVAC replacement Kearny NJ" |
| `/about` | Our Story | Marca / confiança |
| `/service-areas` | Service Area (Kearny) | Local: "HVAC company Kearny NJ" |
| `/contact` | Contact | Contato direto |
| `/privacy-policy` | Privacy Policy | Institucional |
| `/404` | Página não encontrada (`noindex`) | — |

## Publicar na Vercel

1. Importe o repositório na Vercel e defina **Root Directory = `mountain-weather`**.
2. Não é preciso escolher framework. O `vercel.json` desta pasta já define o build
   (`node scripts/build.mjs && node scripts/check.mjs`), a saída (`dist/`), URLs limpas, cache
   longo em `/assets/` e cabeçalhos de segurança (CSP incluída).
3. Conecte o domínio definitivo em *Settings → Domains*. As URLs canônicas, o `sitemap.xml`, o
   `robots.txt` e os dados estruturados usam automaticamente o domínio de produção (variável
   `VERCEL_PROJECT_PRODUCTION_URL`). Para forçar outro domínio, crie a variável `SITE_URL`
   (ex.: `https://www.exemplo.com`) e faça um novo deploy.

A pasta `dist/` também vai versionada. Ela foi gerada com o domínio provisório
`https://mountain-weather.vercel.app`, e a Vercel a recria a cada deploy com o domínio correto.

## Comandos locais (Node 18+)

```bash
node scripts/build.mjs     # gera dist/
node scripts/check.mjs     # QA: títulos, descrições, canonical, H1 único, níveis de título,
                           # alt/width/height das imagens, links internos, sms/tel/WhatsApp,
                           # FAQ visível = FAQPage, ausência do endereço, hash da CSP
node scripts/serve.mjs     # pré-visualização em http://localhost:4173 (mesmas URLs e cabeçalhos da Vercel)
```

## Estrutura

```
src/config.mjs          dados da empresa (telefone, e-mail, redes, licença) e mensagens pré-preenchidas
src/lib/layout.mjs      <head>, cabeçalho, menu mobile, rodapé, barra fixa de contato, JSON-LD da empresa
src/lib/sections.mjs    componentes: gauge (arco da marca), FAQ, passos, CTA final, seletor Cooling/Heating
src/lib/html.mjs        <picture> AVIF/WebP responsivo, ícones, botões de contato
src/pages/*.mjs         conteúdo de cada página (copy em inglês americano) + dados estruturados
src/styles.css          design system (tokens extraídos do logo) e todos os estilos
src/main.js             menu, revelação no scroll, acordeão, seletor Cooling/Heating, compositor de mensagem
scripts/optimize-images.mjs  gera as variantes AVIF/WebP, ícones e a imagem OG (precisa de `npm install`)
public/                 fontes, imagens otimizadas, logotipo e favicons
```

Para trocar fotos, coloque os JPGs originais numa pasta com os mesmos nomes de arquivo
(ver `CREDITS.md`), rode `npm install` e depois
`node scripts/optimize-images.mjs <pasta-das-fotos> <pasta-da-marca>`.

## Decisões tomadas a partir do briefing

- **Sem formulário com envio.** Não existe infraestrutura de envio (CRM ou e-mail transacional).
  A página Contact tem um compositor que monta a mensagem e a abre no SMS, no WhatsApp ou no
  e-mail do visitante, que confere e envia. O site não envia nem armazena nada, e a Política de
  Privacidade descreve exatamente isso.
- **Conversão:** o SMS é o CTA principal (`sms:+18622708862` com texto pré-preenchido por
  contexto), a ligação é o secundário e o WhatsApp vem em seguida. No celular há uma barra fixa
  com Text, Call e WhatsApp.
- **Nada inventado.** Não há 24/7, preços, depoimentos, avaliações, certificações, marcas
  parceiras, garantias nem outras cidades. A seção de depoimentos virou uma área de prova
  verificável (2.000+ clientes desde 2017) com links para Instagram e Facebook. Os fatos técnicos
  usados (ENERGY STAR, fim do R-22 em 2020, padrões SEER2/HSPF2 de 2023) estão citados no texto.
- **Endereço:** não aparece no site. Nos dados estruturados entram só cidade e estado
  (Kearny, NJ), sem rua nem CEP.
- **Logotipo no cabeçalho:** o logo completo fica ilegível com 60 px de altura. Por isso o
  cabeçalho usa o emblema oficial com o nome tipografado nas cores da marca, e o logo completo
  aparece no rodapé. Se o cliente tiver uma versão horizontal oficial, basta substituir.
- **Elemento visual próprio:** o arco-termômetro do logo foi redesenhado em SVG. No hero ele
  emoldura a foto como uma janela em arco, com a faixa "2,000+ customers served" no lugar da
  faixa do logo. Na seção "Too hot or too cold?" ele vira um mostrador com ponteiro que alterna
  entre Cooling e Heating. O padrão inicial segue a estação: Heating de outubro a abril e Cooling
  de maio a setembro. O fundo usa linhas topográficas (a montanha da marca).

## Validação realizada

- Lighthouse (mobile, servidor local com compressão): Performance 99–100, Accessibility 100,
  Best Practices 100 e SEO 100 nas 7 páginas públicas. LCP de 1,6 a 2,0 s, CLS 0 e TBT ≤ 70 ms.
  São medições de laboratório e precisam ser confirmadas em produção (PageSpeed Insights / CrUX).
- `scripts/check.mjs`: 0 erros nas 8 páginas.
- Layout sem rolagem horizontal de 320 px a 2560 px. Menu mobile (Esc, foco preso no menu),
  seletor Cooling/Heating com setas do teclado, FAQ e validação do compositor testados no Chromium.
- `prefers-reduced-motion` desativa todas as animações.

## Pendências antes de publicar (confirmar com o cliente)

1. **Licença de HVACR (obrigatória em NJ).** A regra N.J.A.C. 13:32A-5.1 exige que a publicidade
   mostre o nome do master HVACR contractor e o número da licença. Preencha `license` em
   `src/config.mjs`; o rodapé passa a exibir os dados automaticamente. Até lá, o build mostra um
   aviso.
2. **WhatsApp:** confirmar que o +1 (862) 270-8862 está ativo no WhatsApp.
3. **Domínio definitivo** (ver "Publicar na Vercel").
4. **Nome e foto do fundador.** A página About fala de "our founder" porque o nome não foi
   informado. Um nome e uma foto reais reforçam muito a confiança (E-E-A-T).
5. **Fotos reais** da equipe e de serviços, para substituir o banco de imagens. Duas fotos do
   banco mostram técnicos de máscara.
6. **Depoimentos ou avaliações reais**, com link para a fonte (ex.: Google), para criar a seção
   de depoimentos.
7. **Google Business Profile:** criar ou verificar o perfil e depois incluir o link em `sameAs`
   (`src/lib/layout.mjs`).
8. **Horário de atendimento**, se quiserem exibir. Hoje o site não promete horários.
9. **Escopo técnico:** confirmar quais equipamentos atendem (fornalha, boiler, heat pump,
   mini-split) e se atendem clientes comerciais. O texto foi mantido genérico de propósito.
10. **Outras cidades atendidas:** hoje só Kearny é citada, e o site convida o visitante a
    perguntar pelo seu CEP.
11. **Revisão jurídica** da Política de Privacidade (o texto reflete o funcionamento atual do site).

## Depois de publicar

- Google Search Console: verificar o domínio e enviar `/sitemap.xml`.
- Validar os dados estruturados em https://search.google.com/test/rich-results
- Rodar o PageSpeed Insights nas URLs de produção.
- Se adicionar analytics, pixel ou formulário com backend, atualizar a Política de Privacidade e a
  CSP no `vercel.json`.
