
# ==========================================
# MODULO: BUSCA SEMANTICA
# ==========================================

from math import sqrt

# Importa a funcao de geracao de embeddings
from embeddings import gerar_embedding

# Importa a funcao de busca lexical
from busca_lexical import (
    calcular_relevancia_lexical,
    calcular_relevancia_lexical_combinada
)


def calcular_similaridade(vetor_a, vetor_b):

    # Calcula a multiplicacao dos valores correspondentes
    produto_escalar = sum(
        a * b for a, b in zip(vetor_a, vetor_b)
    )

    # Calcula o tamanho de cada vetor
    norma_a = sqrt(sum(a * a for a in vetor_a))
    norma_b = sqrt(sum(b * b for b in vetor_b))

    # Evita divisao por zero
    if norma_a == 0 or norma_b == 0:
        return 0.0

    # Calcula a similaridade de cosseno
    similaridade = produto_escalar / (norma_a * norma_b)

    return similaridade

# ==========================================
# CALCULO DA RELEVANCIA HIBRIDA
# ==========================================

def calcular_relevancia_hibrida(similaridade, relevancia_lexical):

    # Combina as pontuacoes semantica e lexical
    relevancia = (
        (0.7 * similaridade) +
        (0.3 * relevancia_lexical)
    )

    return relevancia


def expandir_contexto_hierarquico(resultados, base_conhecimento):

    resultados_expandidos = list(resultados)

    # Guarda os registros que ja foram adicionados
    registros_adicionados = {
        (resultado["documento"], resultado["titulo"])
        for resultado in resultados_expandidos
    }

    # Analisa cada resultado encontrado pela busca
    for resultado in resultados:

        nivel_pai = resultado["nivel"]
        hierarquia_pai = resultado["hierarquia"]

        # Procura secoes descendentes na base de conhecimento
        for registro in base_conhecimento:

            # Verifica se pertence ao mesmo documento
            if registro["documento"] != resultado["documento"]:
                continue

            # Procura somente niveis inferiores ao resultado
            if registro["nivel"] <= nivel_pai:
                continue

            # Verifica se todos os niveis superiores coincidem
            pertence_a_hierarquia = all(
                registro["hierarquia"].get(nivel) == titulo
                for nivel, titulo in hierarquia_pai.items()
            )

            if not pertence_a_hierarquia:
                continue

            identificador = (
                registro["documento"],
                registro["titulo"]
            )

            # Evita adicionar registros duplicados
            if identificador in registros_adicionados:
                continue

            resultados_expandidos.append({

                "documento": registro["documento"],
                "nivel": registro["nivel"],
                "titulo": registro["titulo"],
                "hierarquia": registro["hierarquia"],
                "texto": registro["texto"],

                # Este registro foi recuperado pela hierarquia,
                # e nao diretamente pela pontuacao da busca.
                "similaridade": None,
                "relevancia_lexical": None,
                "relevancia_hibrida": None,

                "expansao_hierarquica": True

            })

            registros_adicionados.add(identificador)

    return resultados_expandidos


def buscar_trechos(pergunta, base_conhecimento, quantidade=3, relevancia_hibrida_minima=0.50):

    vetor_pergunta = gerar_embedding(pergunta)

    if vetor_pergunta is None:
        return []

    resultados = []

    for registro in base_conhecimento:

        vetor_documento = registro["embedding"]

        similaridade = calcular_similaridade(
            vetor_pergunta,
            vetor_documento
        )

        relevancia_lexical_conteudo = calcular_relevancia_lexical(
            pergunta,
            registro["texto"]
        )

        relevancia_lexical = calcular_relevancia_lexical_combinada(
            pergunta,
            registro["texto"],
            registro["titulo"]
        )

        relevancia_hibrida = calcular_relevancia_hibrida(
            similaridade,
            relevancia_lexical
        )

        relevancia_lexical_titulo = calcular_relevancia_lexical(
            pergunta,
            registro["titulo"]
        )

        print(f"\nTitulo analisado: {registro['titulo']}")
        print(f"Lexical do conteudo: {relevancia_lexical_conteudo:.4f}")
        print(f"Lexical do titulo: {relevancia_lexical_titulo:.4f}")
        print(f"Lexical combinada: {relevancia_lexical:.4f}")

        resultados.append({

            # Metadados do documento
            "documento": registro["documento"],
            "nivel": registro["nivel"],
            "titulo": registro["titulo"],
            "hierarquia": registro["hierarquia"],

            # Conteudo recuperado
            "texto": registro["texto"],

            # Pontuacoes da busca
            "similaridade": similaridade,
            "relevancia_lexical": relevancia_lexical,
            "relevancia_hibrida": relevancia_hibrida

        })

    # Ordena os resultados pela relevancia hibrida
    resultados.sort(
        key=lambda resultado: resultado["relevancia_hibrida"],
        reverse=True
    )

    print("\n--- PONTUACOES BRUTAS DA BUSCA ---")

    for resultado in resultados:

        print(
            f"Titulo: {resultado['titulo']} | "
            f"Semantica: {resultado['similaridade']:.4f} | "
            f"Lexical: {resultado['relevancia_lexical']:.4f} | "
            f"Hibrida: {resultado['relevancia_hibrida']:.4f}"
        )

    # Filtra os resultados pelo limite minimo
    resultados_relevantes = [
        resultado
        for resultado in resultados
        if resultado["relevancia_hibrida"] >= relevancia_hibrida_minima
    ]

    # Seleciona os melhores resultados da busca hibrida
    melhores_resultados = resultados_relevantes[:quantidade]

    # Expande o contexto utilizando a hierarquia dos documentos
    resultados_expandidos = expandir_contexto_hierarquico(
        melhores_resultados,
        base_conhecimento
    )   

    return resultados_expandidos

if __name__ == "__main__":

    from base_conhecimento import construir_base_conhecimento

    base = construir_base_conhecimento()

    pergunta = "O que é confidencialidade?"

    resultados = buscar_trechos(
        pergunta,
        base,
        quantidade=2
    )

    print("\n--- RESULTADOS DA BUSCA EXPANDIDA ---")

    for resultado in resultados:

        print("\n-----------------------------")
        print(f"Titulo: {resultado['titulo']}")
        print(f"Nivel: {resultado['nivel']}")
        print(f"Hierarquia: {resultado['hierarquia']}")
        print(f"Texto: {resultado['texto']}")

        if resultado.get("expansao_hierarquica"):
            print("Origem: Expansao hierarquica")
        else:
            print("Origem: Busca hibrida")
            print(f"Similaridade: {resultado['similaridade']:.4f}")
            print(f"Lexical: {resultado['relevancia_lexical']:.4f}")
            print(f"Hibrida: {resultado['relevancia_hibrida']:.4f}")