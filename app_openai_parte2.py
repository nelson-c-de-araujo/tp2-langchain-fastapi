import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

app = FastAPI(title="Tradutor com LangChain e OpenAI- TP2")


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0 
)

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "Você é um tradutor profissional. Traduza o texto em inglês fornecido para o francês com precisão. Retorne apenas o texto traduzido, sem explicações adicionais."),
    ("human", "{texto_ingles}")
])

cadeia_traducao = prompt_template | llm | StrOutputParser()

class RequisicaoTraducao(BaseModel):
    texto: str

class RespostaTraducao(BaseModel):
    texto_original: str
    texto_traduzido: str

@app.get("/")
def home():
    return {"mensagem": "API OK!"}

@app.post("/traduzir", response_model=RespostaTraducao)
def traduzir_texto(dados: RequisicaoTraducao):
    if not os.getenv("GROQ_API_KEY"):
        raise HTTPException(
            status_code=500,
            detail="GROQ_API_KEY não foi encontrada no .env."
        )

    try:
        resultado_frances = cadeia_traducao.invoke({"texto_ingles": dados.texto})

        return RespostaTraducao(
            texto_original=dados.texto,
            texto_traduzido=resultado_frances.strip()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao processar a tradução: {str(e)}"
        )
