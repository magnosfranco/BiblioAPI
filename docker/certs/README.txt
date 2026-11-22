Certificados CA públicos para o build Docker (inspeção HTTPS Norton no host Windows).

O Dockerfile copia docker/certs/*.crt para /usr/local/share/ca-certificates/ e executa update-ca-certificates.

SEGURANCA (decisão A6 — Magno da Silva Franco, 2026-11-22):
- PODE versionar: certificado público (.crt / BEGIN CERTIFICATE), ex.: raiz Norton.
- NUNCA versionar: chave privada (.key, BEGIN PRIVATE KEY), .pfx/.p12, nem bundles com material secreto.

REPLACE_WITH_NORTON_ROOT.crt é placeholder self-signed só para validar o Dockerfile.
Substitua-o pelo certificado raiz real do Norton antes de depender de pip/npx no container.
