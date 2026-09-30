# Guia de SEO técnico aplicado — páginas comerciais por intenção de busca

Fonte: framework "Anatomia da página comercial por intenção de busca" (Anderson Melo SEO).
Original interativo salvo em [`anatomia-pagina-comercial.html`](./anatomia-pagina-comercial.html)
(abrir no navegador: tem esqueleto por intenção, modelos para copiar e checklist de auditoria com exportação JSON).

Este arquivo é a versão de trabalho: **use-o como regra ao criar qualquer página/site neste repositório.**
Os exemplos (empresa fictícia "Solaris", energia solar em Campinas) são ilustrativos e servem para qualquer serviço.

---

## 1. Princípio: a intenção decide a página

A página não é definida pelo que a empresa quer dizer, e sim pelo que quem buscou precisa encontrar para decidir.
Antes de escrever, classifique a busca principal em **uma** das 7 intenções. Uma busca = uma página.

| Intenção | O que a pessoa quer | Exemplo de busca |
|---|---|---|
| Transacional | Já decidiu, quer agir | "orçamento energia solar residencial" |
| Comercial | Está escolhendo, quer critérios | "energia solar para casa" |
| Preço | Um número ou faixa | "quanto custa energia solar residencial" |
| Comparativa | Está entre duas opções | "energia solar on-grid ou off-grid" |
| Local | Quem atende perto | "energia solar em Campinas" |
| Marca | Confirmar quem é a empresa (home e Sobre) | "Solaris energia é confiável" |
| Informacional | Aprender (alimenta as comerciais) | "como funciona energia solar" |

Legenda de peso usada abaixo: ✅ Obrigatório · 🔵 Recomendado · ⚪ Opcional · ⚠️ Limitar (não pode dominar)

---

## 2. Os 17 blocos (com modelo para preencher)

### 1. Hero — H1, promessa, prova e CTA
H1 com a entidade da página, subtítulo com promessa concreta, 3–4 provas curtas, CTA primário + secundário, selo de confiança.
```
H1: [serviço] [qualificador] para [público ou cidade]
Sub: [resultado com número] com [mecanismo que entrega o resultado]
Provas: [volume atendido] · [garantia] · [o que vem incluso]
CTA 1: [verbo + o que a pessoa recebe]   CTA 2: Falar no WhatsApp
Selo: [registro, certificação ou avaliação externa]
```
Ex.: "Energia solar residencial com projeto, instalação e homologação" · "Reduza a conta de luz em até 95%… homologado em até 30 dias" · chips "380 casas instaladas / 25 anos de garantia / Homologação inclusa / 4,9 no Google (212 avaliações)" · botões "Receber orçamento gratuito" + "Falar no WhatsApp".

### 2. Sentença definicional — uma frase que define a página
Logo após o hero, **em negrito**. É o trecho que vira snippet e que assistentes de IA citam.
```
[Entidade] é [categoria] que [função principal] para [público], [resultado mensurável ou prazo].
Regra: 20 a 35 palavras, sem adjetivo, sem marca.
```
Ex.: **Energia solar residencial** é o sistema fotovoltaico instalado no telhado da casa que gera a própria energia e compensa o consumo na conta da distribuidora, reduzindo a fatura em até 95%.

### 3. Breadcrumb — posição da página no site
Visível **e** marcado em `BreadcrumbList`. Diz ao buscador de qual cluster a página faz parte.
```
Início › [hub de serviço] › [página atual]
Local: Início › [hub] › [serviço] › [cidade]
```

### 4. Para quem é e para quem não é — qualificação
2–3 perfis que se beneficiam (condição mensurável) e 1–2 que não (com link para a página certa).
```
É para você se: [condição mensurável 1] / [condição mensurável 2] / [situação típica do cliente ideal]
Não é para você se: [condição que inviabiliza] / [caso em que outro serviço resolve melhor + link]
```

