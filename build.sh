# 要為您的專案部署設定多個命令，Render 將在部署 Django 應用程式期間執行此腳本。
# !/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
