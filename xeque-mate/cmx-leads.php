<?php
/**
 * XEQUE-MATE · Captura de leads do formulário (Nome, E-mail, Telefone)
 *
 * O que este snippet faz:
 *  1. Cria o endpoint POST /wp-json/cmx/v1/lead (usado pelo widget HTML do Elementor).
 *  2. Salva cada lead no painel do WordPress (menu "Leads Xeque-mate"), para que
 *     nenhum cadastro se perca mesmo se o e-mail falhar.
 *  3. Envia um e-mail para admin@drclaudiowatanabe.com.br com os dados preenchidos.
 *  4. Permite exportar todos os leads em CSV (Leads Xeque-mate → Exportar CSV).
 *  5. Proteção anti-spam: campo isca (honeypot), tempo mínimo de preenchimento
 *     e limite de envios por IP.
 *
 * Instalação (escolha UMA opção):
 *  A) Plugin "Code Snippets" → Adicionar novo → cole o código SEM a linha "<?php"
 *     → "Executar em todo o site" → Salvar e ativar.
 *  B) Tema filho → functions.php → cole o código a partir da linha abaixo de "<?php".
 *
 * Importante: para o e-mail chegar (e não cair no spam), configure o envio SMTP
 * com o plugin "WP Mail SMTP" (ou similar) usando uma conta do próprio domínio.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

if ( ! defined( 'CMX_LEAD_TO' ) ) {
	define( 'CMX_LEAD_TO', 'admin@drclaudiowatanabe.com.br' );
}

/* -------------------------------------------------------------------------
 * 1. Tipo de conteúdo privado para guardar os leads
 * ---------------------------------------------------------------------- */
add_action( 'init', function () {
	register_post_type( 'cmx_lead', array(
		'labels'          => array(
			'name'          => 'Leads Xeque-mate',
			'singular_name' => 'Lead Xeque-mate',
			'menu_name'     => 'Leads Xeque-mate',
			'all_items'     => 'Todos os leads',
			'search_items'  => 'Buscar leads',
			'not_found'     => 'Nenhum lead ainda.',
		),
		'public'          => false,
		'show_ui'         => true,
		'show_in_menu'    => true,
		'show_in_rest'    => false,
		'menu_icon'       => 'dashicons-groups',
		'menu_position'   => 26,
		'supports'        => array( 'title' ),
		'capability_type' => 'post',
		'capabilities'    => array( 'create_posts' => 'do_not_allow' ),
		'map_meta_cap'    => true,
	) );
} );

/* -------------------------------------------------------------------------
 * 2. Endpoint REST: POST /wp-json/cmx/v1/lead
 * ---------------------------------------------------------------------- */
add_action( 'rest_api_init', function () {
	register_rest_route( 'cmx/v1', '/lead', array(
		'methods'             => 'POST',
		'callback'            => 'cmx_handle_lead',
		'permission_callback' => '__return_true',
	) );
} );

