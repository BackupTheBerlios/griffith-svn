﻿; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
AppName=Griffith
AppVerName=Griffith 0.12.1
AppPublisher=Vasco Nunes, Piotr Ożarowski
AppPublisherURL=http://www.griffith.cc/
AppSupportURL=http://www.griffith.cc/
AppUpdatesURL=http://www.griffith.cc/
DefaultDirName={pf}\Griffith
DefaultGroupName=Griffith
AllowNoIcons=true
LicenseFile=COPYING
InfoAfterFile=README
OutputDir=installer
OutputBaseFilename=griffith-0.12.1-win32.1
SetupIconFile=images\griffith.ico
UninstallDisplayIcon={app}\griffith.exe
Compression=lzma
SolidCompression=true
WizardImageFile=images\griffith_win32_installer.bmp
InternalCompressLevel=ultra
AppCopyright=Vasco Nunes/Piotr Ożarowski
DisableStartupPrompt=false
AppVersion=0.12.1
VersionInfoVersion=0.12.1

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
Name: chi; MessagesFile: compiler:languages\ChineseSimp-12-5.1.11.isl
Name: gre; MessagesFile: compiler:languages\Greek-4-5.1.11.isl
Name: jap; MessagesFile: compiler:languages\Japanese-5-5.1.11.isl
Name: bul; MessagesFile: compiler:languages\Bulgarian-5.1.11.isl

;[LangOptions]
;LanguageCodePage=0

[Tasks]
Name: desktopicon; Description: {cm:CreateDesktopIcon}; GroupDescription: {cm:AdditionalIcons}; Flags: unchecked
Name: quicklaunchicon; Description: {cm:CreateQuickLaunchIcon}; GroupDescription: {cm:AdditionalIcons}; Flags: unchecked

