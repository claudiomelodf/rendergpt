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

        preco_normal = "Preço não disponível"
        for tag in soup.select("span, div, strong, p"):
            if tag and "R$" in tag.text:
                match = re.search(r'R\$[\s]*[\d.,]+', tag.text)
                if match:
                    preco_normal = match.group(0)
                    break

        # Preço no Pix
        preco_pix = "Não identificado"
        pix_match = soup.find(string=re.compile("Pix", re.IGNORECASE))
        if pix_match and pix_match.find_parent():
            pix_text = pix_match.find_parent().text
            pix_valor = re.search(r'R\$[\s]*[\d.,]+', pix_text)
            if pix_valor:
                preco_pix = pix_valor.group(0)

        # Parcelamento
        parcelamento = "Não identificado"
        parcela_match = soup.find(string=re.compile(r"\d+x de R\$"))
        if parcela_match:
            parcelamento = parcela_match.strip()

        descricao_element = soup.select_one('#descricao, .product-description, .product-tab, #content')
        descricao = descricao_element.get_text(separator="\n", strip=True) if descricao_element else "Sem descrição disponível"

        return {
            "status": "sucesso",
            "nome": nome,
            "preco_normal": preco_normal,
            "preco_pix": preco_pix,
            "parcelamento": parcelamento,
            "descricao": descricao,
            "url": url
        }

    except Exception as e:
        return {
            "status": "erro",
            "mensagem": str(e),
            "url": url
        }
