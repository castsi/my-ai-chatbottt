import os
from dotenv import load_dotenv
from langchain_community.llms import Tongyi

load_dotenv()

llm = Tongyi(temperature=0.7, model_name="qwen-turbo")

print("AI is thinking...")
response = llm.invoke("Hello! Introduce yourself in English in 2 sentences.")
print("AI says:")
print(response)