function cmx_handle_lead( WP_REST_Request $request ) {
	$ok = new WP_REST_Response( array( 'ok' => true ), 200 );

	// Anti-spam 1: campo isca preenchido = robô. Responde "ok" sem salvar.
	if ( '' !== trim( (string) $request->get_param( 'website' ) ) ) {
		return $ok;
	}

	// Anti-spam 2: formulário enviado rápido demais (menos de 2 segundos).
	$elapsed = (int) $request->get_param( 'elapsed' );
	if ( $elapsed > 0 && $elapsed < 2000 ) {
		return $ok;
	}

	// Anti-spam 3: no máximo 5 envios a cada 15 minutos por IP.
	$ip      = isset( $_SERVER['REMOTE_ADDR'] ) ? sanitize_text_field( wp_unslash( $_SERVER['REMOTE_ADDR'] ) ) : '';
	$rl_key  = 'cmx_rl_' . md5( $ip );
	$count   = (int) get_transient( $rl_key );
	if ( $count >= 5 ) {
		return new WP_REST_Response( array( 'ok' => false, 'message' => 'Muitas tentativas. Tente novamente em alguns minutos.' ), 429 );
	}
	set_transient( $rl_key, $count + 1, 15 * MINUTE_IN_SECONDS );

	// Dados do formulário
	$name  = sanitize_text_field( (string) $request->get_param( 'name' ) );
	$email = sanitize_email( (string) $request->get_param( 'email' ) );
	$phone = preg_replace( '/\D+/', '', (string) $request->get_param( 'phone' ) );

	$errors = array();
	if ( mb_strlen( $name ) < 3 || mb_strlen( $name ) > 120 ) {
		$errors[] = 'name';
	}
	if ( ! is_email( $email ) ) {
		$errors[] = 'email';
	}
	if ( strlen( $phone ) < 10 || strlen( $phone ) > 11 ) {
		$errors[] = 'phone';
	}
	if ( $errors ) {
		return new WP_REST_Response( array( 'ok' => false, 'errors' => $errors ), 422 );
	}

	$phone_fmt = strlen( $phone ) === 11
		? sprintf( '(%s) %s-%s', substr( $phone, 0, 2 ), substr( $phone, 2, 5 ), substr( $phone, 7 ) )
		: sprintf( '(%s) %s-%s', substr( $phone, 0, 2 ), substr( $phone, 2, 4 ), substr( $phone, 6 ) );

	// Rastreamento (UTM e parâmetros da Hotmart)
	$tracking = array();
	foreach ( array( 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'src', 'sck', 'fbclid', 'gclid' ) as $key ) {
		$value = sanitize_text_field( (string) $request->get_param( $key ) );
		if ( '' !== $value ) {
			$tracking[ $key ] = mb_substr( $value, 0, 200 );
		}
	}
	$page     = esc_url_raw( (string) $request->get_param( 'page' ) );
	$referrer = esc_url_raw( (string) $request->get_param( 'referrer' ) );
	$date     = wp_date( 'd/m/Y H:i' );

	// Salva no painel
	$post_id = wp_insert_post( array(
		'post_type'   => 'cmx_lead',
		'post_status' => 'private',
		'post_title'  => $name . ' — ' . $email,
	) );
	if ( $post_id && ! is_wp_error( $post_id ) ) {
		update_post_meta( $post_id, '_cmx_name', $name );
		update_post_meta( $post_id, '_cmx_email', $email );
		update_post_meta( $post_id, '_cmx_phone', $phone_fmt );
		update_post_meta( $post_id, '_cmx_whatsapp', 'https://wa.me/55' . $phone );
		update_post_meta( $post_id, '_cmx_page', $page );
		update_post_meta( $post_id, '_cmx_referrer', $referrer );
		update_post_meta( $post_id, '_cmx_tracking', $tracking );
		update_post_meta( $post_id, '_cmx_ip', $ip );
	}

	// E-mail para o administrador
	$rows = array(
		'Nome'     => esc_html( $name ),
		'E-mail'   => '<a href="mailto:' . esc_attr( $email ) . '">' . esc_html( $email ) . '</a>',
		'Telefone' => esc_html( $phone_fmt ) . ' · <a href="https://wa.me/55' . esc_attr( $phone ) . '">abrir no WhatsApp</a>',
		'Data'     => esc_html( $date ),
		'Página'   => esc_html( $page ),
	);
	foreach ( $tracking as $key => $value ) {
		$rows[ $key ] = esc_html( $value );
	}

	$html  = '<div style="font-family:Arial,sans-serif;font-size:15px;color:#261710;max-width:560px">';
	$html .= '<div style="height:10px;background:repeating-linear-gradient(90deg,#8c511f 0 10px,#2b1108 10px 20px)"></div>';
	$html .= '<h2 style="font-family:Georgia,serif;color:#2a0f08;margin:18px 0 6px">Novo lead · Xeque-mate</h2>';
	$html .= '<p style="margin:0 0 16px;color:#756356">Alguém preencheu o formulário e foi encaminhado para o checkout (R$ 67,00).</p>';
	$html .= '<table cellpadding="8" cellspacing="0" style="border-collapse:collapse;width:100%">';
	foreach ( $rows as $label => $value ) {
		$html .= '<tr><td style="border-bottom:1px solid #ead7bb;font-weight:bold;width:130px">' . esc_html( $label ) . '</td><td style="border-bottom:1px solid #ead7bb">' . $value . '</td></tr>';
	}
	$html .= '</table>';
	$html .= '<p style="margin-top:16px;font-size:12px;color:#8f837b">Lembre-se: o preenchimento não confirma a compra. Confira o status do pagamento na Hotmart.</p>';
	$html .= '</div>';

	$headers = array(
		'Content-Type: text/html; charset=UTF-8',
		'Reply-To: ' . str_replace( array( "\r", "\n", '<', '>', ',' ), '', $name ) . ' <' . $email . '>',
	);
	$sent = wp_mail( CMX_LEAD_TO, 'Novo lead Xeque-mate: ' . $name, $html, $headers );

	if ( $post_id && ! is_wp_error( $post_id ) ) {
		update_post_meta( $post_id, '_cmx_mail_sent', $sent ? 'sim' : 'não' );
	}

	return $ok;
}

/* -------------------------------------------------------------------------
 * 3. Colunas da lista de leads no painel
 * ---------------------------------------------------------------------- */
