# ==========================================
# MODULO: GERACAO DE EMBEDDINGS
# ==========================================

import requests

# Importa as configurações do projeto
from config import URL_EMBEDDING, MODELO_EMBEDDING, TIMEOUT_OLLAMA


def gerar_embedding(texto):

    # Monta os dados que serão enviados ao Ollama
    dados = {
        "model": MODELO_EMBEDDING,
        "input": texto
    }

    try:

        # Envia o texto para o modelo de embeddings
        resposta = requests.post(
            URL_EMBEDDING,
            json=dados,
            timeout=TIMEOUT_OLLAMA
        )

        # Verifica se ocorreu algum erro na requisição
        resposta.raise_for_status()

        # Converte a resposta recebida para JSON
        resultado = resposta.json()

        # Extrai o vetor numérico gerado pelo modelo
        vetor = resultado["embeddings"][0]

        # Devolve o vetor para quem chamou a função
        return vetor

    except requests.exceptions.RequestException as erro:

        print(f"\nErro ao gerar embedding: {erro}\n")
        return None

    except (ValueError, KeyError, IndexError) as erro:

        print(f"\nErro ao interpretar o embedding: {erro}\n")
        return None