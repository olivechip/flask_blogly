# flask_blogly

This application allows the client to create, read, update, and delete users & posts from a local PostgreSQL database using Python, Flask, and SQLAlchemy. Must create a database named "blogly".

- app.py holds all the main application and its functions;
- models.py holds the main 'User', 'Post' models and database functions;
- seed.py holds sample data;
- various html templates use jinja to manipulate and display data from routes/view functions from app.py
