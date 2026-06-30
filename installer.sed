[Version]
Class=IEXPRESS
SEDVersion=3

[Options]
PackagePurpose=InstallApp
ShowInstallProgramWindow=0
HideExtractAnimation=0
UseLongFileName=1
InsideCompressed=0
CAB_FixedSize=0
CAB_ResvCodeSize=0
RebootMode=N
InstallPrompt=%InstallPrompt%
DisplayLicense=%DisplayLicense%
FinishMessage=%FinishMessage%
TargetName=%TargetName%
FriendlyName=%FriendlyName%
AppLaunched=%AppLaunched%
PostInstallCmd=%PostInstallCmd%
AdminQuietInstCmd=%AdminQuietInstCmd%
UserQuietInstCmd=%UserQuietInstCmd%
SourceFiles=SourceFiles

[SourceFiles]
SourceFiles0=C:\Users\zaiaj\OneDrive\Escritorio\orgEmpresarialProyecte\
SourceFiles1=C:\Users\zaiaj\OneDrive\Escritorio\orgEmpresarialProyecte\dist\

[SourceFiles0]
%FILE0%=
%FILE1%=

[SourceFiles1]
%FILE2%=

[Strings]
InstallPrompt=
DisplayLicense=
FinishMessage=
TargetName=C:\Users\zaiaj\OneDrive\Escritorio\orgEmpresarialProyecte\Instalador_SistemaVentas.exe
FriendlyName=Instalador Sistema de Ventas
AppLaunched=cmd.exe /c instalar.bat
PostInstallCmd=<None>
AdminQuietInstCmd=
UserQuietInstCmd=
FILE0=instalar.bat
FILE1=caja.ico
FILE2=main.exe
