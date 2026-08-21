@echo off
chcp 65001 >nul

title AI SPORT CONSULTANT - VK BOT

cd /d C:\sport-selector-ai-vk\sport-selector-ai-vk

echo ============================================
echo       AI SPORT CONSULTANT
echo       VK + GIGACHAT
echo ============================================
echo.
echo Папка проекта:
echo %CD%
echo.

echo Активация виртуального окружения...
call .venv\Scripts\activate.bat

if errorlevel 1 (
    echo.
    echo ОШИБКА: не удалось активировать .venv
    pause
    exit /b 1
)

echo.
echo Виртуальное окружение активировано.
echo.
echo Запуск VK-бота...
echo.

python vk_bot.py

echo.
echo ============================================
echo БОТ ОСТАНОВЛЕН
echo ============================================
if errorlevel 1 pause