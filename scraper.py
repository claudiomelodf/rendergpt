import requests
from bs4 import BeautifulSoup
import re

def extrair_dados_produto(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        nome = soup.select_one("h1, .product-name")
        nome = nome.text.strip() if nome else "Produto sem nome"

        preco = "Preço não disponível"
        for tag in soup.select("span, div, strong, p"):
            if tag and "R$" in tag.text:
                match = re.search(r'R\$[\s]*[\d.,]+', tag.text)
                if match:
                    preco = match.group(0)
                    break

        descricao = soup.select_one(".product-description")
        descricao = descricao.text.strip() if descricao else "Sem descrição disponível"

        return {
            "status": "sucesso",
            "nome": nome,
            "preco": preco,
            "descricao": descricao,
            "url": url
        }

    except Exception as e:
        return {
            "status": "erro",
            "mensagem": str(e),
            "url": url
        }