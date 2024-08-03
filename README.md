# Django_familySNS
Develop clone Instagram in Python with Django.
This project is done for understanding basic functionalities of Django and Web develop.

## URL
http://leesns.duckdns.org/main

## Skills
Django, uwsgi, Python, nginx, AWS EC2, SQLite3, MySQL, Docker, github action(CI/CD)

## version
Python : 3.10.11

## DB
SQLite3, MySQL

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
  
#### POST /reply
This endpoint handles to upload reply to the someone's feed. User enters comment in the comment box in each feed.

#### Features

- **Data Extraction**: Extracts feed ID, reply content, and email from the request data.
- **Reply Creation**: Creates a new reply for the specified feed post.

#### Detailed Workflow

1. **Data Extraction**:
    - Retrieves the `feed_id` and `reply_content` from the request data.
    - Retrieves the email from the session data.

2. **Reply Creation**:
    - Creates a new `Reply` object with the specified feed ID, reply content, and email.

3. **Response**:
    - Returns a 200 status response upon successful reply creation.

#### POST /like
This endpoint handles user's like data for each feed. User clicks the favorite button in each feed to like the feed. 

#### Features

- **Data Extraction**: Extracts feed ID and favorite text from the request data.
- **Like Status Determination**: Determines whether to like or unlike the feed post based on the favorite text.
- **Like Toggle**: Toggles the like status for the specified feed post.

#### Detailed Workflow

1. **Data Extraction**:
    - Retrieves the feed_id and favorite_text from the request data.
    - Retrieves the email from the session data.

2. **Like Status Determination**:
    - Sets is_like to True if favorite_text is 'favorite', otherwise sets it to False.

3. **Like Toggle**:
    - Searches for an existing Like object with the specified feed ID and email.
    - If a Like object is found, updates its is_like status.
    - If no Like object is found, creates a new Like object with the specified feed ID, is_like status, and email.
  
4. **Response**:
    - Returns a 200 status response upon successful like toggle.
  
#### POST /bookmark
This endpoint handles user's bookmark data for each feed. User clicks the bookmark button in each feed to save the feed as bookmark. 

#### Features

- **Data Extraction**: Extracts feed ID and bookmark text from the request data.
- **Bookmark Status Determination**: Determines whether to bookmark or un-bookmark the feed post based on the bookmark text.
- **Bookmark Toggle**: Toggles the bookmark status for the specified feed post.

#### Detailed Workflow

1. **Data Extraction**:
    - Retrieves the feed_id and bookmark_text from the request data.
    - Retrieves the email from the session data.

2. **Bookmark Status Determination**:
    - Sets is_makred to True if bookmakr_text is 'bookmark', otherwise sets it to False.

3. **Bookmark Toggle**:
    - Searches for an existing Bookmark object with the specified feed ID and email.
    - If a Bookmark object is found, updates its is_marked status.
    - If no Bookmark object is found, creates a new Bookmark object with the specified feed ID, is_marked status, and email.
  
4. **Response**:
    - Returns a 200 status response upon successful Bookmark toggle.
  
#### POST /delete
This endpoint handles delete function for created feeds. Users delete feeds by hovering the mouse pointer over a post on their profile page and pressing the delete button.

#### Features

- **Feed Deletion**: Deletes a feed post from the database.

#### Detailed Workflow

1. **Feed Deletion**:
    - Retrieves the `feed_id` from the request data.
    - Deletes the feed post with the corresponding `feed_id` from the database using `Feed.objects.filter(id=feed_id).delete()`.

2. **Response**:
    - Returns a 200 status response upon successful deletion of the feed post.

### user

#### GET, POST /join
This endpoint handles user registration, rendering the registration page and processing registration data to create new users.

#### Features

- **Render Registration Page**: Renders the registration page for new users.
- **User Registration**: Processes user registration data and creates a new user.

#### Detailed Workflow

1. **Render Registration Page**:
    - On a `GET` request, renders the `join.html` page.

2. **User Registration**:
    - On a `POST` request:
        - Retrieves the email, nickname, name, and password from the request data.
        - Encrypts the password using Django's `make_password` function.
        - Creates a new `User` object with the provided data and a default profile image.

3. **Response**:
    - Returns a 200 status response upon successful user creation.
  
#### GET, POST /login
This endpoint handles user login, rendering the login page and processing login data to authenticate users.

#### Features

- **Render Login Page**: Renders the login page for users.
- **User Authentication**: Processes login data to authenticate users.

#### Detailed Workflow

1. **Render Login Page**:
    - On a `GET` request, renders the `login.html` page.

2. **User Authentication**:
    - On a `POST` request:
        - Retrieves the email and password from the request data.
        - Searches for a user with the provided email.
        - If no user is found, returns a 400 status response with an error message.
        - Checks the provided password against the stored password.
        - If the password is correct, sets the user email in the session and returns a 200 status response.
        - If the password is incorrect, returns a 400 status response with an error message.

#### GET /logout
This endpoint handles user logout by clearing the session and rendering the login page.

#### Features

- **Session Clearing**: Clears the user session data upon logout.
- **Render Login Page**: Renders the login page after logout.

#### Detailed Workflow

1. **Session Clearing**:
    - Clears all session data using `request.session.flush()`.

2. **Render Login Page**:
    - Renders the `login.html` page to allow users to log in again.
  
#### POST /profile/upload
This endpoint handles the upload of a user's profile picture.

#### Features

- **File Upload**: Receives and saves a profile picture file.
- **Profile Image Update**: Updates the user's profile image path in the database.

#### Detailed Workflow

1. **File Upload**:
    - Retrieves the uploaded file from the request data.
    - Generates a unique name (`uuid_name`) for the file to avoid conflicts.
    - Constructs the save path using the `MEDIA_ROOT` and `uuid_name`.
    - Writes the uploaded file chunks to the specified save path.

2. **Profile Image Update**:
    - Retrieves the user's email from the request data.
    - Finds the corresponding user object in the database based on the email.
    - Updates the `profile_img` field of the user object with the generated `uuid_name`.
    - Saves the updated user object.

3. **Response**:
    - Returns a 200 status response upon successful profile image upload and update.
  
## RoadMap
This section lists possible future works.

### 1. Chat window for users

### 2. Follow user

### 3. User search




