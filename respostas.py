def eh_pergunta_definicao(pergunta):

    # Converte a pergunta para letras minusculas
    pergunta = pergunta.lower().strip()

    # Expressoes que indicam uma pergunta de definicao
    indicadores = [
        "o que é ",
        "o que significa ",
        "defina ",
        "conceito de "
    ]

    # Verifica se a pergunta comeca com algum indicador
    for indicador in indicadores:

        if pergunta.startswith(indicador):
            return True

    # Caso nenhum indicador seja encontrado
    return False

# ==========================================
# FUNCAO: IDENTIFICAR O CONCEITO PERGUNTADO
# ==========================================


def identificar_conceitos(pergunta):

    # Converte a pergunta para letras minusculas
    pergunta = pergunta.lower().strip()

    # Lista dos conceitos existentes na base
    conceitos = [
        "confidencialidade",
        "integridade",
        "disponibilidade"
    ]

    # Lista que armazenara os conceitos encontrados
    conceitos_encontrados = []

    # Procura todos os conceitos dentro da pergunta
    for conceito in conceitos:

        if conceito in pergunta:
            conceitos_encontrados.append(conceito)

    # Retorna a lista de conceitos encontrados
    return conceitos_encontrados

# ==========================================
# FUNCAO: OBTER RESPOSTA DIRETA DO DOCUMENTO
# ==========================================


def obter_resposta_direta(pergunta, resultados):

    # Verifica se a pergunta e de definicao
    if not eh_pergunta_definicao(pergunta):
        return None

    # Identifica todos os conceitos perguntados
    conceitos = identificar_conceitos(pergunta)

    # Lista que armazenara as definicoes encontradas
    respostas = []

    # Se nenhum conceito conhecido foi identificado
    if not conceitos:

        # Procura uma secao de conceito geral
        for resultado in resultados:

            titulo = resultado["titulo"].lower()

            if "conceito geral" in titulo:
                return resultado["texto"]

        return None

    # Procura uma secao correspondente a cada conceito
    for conceito in conceitos:

        for resultado in resultados:

            titulo = resultado["titulo"].lower()

            if conceito in titulo:

                respostas.append(resultado["texto"])
                break

    # Verifica se alguma definicao foi encontrada
    if not respostas:
        return None

    # Junta as definicoes encontradas
    return "\n\n".join(respostas)
