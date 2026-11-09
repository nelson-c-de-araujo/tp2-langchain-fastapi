from fastapi import FastAPI
from pydantic import BaseModel
from transformers import MarianTokenizer, MarianMTModel

app = FastAPI(title="TP2 - Tradutor Inglês para Francês")
# Na versão nova da transformers precisa usar esse MarianTokenizer. Tive que aprender.
nome_modelo = "Helsinki-NLP/opus-mt-en-fr"
tokenizador = MarianTokenizer.from_pretrained(nome_modelo)
modelo = MarianMTModel.from_pretrained(nome_modelo)

class RequisicaoTraducao(BaseModel):
    texto: str

class RespostaTraducao(BaseModel):
    texto_original: str
    texto_traduzido: str

@app.get("/")
def home():
    return {"mensagem": "API de tradução OK!"}

@app.post("/traduzir", response_model=RespostaTraducao)
def traduzir_texto(dados: RequisicaoTraducao):

    tokens_entrada = tokenizador(dados.texto, return_tensors="pt", padding=True)


    tokens_saida = modelo.generate(**tokens_entrada)


    texto_frances = tokenizador.decode(tokens_saida[0], skip_special_tokens=True)

    return RespostaTraducao(
        texto_original=dados.texto,
        texto_traduzido=texto_frances
    )
