from transformers import pipeline
import requests, string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

#Download Library for keyword extraction
nltk.download('punkt')  
nltk.download('stopwords')
nltk.download('punkt_tab')
# End

def generate_summary(text):
    """
    Generates a concise summary for a given text.
    """
    # Initialize the summarizer pipeline
    summarizer = pipeline("summarization")
    # Generate a summary with specified length parameters
    summary = summarizer(text, max_length=50, min_length=25, do_sample=False)
    # Extract and return the summary text
    return summary[0]['summary_text']


def generate_image_from_keywords(keyword):
    """
    Fetches an image URL based on a keyword by querying the Lexica API.
    """   
    # Make a request to Lexica API with the specified keyword
    response = requests.get(f"https://lexica.art/api/v1/search?q={keyword}")
    
    # Parse the JSON response from the API
    response_data = response.json()
    # Default image URL to None in case no images are found
    image_url = None
        # If images are available in the response, retrieve the first image's URL
    if response_data:
        images_data = response_data.get('images', [])
        if images_data:
            image_url = images_data[0].get('src')
    
    return image_url


def post_to_social_media(**article):
    """
    Simulates posting article details to a social media platform by printing them.
    Parameters:
    - article (dict): Article data containing title, summary, image_url, etc.
  
    """
    print("\n\n")
    print(f"Title: {article['title']}\n")  # Display the article title
    print(f"Summary: {article['summary']}\n")  # Display the summary of the article
    print(f"Image URL: {article['image_url']}\n")  # Display the image URL
    print("Link: https://placeholder-url.com")  # Placeholder URL for the article link
    print("\n\n")

def extract_keywords_nltk(title):
    """
        Extract keywords from article's title
    """
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(title)
    keywords = [word for word in words if word.lower() not in stop_words and word not in string.punctuation]
    return keywords