### 5. Como funciona — passos do serviço
3 a 5 passos numerados do primeiro contato à entrega, cada um com prazo ou entregável.
```
1. [Diagnóstico]: [o que a empresa analisa] ([prazo])
2. [Proposta]: [o que o cliente recebe por escrito]
3. [Execução]: [quem faz, quanto tempo leva]
4. [Entrega ou aprovação]: [marco verificável]
5. [Acompanhamento]: [o que continua depois]
```

### 6. Critérios de escolha — tabela do que verificar
Tabela (não lista) com critérios que o cliente deveria conferir em qualquer fornecedor. Posiciona a empresa como quem passa no próprio teste.
```
| Critério | O que verificar | Como fazemos |
Regra: 5 a 8 linhas, cada uma com a pergunta que o cliente faria a um concorrente.
```

### 7. Preço ou lógica de preço — faixa, exemplo e variáveis
Sem isso a página não concorre em buscas de custo.
```
Faixa de referência ([mês/ano]): [perfil típico] em [cidade/região]: de R$ [mín] a R$ [máx].
O que altera o valor:
| Variável | Efeito no preço |
Aviso: valores de referência; a proposta é feita por [o que define o valor final]. Link: [simulador]
```

### 8. Prova — antes e depois, números, depoimentos
```
Antes: [métrica] → Depois: [métrica] em [prazo] ([cidade, mês/ano])
[N] clientes desde [ano] · [% ou métrica de continuidade]
Foto antes e depois: mesma casa, mesmo ângulo, legenda com cidade e data
Depoimento: "[resultado em números]" – [Nome, Cidade]
```

### 9. Diferencial contra a alternativa
Compara com as alternativas reais: outro fornecedor, fazer sozinho, não fazer nada.
```
| | [Alternativa 1: fazer sozinho] | [Alternativa 2: concorrente típico] | Aqui |
| [critério que mais pesa] | ... | ... | ... |
Fechamento: uma frase dizendo para quem cada alternativa faz sentido.
```

### 10. Objeções e garantia
As 3–4 perguntas que travam a assinatura, na voz do cliente, respondidas com garantia, prazo e responsabilidade.
```
"[objeção na voz do cliente]" → [o que acontece de fato] + [garantia por escrito]
Garantia central: se [condição], então [o que a empresa faz, em quanto tempo, sem custo].
```

### 11. Autoria e responsabilidade (E-E-A-T)
Nome do responsável, registro profissional, data de revisão. Obrigatório em saúde, dinheiro e setores regulados.
```
Conteúdo revisado por [Nome], [registro profissional], [função]. Atualizado em [mês/ano].
Link para a página do autor com foto, formação e perfis oficiais.
```

### 12. FAQ — mínimo de 10 perguntas
Respostas de **40 a 80 palavras com dado concreto**. O `FAQPage` do JSON-LD deve ter **exatamente** as mesmas perguntas visíveis.
```
1. Prazo  2. Preço  3. Pagamento/financiamento  4. Garantia (e se falhar?)  5. Cobertura (condição limite)
6. Manutenção  7. Requisito/pré-requisito  8. Comparação A ou B  9. Cancelamento  10. Prova (quantos clientes)
```

### 13. Links contextuais — ligação com páginas irmãs
Links **dentro do texto**, com a diferença explícita entre as páginas (evita canibalização).
```
Aqui tratamos de [escopo desta página]. Para [escopo da irmã], veja [âncora descritiva].
Regra: 3 a 6 links no corpo, âncoras diferentes do H1 da página de destino.
```

### 14. Cobertura geográfica
Cidades/regiões atendidas, cada uma linkando para a própria página local, âncoras variadas.
```
Atendemos [região]: [serviço em Cidade A] · [instalação em Cidade B] · [o que muda em Cidade C]
Regra: nunca a mesma âncora duas vezes.
```

