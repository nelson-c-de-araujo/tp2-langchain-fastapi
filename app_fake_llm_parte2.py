from fastapi import FastAPI
from pydantic import BaseModel
from langchain_community.llms import FakeListLLM

app = FastAPI(title="Chatbot com FakeLLM - TP2")

respostas_simuladas = [
    "Chatbot simulado usando Fake LLM.",
    "Modo de teste!",
    "Essa resposta é simulada.."
]

llm_falso = FakeListLLM(responses=respostas_simuladas)


class MensagemEntrada(BaseModel):
    pergunta: str


class MensagemSaida(BaseModel):
    pergunta: str
    resposta: str


@app.get("/")
def home():
    return {"mensagem": "API Ativa!"}


@app.post("/chat", response_model=MensagemSaida)
def conversar(dados: MensagemEntrada):
    resposta_simulada = llm_falso.invoke(dados.pergunta)

    return MensagemSaida(
        pergunta=dados.pergunta,
        resposta=resposta_simulada
    )

