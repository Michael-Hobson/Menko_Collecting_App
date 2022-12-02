# Checklist

- Create a folder for the project
- Go into project folder
- Open terminal in current folder
- Install dependencies
```
pipenv install flask pymysql flask-bcrypt
```
- Go into the shell
```
pipenv shell
```
`WARNING`: Look for Pipefile and Pipefile.lock

## File Structure (MVC)
    - flask_app (folder)
        - config
            - mysqlconnections.py (file)
        - controllers
            - controller_user.py (file)
        - models
            - model_user.py
        - static
            - CSS
                - style.css
            -js
                = script.js
        - templates
            - index.html
        -__init__
    - pipfile (file)
    - pipfile.lock (file)
    - server.py (file)

## server.py
```py
from flask_app import app
# from flask_app.controllers import controller_user

if __name__ == '__main__':
    app.run(debug=True)
```

## __init__.py
```py
from flask import Flask

app = Flask(__name__)
app.secret_key = "shhhhhh"
```

## mysqlconnections.py
```py
# a cursor is the object we use to interact with the database
import pymysql.cursors
# this class will give us an instance of a connection to our database


class MySQLConnection:
    def __init__(self, db):
        # change the user and password as needed
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='root',
                                     db=db,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor,
                                     autocommit=True)
        # establish the connection to the database
        self.connection = connection
    # the method to query the database

    def query_db(self, query, data=None):
        with self.connection.cursor() as cursor:
            try:
                query = cursor.mogrify(query, data)
                print("Running Query:", query)

                cursor.execute(query, data)
                if query.lower().find("insert") >= 0:
                    # INSERT queries will return the ID NUMBER of the row inserted
                    self.connection.commit()
                    return cursor.lastrowid
                elif query.lower().find("select") >= 0:
                    # SELECT queries will return the data from the database as a LIST OF DICTIONARIES
                    result = cursor.fetchall()
                    return result
                else:
                    # UPDATE and DELETE queries will return nothing
                    self.connection.commit()
            except Exception as e:
                # if the query fails the method will return FALSE
                print("Something went wrong", e)
                return False
            finally:
                # close the connection
                self.connection.close()
# connectToMySQL receives the database we're using and uses it to create an instance of MySQLConnection


def connectToMySQL(db):
    return MySQLConnection(db)

```

## controller_user.py
`remember one controller file for every table in your database
```py
from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_app.models import model_user
from flask_app.models.model_user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Displays the form/template to create a user, registration page
@app.route('/user/new') 
def user_new():
    return render_template('user_new.html')

# The action route that will accept the data from the registration page to create a user
@app.route('/user/create', methods=['POST'])
def user_create():
    return redirect('/')

# A page to show an individual user's information
@app.route('/user/<int:id>')
def user_show(id):
    data = {
        'id': id
    }
    return render_template("show_user.html", user=User.get_one(data))

# Displays the form in which to edit a user
@app.route('/user/<int:id>/edit')
def user_edit():
    return render_template('user_edit.html')

# An update route that updates the edit form
@app.route('/user/<int:id>/update', methods=['POST'])
def user_update():
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "id": id
    }
    User.update_one(data)
    return redirect ('/')

# Delete route
@app.route('/user/<int:id>/delete')
def user_delete():
    data = {
        'id': id
    }
    User.delete(data)
    return redirect('/')

# Restful Routing Achitechture
#     table_name/<int:id>/action
```

## template.html
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- CSS only -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-iYQeCzEYFbKjA/T2uDLTpkwGzCiq6soy8tYaI1GyVh/UjpbCx/TYkiZhlZB6+fzT" crossorigin="anonymous">
    <!--My CSS-->
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    <title>Document</title>
</head>
<body>
    <div class="container">

    </div>


    <!-- JavaScript Bundle with Popper -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/js/bootstrap.bundle.min.js"
        integrity="sha384-u1OknCvxWvY5kfmNBILK2hRnQC3Pr17a+RTT6rIHI7NnikvbZlHgTPOOmMi466C8"
        crossorigin="anonymous"></script>

    <!--My JS-->
    <script src="{{ url_for('static', filename='js/script.css') }}"></script>
</body>
</html>
```

