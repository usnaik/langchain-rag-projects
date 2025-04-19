from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
# For LangChain Tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"

## Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond to the user queries in a human style."),
    ("user", "Question{question}"),
])

## Streamlit App Freamework
st.set_page_config(page_title="Chatbot", page_icon=":robot:")
st.title("LangChain Demo Chatbot with OpenAI / Streamlit")
st.subheader("Ask me anything!")
input_text = st.text_input("Search the topic of your interest")

# OpenAI LLM
llm = ChatOpenAI(
    temperature=0,
    model_name="GPT-3.5-turbo",
)

# ## Output Parser
output_parser = StrOutputParser()
chain=prompt | llm | output_parser

if input_text:
    # ## Run the chain
    result = chain.invoke({"question": input_text})
    st.write(result)