### 15. CTA final e formulário
3 a 6 campos, pelo menos um que segmenta o lead, botão que diz o que a pessoa recebe, WhatsApp real ao lado.
```
Título: [resultado] em [prazo]. [O que a pessoa recebe ao enviar].
Campos: Nome · WhatsApp · [campo que segmenta] · [campo que qualifica]
Botão: [verbo + o que recebe]   Abaixo: "Resposta em [prazo]. Sem compromisso."
```

### 16. Institucional — entidade verificável
```
[Razão social] · CNPJ [00.000.000/0001-00]
[Endereço completo com CEP] · [telefone com DDD] · [e-mail]
Atendimento: [dias e horário] · [registro no conselho ou órgão]
Links: Política de privacidade · Termos · [perfis oficiais]
```

### 17. Dados estruturados (JSON-LD)
Coerente com o tipo da página e com o que está visível. `Organization` com `@id` único e `sameAs` em **toda** página.
```json
{
  "@context": "https://schema.org",
  "@type": "Service",
  "name": "[nome do serviço]",
  "serviceType": "[categoria]",
  "areaServed": { "@type": "City", "name": "[cidade]" },
  "provider": { "@id": "[url]#organization" },
  "offers": { "@type": "AggregateOffer", "lowPrice": "[mín]", "highPrice": "[máx]", "priceCurrency": "BRL", "validThrough": "[AAAA-MM-DD]" }
}
```
\+ `FAQPage` (mesmas perguntas visíveis) + `BreadcrumbList` + `Organization` com `sameAs`.

---

## 3. Anatomia por intenção (ordem dos blocos e peso)

### Transacional
- URL: `/orcamento-energia-solar/` · H1 modelo: "Orçamento de energia solar residencial em até 24 horas"
- Extensão: 600–900 palavras fora da FAQ. Formulário na primeira dobra ou a um clique.
- Schema: `Service` + `Offer`, `FAQPage`, `BreadcrumbList`
- **Ordem:** 1 Hero ✅ → 2 Definição 🔵 → 3 Breadcrumb 🔵 → 15 Formulário ✅ → 7 Preço ✅ → 5 Como funciona ✅ → 8 Prova ✅ → 10 Objeções ✅ → 4 Para quem 🔵 → 9 Diferencial 🔵 → 12 FAQ 🔵 → 11 Autoria 🔵 → 13 Links 🔵 → 14 Cobertura ⚪ → 16 Institucional ✅ → 17 Schema ✅ · (6 Critérios ⚠️)
- Notas: formulário sobe para a primeira dobra; preço antes ou ao lado do formulário; garantia por escrito acima do formulário (é o que mais move conversão); FAQ de 6–10 perguntas só sobre contratação.
- ⚠️ Não pode dominar: texto educativo longo. Cada parágrafo entre o hero e o formulário reduz a conversão (< 300 palavras ali).

### Comercial (a página mais completa do site)
- URL: `/energia-solar-residencial/` · H1: "Energia solar residencial: projeto, instalação e homologação"
- Extensão: 1.200–2.000 palavras. A tabela de critérios vale mais que o CTA.
- Schema: `Service`, `FAQPage`, `BreadcrumbList`
- **Ordem:** 1→17 na sequência. ✅ 1,2,3,4,5,6,7,11,12,13,15,16,17 · 🔵 8,9,10,14
- Notas: bloco 6 (tabela "o que verificar antes de contratar", 5–8 linhas) é o central e vem antes do CTA final; FAQ com 10+ perguntas; links contextuais obrigatórios explicando a diferença para as páginas irmãs.
- ⚠️ Não pode dominar: vender sem ensinar ("somos os melhores" sem critério).

