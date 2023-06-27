# Social Media API

The Social Media API is a RESTful API that allows users to interact with a social media application. 
It provides various endpoints to perform actions such as creating posts, commenting on posts, liking posts, and managing user profiles.

# Features

- User authentication: Users can register, log in, and log out.
- Post management: Users can create posts, view posts, edit posts, and delete posts.
- Commenting: Users can comment on posts and view comments.
- Likes: Users can like posts and view the number of likes on each post.
- User profiles: Users can view and update their profile information, see posts they create, see posts they liked.
- Followers & following: you can follow and unfollow users, see whom you follow & and whom follow you, see quantity of followers
- Defer post creation: you have an opportunity to indicate date and time for defer post creation.

# Technologies Used

- Django: a Python web framework for building the API.
- Django REST framework: a powerful toolkit for building RESTful APIs.
- Token auth: for user authentication and authorization.
- Celery: defer post creation
- Swagger/redoc: this api fully documented in swagger application, so endpoint info fully available there.

# Getting Started

To get started with the Social Media API, follow these steps:

1. Clone the repository:

    ```shell
    git clone https://github.com/phaishuk/Social-media-API
    ```

2. Navigate to the project directory:

    ```shell
    cd Social-media-API
    ```

3. Create a virtual environment:

    ```shell
   python -m venv venv
   ```

4. Activate the virtual environment:

   - For Windows:
   ```shell
   env\Scripts\activate
   ```
   - For MacOS, Unix, Linux:
   ```shell
   source env/bin/activate
   ```

5. Install the required dependencies:
```shell
pip install -r requirements.txt
```

6. Apply database migrations & and prepared data for testing:
```shell
python manage.py migrate
```

### Defer post creation

Using this functionality that's required to have installed **redis server** on your local computer.
Server have to be up on default redis port `redis://localhost:6379` \
Check it out how to configure it here: [Official link on configuration](https://redis.io/docs/getting-started/)
- Open terminal check it works by command `redis-cli ping`. If answer is `PONG` everything works.
- Go to directory where project cloned `cd Social-media-API`
- Start celery worker in terminal by command `celery -A app worker --loglevel=info`

After that actions defer post creation have to work properly.

# API Documentation

The API documentation, including the available endpoints 
and their request/response formats, can be found at http://localhost:8000/api/doc/swagger when the server is running.

