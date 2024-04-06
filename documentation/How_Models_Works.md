
# this is documentation about how my models works AND what is the purpose of each model in my project. 
# also i will explain the relationship between models and how they are connected to each other. 



# explanation : 
models folder [models.py,] [serializers.py] [permissions&groups.py] 
logic folder [users_viewset.py] 



# Understanding the Models and Serializers


# the flow of information is as follows: Request -> URL -> Viewset -> Serializer -> Model -> Serializer -> Viewset -> Response. The permissions are checked at the Viewset level.

let's break down the flow of information in your Django application:

Request: When a client (like a web browser or a mobile app) makes a request to your Django application, it first hits the URLs defined in your urls.py file. This file routes the request to the appropriate viewset in users_viewset.py based on the URL pattern.

Viewset: The viewset in users_viewset.py handles the request. It uses the appropriate serializer to validate the incoming data (for POST, PUT, PATCH requests) or to fetch the data from the database (for GET requests). The viewset also checks the permissions of the user making the request to ensure they are allowed to perform the requested operation.

Serializer: The serializer in serializers.py transforms the data between complex types (like Django model instances) and native Python data types. For incoming data, it validates the data and transforms it into a Django model instance. For outgoing data, it transforms the Django model instance into a Python dictionary that can be easily converted to JSON.

Model: The model in models.py represents the structure of your database tables. When the serializer validates incoming data, it creates or updates an instance of the model. When the serializer is preparing outgoing data, it fetches an instance of the model from the database.

Response: After the viewset has processed the request, it sends a response back to the client. This response is typically a JSON representation of the data, which is created by the serializer.

Permissions: The permissions&groups.py file defines the permissions for different types of users in your application. These permissions are checked by the viewset when processing a request to ensure the user is allowed to perform the requested operation.

## models.py

The `models.py` file contains the data models for our Django application. These models are Python classes that define the structure of our database tables and their relationships.

1. **UserProfile**: This model extends Django's `AbstractUser` model, adding additional fields such as `user_nickname`, `user_lastname`, `user_gender`, etc. It also includes methods for generating a unique nickname, calculating the user's age, and validating that the user is at least 18 years old.

2. **Post**: This model represents a post made by a user. It includes fields for the content of the post, an associated image, the date and time the post was made, and whether the post is private.

3. **Comment**: This model represents a comment made by a user on a post. It includes fields for the content of the comment, the date and time the comment was made, and a reference to the post and user associated with the comment.

4. **Like**: This model represents a like made by a user on a post or a comment. It includes fields for the date and time the like was made, and references to the post, comment, and user associated with the like.

5. **Follow**: This model represents a follow relationship between two users. It includes fields for the date and time the follow was made, and references to the user and follower associated with the follow.

The file also includes Django signals that are triggered when a `Post`, `Like`, `Comment`, or `Follow` instance is created or deleted. These signals update the relevant count fields on the associated `UserProfile` instances.

## serializers.py

The `serializers.py` file contains Django Rest Framework serializers for our data models. These serializers allow us to convert complex data types, like Django models, into Python native data types that can then be easily rendered into JSON, XML, or other content types.

1. **UserProfileSerializers**: This serializer is for the `UserProfile` model. It includes a `get_fields` method that removes certain fields from the serialized data if the user is not a superuser.

2. **PostSerializers**: This serializer is for the `Post` model. It includes all fields in the serialized data.

3. **CommentSerializers**: This serializer is for the `Comment` model. It includes all fields in the serialized data.

4. **LikeSerializers**: This serializer is for the `Like` model. It includes all fields in the serialized data.

5. **FollowSerializers**: This serializer is for the `Follow` model. It includes all fields in the serialized data.

In summary, these serializers allow our Django application to send and receive data in a format that can be easily processed by client-side applications.
 

## users_viewset.py

The `users_viewset.py` file contains Django Rest Framework viewsets for our data models. These viewsets define the view behavior for each model. By using `viewsets.ModelViewSet`, we can automatically generate the CRUD (Create, Read, Update, Delete) operations for each model in the database.

1. **UserProfileViewSet**: This viewset is for the `UserProfile` model. It uses the `UserProfileSerializers` to serialize the data and `UserProfile.objects.all()` as the queryset to fetch all user profiles.

2. **PostViewSet**: This viewset is for the `Post` model. It uses the `PostSerializers` to serialize the data and `Post.objects.all()` as the queryset to fetch all posts.

3. **CommentViewSet**: This viewset is for the `Comment` model. It uses the `CommentSerializers` to serialize the data and `Comment.objects.all()` as the queryset to fetch all comments.

4. **LikeViewSet**: This viewset is for the `Like` model. It uses the `LikeSerializers` to serialize the data and `Like.objects.all()` as the queryset to fetch all likes.

5. **FollowViewSet**: This viewset is for the `Follow` model. It uses the `FollowSerializers` to serialize the data and `Follow.objects.all()` as the queryset to fetch all follows.

## permissions&groups.py

The `permissions&groups.py` file contains a Django signal that is triggered after a database migration. This signal creates three user groups (`user`, `admin`, `staff`) if they do not already exist, and assigns different permissions to each group.

1. **Admin Group**: This group is granted all permissions.

2. **Staff Group**: This group is granted permissions for user and content management. Specifically, it is granted permissions to add, change, delete, and view instances of the `post`, `like`, `comment`, `follow`, `user`, `group`, `content type`, and `response` models.

3. **User Group**: This group is granted permissions for their own content. Specifically, it is granted permissions to add, change, delete, and view instances of the `post`, `like`, `comment`, and `follow` models.

The signal also adds a user with the username 'username' to the `user` group, a user with the username 'admin' to the `admin` group, and a user with the username 'staff' to the `staff` group.

