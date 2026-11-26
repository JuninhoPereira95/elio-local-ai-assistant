
# ==========================================
# MODULO: BUSCA LEXICAL
# ==========================================

# Importa recursos para trabalhar com expressoes regulares
import re


# Lista de palavras pouco relevantes para a busca
stopwords = {
    "a", "o", "as", "os",
    "um", "uma", "uns", "umas",
    "de", "do", "da", "dos", "das",
    "em", "no", "na", "nos", "nas",
    "por", "para", "com",
    "e", "ou",
    "que", "qual", "quais",
    "é", "ser", "são",
    "como", "sobre",
    "podem", "pode",
    "utilizado", "utilizada",
    "utilizados", "utilizadas",
    "será", "serão",
    "qualquer", "também"
}


def extrair_palavras(texto):

    # Converte o texto para letras minusculas
    texto = texto.lower()

    # Extrai palavras, ignorando pontuacoes
    palavras = re.findall(r"\b[\w-]+\b", texto)

    # Remove palavras pouco relevantes
    palavras_filtradas = [
        palavra
        for palavra in palavras
        if palavra not in stopwords
    ]

    return palavras_filtradas


def calcular_relevancia_lexical(pergunta, texto):

    # Extrai as palavras importantes da pergunta
    palavras_pergunta = extrair_palavras(pergunta)

    # Extrai as palavras importantes do trecho
    palavras_texto = extrair_palavras(texto)

    # Verifica se existem palavras para comparar
    if not palavras_pergunta:
        return 0.0

    # Conta quantas palavras da pergunta aparecem no trecho
    palavras_encontradas = [
        palavra
        for palavra in palavras_pergunta
        if palavra in palavras_texto
    ]

    # Calcula a proporcao de palavras encontradas
    relevancia = len(palavras_encontradas) / len(palavras_pergunta)

    return relevancia


def calcular_relevancia_lexical_combinada(pergunta, texto, titulo):

    # Calcula a relevancia lexical do conteudo
    relevancia_conteudo = calcular_relevancia_lexical(
        pergunta,
        texto
    )

    # Calcula a relevancia lexical do titulo
    relevancia_titulo = calcular_relevancia_lexical(
        pergunta,
        titulo
    )

    # Combina as duas pontuacoes
    relevancia = (
        (0.7 * relevancia_conteudo) +
        (0.3 * relevancia_titulo)
    )

    return relevancia


# ==========================================
# TESTE DA RELEVANCIA LEXICAL COMBINADA
# ==========================================

if __name__ == "__main__":

    from documentos import carregar_documentos, dividir_texto

    perguntas = [
        "O que é confidencialidade?",
        "O que é integridade?",
        "O que é disponibilidade?",
        "Quais algoritmos podem ser utilizados para implementá-la?"
    ]

    documentos = carregar_documentos()

    for pergunta in perguntas:

        print(f"\nPergunta: {pergunta}")
        print("Palavras extraídas:", extrair_palavras(pergunta))

        for documento in documentos:

            chunks = dividir_texto(documento["conteudo"])

            for chunk in chunks:

                relevancia = calcular_relevancia_lexical_combinada(
                    pergunta,
                    chunk["conteudo"],
                    chunk["titulo"]
                )

                print(f"\nTitulo: {chunk['titulo']}")
                print(f"Relevancia combinada: {relevancia:.4f}")