### Preço
- URL: `/quanto-custa-energia-solar/` · H1: "Quanto custa energia solar residencial em 2026"
- Extensão: 800–1.400 palavras. Faixa na primeira dobra.
- Schema: `Service` + `AggregateOffer` (lowPrice, highPrice, priceCurrency, validThrough)
- **Ordem:** 1 Hero ✅ → 7 Preço ✅ → 2 Definição 🔵 → 3 Breadcrumb 🔵 → 6 Critérios 🔵 → 5 Como funciona 🔵 → 11 Autoria ✅ → 8 Prova 🔵 → 12 FAQ ✅ → 13 Links 🔵 → 14 Cobertura 🔵 → 15 Formulário ✅ → 4 ⚪ → 9 ⚪ → 10 ⚪ → 16 ✅ → 17 ✅
- Notas: preço logo após o hero (faixa, exemplo datado, variáveis, simulador, tudo com data); quem assina a faixa e quando revisou; FAQ de custo (financiamento, payback, manutenção, custo por kWp).
- ⚠️ Não pode dominar: "não existe preço único" como resposta final.

### Comparativa
- URL: `/on-grid-ou-off-grid/` · H1: "Energia solar on-grid ou off-grid: qual escolher para sua casa"
- Extensão: 900–1.500 palavras. Tabela lado a lado na primeira dobra.
- Schema: `Article` com `about` listando as duas entidades, `FAQPage`
- **Ordem:** 1 ✅ → 2 🔵 → 3 ✅ → 6 Tabela lado a lado ✅ → 9 Veredito ✅ → 4 🔵 → 7 🔵 → 8 ✅ → 11 ✅ → 12 ✅ → 13 ✅ → 15 ✅ → 5 ⚪ → 10 ⚪ → 14 ⚪ → 16 ✅ → 17 ✅
- Notas: mesmos critérios nas mesmas linhas para as duas opções; veredito por perfil ("para X, escolha Y"); CTA oferece orçamento das duas opções.
- ⚠️ Não pode dominar: neutralidade vazia ("depende do seu caso" sem completar).

### Local
- URL: `/energia-solar/campinas/` · H1: "Energia solar residencial em Campinas"
- Extensão: 700–1.200 palavras com **dado único da cidade**.
- Schema: `LocalBusiness` ou `Service` com `areaServed`, `BreadcrumbList`, `FAQPage`
- **Ordem:** 1 ✅ → 2 🔵 → 3 ✅ → 8 Prova local ✅ → 7 Faixa regional ✅ → 5 🔵 → 6 🔵 → 12 ✅ → 14 Cidades vizinhas 🔵 → 13 ✅ → 15 ✅ → 11 🔵 → 4 ⚪ → 9 ⚪ → 10 ⚪ → 16 ✅ → 17 ✅
- Notas: cidade no H1 e na definição; prova daquela cidade com bairro e data; faixa regional datada; endereço físico ou área explícita, DDD local.
- ⚠️ Não pode dominar: template nacional com o nome da cidade trocado (conteúdo escalado sem valor).

### Marca (home e Sobre)
- URL: `/sobre/` · H1: "Solaris Energia: quem somos e o que entregamos"
- Extensão: home curta (distribui para os hubs); Sobre 600–1.000 palavras de fatos verificáveis.
- Schema: `Organization` com `@id`, `sameAs`, `founder`, `foundingDate`, `address`; `WebSite` na home
- **Ordem:** 1 ✅ → 2 ✅ → 8 Prova ✅ → 11 Autoria/fundadores ✅ → 5 🔵 → 4 🔵 → 9 🔵 → 13 ✅ → 16 ✅ → 12 🔵 → 15 🔵 → 3 ⚪ → 7 ⚪ → 10 ⚪ → 14 ⚪ → 17 ✅ · (6 Critérios ⚠️)
- Notas: definição da empresa (o que faz, desde quando, onde, com quem); volume, tempo de mercado, avaliações externas **com link**; fundadores com nome, foto e registro; links da home para cada hub e páginas locais.
- ⚠️ Não pode dominar: conteúdo informacional na home; história emocional sem fato.

