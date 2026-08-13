#define MyAppName "COSMOS Bio CNS"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "Cory Shane Davis / NavisWORLD"
#define MyAppExeName "COSMOS-Bio-CNS.exe"

[Setup]
AppId={{B1B20686-3471-45C4-A22E-17B517925B83}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={localappdata}\Programs\COSMOS Bio CNS
DefaultGroupName=COSMOS Bio CNS
DisableProgramGroupPage=yes
OutputDir=..\..\release
OutputBaseFilename=COSMOS-Bio-CNS-Setup-Windows-x64
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
UninstallDisplayIcon={app}\{#MyAppExeName}

[Files]
Source: "..\..\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\COSMOS Bio CNS"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\COSMOS Bio CNS"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch COSMOS Bio CNS"; Flags: nowait postinstall skipifsilent
