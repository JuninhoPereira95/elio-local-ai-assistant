# Escopo do Projeto — Versão 1.0

## 1. Visão geral

O projeto consiste no desenvolvimento de um assistente de IA local, executado no próprio computador, utilizando Python, Ollama e um modelo de linguagem local.

A primeira versão tem como foco um assistente especializado em **Segurança da Informação**, capaz de consultar documentos fornecidos pelo usuário por meio de uma arquitetura RAG (*Retrieval-Augmented Generation*).

O objetivo é construir uma prova de conceito funcional, compreensível e demonstrável, priorizando simplicidade, controle sobre as respostas e aprendizado durante o desenvolvimento.

A interface gráfica também faz parte do escopo da versão 1.0.

## 2. Objetivos da versão 1.0

Ao final da versão 1.0, o sistema deverá:

- Executar localmente, sem depender de um serviço de IA hospedado na nuvem para gerar as respostas.
- Permitir interação com o assistente por meio de uma interface gráfica.
- Utilizar um modelo local disponibilizado pelo Ollama.
- Consultar uma base de documentos fornecida pelo usuário.
- Recuperar trechos relevantes dos documentos usando busca semântica e lexical combinadas.
- Gerar respostas fundamentadas no conteúdo recuperado.
- Apresentar respostas diretamente extraídas dos documentos em casos simples de definição, quando aplicável, para preservar a precisão do texto original.
- Reconhecer quando a base de conhecimento não contém informação suficiente para responder.
- Manter o histórico da conversa durante a sessão e permitir iniciar uma conversa limpa.
- Permitir selecionar perfis de comportamento do assistente.
- Organizar o código em módulos com responsabilidades claras.

## 3. Funcionalidades previstas

### 3.1. Assistente local

- Comunicação com o Ollama por meio de sua API local.
- Uso de um modelo de linguagem local.
- Tratamento básico de falhas de comunicação e respostas inesperadas.
- Configuração centralizada de modelo, endereços da API e parâmetros relevantes.

### 3.2. Base de conhecimento documental

- Leitura de documentos suportados pelo projeto.
- Organização do conteúdo em seções.
- Divisão do conteúdo em trechos (*chunks*).
- Preservação de metadados, como nome do documento, título e hierarquia das seções.
- Geração de embeddings para representar semanticamente os trechos.

Na versão inicial, a base será composta por documentos adicionados manualmente ao diretório definido pelo projeto.

### 3.3. Recuperação de informações (RAG)

- Busca semântica por similaridade entre embeddings.
- Busca lexical para identificar correspondências entre os termos da pergunta e o conteúdo documental.
- Combinação dos resultados semânticos e lexicais em uma pontuação híbrida.
- Seleção dos trechos mais relevantes conforme os critérios definidos.
- Expansão contextual por hierarquia documental quando isso ajudar a fornecer contexto.
- Encaminhamento dos trechos recuperados ao modelo para perguntas que exijam elaboração ou interpretação.

### 3.4. Respostas fundamentadas

O comportamento esperado é:

- Utilizar os documentos recuperados como fonte de informação para respostas relacionadas à base.
- Evitar acrescentar informações externas quando a tarefa exigir uma resposta restrita ao conteúdo documental.
- Informar quando não forem encontrados trechos suficientes para responder.
- Tratar o conteúdo dos documentos como dado de referência, e não como instruções que possam substituir as regras do assistente.
- Utilizar resposta direta extraída do documento para formatos simples de pergunta de definição reconhecidos pelo sistema, quando houver correspondência confiável.

**Limitação conhecida:** instruções no prompt ajudam a orientar o modelo, mas não garantem fidelidade absoluta. Por isso, a versão inicial combina o modelo de linguagem com lógica implementada em Python nos casos em que a reprodução exata do documento é importante.

### 3.5. Histórico e comandos da conversa

