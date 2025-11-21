@echo off
color 03
title Epic Gladiators

py game.py

if %errorlevel% neq 0 (
    echo Error occured; press any key to exit.
    pause >nul
)
exit /b %errorlevel%