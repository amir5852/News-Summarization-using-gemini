import requests
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()

# API key from the .env file
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
API_KEY = os.getenv('GENAI_API_KEY')

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(model_name="gemini-1.0-pro")

def summarize_text(text):
    response = model.generate_content(f'Please summarise this document: {text}')
    return response

def get_news(topic):
    try:
        url = f"https://newsapi.org/v2/everything?q={topic}&sortBy=publishedAt&apiKey={NEWS_API_KEY}&language=en"
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data['articles'][:10]
    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        st.error(f"An error occurred: {err}")

# Define the Streamlit application with improved UI
def app():
    st.title('News App')

    # Create a select box for the user to choose the mode
    mode = st.selectbox('Choose your option', ['Select Topic', 'Search Topic'])

    # If the user wants to select a topic from a list
    if mode == 'Select Topic':
        av_topics = ['Choose Topic', 'WORLD', 'NATION', 'BUSINESS', 'TECHNOLOGY', 'ENTERTAINMENT', 'SPORTS', 'SCIENCE', 'HEALTH']
        topic = st.selectbox('Select a topic', av_topics)

        # Check if the user has selected a topic other than 'Choose Topic'
        if topic != 'Choose Topic':
            # Fetch and display the news for the selected topic
            news_list = get_news(topic)
            if news_list:
                # Create two columns and five rows to display news
                for i in range(0, len(news_list), 2):
                    col1, col2 = st.columns(2)
                    with col1:
                        news = news_list[i]
                        if news['urlToImage']:
                            st.image(news['urlToImage'], width=250)
                        else:
                            st.image("image1.png", width=250)

                        st.subheader(news['title'])
                        summary = summarize_text(news['description'])  # Summarize the description
                        st.write(summary.text)
                        st.markdown(f"Read more {news['url']}")
                    if i + 1 < len(news_list):
                        with col2:
                            news = news_list[i + 1]
                            if news['urlToImage']:
                                st.image(news['urlToImage'], width=250)
                            else:
                                st.image("image1.png", width=250)

                            st.subheader(news['title'])
                            summary = summarize_text(news['description'])  # Summarize the description
                            st.write(summary.text)
                            st.markdown(f"Read more {news['url']}")
                    st.markdown("---")

    # If the user wants to search for a specific topic
    elif mode == 'Search Topic':
        st.markdown("### Enter a topic to get the latest news")
        searchTopic = st.text_input('', placeholder='Enter a topic here...')

        if st.button('Get News'):
            # Fetch and display the news for the searched topic
            news_list = get_news(searchTopic)
            if news_list:
                # Create two columns and five rows to display news
                for i in range(0, len(news_list), 2):
                    col1, col2 = st.columns(2)
                    with col1:
                        news = news_list[i]
                        if news['urlToImage']:
                            st.image(news['urlToImage'], width=250)
                        else:
                            st.image("image1.png", width=250)

                        st.subheader(news['title'])
                        summary = summarize_text(news['description'])  # Summarize the description
                        st.write(summary.text)
                        st.markdown(f"Read more {news['url']}")
                    if i + 1 < len(news_list):
                        with col2:
                            news = news_list[i + 1]
                            if news['urlToImage']:
                                st.image(news['urlToImage'], width=250)
                            else:
                                st.image("image1.png", width=250)

                            st.subheader(news['title'])
                            summary = summarize_text(news['description'])  # Summarize the description
                            st.write(summary.text)
                            st.markdown(f"Read more {news['url']}")
                    st.markdown("---")

# Run the Streamlit application
app()
