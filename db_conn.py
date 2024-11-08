import sqlite3

# Database file path
db_file = 'engagement.db'

def create_connection():
    """ 
    Create a database connection to the SQLite database specified by db_file.
    Returns the connection object if successful, or None if there's an error.
    """
    conn = None
    try:
        # Attempt to establish a connection to the SQLite database
        conn = sqlite3.connect(db_file)
        print("Connection established to SQLite database.")
    except sqlite3.Error as e:
        # Handle any SQLite connection errors
        print(f"Error connecting to database: {e}")
    return conn

def initialize_db():
    """
    Initialize the database by creating the necessary table(s).
    Specifically, this function creates the 'engagement' table if it doesn't already exist.
    """
    # Establish a connection to the database
    conn = create_connection()
    # Create a cursor object to execute SQL commands
    c = conn.cursor()
    # Create the 'engagement' table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS engagement 
                 (id INTEGER PRIMARY KEY, title TEXT, summary TEXT, image_url TEXT, views INTEGER, shares INTEGER)''')
    # Commit the changes to the database (to ensure the table is created)
    conn.commit()
    # Close the connection to the database
    conn.close()

def store_engagement_data(**article):
    """
    Store engagement data (title, summary, image_url, views, and shares) for an article
    into the 'engagement' table.
    Keyword arguments:
    - article: A dictionary containing the article details (title, summary, image_url, views, shares)
    """
    # Establish a connection to the database
    conn = create_connection()
    # Create a cursor object to execute SQL commands
    c = conn.cursor()
    # Insert the article data into the 'engagement' table
    c.execute("INSERT INTO engagement (title, summary, image_url, views, shares) VALUES (?, ?, ?, ?, ?)",
              (article['title'], article['summary'], article['image_url'], article['views'], article['shares']))
    # Commit the changes to the database (save the new data)
    conn.commit()
    # Close the connection to the database
    conn.close()
