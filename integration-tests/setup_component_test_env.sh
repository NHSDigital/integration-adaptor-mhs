#!/bin/bash

set -e

mkdir -p ./generated-certs/fake-spine/
mkdir -p ./generated-certs/inbound/
mkdir -p ./generated-certs/outbound/

(cd ./generated-certs/fake-spine || exit; openssl req -x509 -subj "/CN=fakespine" -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 365)
(cd ./generated-certs/inbound || exit; openssl req -x509 -subj "/CN=inbound" -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 365)
(cd ./generated-certs/outbound || exit; openssl req -x509 -subj "/CN=outbound" -newkey rsa:2048 -nodes -keyout key.pem -out cert.pem -days 365)

touch component-test-source.sh
echo -e "export FAKE_SPINE_CERTIFICATE=\"$(cat ./generated-certs/fake-spine/cert.pem)\"" >> component-test-source.sh
echo -e "export FAKE_SPINE_PRIVATE_KEY=\"$(cat ./generated-certs/fake-spine/key.pem)\"" >> component-test-source.sh
echo -e "export OUTBOUND_CERTIFICATE=\"$(cat ./generated-certs/outbound/cert.pem)\"" >> component-test-source.sh
echo -e "export OUTBOUND_PRIVATE_KEY=\"$(cat ./generated-certs/outbound/key.pem)\"" >> component-test-source.sh
echo -e "export INBOUND_CERTIFICATE=\"$(cat ./generated-certs/inbound/cert.pem)\"" >> component-test-source.sh
echo -e "export INBOUND_PRIVATE_KEY=\"$(cat ./generated-certs/inbound/key.pem)\"" >> component-test-source.sh
echo -e "export FAKE_SPINE_CA_STORE=\"$(cat ./generated-certs/outbound/cert.pem)\n$(cat ./generated-certs/inbound/cert.pem)\"" >> component-test-source.sh
echo -e "export OUTBOUND_CA_STORE=\"$(cat ./generated-certs/fake-spine/cert.pem)\"" >> component-test-source.sh
echo -e "export INBOUND_CA_STORE=\"$(cat ./generated-certs/fake-spine/cert.pem)\"" >> component-test-source.sh
echo -e "export MHS_SECRET_PARTY_KEY=\"test-party-key\"" >> component-test-source.sh
echo -e "export MHS_OUTBOUND_VALIDATE_CERTIFICATE=\"False\"" >> component-test-source.sh
echo -e "export SUPPORTED_FILE_TYPES=\"text/plain,text/html,application/pdf,text/xml,application/xml,text/rtf,audio/basic,audio/mpeg,image/png,image/gif,image/jpeg,image/tiff,video/mpeg,application/msword,application/octet-stream,application/vnd.ms-excel.addin.macroEnabled.12,application/vnd.ms-excel.sheet.binary.macroEnabled.12,application/vnd.ms-excel.sheet.macroEnabled.12,application/vnd.ms-excel.template.macroEnabled.12,application/vnd.ms-powerpoint.presentation.macroEnabled.12,application/vnd.ms-powerpoint.slideshow.macroEnabled.12,application/vnd.ms-powerpoint.template.macroEnabled.12,application/vnd.ms-word.document.macroEnabled.12,application/vnd.ms-word.template.macroEnabled.12,application/vnd.openxmlformats-officedocument.presentationml.template,application/vnd.openxmlformats-officedocument.presentationml.slideshow,application/vnd.openxmlformats-officedocument.presentationml.presentation,application/vnd.openxmlformats-officedocument.spreadsheetml.sheet,application/vnd.openxmlformats-officedocument.spreadsheetml.template,application/vnd.openxmlformats-officedocument.wordprocessingml.template,application/vnd.openxmlformats-officedocument.wordprocessingml.document,image/bmp,text/richtext,text/rtf,application/x-hl7,application/pgp-signature,video/msvideo,application/pgp,application/x-shockwave-flash,application/x-rar-compressed,video/x-msvideo,audio/wav,application/hl7-v2,audio/x-wav,application/vnd.ms-excel,audio/x-aiff,audio/wave,application/pgp-encrypted,video/x-ms-asf,image/x-windows-bmp,video/3gpp2,application/x-netcdf,video/x-ms-wmv,application/x-rtf,application/x-mplayer2,chemical/x-pdb,text/csv,image/x-pict,audio/vnd.rn-realaudio,text/css,video/quicktime,video/mp4,multipart/x-zip,application/pgp-keys,audio/x-mpegurl,audio/x-ms-wma,chemical/x-mdl-sdfile,application/x-troff-msvideo,application/x-compressed,image/svg+xml,chemical/x-mdl-molfile,application/EDI-X12,application/postscript,application/xhtml+xml,video/x-flv,application/x-zip-compressed,application/hl7-v2+xml,application/vnd.openxmlformats-package.relationships+xml,video/x-ms-vob,application/x-gzip,audio/x-pn-wav,application/msoutlook,video/3gpp,application/cdf,application/EDIFACT,application/x-cdf,application/x-pgp-plugin,audio/x-au,application/dicom,application/EDI-Consent,application/zip,application/json,application/x-pkcs10,application/pkix-cert,application/x-pkcs12,application/x-pkcs7-mime,application/pkcs10,application/x-x509-ca-cert,application/pkcs-12,application/pkcs7-signature,application/x-pkcs7-signature,application/pkcs7-mime\"" >> component-test-source.sh

rm -rf ./generated-certs