from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import MarianTokenizer, MarianMTModel
from langchain_core.language_models.llms import LLM
from typing import Optional, List

app = FastAPI(title="Tradutor Alemão TP2")

nome_modelo = "Helsinki-NLP/opus-mt-en-de"
tokenizador = MarianTokenizer.from_pretrained(nome_modelo)
modelo = MarianMTModel.from_pretrained(nome_modelo)


class TradutorHelsinkiLLM(LLM):
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        tokens = tokenizador(prompt, return_tensors="pt", padding=True)
        saida = modelo.generate(**tokens)
        return tokenizador.decode(saida[0], skip_special_tokens=True) 
    #Sem herdar essa classe tava bugando no Transformers 5

    @property
    def _llm_type(self) -> str:
        return "helsinki_marian_mt"

llm_hf = TradutorHelsinkiLLM()

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
    try:
        resultado_alemao = llm_hf.invoke(dados.texto)

        return RespostaTraducao(
            texto_original=dados.texto,
            texto_traduzido=resultado_alemao.strip()
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro ao traduzir: {str(e)}"
        )
