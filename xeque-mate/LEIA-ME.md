# Xeque-mate — página para Elementor

## Arquivos
- `widget-elementor.html` — página completa. Cole tudo em um widget **HTML** do Elementor.
- `cmx-leads.php` — snippet que recebe o formulário, envia para `admin@drclaudiowatanabe.com.br` e guarda os leads no painel.

## Passo a passo
1. **Snippet PHP**: instale `cmx-leads.php` pelo plugin *Code Snippets* (cole sem a linha `<?php`, "Executar em todo o site") ou no `functions.php` do tema filho.
2. **SMTP**: instale o *WP Mail SMTP* e configure com uma conta do domínio. Sem isso, o e-mail pode cair no spam ou não chegar. Os leads ficam salvos em **Leads Xeque-mate** de qualquer forma.
3. **Elementor**: página com modelo *Elementor Canvas* (ou *Largura total*), contêiner com largura total e sem espaçamento interno, e o widget HTML dentro.
4. **Checkout**: confira `CONFIG.CHECKOUT_URL` no fim do `widget-elementor.html`. O ideal é o link de pagamento da Hotmart (`https://pay.hotmart.com/...`). Nome, e-mail e telefone (`phoneac` + `phonenumber`) chegam preenchidos no checkout, e os parâmetros UTM/`src`/`sck` são repassados.
5. **Teste**: preencha o formulário. O lead deve aparecer em *Leads Xeque-mate*, o e-mail deve chegar e a compradora deve ser levada ao checkout.

## Extras
- Link direto que abre o formulário: `https://seusite.com.br/pagina/#comecar`
- Se houver Pixel da Meta ou GTM na página, o formulário dispara `InitiateCheckout` ao abrir e `Lead` ao enviar.
