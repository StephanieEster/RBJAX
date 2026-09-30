---
name: seo-tecnico
description: SEO técnico aplicado para criar, reescrever ou auditar sites e páginas (landing page, página de serviço, preço, comparativa, local/cidade, home/Sobre, artigo/guia) seguindo o framework de página comercial por intenção de busca, com 17 blocos, ordem por intenção, JSON-LD, checklist e teste final. Use sempre que for criar ou alterar qualquer página HTML deste projeto, ou quando pedirem SEO, SEO técnico, SEO on-page, auditoria de SEO, estrutura de página, H1, meta tags, schema/dados estruturados, FAQ, sitemap, página local ou copy que ranqueie no Google e seja citada por IA.
---

# SEO técnico aplicado

A página não é definida pelo que a empresa quer dizer, e sim pelo que quem buscou precisa encontrar para decidir.
Uma busca principal = uma intenção = uma página.

Referências completas (ler quando precisar do detalhe):
- `references/guia-seo-tecnico.md`: os 17 blocos com modelo para preencher e exemplo, a ordem e o peso por intenção, as tabelas de prova e preço, o checklist completo e a base técnica. **Leia antes de montar a página.**
- `references/anatomia-pagina-comercial.html`: o documento original interativo (Anderson Melo SEO). Use só para consultar um exemplo preenchido.
- `references/sites-referencia.md`: sites feitos por especialista (wtsseguros.com, nidavitae.com) e o que observar neles.

## Fluxo de trabalho

1. **Levantar os dados reais do negócio**: serviço, público, cidade/região, números (volume atendido, anos, avaliações), garantias, preço ou faixa com data, responsável técnico com registro, CNPJ, endereço, telefone/WhatsApp e perfis oficiais. Nunca invente CNPJ, depoimento, número ou avaliação. O que faltar entra como `[PREENCHER: ...]` e vai listado para o usuário no fim.
2. **Classificar a intenção** da busca principal:

   | Intenção | Quer | Blocos-chave | Schema principal | Não pode dominar |
   |---|---|---|---|---|
   | Transacional | Agir agora | Formulário na 1ª dobra, preço ao lado, garantia | Service + Offer | Texto educativo longo |
   | Comercial | Escolher com critério | Tabela de critérios (5–8 linhas), FAQ 10+ | Service | Vender sem ensinar |
   | Preço | Número/faixa | Faixa datada logo após o hero, variáveis, simulador | Service + AggregateOffer | "Não existe preço único" |
   | Comparativa | Decidir entre A e B | Tabela lado a lado, veredito por perfil | Article (about A e B) | Neutralidade vazia |
   | Local | Quem atende perto | Cidade no H1, prova local com bairro e data, faixa regional | LocalBusiness / Service + areaServed | Template com a cidade trocada |
   | Marca | Confirmar a empresa | Fatos, volume, avaliações com link, fundadores | Organization + WebSite | Conteúdo informacional na home |
   | Informacional | Aprender | Definição na 1ª frase, link para a página comercial | Article | CTA agressivo |

3. **Montar os blocos na ordem da intenção** (tabela de ordem e pesos em `references/guia-seo-tecnico.md`, seção 3). Os 17 blocos:
   1 Hero · 2 Sentença definicional · 3 Breadcrumb · 4 Para quem é/não é · 5 Como funciona · 6 Critérios de escolha · 7 Preço · 8 Prova · 9 Diferencial contra a alternativa · 10 Objeções e garantia · 11 Autoria · 12 FAQ · 13 Links contextuais · 14 Cobertura geográfica · 15 CTA final e formulário · 16 Institucional · 17 Dados estruturados
4. **Aplicar a base técnica** (abaixo).
5. **Auditar**: checklist da seção 5 do guia, depois o teste final. Entregar ao usuário a intenção escolhida, os blocos usados e os `[PREENCHER]` pendentes.

## Regras que não mudam

- **H1**: um só, nomeia a entidade e o contexto ("Energia solar residencial em Campinas"), nunca slogan.
- **Sentença definicional**: logo após o hero, em `<strong>`, 20–35 palavras, sem adjetivo e sem marca: `[Entidade] é [categoria] que [função] para [público], [resultado mensurável]`.
- **Prova**: pareada (antes → depois, com prazo, cidade e data), volume com número e ano, depoimento com nome, cidade e resultado.
- **Preço**: faixa, exemplo datado ou tabela de variáveis, sempre com data e região. Nunca valor fixo sem contexto.
- **FAQ**: 10 ou mais perguntas reais, respostas de 40–80 palavras com dado concreto. O `FAQPage` do JSON-LD tem **exatamente** as mesmas perguntas visíveis.
- **Links contextuais**: 3–6 no corpo do texto, com a diferença entre as páginas irmãs escrita e âncoras diferentes do H1 do destino.
- **Formulário**: 3–6 campos, pelo menos um que segmenta; o botão diz o que a pessoa recebe ("Receber simulação gratuita", não "Enviar"); WhatsApp `https://wa.me/55DDDNUMERO` real. Nenhum `href="#"` publicado.
- **Autoria**: nome, registro profissional e "Atualizado em [mês/ano]" visíveis.
- **Institucional**: razão social, CNPJ, endereço com CEP, telefone com DDD, horário, política de privacidade e termos.

