import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from langchain import hub
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)


from tools.tool import get_profile_url_tavily

load_dotenv()

def lookup(name:str)->str:
    llm=ChatOpenAI(temperature=0,model_name='gpt-4o-mini')

    template="""Given the full name {name_of_person} I want you to get me a link to their Linkedin 
    profile page. Your answer should contain only a URL"""

    prompt_template=PromptTemplate(template=template,input_variables=['name_of_person'])

    tools_for_agent=[
        Tool(
            name="Crawl Google 4 linkedin profile page",
            func=get_profile_url_tavily,
            description='useful for when you need to get the Linkedin Page URL'
        )
    ]

    react_prompt=hub.pull('hwchase17/react')
    agent=create_react_agent(llm=llm,tools=tools_for_agent,prompt=react_prompt)
    agent_executor=AgentExecutor(agent=agent,tools=tools_for_agent,verbose=True)

    result=agent_executor.invoke(
        input={'input':prompt_template.format(name_of_person=name)}
    )

    linkedin_profile_url=result['output']

    return linkedin_profile_url


# if __name__ == "__main__":
#     linkedin_url=lookup(name="Vasireddy Bindu Hasitha")
#     print(linkedin_url)
