# Teste de Performance 2 (TP2) - FastAPI e LangChain com LLMs

Este repositório contém as aplicações desenvolvidas para o TP2. O objetivo do projeto é demonstrar, de forma prática, como criar APIs simples com **FastAPI** integrando modelos de linguagem (**LLMs**) tanto de forma direta (usando **Hugging Face**) quanto utilizando o framework de orquestração **LangChain**.

---

## 📁 Estrutura de Arquivos do Projeto

```text
tp2_langchain/
├── app_gpt2_parte1.py       # Parte 1 - Questão 1: Geração de texto com GPT-2
├── app_tradutor_parte1.py   # Parte 1 - Questão 2: Tradutor EN -> FR com Hugging Face (MarianMT)
├── app_fake_llm_parte2.py   # Parte 2 - Questão 1: Chatbot simulado com Fake LLM do LangChain
├── app_openai_parte2.py     # Parte 2 - Questão 2: Tradutor EN -> FR com LangChain e API de LLM (Groq)
├── app_hf_parte2.py         # Parte 2 - Questão 3: Tradutor EN -> DE com LangChain e Hugging Face
├── .env                     # Arquivo local com chaves de API (ignorado pelo Git)
├── .gitignore               # Configuração para não subir arquivos sensíveis ou pesados
└── README.md                # Documentação do projeto
```

---

## ⚙️ Pré-requisitos e Instalação

1. **Clone este repositório** ou abra a pasta do projeto no VS Code:
   ```bash
   git clone <URL_DO_SEU_REPOSITORIO>
   cd tp2_langchain
   ```

2. **Crie e ative o ambiente virtual Python**:
   ```bash
   # Criar o ambiente virtual
   python -m venv venv

   # Ativar no Windows (PowerShell):
   .\venv\Scripts\Activate.ps1
   ```

3. **Instale as bibliotecas necessárias**:
   ```bash
   pip install fastapi uvicorn pydantic transformers torch langchain langchain-community langchain-core langchain-groq python-dotenv
   ```

4. **Configuração do arquivo `.env`**:
   Crie um arquivo chamado `.env` na raiz do projeto com a chave da sua API (exemplo gratuito da Groq):
   ```env
   GROQ_API_KEY=sua_chave_aqui
   ```

---

## 🚀 Como Executar cada Aplicação

Para rodar qualquer uma das aplicações, basta abrir o terminal na pasta do projeto e executar o comando do **Uvicorn**. Em seguida, abra o navegador em `http://127.0.0.1:8000/docs` para testar visualmente pela interface automática do Swagger, ou use o Postman/cURL.

---

### 1. Aplicação `app_gpt2_parte1.py` (Parte 1 - Questão 1)
* **Objetivo**: Receber um texto em inglês via requisição HTTP e gerar uma continuação usando o modelo GPT-2 da Hugging Face.
* **Comando para rodar**:
  ```bash
  uvicorn app_gpt2_parte1:app --reload
  ```
* **Endpoint**: `POST /gerar`
* **Exemplo de Envio (JSON)**:
  ```json
  {
    "prompt": "Artificial intelligence is",
    "max_length": 40
  }
  ```
* **Fluxo da Aplicação**:
  ```mermaid
  flowchart LR
      Cliente -->|"POST /gerar"| FastAPI
      FastAPI -->|"Prompt"| HuggingFace_GPT2
      HuggingFace_GPT2 -->|"Texto continuado"| FastAPI
      FastAPI -->|"JSON"| Cliente
  ```

---

### 2. Aplicação `app_tradutor_parte1.py` (Parte 1 - Questão 2)
* **Objetivo**: Traduzir textos de inglês para francês usando o modelo local `Helsinki-NLP/opus-mt-en-fr` diretamente com a biblioteca Transformers.
* **Comando para rodar**:
  ```bash
  uvicorn app_tradutor_parte1:app --reload
  ```
* **Endpoint**: `POST /traduzir`
* **Exemplo de Envio (JSON)**:
  ```json
  {
    "texto": "Hello! I am a data science student."
  }
  ```
* **Fluxo da Aplicação**:
  ```mermaid
  flowchart LR
      Cliente -->|"POST /traduzir"| FastAPI
      FastAPI -->|"Texto EN"| MarianMT_Model
      MarianMT_Model -->|"Texto FR"| FastAPI
      FastAPI -->|"JSON"| Cliente
  ```

---

