import sqlite3


# Initialize the SQLite database and create the 'users' table if it doesn't exist
def initialize_db():
    """Initialize the Users.db database by creating the 'users' table if it doesn't exist.

    This function creates a SQLite database named 'Users.db' and creates a table named
    'users' with columns for the user's name, email, and preferred city. The email column
    is marked as unique to ensure that each user's email is unique.
    """
    # Connect to the database and create a cursor
    conn = sqlite3.connect('Users.db')
    c = conn.cursor()

    # Create the 'users' table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 UserName TEXT, 
                 Mail TEXT UNIQUE, 
                 City TEXT)''')

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


# Subscribe a user by adding them to the database or updating their city
def subscribe(UserName, Mail, City):
    """Subscribe a user by adding them to the database or updating their city.

    This function checks if the user already exists in the database. If the user
    exists, it updates their city. If the user does not exist, it creates a new
    record with the given information.

    Parameters
    ----------
    UserName : str
        The name of the user to subscribe.
    Mail : str
        The email address of the user to subscribe.
    City : str
        The preferred city of the user to subscribe.
    """
    # Connect to the database and create a cursor
    conn = sqlite3.connect('Users.db')
    c = conn.cursor()

    # Check if the user already exists
    c.execute("SELECT * FROM users WHERE Mail = ?", (Mail,))
    existing_user = c.fetchone()

    if existing_user:
        # User exists, update the city
        c.execute("UPDATE users SET City = ? WHERE Mail = ?", (City, Mail))
    else:
        # User does not exist, insert a new record
        c.execute("INSERT INTO users (UserName, Mail, City) VALUES (?, ?, ?)", (UserName, Mail, City))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


# Unsubscribe a user by removing their record from the database
def unsubscribe(Mail):
    """Unsubscribe a user by removing their record from the database.

    This function first checks if the user exists in the database. If the user
    exists, it deletes the record.
    """
    conn = sqlite3.connect('Users.db')
    c = conn.cursor()

    # Check if the user exists
    c.execute("SELECT * FROM users WHERE Mail = ?", (Mail,))
    existing_user = c.fetchone()

    if existing_user:
        # User exists, delete the record
        c.execute("DELETE FROM users WHERE Mail = ?", (Mail,))

    # Commit the changes and close the connection
    conn.commit()
    conn.close()


# Retrieve and return a list of users in a specific city
def get_users_by_city(city):
    """
    Retrieve and return a list of users in a specific city.

    This function takes a city as a parameter and returns a list of tuples,
    where each tuple contains the user's name and email address.

    Parameters
    ----------
    city : str
        The city for which to retrieve users.

    Returns
    -------
    list
        A list of tuples, where each tuple contains the user's name and email
        address.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect('Users.db')
    c = conn.cursor()

    # Fetch users based on the specified city
    c.execute("SELECT UserName, Mail FROM users WHERE City = ?", (city,))
    users = c.fetchall()
    conn.close()

    return users