add_filter( 'manage_cmx_lead_posts_columns', function () {
	return array(
		'cb'           => '<input type="checkbox" />',
		'cmx_name'     => 'Nome',
		'cmx_email'    => 'E-mail',
		'cmx_phone'    => 'Telefone',
		'cmx_source'   => 'Origem',
		'cmx_mail'     => 'E-mail enviado?',
		'date'         => 'Data',
	);
} );

add_action( 'manage_cmx_lead_posts_custom_column', function ( $column, $post_id ) {
	switch ( $column ) {
		case 'cmx_name':
			echo esc_html( get_post_meta( $post_id, '_cmx_name', true ) );
			break;
		case 'cmx_email':
			$email = get_post_meta( $post_id, '_cmx_email', true );
			echo '<a href="mailto:' . esc_attr( $email ) . '">' . esc_html( $email ) . '</a>';
			break;
		case 'cmx_phone':
			echo '<a href="' . esc_url( get_post_meta( $post_id, '_cmx_whatsapp', true ) ) . '" target="_blank" rel="noopener">' . esc_html( get_post_meta( $post_id, '_cmx_phone', true ) ) . '</a>';
			break;
		case 'cmx_source':
			$t = (array) get_post_meta( $post_id, '_cmx_tracking', true );
			echo esc_html( isset( $t['utm_source'] ) ? $t['utm_source'] : ( isset( $t['src'] ) ? $t['src'] : '—' ) );
			break;
		case 'cmx_mail':
			echo esc_html( get_post_meta( $post_id, '_cmx_mail_sent', true ) ?: '—' );
			break;
	}
}, 10, 2 );

/* -------------------------------------------------------------------------
 * 4. Exportar leads em CSV (abre no Excel / Google Planilhas)
 * ---------------------------------------------------------------------- */
add_action( 'admin_menu', function () {
	add_submenu_page(
		'edit.php?post_type=cmx_lead',
		'Exportar CSV',
		'Exportar CSV',
		'edit_posts',
		'cmx-lead-export',
		function () {
			$url = wp_nonce_url( admin_url( 'admin-post.php?action=cmx_export_leads' ), 'cmx_export_leads' );
			echo '<div class="wrap"><h1>Exportar leads do Xeque-mate</h1>';
			echo '<p>Baixe todos os cadastros em uma planilha CSV.</p>';
			echo '<p><a class="button button-primary" href="' . esc_url( $url ) . '">Baixar CSV</a></p></div>';
		}
	);
} );

add_action( 'admin_post_cmx_export_leads', function () {
	if ( ! current_user_can( 'edit_posts' ) || ! check_admin_referer( 'cmx_export_leads' ) ) {
		wp_die( 'Sem permissão.' );
	}
	$leads = get_posts( array(
		'post_type'      => 'cmx_lead',
		'post_status'    => 'any',
		'posts_per_page' => -1,
		'orderby'        => 'date',
		'order'          => 'DESC',
	) );

	nocache_headers();
	header( 'Content-Type: text/csv; charset=UTF-8' );
	header( 'Content-Disposition: attachment; filename=leads-xeque-mate-' . wp_date( 'Y-m-d' ) . '.csv' );

	$out = fopen( 'php://output', 'w' );
	fwrite( $out, "\xEF\xBB\xBF" ); // BOM para acentos no Excel
	fputcsv( $out, array( 'Data', 'Nome', 'E-mail', 'Telefone', 'utm_source', 'utm_medium', 'utm_campaign', 'src', 'sck', 'Página' ), ';' );
	foreach ( $leads as $lead ) {
		$t = (array) get_post_meta( $lead->ID, '_cmx_tracking', true );
		$row = array(
			get_the_date( 'd/m/Y H:i', $lead ),
			get_post_meta( $lead->ID, '_cmx_name', true ),
			get_post_meta( $lead->ID, '_cmx_email', true ),
			get_post_meta( $lead->ID, '_cmx_phone', true ),
			isset( $t['utm_source'] ) ? $t['utm_source'] : '',
			isset( $t['utm_medium'] ) ? $t['utm_medium'] : '',
			isset( $t['utm_campaign'] ) ? $t['utm_campaign'] : '',
			isset( $t['src'] ) ? $t['src'] : '',
			isset( $t['sck'] ) ? $t['sck'] : '',
			get_post_meta( $lead->ID, '_cmx_page', true ),
		);
		// Evita injeção de fórmulas ao abrir no Excel
		$row = array_map( function ( $v ) {
			$v = (string) $v;
			return preg_match( '/^[=+\-@\t\r]/', $v ) ? "'" . $v : $v;
		}, $row );
		fputcsv( $out, $row, ';' );
	}
	fclose( $out );
	exit;
} );