- Manter as mensagens da conversa durante a sessão.
- Enviar o histórico ao modelo quando a resposta depender de mensagens anteriores.
- Disponibilizar um comando ou ação para limpar o histórico e começar uma nova conversa.

O histórico da conversa e a recuperação documental são mecanismos distintos: o histórico fornece contexto conversacional ao modelo, enquanto a busca RAG procura informações na base de documentos.

### 3.6. Perfis do assistente

Disponibilizar perfis de comportamento, inicialmente:

- Geral.
- Segurança da Informação.
- Desenvolvimento de jogos.

Os perfis orientam o estilo e o foco das respostas. Quando uma pergunta estiver sendo respondida com base documental, as regras de fidelidade ao conteúdo recuperado devem ter prioridade sobre instruções gerais de estilo.

### 3.7. Interface gráfica

A interface gráfica faz parte da versão 1.0 e deverá oferecer, no mínimo:

- Campo para digitar e enviar mensagens.
- Exibição das mensagens do usuário e do assistente.
- Acesso à seleção de perfil.
- Opção para limpar ou reiniciar a conversa.
- Indicação compreensível de processamento e de erros básicos.
- Apresentação clara das respostas.

A tecnologia utilizada é o Streamlit. A interface está implementada e
integrada ao fluxo da POC. A personalização visual simples da V1.0 foi
concluída: o assistente recebeu o nome **Elio**, identidade com ícone de
brilho e a paleta padrão **Dark 2 — Deep Blue**. Melhorias mais profundas
de layout e novas opções visuais ficam reservadas para o pós-POC.

## 4. Organização técnica

O projeto está organizado em módulos Python com responsabilidades separadas, facilitando a compreensão, a manutenção e a evolução da aplicação.

### Principais módulos

- `app.py`: interface gráfica desenvolvida com Streamlit e coordenação do fluxo da aplicação.
- `respostas.py`: reconhecimento de perguntas simples de definição e montagem de respostas diretas.
- `perfis.py`: definição dos perfis de comportamento do assistente.
- `ollama.py`: comunicação com o modelo de linguagem local.
- `config.py`: centralização das configurações da aplicação.
- `embeddings.py`: geração de embeddings para os textos.
- `documentos.py`: leitura, divisão e organização dos documentos.
- `base_conhecimento.py`: construção da base de conhecimento.
- `busca.py`: recuperação semântica e híbrida dos trechos.
- `busca_lexical.py`: processamento e pontuação da busca lexical.

### Diretórios e arquivos auxiliares

- `Documentos/`: documentos utilizados como base de conhecimento.
- `images/`: imagens utilizadas na documentação do projeto.
- `.streamlit/`: configurações visuais da interface.
- `requirements.txt`: dependências Python necessárias para executar o projeto.
- `.gitignore`: definição de arquivos e diretórios que não devem ser enviados ao repositório.

## 5. Critérios para considerar a versão 1.0 concluída

A versão 1.0 será considerada concluída quando:

1. O projeto puder ser instalado e executado seguindo instruções documentadas.
2. O assistente funcionar localmente com o Ollama e o modelo configurado.
3. A interface gráfica permitir conversar com o assistente.
4. Os documentos de exemplo forem carregados e processados corretamente.
5. A recuperação conseguir localizar trechos relevantes para perguntas previstas nos testes.
6. Perguntas simples de definição puderem receber respostas diretamente sustentadas pelo documento.
7. Perguntas que exigem elaboração puderem ser encaminhadas ao modelo com o contexto recuperado.
8. O sistema reconhecer situações em que não há informação suficiente na base.
9. O histórico funcionar durante a conversa e puder ser limpo.
10. A seleção de perfis funcionar.
11. Os principais fluxos forem testados e os problemas conhecidos estiverem documentados.
12. O repositório possuir documentação básica para que outra pessoa entenda e execute o projeto.
13. A interface receber a personalização visual simples planejada, sem comprometer os fluxos já implementados. **Concluído:** identidade Elio e paleta Dark 2 — Deep Blue aplicadas.

