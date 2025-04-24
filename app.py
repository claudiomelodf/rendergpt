from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from scraper import extrair_dados_produto

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/produto")
def get_produto(url: str = Query(...)):
    return extrair_dados_produto(url)