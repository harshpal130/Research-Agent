from langchain.agents import create_agent
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
import os
from dotenv import load_dotenv
load_dotenv()

llm = ChatMistralAI(model="mistral-small-2506", temperature=0.5)

#1st agent 

def build_search_agent():
    return create_agent(
        model= llm,
        tools=[web_search]
    )

#2nd agent

def build_reader_agent():
    return create_agent(
        model= llm,
        tools=[scrape_url]
    )

#writer chain

writer_prompt = ChatPromptTemplate.from_messages([
    ("system","you are expert research writer. write clear, structured and insightful reports."),
    ("human",""" write the deatiled research reporton the topic below.
     topic: {topic} 
     
     Research Gathered:
     {research}

     Structure the prompt as:
     -Introduction
     -key Findings(minimum 3 well explained points)
     -conclusion
     -sources( list all the URL find in the research)

     be deatiled, factual and professional.
     
     """),
])

writer_chain = writer_prompt | llm | StrOutputParser()

#critic chain - koi..bbhi diikat ho toh usko score do aur btao kyakya shi kare(improvement)

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "you are sharp and constructive research critic . Be honest and specific "),
    ("human", """ Review the research  report below and evalute it strictly.
     
     Report:
     {report}

     respond in the exact format:

     Score:X/10

     strengths:
     -.....
     -.....

     Area to imporve:
     -.....
     -.....
    
     one line verdict:
     ...
      """)
])

critic_chain = critic_prompt | llm |StrOutputParser()
