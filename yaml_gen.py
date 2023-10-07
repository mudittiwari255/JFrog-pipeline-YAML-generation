import openai
import os
import joblib
import faiss
from langchain.prompts import PromptTemplate
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryMemory
from templates import template_context

openai_keys = "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"
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = openai_keys

db = joblib.load("jfrog_pipe_vector_db.pkl")

llm = ChatOpenAI(model="gpt-3.5-turbo-0613", temperature = 0)

PROMPT_CONTEXT = PromptTemplate(
        template=template_context, input_variables = ["question", "context"], output_key = "answer"
)

memory = ConversationSummaryMemory(llm = llm, memory_key="chat_history", input_key="question", 
                                  return_messages=True, output_key='answer')


def get_yaml_response(query):
    chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=db.as_retriever(search_kwargs = {"k" : 2}), 
                            chain_type = 'stuff', 
                            memory=memory,
                            return_source_documents=True,
                            verbose=False,
                            combine_docs_chain_kwargs = {"prompt" : PROMPT_CONTEXT})
    memory.clear()
    output = chain({"question" : query})
    return output['answer']

# output = get_yaml_response("how to build docker pipeline")
# print(output)