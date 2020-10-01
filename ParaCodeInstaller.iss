#define AppName "ParaCode Shell"
#define AppVersion "1.2.2"
#define AppPublisher "DaRubyMiner360"
#define AppURL "http://darubyminer360.ml/ParaCode/"
#define AppSupportURL "http://darubyminer360.ml/ParaCode/Support"
#define AppUpdatesURL "http://darubyminer360.ml/ParaCode/"
#define AppExeName "ParaCodeShell.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{368D0364-FBAA-45F8-ABF4-1658AE05BEBC}
AppName={#AppName}
AppVersion={#AppVersion}
;AppVerName={#AppName} {#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppSupportURL}
AppUpdatesURL={#AppUpdatesURL}
DefaultDirName={autopf}\{#AppName}
DisableProgramGroupPage=yes
; The [Icons] "quicklaunchicon" entry uses {userappdata} but its [Tasks] entry has a proper IsAdminInstallMode Check.
UsedUserAreasWarning=no
; Remove the following line to run in administrative install mode (install for all users.)
PrivilegesRequired=admin
;PrivilegesRequiredOverridesAllowed=dialog
OutputBaseFilename=ParaCodeInstaller
SetupIconFile=C:\Users\Robert\Desktop\Code\Languages\ParaCode\icon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ChangesAssociations=yes
; Tell Windows Explorer to reload the environment
ChangesEnvironment=yes
ShowLanguageDialog=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "dutch"; MessagesFile: "compiler:Languages\Dutch.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode
Name: "envPath"; Description: "Add to PATH variable"
Name: "paraFileAssociation"; Description: "Associate the .para extension"
Name: "paracodeFileAssociation"; Description: "Associate the .paracode extension"

[Files]
Source: "C:\Users\Robert\Desktop\Code\Languages\ParaCode\dist\ParaCodeShell.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Robert\Desktop\Code\Languages\ParaCode\dist\config.toml"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Robert\Desktop\Code\Languages\ParaCode\icon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\Robert\Desktop\Code\Languages\ParaCode\Examples\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#AppName}"; Filename: "{app}\{#AppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Registry]
Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"

; Add 'Open In ParaCode Shell' menu item to the Shell menu for PDF files:
Root: "HKCR"; Subkey: "SystemFileAssociations\.para\shell\Open In ParaCode Shell"; ValueType: none; ValueName: ""; ValueData: "ParaCode Source File"; Flags: uninsdeletekey
; Specify icon for the menu item:
Root: "HKCR"; Subkey: "SystemFileAssociations\.para\shell\Open In ParaCode Shell"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\icon.ico"; Flags: uninsdeletekey
; Add separator before and after the menu item:
;Root: "HKCR"; Subkey: "SystemFileAssociations\.para\shell\Open In ParaCode Shell"; ValueType: string; ValueName: "SeparatorBefore"; ValueData: ""; Flags: uninsdeletekey
;Root: "HKCR"; Subkey: "SystemFileAssociations\.para\shell\Open In ParaCode Shell"; ValueType: string; ValueName: "SeparatorAfter"; ValueData: ""; Flags: uninsdeletekey
; Define command for the menu item:
Root: "HKCR"; Subkey: "SystemFileAssociations\.para\shell\Open In ParaCode Shell\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#AppExeName}""  ""RUN(%1)"""; Flags: uninsdeletekey


; Add 'Open In ParaCode Shell' menu item to the Shell menu for PDF files:
Root: "HKCR"; Subkey: "SystemFileAssociations\.paracode\shell\Open In ParaCode Shell"; ValueType: none; ValueName: ""; ValueData: "ParaCode Source File"; Flags: uninsdeletekey
; Specify icon for the menu item:
Root: "HKCR"; Subkey: "SystemFileAssociations\.paracode\shell\Open In ParaCode Shell"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\icon.ico"; Flags: uninsdeletekey
; Add separator before and after the menu item:
;Root: "HKCR"; Subkey: "SystemFileAssociations\.paracode\shell\Open In ParaCode Shell"; ValueType: string; ValueName: "SeparatorBefore"; ValueData: ""; Flags: uninsdeletekey
;Root: "HKCR"; Subkey: "SystemFileAssociations\.paracode\shell\Open In ParaCode Shell"; ValueType: string; ValueName: "SeparatorAfter"; ValueData: ""; Flags: uninsdeletekey
; Define command for the menu item:
Root: "HKCR"; Subkey: "SystemFileAssociations\.paracode\shell\Open In ParaCode Shell\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#AppExeName}""  ""RUN(%1)"""; Flags: uninsdeletekey

