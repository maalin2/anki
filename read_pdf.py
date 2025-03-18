import os
from dotenv import load_dotenv
import pymupdf

def ask_gemini():
    ""ask nicely"""
    return 'i dont know'

def read_pdf(doc):
    """read pages as images"""
    paths = []
    
    for i, p in enumerate(doc):
        img = p.get_pixmap()
        # TODO: parameterize folder, path name to organize slide decks 
        path = f'./img/page-{i}.png'
        img.save(path)
        paths.append(path)
        print(f'saved {path}')

    return paths
    
def main():
    # get from .env file
    path = os.environ.get('FILE_PATH')
    key = os.environ.get('GEMINI_KEY')
    pages = []

    doc = pymupdf.open(path)
    pages = read_pdf(doc)
    for p in pages:
        ask_gemini(p)

if __name__ == '__main__':
    load_dotenv()
    main()
