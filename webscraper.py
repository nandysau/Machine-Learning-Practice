# imports

import os
from dotenv import load_dotenv
from scraper import fetch_website_contents
from IPython.display import Markdown, display
from openai import OpenAI
# Load environment variables in a file called .env
from dotenv import load_dotenv
import os

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

# Check the key
if not api_key:
    print("No API key was found - please check your .env file and ensure OPENAI_API_KEY is set.")
elif not api_key.startswith("sk-"):
    print("An API key was found, but it doesn't start with 'sk-'; please check you're using a valid OpenAI key.")
elif api_key.strip() != api_key:
    print("An API key was found, but it looks like it might have leading or trailing spaces - please remove them.")
else:
    print("OpenAI API key found and looks good so far!")
message = "Hello, GPT! This is my first ever message to you! Hi!"

messages = [
    {
        "role": "user",
        "content": message
    }
]
messages
openai = OpenAI()
response = openai.chat.completions.create(
    model="gpt-5-nano",
    messages=messages
)
response.choices[0].message.content 
# Let's try out this utility

ed = fetch_website_contents("https://edwarddonner.com")

print(ed)
# Define our system prompt - you can experiment with this later, changing the last sentence to 'Respond in markdown in Spanish."

system_prompt = """
You are a snarky assistant that analyzes the contents of a website,
and provides a short, snarky, humorous summary, ignoring text that might be navigation related.
Respond in markdown. Do not wrap the markdown in a code block - respond just with the markdown.
"""
# Define our user prompt

user_prompt_prefix = """
Here are the contents of a website.
Provide a short summary of this website.
If it includes news or announcements, then summarize these too.

"""
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What is 2 + 2?"}
]

response = openai.chat.completions.create(model="gpt-4.1-nano", messages=messages)
response.choices[0].message.content
# See how this function creates exactly the format above

def messages_for(website):
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_prefix + website}
    ]
# Try this out, and then try for a few more websites

messages_for(ed)
# And now: call the OpenAI API. You will get very familiar with this!

def summarize(url):
    website = fetch_website_contents(url)
    response = openai.chat.completions.create(
        model = "gpt-4.1-mini",
        messages = messages_for(website)
    )
    return response.choices[0].message.content
summarize("https://edwarddonner.com")
# A function to display this nicely in the output, using markdown

def display_summary(url):
    summary = summarize(url)
    display(Markdown(summary))
display_summary("https://edwarddonner.com")


#define fetch_website_contents here for testing purposes
import requests
from bs4 import BeautifulSoup 
def fetch_website_contents(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup.get_text()
#define selenium version of fetch_website_contents here for testing purposes
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
def fetch_website_contents(url):      
    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    content = driver.page_source
    driver.quit()
    soup = BeautifulSoup(content, 'html.parser')
    return soup.get_text()
