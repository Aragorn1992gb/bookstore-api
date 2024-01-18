# Bookstore API
Bookstore API provides APIs for a rudimentary software used to keep track of the stock of a bookstore. 
The main functionality of these APIs provides the possibility to insert books and increase or decrease the quantity of the books. 
When a book's quantity goes to 0, an external service notifies the bookstore owner through a pub/sub system.

## Start the project
To start the project, execute the following command in the main directory of the project:
```
docker-compose up
```
It will creates 5 containers:
- bookstore-api-backend-1: the backend side
- bookstore-api-pgdb-1: the PostgreSQL db
- bookstore-api-mongodb-1: the Mongo db
- bookstore-api-rabbitmq-1: the RabbitMQ
- pgadmin4_container: the pgAdmin to manage PostgreSQL db

During the process, the script `entrypoint.sh` is called, which will:
- Collect static resources for the Django Admin panel
- Apply database migrations to generate the db
- Create a Django superuser that can access the Django Admin console
- Generate groups that provide authorization for the execution of the APIs
- Start the server on port 8000

Note that there might be an issue that lets this file not be read correctly. This issue is caused because on Windows, the break line is CRLF and not LF. This should be fixed by the file `.gitattributes`. If the issue persists, open the file with an IDE like Visual Studio and change the break line with LF, as shown in this image.

[1]
<br>

#### Different environments
The git code follows the GitFlow guidelines. There are 3 main branches:
- **Dev**: used for development
- **Test**: used for test
- **Main**: used for prod

The environment variables for the backend container are placed in three files:
- **.env**: for dev environment
- **.env.test**: for test environment
- **.env.prod**: for prod enviroment

The environment variables for the PostgreSQL database are placed in three files:
- **.env.postgres**: for dev environment
- **.env.postgres.test**: for test environment
- **.env.postgres.prod**: for prod enviroment

Choose the environment properly by changing the env variables in the `docker-compose.yaml` file.

## Initialize the project
The bookstore has 2 authorization groups:
- **STOCK_MANAGER**: associated with the user that can see the books, authors, editors, decrease, increase, or update book quantity
- **ADMIN**: associated with the user that can update or create books, authors, editors

The first thing to do is to access the Django Admin Panel with the credentials:
> user: admin <br>
> passsword: admin

from
> http://localhost:8000/admin/

and create 2 users to be associated with respectively STOCK_MANAGER and ADMIN group:
[2]
[3]
From each of those users generate a token:
[4]
and use this token to authenticate the request.

It is a rudimental software, so the users must be set from the admin, I don't provide APIs for registration.

## Execute the APIs
The APIs are documented in Swagger:
> http://localhost:8000/swagger

First of all, you need to authenticate the requests with the token of one of the 2 users created; it depends on the call that you want to make:
[5]
Then you can execute the APIs, following the Swagger documentation.
## Architecture
The project involves the subsequent technologies:
- Python
- Django-rest framework
- PostgreSQL
- MongoDB
- RabbitMQ
- Swagger
<br>

#### PostgreSQL
PostgreSQL is used to store the details of the Books, Authors, and Editors. This is a rudimental project, so it is enough just to create a field called "quatity" in the book table to keep track of the remaining quantity for each book. Every book has a foreign key to author and editor tables. 
You can analyze the database through PgAdmin:
> http://localhost:5055/browser/ <br>
> user: admin@admin.com <br>
> passsword: root

<br>

#### MongoDB
MongoDB is used for Data Warehouse purposes and to keep notifications "sent" or "to be sent" to the external notification-service.
Quantity of books added or removed is keeped on MongoDB. This choice has been done in order to grant the best condition for Data Warehouse analysis and isolate the data between projects. This project need just to keep track of the book stocked, not sold. I suppose that when the bookstore owner print the receipt, automatically the book is decreased in the "quantity" field of the PostgreSQL book table, no need nothing else. But it is important to keep track of the removed book (that can be removed for different purpose, not only if sold). All of those details are stored in MongoDB and can be integrated with other project/tools.
MongoDB also stores notification "sent" or "not sent" to the notification-service. In this way, if the Pub/Sub engine is not working, the notification is stored as "delivered=no"
The collections are:
- **history_book**: contains details about removed books
- **history_add_book**: contains details about inserted books
- **notification**: contains the notification "published" or "not published" on RabbitMQ, the pub/sub service that interacts with the notification-service.
<br>

#### RabbitMQ
RabbitMQ is used as a pub/sub service for the integration with the notification-service. When a book is out of stock, a message in the queue "book_ooo_notifications" is sent and can be consumed by the notification-service.
You can access to the RabbitMQ console from:
>http://localhost:15672/

#### Test
You can run Unit Tests made on the book app. To run, you should go inside the docker container bookstore-api-backend-1, inside the "bookstore_api" folder and execute:
```
python manage.py test book
```
