@echo off
setlocal

gcc Code/Main.c
echo Exit error level: %errorlevel%
exit /b %errorlevel%

endlocal
