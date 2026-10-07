<?php
/**
 * Minimal, dependency-free mail sender.
 * Uses authenticated SMTP when configured (recommended on Hostinger), otherwise PHP mail().
 */
if (basename($_SERVER['SCRIPT_FILENAME'] ?? '') === 'mailer.php') {
    http_response_code(403);
    exit;
}

function mail_header_encode(string $s): string
{
    return preg_match('/[^\x20-\x7E]/', $s) ? '=?UTF-8?B?' . base64_encode($s) . '?=' : $s;
}

function mail_clean(string $s): string
{
    return trim(str_replace(["\r", "\n", '%0a', '%0d'], ' ', $s));
}

/** @param string|array $to */
function send_mail($to, string $subject, string $html, string $text, string $replyTo = '', string $replyName = ''): bool
{
    $toList = array_values(array_filter(array_map('trim', is_array($to) ? $to : explode(',', $to))));
    if (!$toList) {
        return false;
    }
    $boundary = 'b' . bin2hex(random_bytes(12));
    $from = mail_clean(MAIL_FROM);
    $headers = [
        'Date: ' . date('r'),
        'From: ' . mail_header_encode(mail_clean(MAIL_FROM_NAME)) . ' <' . $from . '>',
        'Message-ID: <' . bin2hex(random_bytes(10)) . '@' . (parse_url(SITE_URL, PHP_URL_HOST) ?: 'localhost') . '>',
        'MIME-Version: 1.0',
        'Content-Type: multipart/alternative; boundary="' . $boundary . '"',
    ];
    if ($replyTo !== '' && filter_var($replyTo, FILTER_VALIDATE_EMAIL)) {
        $headers[] = 'Reply-To: ' . ($replyName !== '' ? mail_header_encode(mail_clean($replyName)) . ' ' : '')
            . '<' . mail_clean($replyTo) . '>';
    }
    $body = "--{$boundary}\r\n"
        . "Content-Type: text/plain; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n"
        . chunk_split(base64_encode($text)) . "\r\n"
        . "--{$boundary}\r\n"
        . "Content-Type: text/html; charset=UTF-8\r\nContent-Transfer-Encoding: base64\r\n\r\n"
        . chunk_split(base64_encode($html)) . "\r\n"
        . "--{$boundary}--\r\n";
    $subjectEnc = mail_header_encode(mail_clean($subject));

    if (SMTP_ENABLED && SMTP_PASS !== '') {
        if (smtp_send($toList, $subjectEnc, $headers, $body)) {
            return true;
        }
        error_log('[Rio mailer] SMTP failed, falling back to mail()');
    }
    $params = filter_var($from, FILTER_VALIDATE_EMAIL) ? '-f' . $from : '';
    return @mail(implode(', ', $toList), $subjectEnc, $body, implode("\r\n", $headers), $params);
}

function smtp_send(array $toList, string $subjectEnc, array $headers, string $body): bool
{
    $host = (SMTP_SECURE === 'ssl' ? 'ssl://' : '') . SMTP_HOST;
    $errno = 0;
    $errstr = '';
    $ctx = stream_context_create(['ssl' => ['verify_peer' => true, 'verify_peer_name' => true]]);
    $fp = @stream_socket_client($host . ':' . SMTP_PORT, $errno, $errstr, 15, STREAM_CLIENT_CONNECT, $ctx);
    if (!$fp) {
        error_log("[Rio mailer] SMTP connect error: $errstr ($errno)");
        return false;
    }
    stream_set_timeout($fp, 15);

    $read = function () use ($fp): string {
        $data = '';
        while (($line = fgets($fp, 515)) !== false) {
            $data .= $line;
            if (isset($line[3]) && $line[3] === ' ') {
                break;
            }
        }
        return $data;
    };
    $cmd = function (string $c, array $expect) use ($fp, $read): bool {
        fwrite($fp, $c . "\r\n");
        $r = $read();
        $ok = in_array((int) substr($r, 0, 3), $expect, true);
        if (!$ok) {
            error_log('[Rio mailer] SMTP unexpected reply to "' . strtok($c, ' ') . '": ' . trim($r));
        }
        return $ok;
    };

    $ehlo = parse_url(SITE_URL, PHP_URL_HOST) ?: 'localhost';
    $ok = (int) substr($read(), 0, 3) === 220 && $cmd('EHLO ' . $ehlo, [250]);
    if ($ok && SMTP_SECURE === 'tls') {
        $ok = $cmd('STARTTLS', [220])
            && stream_socket_enable_crypto($fp, true, STREAM_CRYPTO_METHOD_TLS_CLIENT)
            && $cmd('EHLO ' . $ehlo, [250]);
    }
    $ok = $ok
        && $cmd('AUTH LOGIN', [334])
        && $cmd(base64_encode(SMTP_USER), [334])
        && $cmd(base64_encode(SMTP_PASS), [235])
        && $cmd('MAIL FROM:<' . mail_clean(MAIL_FROM) . '>', [250]);
    foreach ($toList as $rcpt) {
        $ok = $ok && $cmd('RCPT TO:<' . mail_clean($rcpt) . '>', [250, 251]);
    }
    if ($ok && $cmd('DATA', [354])) {
        $msg = implode("\r\n", array_merge(['To: ' . implode(', ', $toList), 'Subject: ' . $subjectEnc], $headers))
            . "\r\n\r\n" . $body;
        $msg = preg_replace('/^\./m', '..', $msg);   // dot-stuffing
        $ok = $cmd($msg . "\r\n.", [250]);
    } else {
        $ok = false;
    }
    @fwrite($fp, "QUIT\r\n");
    fclose($fp);
    return $ok;
}
