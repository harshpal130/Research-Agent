from langchain.tools import tool
import requests  # khin online jane ke lay 

from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from rich import print
from dotenv import load_dotenv
load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query:str)->str:
    """search the web for recent and relibale info for the topic. returns title, URl and snippetd"""
    result=tavily.search(query=query , max_results=5)

    out = []

    for r in result['results']:
        out.append(
            f"Title:{r['title']}\nURL:{r['url']}\nSnippet:{['content'][:300]}\r"
        )

    return "\n-------\n".join(out)

# print(web_search.invoke("what is recent news about CJP in india"))

@tool
def scrape_url(url: str)-> str:
    """Scrape and return clean text content from the givin url for deeper reading"""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style" , "nav", "footer"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"    

#print(scrape_url.invoke("https://www.bbc.com/news/articles/cvgqp94ynn0o"))
 