### Informacional
- URL: `/guia/como-funciona-energia-solar/` · H1: "Como funciona a energia solar residencial"
- Extensão: 1.200–2.500 palavras, definição no primeiro parágrafo.
- Schema: `Article` com `author`, `datePublished`, `dateModified`, `about`
- **Ordem:** 3 ✅ → 1 🔵 → 2 ✅ → 11 ✅ → 5 🔵 → 6 🔵 → 13 ✅ → 12 ✅ → 7 ⚪ → 8 ⚪ → 15 ⚠️ → 4 ⚪ → 9 ⚪ → 10 ⚪ → 14 ⚪ → 16 ✅ → 17 ✅
- Notas: H1 é a pergunta/conceito, sem promessa comercial; definição direta na 1ª frase (20–35 palavras); sempre linka para a página comercial correspondente com transição escrita.
- ⚠️ Não pode dominar: CTA agressivo. Um CTA contextual no meio e um no fim.

---

## 4. Prova e preço — os dois blocos que mais faltam

**Formato da prova por tipo de serviço**

| Tipo de serviço | Formato da prova | Exemplo |
|---|---|---|
| Físico visível | Foto pareada, mesmo ângulo, data e cidade | Telhado antes/depois, Sorocaba, maio/2026 |
| Resultado numérico | Métrica antes → depois + prazo | Conta de R$ 620 → R$ 74 em 3 meses |
| Intangível | Marco antes → depois + tempo | Projeto aprovado em 18 dias vs. média de 45 |
| Recorrente | Volume e continuidade | 380 residências desde 2019, 94% ativas |
| Qualquer | Depoimento com nome, cidade, contexto e resultado | "Marcos R., Indaiatuba: 88% de economia" |

**Como mostrar preço quando o preço varia**

| Formato | O que publicar |
|---|---|
| Faixa por variável | Tabela com variáveis que alteram o preço e o efeito de cada uma |
| Exemplo datado | Caso fechado com perfil, cidade, mês e faixa, marcado como referência |
| Faixa regional | Nas páginas locais, faixa daquela região revisada por trimestre |
| Simulador | 2–3 dados do usuário geram faixa mín/máx exibida na página |
| **Evitar** | Valor fixo sem data, região e variáveis ("A partir de R$ 9.990") |

---

## 5. Checklist de auditoria (bloco a bloco)

