# IMPORTANT

The database might be unavailable due to the limitations of the free plan. \
In such a case, the API will not work and will return a verbose exception. \

# Overview

RESTful API for managing a blogging platform service.  
Provides CRUD operations for managing blog posts.  

The API doesn't implement user authentication, which is why it should communicate with only one client, serving as an internal usage API for another application.

## Technologies Used

Django REST framework was used for:
- Handling requests and responses with the client.
- Saving and retrieving data from the database.
- Connecting to an external database host.

PostgreSQL database from [https://aiven.io](https://aiven.io) was used for storing user posts.

# Starting the Environment

*Note: If the project is hosted on a domain, there's no need to follow the steps below.*

1. Ensure Python 3.13+ is installed.
2. Create a virtual environment, for example, by running `py -m venv venv` in the Command Prompt.
3. Activate the environment.
4. Install dependencies from `requirements.txt`.
5. Create a `.env` file based on the `.env.example` in the `./BloggingPlatform/` directory. (UWAGA: nie można wysłać do repozytorium haseł do stworzenia pliku `.env` z powodu wykrywania przez Git-a hasła do bazy danych, w celu uzyskania haseł proszę o kontakt).
6. Change the Command Prompt's current working directory to the `./BloggingPlatform/` directory.
7. Run `manage.py runserver` and open the browser on the provided host.

# Usage

When the API is hosted, operations can be performed by sending proper requests to the following URLs:

- `/getById/<int:id>`  
  Returns the blog post from the database with the given ID number.  
  ID numbers are provided within the response for the `/post` operation.  
  Requires the `GET` HTTP method.

- `/getByTitle/<str:title>`  
  Returns the blog post based on its title.  
  The title must match the one provided within the `/post` method, but spaces (white characters) should be removed.  
  Requires the `GET` HTTP method.

- `/post`  
  Allows the API user to send a blog post to be saved to the database.  
  The request must contain fields like `title`, `content`, `category` (as strings), and `tags` (as a list of strings).  
  Requires the `POST` HTTP method.

- `/update/<int:id>`  
  Updates the existing blog post with the provided ID using the newly requested field values.  
  The request should contain fields similar to those in the `/post` method.  
  Requires the `PUT` HTTP method.

- `/delete/<int:id>`  
  Deletes the blog post with the provided ID.  
  Requires the `DELETE` HTTP method.

- `/getall`  
  Returns all posts available in the database.  
  Requires the `GET` HTTP method.

- `/getByTag/<str:tag>`  
  Returns all posts that contain the provided tag.  
  Requires the `GET` HTTP method.

# Credits

- Idea: [https://roadmap.sh/projects/blogging-platform-api](https://roadmap.sh/projects/blogging-platform-api)  
- Database Host: [https://aiven.io](https://aiven.io)  
- Code: [https://github.com/piotr-czarnecki07](https://github.com/piotr-czarnecki07)