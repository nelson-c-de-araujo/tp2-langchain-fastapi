
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(title="TP2 - GPT2")

gerador = pipeline("text-generation", model="gpt2")
print("Modelo carregado com sucesso!")

class RequisicaoEntrada(BaseModel):
    prompt: str
    max_length: int = 50

class RespostaSaida(BaseModel):
    prompt: str
    texto_gerado: str

@app.get("/")
def home():
    return {"mensagem": "API Ok!"}

@app.post("/gerar", response_model=RespostaSaida)
def gerar_texto(dados: RequisicaoEntrada):
    
    resultado = gerador(
        dados.prompt,
        max_length=dados.max_length,
        num_return_sequences=1,
        temperature=1.0,
        pad_token_id=50256
    )

    texto_final = resultado[0]["generated_text"]

    return RespostaSaida(
        prompt=dados.prompt,
        texto_gerado=texto_final
    )