[Files]
Source: dist\griffith.exe; DestDir: {app}; Flags: ignoreversion
; don't use recursion because of components selection (movie plugins, ...)
Source: dist\*;        DestDir: {app}; Flags: ignoreversion
; use recursion, no components
Source: dist\etc\*;    DestDir: {app}\etc;    Flags: ignoreversion recursesubdirs createallsubdirs
Source: dist\glade\*;  DestDir: {app}\glade;  Flags: ignoreversion recursesubdirs createallsubdirs
Source: dist\i18n\*;   DestDir: {app}\i18n;   Flags: ignoreversion recursesubdirs createallsubdirs
Source: dist\images\*; DestDir: {app}\images; Flags: ignoreversion recursesubdirs createallsubdirs
Source: dist\share\*;  DestDir: {app}\share;  Flags: ignoreversion recursesubdirs createallsubdirs
; don't use recursion because of components selection (movie plugins, ...)
Source: dist\lib\*;    DestDir: {app}\lib;    Flags: ignoreversion
; use recursion, no components
Source: dist\lib\db\*;           DestDir: {app}\lib\db;           Flags: ignoreversion recursesubdirs createallsubdirs
Source: dist\lib\gettext\*;      DestDir: {app}\lib\gettext;      Flags: ignoreversion recursesubdirs createallsubdirs
Source: dist\lib\glade3\*;       DestDir: {app}\lib\glade3;       Flags: ignoreversion recursesubdirs createallsubdirs
;Source: dist\lib\glib-2.0\*;     DestDir: {app}\lib\glib-2.0;     Flags: ignoreversion recursesubdirs createallsubdirs
Source: dist\lib\gtk-2.0\*;      DestDir: {app}\lib\gtk-2.0;      Flags: ignoreversion recursesubdirs createallsubdirs
;Source: dist\lib\gtkglext-1.0\*; DestDir: {app}\lib\gtkglext-1.0; Flags: ignoreversion recursesubdirs createallsubdirs
;Source: dist\lib\libglade\*;     DestDir: {app}\lib\libglade;     Flags: ignoreversion recursesubdirs createallsubdirs
;Source: dist\lib\pango\*;        DestDir: {app}\lib\pango;        Flags: ignoreversion recursesubdirs createallsubdirs
;Source: dist\lib\pkgconfig\*;    DestDir: {app}\lib\pkgconfig;    Flags: ignoreversion recursesubdirs createallsubdirs
; don't use recursion because of components selection (movie plugins, ...)
Source: dist\lib\plugins\*;      DestDir: {app}\lib\plugins;      Flags: ignoreversion
; use recursion, no components
Source: dist\lib\plugins\export\*;     DestDir: {app}\lib\plugins\export;     Flags: ignoreversion recursesubdirs createallsubdirs
Source: dist\lib\plugins\extensions\*; DestDir: {app}\lib\plugins\extensions; Flags: ignoreversion recursesubdirs createallsubdirs
Source: dist\lib\plugins\imp\*;        DestDir: {app}\lib\plugins\imp;        Flags: ignoreversion recursesubdirs createallsubdirs
; component based installation
Source: dist\lib\plugins\movie\PluginMovie7arte.py;         DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\Portuguese\7arte
Source: dist\lib\plugins\movie\PluginMovieAllRovi.py;       DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\English\AllRovi
Source: dist\lib\plugins\movie\PluginMovieAllocine.py;      DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\French\Allocine
Source: dist\lib\plugins\movie\PluginMovieAmazon.py;        DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\Amazon
Source: dist\lib\plugins\movie\PluginMovieAniDB.py;         DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\English\AnimeDB
Source: dist\lib\plugins\movie\PluginMovieCinematografo.py; DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\Italian\Cinematografo
Source: dist\lib\plugins\movie\PluginMovieCineMovies.py;    DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\French\CineMovies
Source: dist\lib\plugins\movie\PluginMovieCineteka.py;      DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\Portuguese\Cineteka
Source: dist\lib\plugins\movie\PluginMovieClubedevideo.py;  DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\Portuguese\Clubedevideo
Source: dist\lib\plugins\movie\PluginMovieCSFD.py;          DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\Czech\CSFD
Source: dist\lib\plugins\movie\PluginMovieCulturalia.py;    DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\Spanish\Culturalia
Source: dist\lib\plugins\movie\PluginMovieDVDEmpire.py;     DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\English\DVD_Empire
Source: dist\lib\plugins\movie\PluginMovieDVDPalace.py;     DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\German\DVD_Palace
Source: dist\lib\plugins\movie\PluginMovieE-Pipoca.py;      DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\Brazilian_Portuguese\E_Pipoca
Source: dist\lib\plugins\movie\PluginMovieFDb.py;           DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\Polish\FDb
Source: dist\lib\plugins\movie\PluginMovieFilmAffinity.py;  DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\Spanish\FilmAffinity
Source: dist\lib\plugins\movie\PluginMovieFilmDb.py;        DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\German\FilmDb
Source: dist\lib\plugins\movie\PluginMovieFilmeVonAZ.py;    DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\German\Filme_von_A_bis_Z
Source: dist\lib\plugins\movie\PluginMovieFilmtipset.py;    DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\Swedish\Film_tip_set
Source: dist\lib\plugins\movie\PluginMovieFilmweb.py;       DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\Polish\Filmweb
Source: dist\lib\plugins\movie\PluginMovieHKMDB.py;         DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\English\HKMDB
Source: dist\lib\plugins\movie\PluginMovieIMDB.py;          DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\IMDB
Source: dist\lib\plugins\movie\PluginMovieIMDB-de.py;       DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\German\IMDBde
Source: dist\lib\plugins\movie\PluginMovieIMDB-es.py;       DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\Spanish\IMDB_es
Source: dist\lib\plugins\movie\PluginMovieKinoDe.py;        DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\German\Kinode
Source: dist\lib\plugins\movie\PluginMovieMediadis.py;      DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\English\Mediadis
Source: dist\lib\plugins\movie\PluginMovieMoviefone.py;     DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\English\Moviefone
Source: dist\lib\plugins\movie\PluginMovieMovieMeter.py;    DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\Dutch\MovieMeter
Source: dist\lib\plugins\movie\PluginMovieMyMoviesIt.py;    DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\Italian\MyMoviesIt
Source: dist\lib\plugins\movie\PluginMovieOFDb.py;          DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\German\OFDb
Source: dist\lib\plugins\movie\PluginMovieOnet.py;          DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\Polish\Onet
Source: dist\lib\plugins\movie\PluginMoviePTGate.py;        DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\Portuguese\PTGate
Source: dist\lib\plugins\movie\PluginMovieScope.py;         DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\Danish\Scope
Source: dist\lib\plugins\movie\PluginMovieStopklatka.py;    DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\Polish\Stopklatka
Source: dist\lib\plugins\movie\PluginMovieTanukiAnime.py;   DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\Polish\Tanuki_Anime
Source: dist\lib\plugins\movie\PluginMovieWP.py;            DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\Polish\Wirtualna_Polska
Source: dist\lib\plugins\movie\PluginMovieZelluloid.py;     DestDir: {app}\lib\plugins\movie; Flags: ignoreversion; Components: Movie_Import_Plugins\German\Zelluloid

; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: {group}\{cm:LaunchProgram,Griffith};    Filename: {app}\griffith.exe
Name: {group}\{cm:UninstallProgram,Griffith}; Filename: {uninstallexe}
Name: {group}\{cm:ProgramOnTheWeb,Griffith};  Filename: http://www.griffith.cc
Name: {group}\Debug\Griffith Debug Start;     Filename: {app}\griffith.exe;         Parameters: --debug
Name: {group}\Debug\Griffith Log File;        Filename: %APPDATA%\Griffith\griffith.log
Name: {group}\Doc\Griffith Forum;             Filename: http://www.griffith.cc/forum/
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
Type: files; Name: {app}\lib\db\*.pyo
Type: files; Name: {app}\lib\plugins\*.pyo
Type: files; Name: {app}\lib\plugins\export\*.pyo
Type: files; Name: {app}\lib\plugins\extensions\*.pyo
Type: files; Name: {app}\lib\plugins\imp\*.pyo
Type: files; Name: {app}\lib\plugins\movie\*.pyo

[Components]
Name: Griffith;                                      Description: Griffith; Types: custom compact full; Flags: fixed
Name: Movie_Import_Plugins;                          Description: Movie Import Plugins; Types: custom compact full; Flags: fixed
Name: Movie_Import_Plugins\IMDB;                     Description: IMDB Import Plugin; Types: custom compact full; Flags: fixed
Name: Movie_Import_Plugins\Amazon;                   Description: Amazon Import Plugin; Types: full

Name: Movie_Import_Plugins\English;                  Description: English Import Plugins; Types: full
Name: Movie_Import_Plugins\English\AllRovi;          Description: Rovi / www.allrovi.com; Types: full
Name: Movie_Import_Plugins\English\AnimeDB;          Description: AnimeDB / www.anidb.net; Types: full
Name: Movie_Import_Plugins\English\DVD_Empire;       Description: DVD Empire / www.dvdempire.com; Types: full
Name: Movie_Import_Plugins\English\HKMDB;            Description: Hongkong Movie Database / www.hkmdb.com; Types: full
Name: Movie_Import_Plugins\English\Mediadis;         Description: Mediadis / www.mediadis.com; Types: full
Name: Movie_Import_Plugins\English\Moviefone;        Description: Moviefone / www.moviefone.com; Types: full

Name: Movie_Import_Plugins\Danish;                   Description: Danish Import Plugins; Types: full
Name: Movie_Import_Plugins\Danish\Scope;             Description: Scope / www.scope.dk; Types: full

Name: Movie_Import_Plugins\Dutch;                    Description: Dutch Import Plugins; Types: full
Name: Movie_Import_Plugins\Dutch\MovieMeter;         Description: MovieMeter / www.moviemeter.nl; Types: full

Name: Movie_Import_Plugins\Czech;                    Description: Czech Import Plugins; Types: full
Name: Movie_Import_Plugins\Czech\CSFD;               Description: CSFD / www.csfd.cz; Types: full

