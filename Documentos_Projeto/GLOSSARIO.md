# Glossário

Este glossário reúne conceitos técnicos utilizados no desenvolvimento do Elio, um assistente de IA local baseado em Python, Ollama, Streamlit e RAG.

Cada entrada apresenta o significado do termo, uma explicação em linguagem simples e sua aplicação prática no projeto.

## Como este glossário será organizado

Cada termo deverá conter, sempre que possível:

1.  **Significado:** definição técnica.
2.  **Em palavras simples:** explicação acessível ou analogia.
3.  **No projeto:** onde o conceito aparece e qual é sua função.

A ideia não é reunir definições soltas copiadas de outras fontes, mas
explicar os conceitos que realmente encontramos e utilizamos durante a
construção do assistente.

------------------------------------------------------------------------

## 1. RAG --- Retrieval-Augmented Generation

**Significado:** técnica que combina a recuperação de informações em uma
fonte externa com a geração de texto por um modelo de linguagem.

**Em palavras simples:** antes de responder, o assistente procura
informações em documentos de referência. Depois, envia os trechos
encontrados ao modelo para ajudar a formular a resposta.

**No projeto:** o assistente procura trechos nos arquivos da pasta
`documentos/` e utiliza os resultados como contexto para a Gemma. Para
algumas definições simples, o Python retorna diretamente o texto do
documento.

## 2. LLM --- Large Language Model

**Significado:** modelo de linguagem de grande porte, treinado para
processar e gerar texto.

**Em palavras simples:** é o modelo de IA que interpreta mensagens e
produz respostas em linguagem natural.

**No projeto:** utilizamos a Gemma 3 1B por meio do Ollama para gerar
respostas que exigem elaboração, síntese ou interpretação.

## 3. Embedding

**Significado:** representação numérica de um texto em forma de vetor,
construída de modo que relações de significado possam ser comparadas
matematicamente.

**Em palavras simples:** é uma maneira de transformar texto em números
para que o programa consiga comparar o significado aproximado de
perguntas e trechos.

**No projeto:** o modelo `nomic-embed-text` gera embeddings para os
trechos dos documentos e para as perguntas. Os vetores são utilizados na
busca semântica.

## 4. Busca semântica

**Significado:** método de recuperação que compara representações
vetoriais para encontrar conteúdos semanticamente relacionados, mesmo
quando as palavras utilizadas são diferentes.

**Em palavras simples:** tenta encontrar trechos que tratam da mesma
ideia, não apenas trechos que repetem as palavras da pergunta.

**No projeto:** a busca semântica compara o embedding da pergunta com os
embeddings dos trechos da base de conhecimento.

## 5. Busca lexical

**Significado:** método de recuperação baseado na correspondência entre
palavras ou termos presentes na consulta e no conteúdo pesquisado.

**Em palavras simples:** verifica se as palavras importantes da pergunta
aparecem no trecho ou no título da seção.

**No projeto:** o módulo `busca_lexical.py` extrai palavras da pergunta
e calcula uma pontuação de correspondência com o conteúdo e o título dos
trechos.

## 6. Busca híbrida

**Significado:** combinação de mais de um método de recuperação para
aproveitar características complementares.

**Em palavras simples:** combina a busca por significado com a busca por
palavras correspondentes.

**No projeto:** a pontuação híbrida utiliza atualmente 70% da
similaridade semântica e 30% da relevância lexical:

`relevância_híbrida = 0,70 × similaridade_semântica + 0,30 × relevância_lexical`

## 7. Similaridade de cosseno

**Significado:** medida matemática que compara a orientação de dois
vetores, sendo frequentemente utilizada para estimar a proximidade entre
embeddings.

**Em palavras simples:** compara a direção de dois vetores para estimar
o quanto seus conteúdos estão relacionados.

**No projeto:** é utilizada em `busca.py` para comparar o embedding da
pergunta com os embeddings dos trechos documentais.

## 8. Chunk / Chunking

**Significado:** um chunk é um trecho de texto; chunking é o processo de
dividir um documento em partes menores para processamento e recuperação.

**Em palavras simples:** em vez de procurar em um documento inteiro de
uma vez, o assistente trabalha com pedaços menores.

