; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
AppName=Griffith
AppVerName=Griffith 0.9~rc1
AppPublisher=Vasco Nunes, Piotr Ożarowski
AppPublisherURL=http://griffith.berlios.de/
AppSupportURL=http://griffith.berlios.de/
AppUpdatesURL=http://griffith.berlios.de/
DefaultDirName={pf}\Griffith
DefaultGroupName=Griffith
AllowNoIcons=yes
LicenseFile=C:\griffith\COPYING
InfoAfterFile=C:\griffith\README
OutputDir=C:\griffith\installer
OutputBaseFilename=griffith-0.6.1-win32
SetupIconFile=C:\griffith\images\griffith.ico
Compression=lzma
SolidCompression=yes
WizardImageFile=C:\griffith\images\griffith_win32_installer.bmp

[Languages]
Name: "eng"; MessagesFile: "compiler:Default.isl"
Name: "por"; MessagesFile: "compiler:Portuguese.isl"
Name: "por"; MessagesFile: "compiler:BrazilianPortuguese.isl"
Name: "pol"; MessagesFile: "compiler:Polish.isl"
Name: "ger"; MessagesFile: "compiler:German.isl"
Name: "cze"; MessagesFile: "compiler:Czech.isl"
Name: "fre"; MessagesFile: "compiler:French.isl"

[LangOptions]
LanguageCodePage=0

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\griffith\dist\griffith.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\griffith\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[INI]
Filename: "{app}\griffith.url"; Section: "InternetShortcut"; Key: "URL"; String: "http://griffith.berlios.de/"

[Icons]
Name: "{group}\Griffith"; Filename: "{app}\griffith.exe"
Name: "{group}\{cm:ProgramOnTheWeb,Griffith}"; Filename: "{app}\griffith.url"
Name: "{group}\{cm:UninstallProgram,Griffith}"; Filename: "{uninstallexe}"
Name: "{userdesktop}\Griffith"; Filename: "{app}\griffith.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\Griffith"; Filename: "{app}\griffith.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\griffith.exe"; Description: "{cm:LaunchProgram,Griffith}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: files; Name: "{app}\griffith.url"

