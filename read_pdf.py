from langchain_community.document_loaders import PyPDFLoader
import asyncio
from dotenv import load_dotenv
import os

async def main():
    path = os.getenv('FILE_PATH')
    pages = []

    loader = PyPDFLoader(path)
    async for page in loader.alazy_load():
        pages.append(page)

    for page in pages:
        print(page.page_content.strip())

if __name__ == '__main__':
    load_dotenv()
    asyncio.run(main())