## Base técnica (toda página)

```html
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>[Entidade + contexto, ~50–60 caracteres] | [Marca]</title>
  <meta name="description" content="[~140–160 caracteres com resultado e diferencial]">
  <link rel="canonical" href="https://[dominio]/[url-canonica]">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:title" content="[título]">
  <meta property="og:description" content="[descrição]">
  <meta property="og:url" content="https://[dominio]/[url-canonica]">
  <meta property="og:image" content="https://[dominio]/assets/og.jpg"><!-- 1200×630 -->
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <script type="application/ld+json">{ ... }</script>
</head>
```

- **Hierarquia**: H2/H3 em ordem, sem pular nível; H2 que respondem perguntas reais.
- **URLs**: minúsculas, com hífen, sem acento, em cluster (`/servico/`, `/servico/cidade/`, `/guia/tema/`), coerentes com o canonical e com `cleanUrls`/`trailingSlash` do `vercel.json`.
- **Indexação**: `robots.txt` apontando para `sitemap.xml`; sitemap com todas as URLs canônicas e `lastmod`; 404 própria; conteúdo principal no HTML, não injetado por JS.
- **Performance**: imagens WebP/AVIF com `width`/`height`; `fetchpriority="high"` na imagem do hero; `loading="lazy"` abaixo da dobra; fontes com `display=swap`; JS com `defer`; cache longo em `/assets/`.
- **Acessibilidade**: `alt` descritivo, contraste, foco visível, texto de link descritivo, `prefers-reduced-motion`.

### JSON-LD base (um `@graph` por página)

```json
{
  "@context": "https://schema.org",
  "@graph": [
    {
      "@type": "Organization",
      "@id": "https://[dominio]/#organization",
      "name": "[Marca]",
      "legalName": "[Razão social]",
      "url": "https://[dominio]/",
      "logo": "https://[dominio]/assets/logo.png",
      "telephone": "+55-[DDD]-[numero]",
      "address": { "@type": "PostalAddress", "streetAddress": "[rua, nº]", "addressLocality": "[cidade]", "addressRegion": "[UF]", "postalCode": "[CEP]", "addressCountry": "BR" },
      "sameAs": ["[instagram]", "[google perfil da empresa]", "[linkedin]"]
    },
    {
      "@type": "Service",
      "name": "[serviço]",
      "serviceType": "[categoria]",
      "areaServed": { "@type": "City", "name": "[cidade]" },
      "provider": { "@id": "https://[dominio]/#organization" },
      "offers": { "@type": "AggregateOffer", "lowPrice": "[mín]", "highPrice": "[máx]", "priceCurrency": "BRL", "validThrough": "[AAAA-MM-DD]" }
    },
    {
      "@type": "BreadcrumbList",
      "itemListElement": [
        { "@type": "ListItem", "position": 1, "name": "Início", "item": "https://[dominio]/" },
        { "@type": "ListItem", "position": 2, "name": "[página]", "item": "https://[dominio]/[url]" }
      ]
    },
    {
      "@type": "FAQPage",
      "mainEntity": [
        { "@type": "Question", "name": "[pergunta visível 1]", "acceptedAnswer": { "@type": "Answer", "text": "[resposta visível 1]" } }
      ]
    }
  ]
}
```

Troque `Service` pelo tipo da intenção (Article com `author`, `datePublished`, `dateModified` e `about`; LocalBusiness; Organization + WebSite na home). O `@id` da Organization é o mesmo em todas as páginas. Valide em search.google.com/test/rich-results.

## Teste final antes de publicar

Lendo só estes quatro elementos, alguém responde **"o que é, para quem, quanto custa e por que aqui"**?

1. H1
2. Sentença definicional
3. Tabela principal (critérios, variáveis de preço ou comparação)
4. Primeira pergunta da FAQ (a dúvida que mais trava a decisão, 40–80 palavras, com dado)

Se for preciso ler o corpo inteiro, os blocos estão na ordem errada: reordene antes de entregar.
