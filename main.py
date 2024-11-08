import os, json
from helpers import *
from db_conn import *

# Path to the JSON file containing articles
filepath = "articles.json"

def main():
    """
    Main function to automate content processing and posting for new articles.
    
    1. Loads articles from a JSON file.
    2. Checks for new articles not yet processed and stored in the database.
    3. Generates a summary and AI-driven image for each new article.
    4. Posts article data to a mock social media platform.
    5. Stores engagement data in an SQLite database.
    """
    
    # Check if the JSON file with articles exists
    if not os.path.exists(filepath):
        print("Sorry! You don't have any article.")
        return 0
    
    # Open the JSON file and load the articles data
    article_data = {}
    with open(filepath, 'r') as file:
        article_data = json.load(file)
    
    # Retrieve the list of articles
    articles = article_data.get('articles')
    if not articles:
        print("Sorry! You don't have any article.")
        return 0

    # Prepare a list of all article titles, formatted for comparison
    all_articles_title = [str(a['title'].strip().lower()) for a in articles if a.get('title')]
    print(all_articles_title)

    # Establish a database connection
    conn = create_connection()
    c = conn.cursor()

    # Check database for existing articles by title
    c.execute('SELECT title FROM engagement WHERE lower(title) IN ({})'.format(', '.join('?' for _ in all_articles_title)), all_articles_title)
    existing_articles = [row[0] for row in c.fetchall()]

    # Iterate through articles to process new ones
    for article in articles:
        title = article.get('title')
        if title in existing_articles:
            # Skip if the article is already processed
            continue

        print(f"\n\n GENERATE CONTENT FOR ARTICLE - {title} \n")

        # Get the main content of the article for summarization
        content = article.get('content')[0]
        summary = generate_summary(content)

        #extract keyword from atricle's title
        keywords = extract_keywords_nltk(title)

        # Generate image based on keywords in the article's title
        image_url = generate_image_from_keywords(title)
    
        # Prepare the article data for posting and storing
        new_article = {
            "title": title,
            "summary": summary,
            "image_url": image_url,
            "views": 2,
            "shares": 3
        }

        # Simulate posting the article summary to a social media platform
        post_to_social_media(**new_article)
        
        # Store the new article's engagement data in the database
        store_engagement_data(**new_article)


if __name__ == "__main__":
    """
    Entry point for script execution.
    Initializes the database (creating necessary tables if they don't exist)
    and then runs the main function.
    """
    initialize_db()  # For creating the database and table named 'engagement'
    main()
