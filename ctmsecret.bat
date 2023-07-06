@echo off

set sname=%1
set file=%2

rem
rem The ctm cli doesn't return an exit code or error level
rem

FOR /F "usebackq tokens=* delims=" %%i IN (%file%) DO (
    rem echo Secret Value: %%i
    ctm config secret::update %sname% %%i)