Os testes deverão incluir perguntas literais, paráfrases, perguntas cuja resposta esteja ausente da documentação e perguntas que dependam do histórico da conversa.

## 6. Fora do escopo da versão 1.0

Para manter a primeira entrega viável e evitar complexidade prematura, os itens abaixo ficam reservados para avaliações futuras:

- Banco vetorial dedicado e persistência avançada dos embeddings.
- Atualização automática e monitoramento contínuo dos documentos.
- Decomposição automática de perguntas complexas em várias consultas.
- Pipeline avançado de avaliação automatizada da qualidade das respostas.
- Mecanismos sofisticados de reranking e recuperação.
- Autenticação, múltiplos usuários e controle de acesso corporativo.
- Integrações com ferramentas e serviços externos.
- Implantação em servidor ou disponibilização pública como serviço.
- Recursos de IA para NPCs ou integração com jogos.

Esses itens não são requisitos para considerar a prova de conceito inicial funcional. Poderão ser priorizados posteriormente conforme necessidades reais identificadas.

## 7. Evolução após a versão 1.0 (pós-POC)

Com a V1.0 concluída, a evolução do Elio será feita em etapas incrementais. A prioridade inicial do pós-POC será aprofundar a interface; depois, o foco passará para melhorias no funcionamento interno do assistente.

### 7.1. Primeira etapa — Evolução da interface

- Explorar novas paletas de cores, mantendo a **Dark 2 — Deep Blue** como padrão inicial. A ideia é oferecer alternativas identificadas, por exemplo, como Dark 1, Dark 2, Dark 3 e temas claros.
- Permitir que o usuário escolha a paleta visual.
- Avaliar a persistência da preferência de tema entre sessões.
- Aprimorar o layout, a organização da barra lateral e a experiência geral de uso.
- Avaliar melhorias na apresentação e organização do histórico de conversas.

### 7.2. Segunda etapa — Evolução do assistente

Depois da etapa de interface, avaliar e priorizar melhorias funcionais e técnicas, como:

- Streaming das respostas na interface, para exibir o texto progressivamente durante a geração.
- Melhorias na qualidade e precisão da recuperação RAG.
- Persistência da base vetorial para reduzir o tempo de inicialização.
- Gestão mais prática dos documentos.
- Exibição e organização das fontes utilizadas nas respostas.
- Novos perfis e bases de conhecimento.
- Avaliações sistemáticas da recuperação e da geração.
- Melhorias de desempenho e controles adicionais de confiabilidade.
- Avaliar suporte a consultas em diferentes idiomas, incluindo estratégias para recuperar documentos em português a partir de perguntas em outros idiomas.

A inclusão de cada melhoria deverá considerar seu benefício, sua complexidade e sua contribuição para os objetivos do projeto. A ordem poderá ser ajustada conforme os aprendizados e as necessidades identificadas durante o pós-POC.

## 8. Princípios de desenvolvimento

Durante a construção da versão 1.0, serão seguidos estes princípios:

- **Aprendizado:** o código e as decisões técnicas devem ser compreendidos pelo desenvolvedor.
- **Incrementalismo:** implementar e testar uma mudança por vez sempre que possível.
- **Simplicidade:** evitar abstrações e dependências que não sejam necessárias.
- **Precisão:** priorizar respostas sustentadas pelos documentos e reconhecer limitações.
- **Modularidade:** manter cada parte do sistema com uma responsabilidade clara.
- **Escopo controlado:** registrar melhorias interessantes para depois, em vez de incorporá-las automaticamente à primeira versão.

---

**Definição de sucesso:** a versão 1.0 não pretende ser um assistente corporativo completo nem um produto concorrente de grandes serviços de IA. Seu sucesso será entregar uma aplicação local funcional, com interface gráfica, que demonstre de forma clara o funcionamento de um assistente baseado em RAG e permita compreender e evoluir sua arquitetura.
