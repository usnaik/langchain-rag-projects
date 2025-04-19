# LANGSMITH_TRACING=true
# LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
# LANGSMITH_API_KEY="<your-api-key>"
# LANGSMITH_PROJECT="evaluators"
# OPENAI_API_KEY="<your-openai-api-key>"

LANGSMITH_TRACING="true"
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY="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"
OPENAI_API_KEY="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"


from langchain_openai import ChatOpenAI

llm = ChatOpenAI()
llm.invoke("Hello, world!")