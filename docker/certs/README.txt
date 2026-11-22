Certificados CA públicos para o build Docker (inspeção HTTPS Norton no host Windows).

O Dockerfile copia docker/certs/*.crt para /usr/local/share/ca-certificates/ e executa update-ca-certificates.

SEGURANCA (decisão A6 — Magno da Silva Franco, 2026-11-22):
- PODE versionar: certificado público (.crt / BEGIN CERTIFICATE).
- NUNCA versionar: chave privada (.key, BEGIN PRIVATE KEY), .pfx/.p12.

Arquivo em uso:
  norton-web-mail-shield-root.crt
  CN=Norton Web/Mail Shield Root
  Thumbprint (SHA1 Windows)=BC9ABF70E60A1F9D052B9C978D9737726D27B264
  Exportado do store LocalMachine\Root em 2026-11-22 (somente certificado público; HasPrivateKey=False).
