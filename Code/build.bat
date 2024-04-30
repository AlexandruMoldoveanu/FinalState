@echo off
setlocal

gcc Main.c
echo Exit error level: %errorlevel%
exit /b %errorlevel%

endlocal