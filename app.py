
import streamlit as st
from perfis import perfis
from base_conhecimento import construir_base_conhecimento
from busca import buscar_trechos
from respostas import eh_pergunta_definicao
from respostas import obter_resposta_direta
from ollama import enviar_mensagem

# Configurações da página
st.set_page_config(
    page_title="Assistente Local",
    page_icon="🤖",
    layout="wide"
)

# Carrega a base de conhecimento e mantém o resultado em cache
@st.cache_resource
def carregar_base():

    return construir_base_conhecimento()

# Carrega a base de conhecimento
with st.spinner("Carregando base de conhecimento..."):

    base = carregar_base()

# Personalização visual da barra lateral
st.markdown(
    """
    <style>
        /* Reduz o espaço superior da barra lateral */
        [data-testid="stSidebar"] .block-container {
            padding-top: 1rem;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Barra lateral
with st.sidebar:

    # Identidade visual do Elio
    st.markdown(
        """
        <div style="margin-bottom: 0px;">
            <h3 style="margin-bottom: 0px;">✨ Elio</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.title("Configurações")

    # Opções disponíveis na interface
    opcoes_perfis = {
        "Geral": "geral",
        "Segurança da Informação": "seguranca",
        "Desenvolvimento de Jogos": "jogos"
    }


    # Seleção do perfil
    perfil_selecionado = st.selectbox(
        "Selecione o perfil:",
        list(opcoes_perfis.keys())
    )
    # Botão para limpar a conversa
    if st.button("Limpar conversa"):

        # Reinicia o histórico
        st.session_state.historico = [
            {
                "role": "assistant",
                "content": "Olá! Sou seu assistente local. Como posso ajudar?"
            }
        ]

        # Limpa os resultados da busca
        st.session_state.resultados_busca = []

        # Atualiza a interface
        st.rerun()


    # Recupera as instruções do perfil selecionado
    instrucao_system = perfis[
        opcoes_perfis[perfil_selecionado]
    ]


# Área principal
st.title("Assistente Local")

st.caption("Seu assistente pessoal com inteligência artificial local.")

st.divider()



# Inicializa o histórico caso ainda não exista
if "historico" not in st.session_state:

    st.session_state.historico = [
        {
            "role": "assistant",
            "content": "Olá! Como posso ajudar você hoje?"
        }
    ]

# Inicializa os resultados da última busca
if "resultados_busca" not in st.session_state:

    st.session_state.resultados_busca = []


# Exibe as mensagens armazenadas no histórico
for mensagem in st.session_state.historico:

    with st.chat_message(mensagem["role"]):

        # Exibe o conteúdo da mensagem
        st.write(mensagem["content"])

        # Verifica se a mensagem possui fontes associadas
        if mensagem.get("fontes"):

            with st.expander("Consultar fontes utilizadas"):

                # Percorre as fontes da resposta
                for fonte in mensagem["fontes"]:

                    st.markdown(f"**Documento:** {fonte['documento']}")

                    st.markdown(f"**Seção:** {fonte['titulo']}")

                    st.write(fonte["texto"])

                    st.divider()
    
# Campo para digitar uma nova pergunta
pergunta = st.chat_input("Digite sua pergunta...")


# Verifica se o usuário enviou uma mensagem
if pergunta:

    # Armazena a pergunta no histórico
    st.session_state.historico.append(
        {
            "role": "user",
            "content": pergunta
        }
    )

    # Verifica se o perfil selecionado é Segurança da Informação
    if perfil_selecionado == "Segurança da Informação":

        # Verifica se a pergunta é de definição
        if eh_pergunta_definicao(pergunta):

            resultados = buscar_trechos(
                pergunta,
                base,
                relevancia_hibrida_minima=0.30
            )

        else:

            resultados = buscar_trechos(pergunta, base)


        # Verifica se a busca encontrou informações relevantes
        if not resultados:

            mensagem = "Não encontrei informações suficientes na base de conhecimento."

        else:

            # Tenta obter uma resposta diretamente do documento
            resposta_direta = obter_resposta_direta(pergunta, resultados)

            if resposta_direta is not None:

                # Utiliza diretamente a definição recuperada
                mensagem = resposta_direta

            else:

                # Inicializa o contexto dos documentos
                contexto = ""

                # Percorre os trechos recuperados
                for resultado in resultados:

                    # Organiza a hierarquia da seção
                    hierarquia = " > ".join(
                        resultado["hierarquia"].values()
                    )

                    # Adiciona os dados ao contexto
                    contexto += f"""
    Documento: {resultado['documento']}

    Hierarquia: {hierarquia}

    Título: {resultado['titulo']}

    Conteúdo:
    {resultado['texto']}
    """

                # Envia a conversa, o perfil e o contexto ao Gemma
                with st.spinner("O assistente está pensando..."):

                    resposta_gemma = enviar_mensagem(
                        st.session_state.historico,
                        instrucao_system,
                        contexto
                    )

                # Verifica se a comunicação foi bem-sucedida
                if resposta_gemma is not None:

                    mensagem = resposta_gemma

                else:

                    mensagem = "Não foi possível obter uma resposta do assistente. Verifique se o Ollama está funcionando."

    else:

        # Outros perfis não utilizam a base RAG
        resultados = []

        # Envia a pergunta diretamente ao Gemma
        with st.spinner("O assistente está pensando..."):

            resposta_gemma = enviar_mensagem(
                st.session_state.historico,
                instrucao_system
            )

        # Verifica se a comunicação foi bem-sucedida
        if resposta_gemma is not None:

            mensagem = resposta_gemma

        else:

            mensagem = "Não foi possível obter uma resposta do assistente. Verifique se o Ollama está funcionando."


    # Armazena os resultados da busca
    st.session_state.resultados_busca = resultados

    # Inicializa a lista de fontes da resposta
    fontes = []

    # Percorre os resultados recuperados pelo RAG
    for resultado in resultados:

        # Armazena somente as informações necessárias
        fontes.append(
            {
                "documento": resultado["documento"],
                "titulo": resultado["titulo"],
                "texto": resultado["texto"]
            }
        )


    # Adiciona a resposta e suas fontes ao histórico
    st.session_state.historico.append(
        {
            "role": "assistant",
            "content": mensagem,
            "fontes": fontes
        }
    )

    # Atualiza a interface
    st.rerun()
