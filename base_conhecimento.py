# ==========================================
# MODULO: CONSTRUCAO DA BASE DE CONHECIMENTO
# ==========================================

# Importa as funcoes dos outros modulos
from documentos import carregar_documentos, dividir_texto
from embeddings import gerar_embedding



def construir_base_conhecimento():

    documentos = carregar_documentos()

    base_conhecimento = []

    for documento in documentos:

        chunks = dividir_texto(documento["conteudo"])

        for chunk in chunks:

            # Gera o embedding utilizando somente o conteudo textual
            vetor = gerar_embedding(chunk["conteudo"])

            if vetor is not None:

                base_conhecimento.append({

                    "documento": documento["nome"],
                    "nivel": chunk["nivel"],
                    "titulo": chunk["titulo"],
                    "hierarquia": chunk["hierarquia"],
                    "texto": chunk["conteudo"],
                    "embedding": vetor

                })

    return base_conhecimento

    
if __name__ == "__main__":

    base = construir_base_conhecimento()

    print(f"\nQuantidade de registros: {len(base)}")

    for indice, registro in enumerate(base, start=1):

        print("\n-----------------------------")
        print(f"Registro: {indice}")
        print(f"Documento: {registro['documento']}")
        print(f"Nivel: {registro['nivel']}")
        print(f"Titulo: {registro['titulo']}")
        print(f"Hierarquia: {registro['hierarquia']}")
        print(f"Texto: {registro['texto']}")
        print(f"Dimensao do embedding: {len(registro['embedding'])}")