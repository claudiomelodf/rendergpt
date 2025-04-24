import requests
from bs4 import BeautifulSoup
import re

def calcular_pagamentos(valor):
    try:
        valor = float(str(valor).replace("R$", "").replace(".", "").replace(",", ".").strip())
        valor_pix = round(valor * 0.90, 2)
        max_parcelas = min(6, int(valor / 150))
        if max_parcelas < 1:
            return "Não disponível", "Não disponível"
        parcela = round(valor / max_parcelas, 2)
        return f"R$ {valor_pix:,.2f}".replace(".", "#").replace(",", ".").replace("#", ","), f"{max_parcelas}x de R$ {parcela:,.2f}".replace(".", "#").replace(",", ".").replace("#", ",")
    except:
        return "Erro", "Erro"

def extrair_dados_produto(url):
    headers = {
        "User-Agent": "Mozilla/5.0",
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        nome = soup.select_one("h1, .product-name")
        nome = nome.text.strip() if nome else "Produto sem nome"

        preco_normal = "Preço não disponível"
        valor_num = None
        for tag in soup.select("span, div, strong, p"):
            if tag and "R$" in tag.text:
                match = re.search(r'R\$[\s]*[\d.,]+', tag.text)
                if match:
                    preco_normal = match.group(0)
                    valor_num = match.group(0)
                    break

        preco_pix, parcelamento = calcular_pagamentos(valor_num)

        descricao_element = soup.select_one('#descricao, .product-description, .product-tab, #content')
        descricao = descricao_element.get_text(separator="\n", strip=True) if descricao_element else "Sem descrição disponível"

        return {
            "status": "sucesso",
            "nome": nome,
            "preco_normal": preco_normal,
            "preco_pix_calculado": preco_pix,
            "parcelamento_calculado": parcelamento,
            "descricao": descricao,
            "url": url
        }

    except Exception as e:
        return {
            "status": "erro",
            "mensagem": str(e),
            "url": url
        }