Name: Movie_Import_Plugins\French;                   Description: French Import Plugins; Types: full
Name: Movie_Import_Plugins\French\Allocine;          Description: Allocine / www.allocine.fr; Types: full
Name: Movie_Import_Plugins\French\CineMovies;        Description: CineMovies / www.cinemovies.fr; Types: full

Name: Movie_Import_Plugins\German;                   Description: German Import Plugins; Types: full
Name: Movie_Import_Plugins\German\DVD_Palace;        Description: DVD-Palace / www.dvd-palace.de; Types: full
Name: Movie_Import_Plugins\German\FilmDb;            Description: FilmDb / www.filmdb.de; Types: full
Name: Movie_Import_Plugins\German\Filme_von_A_bis_Z; Description: Filme von A-Z / www.filmevona-z.de; Types: full
Name: Movie_Import_Plugins\German\IMDBde;            Description: IMDB.de / german.imdb.com; Types: full
Name: Movie_Import_Plugins\German\OFDb;              Description: OFDb / www.ofdb.de; Types: full
Name: Movie_Import_Plugins\German\Kinode;            Description: Kino.de / www.kino.de; Types: full
Name: Movie_Import_Plugins\German\Zelluloid;         Description: Zelluloid / www.zelluloid.de; Types: full

Name: Movie_Import_Plugins\Italian;                  Description: Italian Import Plugins; Types: full
Name: Movie_Import_Plugins\Italian\Cinematografo;    Description: Cinematografo / www.cinematografo.it; Types: full
Name: Movie_Import_Plugins\Italian\MyMoviesIt;       Description: MyMoviesIt / www.mymovies.it; Types: full

Name: Movie_Import_Plugins\Polish;                   Description: Polish Import Plugins; Types: full
Name: Movie_Import_Plugins\Polish\FDb;               Description: FDb / fdb.pl; Types: full
Name: Movie_Import_Plugins\Polish\Filmweb;           Description: Filmweb / www.filmweb.pl; Types: full
Name: Movie_Import_Plugins\Polish\Onet;              Description: Onet / film.onet.pl; Types: full
Name: Movie_Import_Plugins\Polish\Stopklatka;        Description: Stopklatka / www.stopklatka.pl; Types: full
Name: Movie_Import_Plugins\Polish\Tanuki_Anime;      Description: Tanuki Anime / anime.tanuki.pl; Types: full
Name: Movie_Import_Plugins\Polish\Wirtualna_Polska;  Description: Wirtualna Polska / www.film.wp.pl; Types: full

Name: Movie_Import_Plugins\Portuguese;               Description: Portuguese Import Plugins; Types: full
Name: Movie_Import_Plugins\Portuguese\7arte;         Description: 7arte / 7arte.net; Types: full
Name: Movie_Import_Plugins\Portuguese\Cineteka;      Description: Cineteka / cineteka.com; Types: full
Name: Movie_Import_Plugins\Portuguese\Clubedevideo;  Description: Clubedevideo / www.clubedevideo.com; Types: full
Name: Movie_Import_Plugins\Portuguese\PTGate;        Description: PTGate / cinema.ptgate.pt; Types: full

Name: Movie_Import_Plugins\Brazilian_Portuguese;          Description: Brazilian Portuguese Import Plugins; Types: full
Name: Movie_Import_Plugins\Brazilian_Portuguese\E_Pipoca; Description: E-Pipoca / epipoca.uol.com.br; Types: full

Name: Movie_Import_Plugins\Spanish;                  Description: Spanish Import Plugins; Types: full
Name: Movie_Import_Plugins\Spanish\Culturalia;       Description: Culturalia / www.culturalianet.com; Types: full
Name: Movie_Import_Plugins\Spanish\FilmAffinity;     Description: FilmAffinity / www.filmaffinity.com; Types: full
Name: Movie_Import_Plugins\Spanish\IMDB_es;          Description: IMDB.es / spanish.imdb.com; Types: full

Name: Movie_Import_Plugins\Swedish;                  Description: Swedish Import Plugins; Types: full
Name: Movie_Import_Plugins\Swedish\Film_tip_set;     Description: Film tip set / www.filmtipset.se; Types: full

