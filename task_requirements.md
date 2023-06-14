# Social Media API
## Description:
You are tasked with building a RESTful API for a social media platform. The API should allow users to create profiles, follow other users, create and retrieve posts, manage likes and comments, and perform basic social media actions.

## Requirements:
### User Registration and Authentication:
-[x] Users should be able to register with their email and password to create an account.
-[x] Users should be able to login with their credentials and receive a token for authentication.
-[x] Users should be able to logout and invalidate their token.
### User Profile:
-[x] Users should be able to create and update their profile, including profile picture, bio, and other details.
-[x] Users should be able to retrieve their own profile and view profiles of other users.
-[x] Users should be able to search for users by username or other criteria.
### Follow/Unfollow:
-[x] Users should be able to follow and unfollow other users.
-[x] Users should be able to view the list of users they are following and the list of users following them.
### Post Creation and Retrieval:
-[ ] Users should be able to create new posts with text content and optional media attachments (e.g., images). (Adding images is optional task)
-[ ] Users should be able to retrieve their own posts and posts of users they are following.
-[ ] Users should be able to retrieve posts by hashtags or other criteria.
### Likes and Comments (Optional):
-[ ] Users should be able to like and unlike posts. Users should be able to view the list of posts they have liked. Users should be able to add comments to posts and view comments on posts.

### Schedule Post creation using Celery (Optional):
-[ ] Add possibility to schedule Post creation (you can select the time to create the Post before creating of it).
### API Permissions:
-[ ] Only authenticated users should be able to perform actions such as creating posts, liking posts, and following/unfollowing users.
-[ ] Users should only be able to update and delete their own posts and comments.
-[ ] Users should only be able to update and delete their own profile.
### API Documentation:
-[ ] The API should be well-documented with clear instructions on how to use each endpoint.
-[ ] The documentation should include sample API requests and responses for different endpoints.
### Technical Requirements:
-[ ] Use Django and Django REST framework to build the API.
-[ ] Use token-based authentication for user authentication.
-[ ] Use appropriate serializers for data validation and representation.
-[ ] Use appropriate views and viewsets for handling CRUD operations on models.
-[ ] Use appropriate URL routing for different API endpoints.
-[ ]Use appropriate permissions and authentication classes to implement API permissions.


Follow best practices for RESTful API design and documentation. <br>

Note: You are not required to implement a frontend interface for this task. Focus on building a well-structured and well-documented RESTful API using Django and Django REST framework. This task will test the junior DRF developer's skills in building RESTful APIs, handling authentication and permissions, working with models, serializers, views, and viewsets, and following best practices for API design and documentation.