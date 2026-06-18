@echo off
setlocal

cd /d "%~dp0"

for /d /r %%D in (__pycache__) do (
    if exist "%%D" rmdir /s /q "%%D"
)

endlocal
