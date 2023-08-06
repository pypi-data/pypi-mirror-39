
Caramel is a certificate management system that makes it easy to use client
certificates in web applications, mobile applications, embedded use and
other places. It solves the certificate signing and certificate
management headache, while attempting to be easy to deploy, maintain and
use in a secure manner.

Caramel makes it easier (it's never completely easy) to run your own
certificate authority and manage and maintain keys and signing periods.

Caramel focuses on reliably and continuously updating short-lived certificates
where clients (and embedded devices) continue to "phone home" and fetch
updated certificates.  This means that we do not have to provide OCSP and
CRL endpoints to handle compromised certificates, but only have to stop
updating the certificate. This also means that expired certificates
should be considered broken.


