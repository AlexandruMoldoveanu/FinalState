@echo off
setlocal
echo Exit error level: %errorlevel%
echo 
gcc Code/Main.c
echo Exit error level: %errorlevel%
exit /b %errorlevel%

endlocal
