from dotenv import load_dotenv
load_dotenv()
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import os
import streamlit as st
from urllib.parse import urljoin


gemini_api_key = os.environ.get("GEMINI_API_KEY")  # Retrieve API key from environment variable
genai.configure(api_key=gemini_api_key)
gemini = genai.GenerativeModel('gemini-pro')



def extract_links(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            links = []
            for link in soup.find_all('a'):
                links.append(link.get('href'))
            return links
        else:
            st.error("Error: Failed to fetch the webpage. Status Code:" + str(response.status_code))
            return []
    except Exception as e:
        st.error("Error: " + str(e))
        return []

def extract_images(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            images = []
            for img in soup.find_all('img'):
                src = img.get('src')
                if src:
                    # Convert relative paths to absolute URLs
                    if not src.startswith('http'):
                        src = urljoin(url, src)
                    images.append(src)
            return images
        else:
            st.error("Error: Failed to fetch the webpage. Status Code:" + str(response.status_code))
            return []
    except Exception as e:
        st.error("Error: " + str(e))
        return []

def extract_text(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text("\n", strip=True)  # Extract text and join lines with newline
            return text
        else:
            st.error("Error: Failed to fetch the webpage. Status Code:" + str(response.status_code))
            return ""
    except Exception as e:
        st.error("Error: " + str(e))
        return ""

# def gemini_connect(text, question):
#     try:
#         input = text
#         # prompt = "I am providing you with some text scraped from a website. Answer the question: {question} on the basis of the text i provided you. The text is : {input}"
#         # response = gemini.generate_content(prompt)
#         response = gemini.generate_content("Tell me about geeks for geeks from : {input}")
#         return response.text
#     except Exception as e:
#         st.error("Error: " + str(e))
#         return "Failed to generate response."



st.set_page_config(
    layout='wide',
    page_title="ARE"
)

section = st.sidebar.radio("Select an Option:",["Home","Scrapper", "Reconnaissance"], index=0)

if section == "Home":
    st.title("ARE")
    st.write("Welcome to our project where Reconnaissance is made easier and faster")
    st.write(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Roboto+Mono:ital,wght@0,100..700;1,100..700&display=swap" rel="stylesheet">
        
        <br>
        <br>
        <div style="font-family:'Roboto Mono', sans-serif;">“ The project is still under development phase. As of now, you can use to it to scrape websites and the data you will get will be 'raw' at the moment. We are constantly working to make it better. ”</div>
        """, unsafe_allow_html=True
    )

elif section == "Scrapper":
    st.title("Scraper")
    option =  st.radio("Select any one:",["Image","Text","Hyperlink"])
    if option == "Image":
        # User input for website URL
        website_url = st.text_input("Enter the URL of the website:", "")

        # Button to trigger image extraction
        if st.button("Extract Images"):
            if website_url:
                st.write("Extracting images from:", website_url)
                images = extract_images(website_url)
                if images:
                    st.write("Images found on the webpage:")
                    for img in images:
                        st.image(img)
                else:
                    st.write("No images found on the webpage.")
            else:
                st.warning("Please enter a website URL.")

    elif option == "Text":
        # User input for website URL
        website_url = st.text_input("Enter the URL of the website:", "")

        # Button to trigger text extraction
        if st.button("Extract Text"):
            if website_url:
                st.write("Extracting text from:", website_url)
                extracted_text = extract_text(website_url)
                if extracted_text:
                    st.write("Text found on the webpage:")
                    st.write(extracted_text)
                else:
                    st.write("No text found on the webpage.")
            else:
                st.warning("Please enter a website URL.")


    elif option == "Hyperlink":
         # User input for website URL
        website_url = st.text_input("Enter the URL of the website:", "")

        # Button to trigger hyperlink extraction
        if st.button("Extract Hyperlinks"):
            if website_url:
                st.write("Extracting hyperlinks from:", website_url)
                hyperlinks = extract_links(website_url)
                if hyperlinks:
                    st.write("Hyperlinks found on the webpage:")
                    for link in hyperlinks:
                        st.write(link)
                else:
                    st.write("No hyperlinks found on the webpage.")
            else:
                st.warning("Please enter a website URL.")

elif section == "Reconnaissance":
    st.title ("Reconnaissance")
    st.write ("Hello there, this module will help in scraping the website you need and accessing the information you want from the website without you having to read the entire thing.")

    with st.form("website_question_form"):
        website = st.text_input("Website:")
        question = st.text_input("Ask a question:")
        submit_button = st.form_submit_button("Scrape and Ask")

        if submit_button:
            if website:
                st.write("Extracting text from:", website)
                extracted_text = extract_text(website)
                if extracted_text:
                    st.write("Text Extracted from the webpage:")
                    st.write(extracted_text)
                    if question:
                        st.write("Asking Gemini.....")
                        answer = gemini.generate_content("I am providing you with some text scraped from a website. Answer the question: {question} on the basis of the text i provided you. The text you need to answer from : {extracted_text.text}")
                        # answer = gemini.generate_content("What is crying?")
                        st.write("Gemini's response:")
                        st.write(answer.text)
                    else:
                        st.warning("Please ask a question")
                else:
                    st.warning("No text found on webpage")
            else:
                st.warning("Please enter a website URL")