## models.py
``remember one model file for every table in your database
```py
from flask_app.config.mysqlconnections import connectToMySQL
from flask import flash
import re
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_registration(data):
        is_valid = True
        if len(data['first_name']) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if not str.isalpha(data['first_name']):
            flash("First name can only contain letters.")
            is_valid = False
        if len(data['last_name']) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        if not str.isalpha(data['last_name']):
            flash("First name can only contain letters.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address!")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if data['confirm_password'] != data["password"]:
            flash("Password did not match confirm password.")
            is_valid = False
        return is_valid

        #C
    @classmethod
    def create(cls, data):
        query = "INSERT INTO users ( first_name , last_name , email , created_at, updated_at ) VALUES ( %(first_name)s , %(last_name)s , %(email)s , NOW() , NOW() );"
        return connectToMySQL('users').query_db(query, data)

        #R
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('users').query_db(query, data)
        return cls(result[0])

    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM users;"
        results = connectToMySQL('users').query_db(query)
        users = []
        for user in results:
            users.append(cls(user))
        return users

        #U
    @classmethod
    def update_one(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, updated_at = now() WHERE id = %(id)s;"
        return connectToMySQL('users').query_db(query, data)

    @classmethod
    def update_all(cls, data):
        pass

        #D
    @classmethod
    def delete_one(cls, data):
        query = "DELETE from users WHERE id = %(id)s;"
        return connectToMySQL('users').query_db(query, data)
```

```css
/* CSS reset */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Fixed width container class that will "auto-center" itself */
.container {
    width: 1200px;
    margin: 0 auto;
}

/* // long, rounded search button// */
#button1 {
    background-color: whitesmoke;
    color: green;
    border-radius: 25px;
    border: 2px solid green;
    width: 150px;
    height: 30px;
    text-align: center;
}

/* //circular plus button// */
#button2 {
    background-color: rgb(98, 176, 50);
    color: white;
    border: 0px;
    font-size: 25pt;
    width: 40px;
    height: 40px;
    border-radius: 50%;
}

/* //shadow box rectangular button// */
#button3 {
    background-color: rgb(0, 132, 255);
    color: white;
    font-size: 15pt;
    width: 200px;
    height: 50px;
    box-shadow: 5px 5px black;
}

/* //flex row and col from flex-ible columns assignment// */
.row {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.col {
    flex: 1;
    padding: 20px;
    margin: 20px;
    background-color: aquamarine;
}

/* //classes and ids from flexnav assignment// */
.nav {
    background-color: gray;
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.nav-title {
    color: white;
    padding-left: 20px;
}

.nav-links {
    margin: 20px;
    display: flex;
    text-decoration: none;
    color: white;
    list-style-type: none;
}

a {
    padding: 30px;
    text-decoration: none;
    color: white;
}

.active {
    font-weight: bold;
}

.btn {
    background-color: rgb(0, 132, 255);
    color: white;
    box-shadow: 2px 2px black;
}

/* //End of flexnav classes// */
```

```html
`` Form with flash messages and bootstrap styling
        <div class="card text-white bg-primary" id="box1">
            <div class="card-header">Register</div>
            <div class="card-body">
                {% with messages = get_flashed_messages() %}
                    {% if messages %}
                        {% for message in messages %}
                        <p>{{message}}</p>
                        {% endfor %}
                    {% endif %}
                {% endwith %}
                <form action="/user/create" method="post">
                <label for="first_name">First Name:</label>
                <input type="text" name="first_name">
                <label for="last_name">Last Name:</label>
                <input type="text" name="last_name">
                <label for="email">Email:</label>
                <input type="text" name="email">
                <label for="password">Password:</label>
                <input type="text" name="password">
                <label for="confirm password">Confirm Password:</label>
                <input type="text" name="confirm_password">
                <input type="submit" value="Register" id="btn">
                </form>
            </div>
        </div>

``Table template with jinja
    <h1 class="h1">{{ dojo.name }} Ninjas</h1>
    <div class="container">
        <table class="table table-striped">
            <thead>
                <tr>
                    <th scope="col">First Name</th>
                    <th scope="col">Last Name</th>
                    <th scope="col">Age</th>
                </tr>
            </thead>
            <tbody>
                {% for ninja in dojo.nin_list %}
                <tr>
                    <td>{{ ninja.first_name }}</td>
                    <td>{{ ninja.last_name }}</td>
                    <td>{{ ninja.age }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
    <br>
    <a href="/dojos">Home</a>
```