### 3. Aplicação `app_fake_llm_parte2.py` (Parte 2 - Questão 1)
* **Objetivo**: Simular um chatbot que responde a perguntas usando o `FakeListLLM` do LangChain. Serve para testes rápidos com custo zero de processamento e sem gastar internet ou tokens.
* **Comando para rodar**:
  ```bash
  uvicorn app_fake_llm_parte2:app --reload
  ```
* **Endpoint**: `POST /chat`
* **Exemplo de Envio (JSON)**:
  ```json
  {
    "pergunta": "Como você está?"
  }
  ```
* **Fluxo da Aplicação**:
  ```mermaid
  flowchart LR
      Cliente -->|"POST /chat"| FastAPI
      FastAPI -->|"Pergunta"| LangChain_FakeLLM
      LangChain_FakeLLM -->|"Resposta Simulada"| FastAPI
      FastAPI -->|"JSON"| Cliente
  ```

---

### 4. Aplicação `app_openai_parte2.py` (Parte 2 - Questão 2)
* **Objetivo**: Traduzir textos de inglês para francês integrando o LangChain com uma API de LLM rápida e moderna (usando Groq com modelo da família GPT).
* **Comando para rodar**:
  ```bash
  uvicorn app_openai_parte2:app --reload
  ```
* **Endpoint**: `POST /traduzir`
* **Exemplo de Envio (JSON)**:
  ```json
  {
    "texto": "Data science is transforming industries around the world."
  }
  ```
* **Fluxo da Aplicação**:
  ```mermaid
  flowchart LR
      Cliente -->|"POST /traduzir"| FastAPI
      FastAPI -->|"Cadeia LCEL"| LangChain
      LangChain -->|"Chamada Externa"| Nuvem_API_LLM
      Nuvem_API_LLM -->|"Tradução FR"| LangChain
      LangChain -->|"Texto puro"| FastAPI
      FastAPI -->|"JSON"| Cliente
  ```

---

### 5. Aplicação `app_hf_parte2.py` (Parte 2 - Questão 3)
* **Objetivo**: Traduzir textos de inglês para alemão conectando o modelo da Hugging Face (`Helsinki-NLP/opus-mt-en-de`) dentro de uma classe personalizada de LLM do LangChain.
* **Comando para rodar**:
  ```bash
  uvicorn app_hf_parte2:app --reload
  ```
* **Endpoint**: `POST /traduzir`
* **Exemplo de Envio (JSON)**:
  ```json
  {
    "texto": "Data science and machine learning are essential for the future."
  }
  ```
* **Fluxo da Aplicação**:
  ```mermaid
  flowchart LR
      Cliente -->|"POST /traduzir"| FastAPI
      FastAPI -->|"invoke()"| LangChain_CustomLLM
      LangChain_CustomLLM -->|"Inferência local"| HuggingFace_Helsinki_DE
      HuggingFace_Helsinki_DE -->|"Tradução DE"| LangChain_CustomLLM
      LangChain_CustomLLM -->|"Texto puro"| FastAPI
      FastAPI -->|"JSON"| Cliente
  ```

---

## 📊 Comparativo Teórico Resumido (FastAPI Puro vs. LangChain)

| Critério | FastAPI Puro (Chamada Direta) | LangChain + FastAPI |
| :--- | :--- | :--- |
| **Facilidade de Uso** | Mais simples e direto para tarefas únicas. Poucas dependências. | Exige aprender a estrutura de chains, prompts e parsers. |
| **Desempenho e Latência** | Máxima velocidade e menor consumo de memória intermediária. | Adiciona um pequeno overhead de abstração a cada passo. |
| **Flexibilidade** | Código preso ao modelo específico (precisa mudar lógica para cada LLM). | Muito alta: permite trocar de modelo ou provedor com uma linha de código. |
| **Custo e Escala** | Fixo se rodar localmente (mas exige computadores fortes/GPUs). | Variável se usar APIs em nuvem; muito leve no servidor local. |
| **Onde Aplicar** | Microsserviços específicos focados em desempenho extremo. | Protótipos rápidos, agentes inteligentes e fluxos com vários passos. |

---

## 🔒 Segurança e Boas Práticas

* O arquivo `.env` com as chaves de acesso é mantido exclusivamente no computador local e está listado no `.gitignore` para nunca ser enviado para repositórios públicos.
* Todas as rotas de entrada possuem validação de tipo de dados e geração automática de documentação utilizando esquemas **Pydantic**.

