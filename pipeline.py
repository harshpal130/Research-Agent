from agent import build_reader_agent, build_search_agent, critic_chain, writer_chain

def run_research_pipeline(topic :str )-> dict:

    state = {}

    #search agent working 
    print("\n"+ " ="*50)
    print("step 1 - search agent is working... ")
    print("="*50)

    search_agent = build_search_agent()
    search_result=search_agent.invoke({
        "messages" :[("user", f"Find recent , reliable and deatiled information about: {topic}")]
    })

    state["search_result"] = search_result['messages'][-1].content

    print("\n search result",state['search_result'])

     #reader  agent working 
    print("\n"+ " ="*50)
    print("step 2 - reader agent is scaraping top resouces... ")
    print("="*50)

    reader_agent = build_reader_agent()

    reader_result = reader_agent.invoke({
        "messages":[("user",
                f"based on the following result about '{topic}', "
                f"pick the most relevent URL and scrape it for deeper content.\n\n"
                f"Search result :\n{state['search_result'][:800]}"
             )]
    })

    state['scraped_content'] = reader_result['messages'][-1].content

    print("\nscraped content \n", state['scraped_content' ])

     #step 3 - writer chain 
    print("\n"+ " ="*50)
    print("step 3 - writer is drafting the report ")
    print("="*50)

    research_combined = (
        f"SEARCH RESULT:\n {state['search_result']}"
        f"DETAILED SCRAPED CONTENT :\n{state['scraped_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic" :topic,
        "research": research_combined
    })

    print("\n Final report \n", state["report"])

     #critic report step 4 
    print("\n"+ " ="*50)
    print("step 4 - critic is reviewing thr report.. ")
    print("="*50)

    state["feedback"]=critic_chain.invoke({
        "report":state["report"]
    })

    print("\n critic report \n", state["feedback"])

    return state

if __name__ == "__main__":
    topic = input("\n enter the research topic:")
    run_research_pipeline(topic)

