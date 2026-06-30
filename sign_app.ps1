$ErrorActionPreference = 'Stop'
Write-Host "Generando Certificado Autofirmado..."
$cert = New-SelfSignedCertificate -Subject "CN=SistemaDeRegistroDeVentas" -Type CodeSigningCert -CertStoreLocation "Cert:\CurrentUser\My"
Write-Host "Firmando aplicacion con el certificado: $($cert.Thumbprint)"
Set-AuthenticodeSignature -FilePath "dist\main.exe" -Certificate $cert
Write-Host "Proceso de firma completado."
