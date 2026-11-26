# ==========================================
# MODULO: LEITURA E PROCESSAMENTO DE DOCUMENTOS
# ==========================================

from pathlib import Path
import re

# ==========================================
# IDENTIFICACAO DE TITULOS MARKDOWN
# ==========================================

def identificar_titulo(linha):

    # Verifica se a linha comeca com um ou mais #
    resultado = re.match(r"^#{1,6}\s+", linha)

    return resultado is not None

# ==========================================
# EXTRACAO DE INFORMACOES DO TITULO
# ==========================================

def extrair_titulo(linha):

    # Identifica o nivel e o texto do titulo
    resultado = re.match(r"^(#{1,6})\s+(.*)", linha)

    if resultado:

        return {
            "nivel": len(resultado.group(1)),
            "titulo": resultado.group(2)
        }

    return None

# ==========================================
# SEPARACAO DO DOCUMENTO EM SECOES
# ==========================================

def separar_secoes(texto):

    secoes = []

    # Guarda os titulos encontrados em cada nivel
    hierarquia_atual = {}

    secao_atual = None
    conteudo_atual = []

    for linha in texto.splitlines():

        titulo = extrair_titulo(linha)

        # Verifica se a linha e um titulo Markdown
        if titulo:

            # Salva a secao anterior antes de iniciar outra
            if secao_atual is not None:

                secao_atual["conteudo"] = "\n".join(conteudo_atual).strip()
                secoes.append(secao_atual)

            nivel = titulo["nivel"]

            # Remove titulos anteriores do mesmo nivel ou inferiores
            hierarquia_atual = {
                chave: valor
                for chave, valor in hierarquia_atual.items()
                if chave < nivel
            }

            # Registra o novo titulo na hierarquia
            hierarquia_atual[nivel] = titulo["titulo"]

            # Cria a nova secao
            secao_atual = {
                "nivel": nivel,
                "titulo": titulo["titulo"],
                "hierarquia": dict(hierarquia_atual)
            }

            conteudo_atual = []

        else:
            conteudo_atual.append(linha)

    # Salva a ultima secao do documento
    if secao_atual is not None:

        secao_atual["conteudo"] = "\n".join(conteudo_atual).strip()
        secoes.append(secao_atual)

    return secoes



# Localiza a pasta onde os documentos estão armazenados
PASTA_DOCUMENTOS = Path(__file__).parent / "Documentos"


def carregar_documentos():

    # Lista que armazenará os documentos encontrados
    documentos = []

    # Procura todos os arquivos TXT na pasta
    arquivos = PASTA_DOCUMENTOS.glob("*.md")

    for arquivo in arquivos:

        try:

            # Abre o arquivo e realiza a leitura do conteúdo
            with open(arquivo, "r", encoding="utf-8") as documento:

                conteudo = documento.read()

            # Armazena o nome e o conteúdo do documento
            documentos.append({
                "nome": arquivo.name,
                "conteudo": conteudo
            })

        except OSError as erro:

            print(f"\nErro ao ler o arquivo {arquivo.name}: {erro}\n")

    # Devolve a lista com os documentos encontrados
    return documentos



def dividir_texto(texto, tamanho_chunk=500, sobreposicao=50):

    # Separa o documento em secoes com hierarquia
    secoes = separar_secoes(texto)

    chunks = []

    for secao in secoes:

        conteudo = secao["conteudo"]

        # Ignora secoes sem conteudo
        if not conteudo:
            continue

        # Se o conteudo couber em um chunk
        if len(conteudo) <= tamanho_chunk:

            chunks.append({
                "nivel": secao["nivel"],
                "titulo": secao["titulo"],
                "hierarquia": secao["hierarquia"],
                "conteudo": conteudo
            })

        else:

            inicio = 0

            while inicio < len(conteudo):

                fim = min(inicio + tamanho_chunk, len(conteudo))

                # Tenta preservar a separacao entre paragrafos
                quebra_paragrafo = conteudo.rfind("\n\n", inicio, fim)

                if quebra_paragrafo > inicio + tamanho_chunk // 2:
                    fim = quebra_paragrafo

                else:

                    # Caso nao encontre paragrafo, procura um espaco
                    quebra_espaco = conteudo.rfind(" ", inicio, fim)

                    if quebra_espaco > inicio:
                        fim = quebra_espaco

                chunk = conteudo[inicio:fim].strip()

                if chunk:

                    chunks.append({
                        "nivel": secao["nivel"],
                        "titulo": secao["titulo"],
                        "hierarquia": secao["hierarquia"],
                        "conteudo": chunk
                    })

                if fim >= len(conteudo):
                    break

                # Calcula o inicio do proximo chunk com sobreposicao
                proximo_inicio = max(inicio + 1, fim - sobreposicao)

                while proximo_inicio < len(conteudo) and not conteudo[proximo_inicio].isspace():
                    proximo_inicio += 1

                while proximo_inicio < len(conteudo) and conteudo[proximo_inicio].isspace():
                    proximo_inicio += 1

                inicio = proximo_inicio

    return chunks


if __name__ == "__main__":

    documentos = carregar_documentos()      

    for documento in documentos:

        chunks = dividir_texto(documento["conteudo"])

        print(f"\nDocumento: {documento['nome']}")
        print(f"Quantidade de chunks: {len(chunks)}")

        for indice, chunk in enumerate(chunks, start=1):

            print("\n-----------------------------")
            print(f"Chunk: {indice}")
            print(f"Nivel: {chunk['nivel']}")
            print(f"Titulo: {chunk['titulo']}")
            print(f"Hierarquia: {chunk['hierarquia']}")
            print(f"Conteudo: {chunk['conteudo']}")