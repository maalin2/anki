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
    prompt = '''
        you are a tutor generating flashcards for your student client. this is an image from a lecture deck.
        i want you to generate flaschards for all relevant facts, any understanding questions.
        if the slide is information heavy focus on recall.
        if the slide is a problem ask the problem.
        if the slide has any images that you might base a question on describe the image. 
        if difficult to describe the image focus on what the question you might want to ask is testing,
        then test with a flashcard in a different way.
        focus on making connections, diagrams. feel free to make ascii diagram-like questions, flowcharts..

        i want you to generate them in the format
        <CARD>
            <QUESTION>...</QUESTION>
            <ANSWER>...</ANSWER>
        </CARD>
        do not say anything else. just output a stream of CARDs
    '''


    response = client.models.generate_content(
        model='gemini-2.0-flash-exp',
        contents=[prompt,
            types.Part(
                inline_data=types.Blob(data=p, mime_type='image/png')
            )
        ]
    )

    print(response.text)
    return response.text

def run_agent(client, pages, key):
    """run queries"""
    stream = []

    for p in pages:
        img = open(p, 'rb').read()
        stream.append(ask_gemini(client, img, key))
        # dont want to get rate limited
        sleep(10) 

    out = ''.join(stream)
    
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
