import asyncio
import base64
import os
import pymupdf
from time import sleep
from dotenv import load_dotenv
from google import genai
from google.genai import types

def read_pdf(doc):
    """read pages as images"""
    paths = []
    
    for i, p in enumerate(doc):
        img = p.get_pixmap()
        # TODO: parameterize folder, path name to organize slide decks 
        path = f'./img/page-{i}.png'
        try:
            img.save(path)
        except Exception as e:
            print(f'error {e}')

        paths.append(path)

    return paths

def ask_gemini(client, p, key):
    """ask nicely"""
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp',
        contents=['whats going on here',
            types.Part(
                inline_data=types.Blob(data=p, mime_type='image/png')
            )
        ]
    )

    print(response.text)

def run_agent(client, pages, key):
    """run queries"""
    for p in pages:
        img = open(p, 'rb').read()
        ask_gemini(client, img, key)

        # dont want to get rate limited
        sleep(2) 
    
def main():
    # .env file
    key = os.environ.get('GEMINI_KEY')
    path = os.environ.get('FILE_PATH')

    doc = pymupdf.open(path)
    pages = read_pdf(doc)

    client = genai.Client(api_key=key)

    run_agent(client, pages, key)

if __name__ == '__main__':
    load_dotenv()
    main()
