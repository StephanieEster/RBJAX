# Instruções do projeto

## SEO técnico aplicado (obrigatório em todo site/página)

Antes de criar ou alterar qualquer página, usar a skill **`seo-tecnico`** (`.claude/skills/seo-tecnico/SKILL.md`).
Ela traz o fluxo (intenção de busca → blocos na ordem da intenção → base técnica → checklist → teste final)
e as referências em `.claude/skills/seo-tecnico/references/`:

- `guia-seo-tecnico.md`: 7 intenções, 17 blocos com modelos, ordem e peso por intenção, checklist, base técnica.
- `anatomia-pagina-comercial.html`: documento original interativo (Anderson Melo SEO).
- `sites-referencia.md`: sites de referência feitos por especialista (wtsseguros.com, nidavitae.com).

## Projeto atual

- Landing page estática em `dist/` (HTML/CSS/JS), publicada na Vercel via `vercel.json`. Ver `LEIA-ME.md`.
