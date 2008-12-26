; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
AppName=Griffith
AppVerName=Griffith 0.9.9
AppPublisher=Vasco Nunes, Piotr Ożarowski
AppPublisherURL=http://griffith.cc/
AppSupportURL=http://griffith.cc/
AppUpdatesURL=http://griffith.cc/
DefaultDirName={pf}\Griffith
DefaultGroupName=Griffith
AllowNoIcons=true
LicenseFile=COPYING
InfoAfterFile=README
OutputDir=installer
OutputBaseFilename=griffith-0.9.9-win32
SetupIconFile=images\griffith.ico
Compression=lzma
SolidCompression=true
WizardImageFile=images\griffith_win32_installer.bmp
InternalCompressLevel=ultra
AppCopyright=Vasco Nunes/Piotr Ozarowski
DisableStartupPrompt=false
AppVersion=0.9.9
VersionInfoVersion=0.9.9

[Languages]
Name: eng; MessagesFile: compiler:Default.isl
Name: por; MessagesFile: compiler:languages\Portuguese.isl
Name: por; MessagesFile: compiler:languages\BrazilianPortuguese.isl
Name: pol; MessagesFile: compiler:languages\Polish.isl
Name: ger; MessagesFile: compiler:languages\German.isl
Name: cze; MessagesFile: compiler:languages\Czech.isl
Name: dut; MessagesFile: compiler:languages\Dutch.isl
Name: fin; MessagesFile: compiler:languages\Finnish.isl
Name: ita; MessagesFile: compiler:languages\Italian.isl
Name: fre; MessagesFile: compiler:languages\French.isl
Name: nor; MessagesFile: compiler:languages\Norwegian.isl
Name: hun; MessagesFile: compiler:languages\Hungarian.isl
Name: spa; MessagesFile: compiler:languages\Spanish.isl
Name: chi; MessagesFile: compiler:languages\ChineseSimp-11-5.1.0.isl
Name: gre; MessagesFile: compiler:languages\Greek-4-5.1.11.isl
Name: jap; MessagesFile: compiler:languages\Japanese-5-5.1.11.isl
Name: bul; MessagesFile: compiler:languages\Bulgarian-5.1.11.isl

[LangOptions]
LanguageCodePage=0

[Tasks]
Name: desktopicon; Description: {cm:CreateDesktopIcon}; GroupDescription: {cm:AdditionalIcons}; Flags: unchecked
Name: quicklaunchicon; Description: {cm:CreateQuickLaunchIcon}; GroupDescription: {cm:AdditionalIcons}; Flags: unchecked

[Files]
Source: dist\griffith.exe; DestDir: {app}; Flags: ignoreversion
Source: dist\*; DestDir: {app}; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: {group}\{cm:LaunchProgram,Griffith};    Filename: {app}\griffith.exe
Name: {group}\{cm:UninstallProgram,Griffith}; Filename: {uninstallexe}
Name: {group}\{cm:ProgramOnTheWeb,Griffith};  Filename: http://griffith.cc
Name: {group}\Doc\Griffith Forum;             Filename: http://griffith.cc/forum/
Name: {group}\Doc\Griffith Wiki;              Filename: http://wiki.griffith.cc/
; some information files opened by iexplore which should work on most installations
Name: {group}\Doc\INSTALL;     Filename: "{pf}\Internet Explorer\iexplore.exe"; Parameters: {app}\INSTALL;     IconFilename: %SystemRoot%\system32\SHELL32.dll; IconIndex: -152
Name: {group}\Doc\NEWS;        Filename: "{pf}\Internet Explorer\iexplore.exe"; Parameters: {app}\NEWS;        IconFilename: %SystemRoot%\system32\SHELL32.dll; IconIndex: -152
Name: {group}\Doc\AUTHORS;     Filename: "{pf}\Internet Explorer\iexplore.exe"; Parameters: {app}\AUTHORS;     IconFilename: %SystemRoot%\system32\SHELL32.dll; IconIndex: -152
Name: {group}\Doc\THANKS;      Filename: "{pf}\Internet Explorer\iexplore.exe"; Parameters: {app}\THANKS;      IconFilename: %SystemRoot%\system32\SHELL32.dll; IconIndex: -152
Name: {group}\Doc\License;     Filename: "{pf}\Internet Explorer\iexplore.exe"; Parameters: {app}\COPYING;     IconFilename: %SystemRoot%\system32\SHELL32.dll; IconIndex: -152
Name: {group}\Doc\README;      Filename: "{pf}\Internet Explorer\iexplore.exe"; Parameters: {app}\README;      IconFilename: %SystemRoot%\system32\SHELL32.dll; IconIndex: -152
Name: {group}\Doc\TRANSLATORS; Filename: "{pf}\Internet Explorer\iexplore.exe"; Parameters: {app}\TRANSLATORS; IconFilename: %SystemRoot%\system32\SHELL32.dll; IconIndex: -152
; desktop and quick launch icons
Name: {userdesktop}\Griffith; Filename: {app}\griffith.exe; Tasks: desktopicon
Name: {userappdata}\Microsoft\Internet Explorer\Quick Launch\Griffith; Filename: {app}\griffith.exe; Tasks: quicklaunchicon

[Run]
Filename: {app}\griffith.exe; Description: {cm:LaunchProgram,Griffith}; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: files; Name: {app}\lib\*.pyo
Type: files; Name: {app}\lib\plugins\export\*.pyo
Type: files; Name: {app}\lib\plugins\movie\*.pyo
Type: files; Name: {app}\lib\plugins\imp\*.pyo

