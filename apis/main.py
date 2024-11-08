from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

@app.route('/top_articles', methods=['GET'])
def top_articles():
    """
    Fetches the top 3 most viewed articles from the engagement database and returns them as JSON.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect('engagement.db')
    c = conn.cursor()
    
    # Retrieve top 3 articles ordered by view count
    c.execute("SELECT title, summary, image_url FROM engagement ORDER BY views DESC LIMIT 3")
    articles_data = c.fetchall()
    # Close the database connection
    conn.close()
    # Transform articles data into a list of dictionaries
    top_articles = []
    for article in articles_data:
        article_dict = {
            "title" :  article[0],
            "summary" : article[1],
            "image_url" : article[2]
        }
        top_articles.append(article_dict)
    
    # Return the list of articles as a JSON response
    return jsonify(top_articles)

if __name__ == "__main__":
    app.run(debug=True)
