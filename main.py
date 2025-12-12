import os
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = "AIzaSyCuRubXEWJiUHYI4CD6AQ8i3IadlKC1e2M"

# pick nearest chunk


context = chunks[6]

print("context:"), context
# -------- Prompt Template -------- #

prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
Use the context below to answer the question concisely.

Context:
{context}

Question:
{question}

Answer:
    """
)

# -------- Gemini LLM -------- #

gemini = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.0,
    max_output_tokens=12,
)

# -------- LCEL CHAIN -------- #

chain = prompt | gemini

# -------- Run chain -------- #

response = chain.invoke({
    "context": context,
    "question": "who is defeated by chelsea"
})

print(response.content)
