# Django_instagram
Develop clone Instagram in Python with Django.
This project is done for understanding basic functionalities of Django.
## version
Python : 3.10.11

## DB schema
Feed Table: ID, profile_image, user_id, image, content


Comment Table: F_ID, User, User_Comment


Favorite Table: F_ID, User, Favorite 

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
