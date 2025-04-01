# 建立容器
docker-compose -f docker-compose.yaml create

# 設置資料庫
docker-compose run server python manage.py migrate

# 生成靜態檔案
docker-compose run server python manage.py collectstatic

# 設置系統管理者帳號
docker-compose run server python manage.py createsuperuser

# 啟動
docker-compose -f docker-compose.yaml start

# 停止
docker-compose -f docker-compose.yaml stop"# SkTpehFhirPotal" 