1. **Hero:** H1 nomeia serviço + público/cidade, sem slogan · subtítulo com número ou prazo · ≥3 provas curtas antes de rolar · CTA principal + WhatsApp real na 1ª dobra.
2. **Definição:** 1ª frase após o hero define o que é, para quem e o resultado (20–35 palavras) · em negrito, sem "melhor/líder/incrível".
3. **Breadcrumb:** visível e mostra o hub correto · marcado em `BreadcrumbList`.
4. **Para quem:** condição mensurável · diz para quem não é e aponta a página certa.
5. **Como funciona:** 3–5 passos numerados · cada passo com prazo ou entregável.
6. **Critérios:** tabela (não lista) · cada linha com a pergunta do cliente e a resposta · 5–8 linhas.
7. **Preço:** faixa, exemplo datado ou variáveis · com data, região e perfil · link para simulador/orçamento ao lado.
8. **Prova:** ≥1 antes/depois pareado com data e cidade · volume com número e ano · depoimentos com nome, cidade e resultado.
9. **Diferencial:** compara com alternativas reais · diz para quem cada alternativa faz sentido.
10. **Objeções:** 3 principais na voz do cliente · cada resposta com garantia, prazo ou responsabilidade por escrito.
11. **Autoria:** responsável com registro profissional · data de atualização visível · página de autor linkada (foto, formação).
12. **FAQ:** ≥10 perguntas · respostas de 40–80 palavras com dado · `FAQPage` com exatamente as mesmas perguntas.
13. **Links:** 3–6 links no corpo para páginas irmãs · diferença escrita · âncoras diferentes do H1 do destino.
14. **Cobertura:** cada cidade com página própria · âncoras variadas.
15. **Formulário:** 3–6 campos, ≥1 segmenta · botão diz o que recebe ("Receber simulação gratuita", não "Enviar") · WhatsApp/telefone reais testados (nada de `#` ou 0000).
16. **Institucional:** CNPJ, razão social, endereço completo no rodapé · telefone com DDD + horário · política de privacidade e termos.
17. **Schema:** JSON-LD do tipo correto · `Organization` com `@id` (#organization) e `sameAs` · passa sem erro em search.google.com/test/rich-results.

**Extras por intenção:** transacional (formulário na 1ª dobra; preço antes do formulário; < 300 palavras entre hero e formulário) · comercial (critérios antes do CTA final; diferença das irmãs escrita) · preço (faixa na 1ª dobra; `AggregateOffer` com lowPrice/highPrice/validThrough; quem assina a faixa) · comparativa (mesmos critérios lado a lado; veredito por perfil; CTA para as duas opções) · local (cidade no H1; dado único da cidade; prova local com bairro e data; faixa regional; endereço/DDD local) · marca (avaliações externas com link; fundadores com foto e registro; `Organization` com founder, foundingDate, address, sameAs) · informacional (definição na 1ª frase; máx. 1 CTA no meio e 1 no fim; link para a página de serviço; `Article` com author, datePublished, dateModified).

---

## 6. Teste final antes de publicar

Leia só quatro elementos. Se com eles alguém responde **"o que é, para quem, quanto custa e por que aqui"**, a página está pronta:

1. **H1** — nomeia a entidade e o contexto ("Energia solar residencial em Campinas", não "Soluções em energia").
2. **Sentença definicional** — primeira frase após o hero, em negrito.
3. **Tabela principal** — critérios, variáveis de preço ou comparação lado a lado (é o que buscadores e IAs extraem).
4. **Primeira pergunta da FAQ** — responde a dúvida que mais trava a decisão, 40–80 palavras, com dado concreto.

---

## 7. Base técnica obrigatória em todo site (complemento ao framework)

Checklist técnico aplicado em qualquer site criado aqui (HTML estático na Vercel ou outro):

- **`<head>`**: `lang="pt-BR"`, `<title>` único (≈50–60 caracteres, entidade + contexto), `meta description` única (≈140–160), `<link rel="canonical">` absoluto, `meta viewport`, Open Graph (`og:title`, `og:description`, `og:image` 1200×630, `og:url`, `og:type`, `og:locale=pt_BR`) e Twitter Card.
- **Hierarquia**: um único H1 por página; H2/H3 em ordem lógica, sem pular níveis; H2 que respondem perguntas reais.
- **URLs**: minúsculas, com hífen, sem acento, curtas e descritivas, estrutura em cluster (`/servico/`, `/servico/cidade/`, `/guia/tema/`). Coerente com `cleanUrls`/`trailingSlash` do `vercel.json` e com o canonical.
- **Indexação**: `robots.txt` com link para o `sitemap.xml`; sitemap com todas as URLs canônicas e `lastmod`; página 404 própria; nada de conteúdo importante só via JS.
- **Dados estruturados**: `Organization` (ou `LocalBusiness`/`ProfessionalService`) com `@id` estável reaproveitado em todas as páginas, `WebSite` na home, `BreadcrumbList`, `FAQPage` idêntico ao visível, `Service`/`Article`/`Person` conforme a intenção.
- **Performance (Core Web Vitals)**: imagens em WebP/AVIF com `width`/`height`, `loading="lazy"` abaixo da dobra e `fetchpriority="high"` na imagem do hero; fontes com `preconnect` + `display=swap`; CSS crítico enxuto; JS com `defer`; cache longo em `/assets/`.
- **Acessibilidade = SEO**: `alt` descritivo em imagens, contraste, foco visível, links com texto descritivo (nada de "clique aqui"), `prefers-reduced-motion`.
- **Links internos**: toda página comercial recebe link da home/hub e de pelo menos uma página informacional; âncoras descritivas e variadas.
- **Contato real**: WhatsApp `https://wa.me/55DDDNUMERO` testado, `tel:` com DDD, e-mail real. Nenhum `href="#"` publicado.

Referências de sites feitos por especialista: ver [`sites-referencia.md`](./sites-referencia.md).
