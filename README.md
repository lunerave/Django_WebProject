# Django_instagram
Develop clone Instagram in Python with Django.
This project is done for understanding basic functionalities of Django.
## version
Python : 3.10.11

## DB schema
Feed Table: image, content, email


Reply Table: feed_id, email, reply_content


Like Table: feed_id, email, is_like

Bookmark Table: feed_id, email, is_marked

## How to run
    #가상환경 생성 
    python -m venv venv

    #가상환경 실행
    source ./venv/Scripts/activate
    
    #migrate 명령어로 DB 생성
    python manage.py makemigrations
    python manage.py migrate

    # 필요 package 설치
    pip install -r requirements.txt
    
    #서버 실행
    python manage.py runserver
    
    #브라우져로 접속
    http://127.0.0.1:8000/main/
