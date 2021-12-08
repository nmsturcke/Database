# Database

Want to use a SQLite database but keep on forgetting all commands? \
> **I present you with the solution!** \
> This is a database wrapper for SQLite, add the file to your repository and import it in your main file (with `from .database import DataBase`). Feel free to use it in all your projects

This class incorporates the use of asynchronus and non-asynchronus functions, so you can choose which one you prefer depending on the situation.

# How to use it?

> Initiate the `DataBase` class, enter the path to it along with the columns you'd like the database to have.

# Asynchronus functions
> `1.` **async create_table()** - Creates the table, this is called automatically at the initialization of each function \
> `2.` **async find_one()** - Find an object in the database, you must enter a query that the items must have to be selected \
> `3.` **async find_all()** - Select all objects in the database \
> `4.` **async update_one()** - Update an object, enter a query and the new data you want the item in the database to have \
> `5.` **async insert()** - Insert an object into the database \
> `6.` **async delete()** - Delete an object from the database, you must pass a query that items must have in order to be deleted

# Non-asynchronus functions
> `1.` **na_create_table()** - Creates the table, this is called automatically at the initialization of each function \
> `2.` **na_find_one()** - Find an object in the database, you must enter a query that the items must have to be selected \
> `3.` **na_find_all()** - Select all objects in the database \
> `4.` **na_update_one()** - Update an object, enter a query and the new data you want the item in the database to have \
> `5.` **na_insert()** - Insert an object into the database \
> `6.` **na_delete()** - Delete an object from the database, you must pass a query that items must have in order to be deleted

# Disclaimer

I cannot assure this works for you, if you do find any issues or have any requests, please create an Issue and I'll be more than happy to answer!

*I do not have access to anyone's data, and am not responsible of it in case of it being misused, deleted or otherwise*