**No projeto:** `documentos.py` divide os documentos em trechos e
preserva metadados como título e hierarquia.

## 9. Limiar (threshold)

**Significado:** valor mínimo utilizado como critério para aceitar ou
rejeitar um resultado.

**Em palavras simples:** é uma nota de corte. Se o resultado não atingir
o valor mínimo, ele não é considerado relevante o suficiente.

**No projeto:** a busca híbrida utiliza 0.50 como limiar padrão. Para perguntas de definição reconhecidas pelo sistema, o `app.py` utiliza um limiar reduzido de 0.30, permitindo recuperar trechos relevantes com maior flexibilidade.

## 10. Prompt injection

**Significado:** tentativa de manipular o comportamento de um modelo por
meio de instruções inseridas em mensagens, documentos ou outros
conteúdos processados pelo modelo.

**Em palavras simples:** é quando um texto tenta dar ordens à IA para
que ela ignore as instruções que deveria seguir.

**No projeto:** os documentos são tratados como dados de referência não
confiáveis. As instruções do sistema orientam a Gemma a não obedecer
comandos encontrados dentro do conteúdo documental.

## 11. Metadados

**Significado:** informações adicionais que descrevem ou contextualizam
outro dado, sem necessariamente fazer parte do conteúdo principal.

**Em palavras simples:** são dados que ajudam a identificar, organizar
ou entender melhor um trecho de texto.

**No projeto:** cada chunk mantém informações como nome do documento,
nível e título da seção e hierarquia. Esses metadados são preservados na
base de conhecimento e podem ser utilizados para apresentar fontes e
expandir o contexto.

## 12. Hierarquia documental

**Significado:** organização de conteúdos em níveis relacionados, como
títulos, subtítulos e seções subordinadas.

**Em palavras simples:** é a estrutura de capítulos e subcapítulos de um
documento, que indica quais assuntos pertencem a outros.

**No projeto:** `documentos.py` identifica os títulos Markdown e registra
a hierarquia das seções. `busca.py` utiliza essa estrutura para acrescentar
seções descendentes relacionadas a um trecho recuperado.

## 13. Expansão hierárquica

**Significado:** inclusão de trechos relacionados à estrutura hierárquica
de um documento a partir de um trecho recuperado diretamente.

**Em palavras simples:** quando uma seção relevante é encontrada, o
sistema também pode trazer partes subordinadas a ela para complementar
o contexto.

**No projeto:** `expandir_contexto_hierarquico()` em `busca.py` procura
seções descendentes do mesmo documento que correspondam à hierarquia do
resultado. Os trechos acrescentados são identificados como expansão
hierárquica, não como resultados pontuados diretamente pela busca.

## 14. Stopwords

**Significado:** palavras frequentemente removidas de consultas ou textos
porque, em determinado método de recuperação, contribuem pouco para
distinguir o conteúdo.

**Em palavras simples:** são palavras comuns, como alguns artigos,
preposições e conjunções, que podem ser ignoradas para concentrar a
comparação nos termos mais informativos.

**No projeto:** `busca_lexical.py` mantém uma lista manual de stopwords
em português, removida durante a extração das palavras. A lista é simples
e pode ser ampliada ou refinada futuramente.

## 15. Streamlit

**Significado:** framework Python utilizado para criar aplicações
interativas, especialmente interfaces para ferramentas de dados e
prototipagem.

**Em palavras simples:** permite transformar um programa Python em uma
interface acessível por navegador, com elementos como campos de texto,
botões e áreas de exibição.

**No projeto:** é utilizado em `app.py` para apresentar o assistente,
permitir a seleção de perfil, exibir o histórico, enviar perguntas,
limpar a conversa e mostrar os trechos/fontes recuperados.

------------------------------------------------------------------------

## Termos para acrescentar conforme o projeto avançar

-   API
-   HTTP e requisição/resposta
-   JSON
-   Token
-   Context window / janela de contexto
-   Prompt de sistema
-   Histórico de conversa
-   Recuperação contextual
-   Vetor
-   Normalização de texto
-   Persistência
-   Banco vetorial
-   Alucinação de modelo

> Os termos desta lista ainda não precisam ser tratados como
> funcionalidades implementadas. Serão explicados quando forem
> relevantes para o projeto.
