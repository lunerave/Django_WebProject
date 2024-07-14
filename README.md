# Django_instagram
Develop clone Instagram in Python with Django.
This project is done for understanding basic functionalities of Django.
## version
Python : 3.10.11

## DB schema

#### Feed Table 
image, content, email


#### Reply Table 
feed_id, email, reply_content


#### Like Table 
feed_id, email, is_like


#### Bookmark Table
feed_id, email, is_marked


#### User Table
password, profile_img, name, email, nickname

## How to run
    # Create virtual env(가상환경 생성) 
    python -m venv venv

    # Run virtual env(가상환경 실행)
    source ./venv/Scripts/activate
    
    # Create DB by running migrate commands(migrate 명령어로 DB 생성)
    python manage.py makemigrations
    python manage.py migrate

    # Install needed packages(필요 package 설치)
    pip install -r requirements.txt
    
    # Run server(서버 실행)
    python manage.py runserver
    
    # Connect(브라우져로 접속)
    http://127.0.0.1:8000/main/

## Endpoints
This section details the currently existing API endpoints, and their specifications.   
### content
#### GET /main
This endpoint handles the main feed view for logged-in users. It processes user sessions, retrieves feed data, and renders the main feed page with the appropriate context.

#### Features
- **Session Handling**: Checks if the user is logged in via session data.
- **User Validation**: Validates the logged-in user.
- **Feed Retrieval**: Fetches and displays all feed posts, ordered by their ID in descending order.
- **Reply Handling**: Fetches and displays replies to each feed post.
- **Like Count**: Displays the count of likes for each feed post.
- **User Actions**: Indicates whether the current user has liked or bookmarked each feed post.
- **Contextual Rendering**: Prepares and renders the main page with all the gathered information.

#### Detailed Workflow

1. **Session Check**:
    - Retrieves the email from the session.
    - If no email is found, redirects to the login page (`user/login.html`).

2. **User Validation**:
    - Searches for a user with the retrieved email.
    - If no user is found, redirects to the login page (`user/login.html`).

3. **Feed Retrieval**:
    - Fetches all feed objects and orders them by their ID in descending order.

4. **Feed Data Processing**:
    - For each feed:
        - Retrieves the user who created the feed.
        - Fetches all replies associated with the feed.
        - For each reply, retrieves the user who posted it and prepares a list of replies.
        - Counts the number of likes for the feed.
        - Checks if the current user has liked the feed.
        - Checks if the feed is bookmarked by the current user.
        - Appends all this information to a feed list.

5. **Context Preparation**:
    - Prepares the context with the processed feed data and user information.

6. **Render Page**:
    - Renders the `main.html` template with the context data.
  
#### Post /upload
This endpoint handles to upload new feed for logged-in user. User uploads their feed with image and content of the feed.

#### Features

- **File Handling**: Handles file uploads and saves the uploaded file to a specified directory.
- **Data Extraction**: Extracts content and email from the request data.
- **Feed Creation**: Creates a new feed post with the uploaded image and content.

#### Detailed Workflow

1. **File Upload**:
    - Retrieves the file from the request.
    - Generates a unique filename using `uuid4`.
    - Saves the file to the specified path.

2. **Data Extraction**:
    - Retrieves the content from the request data.
    - Retrieves the email from the session data.

3. **Feed Creation**:
    - Creates a new `Feed` object with the uploaded image, content, and email.

4. **Response**:
    - Returns a 200 status response upon successful feed creation.
  

#### GET /profile
This endpoint handles to show user's uploaded posts, favorite posts(Liked), bookmarked posts in user profile page.

#### Features

- **Session Handling**: Checks if the user is logged in via session data.
- **User Validation**: Validates the logged-in user.
- **User Feed Retrieval**: Fetches all posts created by the logged-in user.
- **Liked Feed Retrieval**: Fetches all posts liked by the logged-in user.
- **Bookmarked Feed Retrieval**: Fetches all posts bookmarked by the logged-in user.
- **Contextual Rendering**: Prepares and renders the profile page with all the gathered information.

#### Detailed Workflow

1. **Session Check**:
    - Retrieves the email from the session.
    - If no email is found, redirects to the login page (`user/login.html`).

2. **User Validation**:
    - Searches for a user with the retrieved email.
    - If no user is found, redirects to the login page (`user/login.html`).

3. **Feed Retrieval**:
    - Fetches all posts created by the logged-in user.

4. **Liked Feed Retrieval**:
    - Fetches the IDs of all posts liked by the logged-in user.
    - Retrieves the corresponding feed posts.

5. **Bookmarked Feed Retrieval**:
    - Fetches the IDs of all posts bookmarked by the logged-in user.
    - Retrieves the corresponding feed posts.

6. **Context Preparation**:
    - Prepares the context with the user's posts, liked posts, and bookmarked posts.

7. **Render Page**:
    - Renders the `profile.html` template with the context data.


        
