@echo off
SETLOCAL EnableDelayedExpansion

REM Terminate NinjaView.exe process if running
taskkill /IM "NinjaView.exe" /F

REM Set variables
SET version_url=https://ninja-view.com/current_version.txt
SET "application_path=%~dp0NinjaView.exe"
SET "temp_download_path=%~dp0NinjaView_new.exe"

REM Check for updates
curl %version_url% -o current_version.txt
SET /p new_version=<current_version.txt
IF NOT EXIST "!application_path!" (
    echo NinjaView is not installed.
    GOTO END
)

REM Extract current version from the executable file name
FOR /F "delims=v tokens=2" %%v in ("%application_path%") do SET "current_version=%%v"

IF "!new_version!" EQU "!current_version!" (
    echo You have the latest version of NinjaView.
    GOTO END
)

REM Download new version
SET download_url=https://ninja-view.com/update/NinjaView_v!new_version!.exe
echo Downloading NinjaView version !new_version!
curl !download_url! -o !temp_download_path!

REM Replace old version
echo Updating NinjaView...
IF EXIST !application_path! (
    DEL !application_path!
)
MOVE /Y !temp_download_path! !application_path!

REM Cleanup
DEL current_version.txt

REM Restart application
START "" "!application_path!"

:END
ENDLOCAL
