# Project Scope — Version 1.0

## 1. Overview

The project consists of developing a local AI assistant that runs on the user's own computer, using Python, Ollama, and a local language model.

The first version focuses on an assistant specialized in Information Security, capable of querying user-provided documents through a RAG (Retrieval-Augmented Generation) architecture.

The goal is to build a functional, understandable, and demonstrable proof of concept, prioritizing simplicity, control over responses, and learning throughout the development process.

The graphical user interface is also part of version 1.0.

## 2. Version 1.0 Objectives

By the end of version 1.0, the system should:

Run locally, without relying on a cloud-hosted AI service to generate responses.

Allow users to interact with the assistant through a graphical interface.

Use a local model provided by Ollama.

Query a user-provided document knowledge base.

Retrieve relevant document passages using a combination of semantic and lexical search.

Generate responses grounded in the retrieved content.

Provide answers directly extracted from documents for simple definition questions, when applicable, to preserve the accuracy of the original text.

Recognize when the knowledge base does not contain enough information to answer a question.

Maintain conversation history during a session and allow users to start a clean conversation.

Allow users to select different assistant behavior profiles.

Organize the code into modules with clearly defined responsibilities.

## 3. Planned Features

### 3.1. Local Assistant

Communication with Ollama through its local API.

Use of a local language model.

Basic handling of communication failures and unexpected responses.

Centralized configuration of the model, API addresses, and relevant parameters.

### 3.2. Document Knowledge Base

Reading of document formats supported by the project.

Organization of content into sections.

Division of content into passages (chunks).

Preservation of metadata, such as document name, title, and section hierarchy.

Generation of embeddings to represent the semantic content of each passage.

In the initial version, the knowledge base will consist of documents manually added to the directory defined by the project.

### 3.3. Information Retrieval (RAG)

Semantic search based on similarity between embeddings.

Lexical search to identify matches between question terms and document content.

Combination of semantic and lexical results into a hybrid score.

Selection of the most relevant passages according to defined criteria.

Contextual expansion through document hierarchy when it helps provide additional context.

Forwarding of retrieved passages to the language model for questions that require elaboration or interpretation.

### 3.4. Grounded Responses

Expected behavior:

Use retrieved documents as the information source for answers related to the knowledge base.

Avoid adding external information when a task requires an answer restricted to document content.

Indicate when insufficient passages are found to answer a question.

Treat document content as reference data, not as instructions that can override the assistant's rules.

Use direct answers extracted from documents for simple definition question formats recognized by the system, when a reliable match is available.

Known limitation: prompt instructions help guide the model, but they cannot guarantee absolute fidelity. Therefore, the initial version combines the language model with logic implemented in Python for cases where exact reproduction of document content is important.

### 3.5. Conversation History and Commands

Maintain conversation messages during the session.

Send conversation history to the model when a response depends on previous messages.

Provide a command or action to clear the history and start a new conversation.

Conversation history and document retrieval are separate mechanisms: conversation history provides conversational context to the model, while RAG search retrieves information from the document knowledge base.

### 3.6. Assistant Profiles

Provide behavior profiles, initially:

General.

Information Security.

Game Development.

Profiles guide the style and focus of responses. When a question is answered using document content, rules for remaining faithful to the retrieved information must take priority over general style instructions.

### 3.7. Graphical User Interface

The graphical interface is part of version 1.0 and should provide, at a minimum:

A field for typing and sending messages.

Display of user and assistant messages.

Access to profile selection.

An option to clear or restart the conversation.

Clear indications of processing and basic errors.

Clear presentation of responses.

The interface is built with Streamlit and is implemented and integrated into the proof-of-concept workflow. The planned basic visual customization for V1.0 has been completed: the assistant received the name Elio, a sparkle icon identity, and the Dark 2 — Deep Blue default color palette. More extensive layout improvements and additional visual options are reserved for the post-POC phase.

## 4. Technical Organization

The project is organized into Python modules with separate responsibilities, making the application easier to understand, maintain, and evolve.

Main Modules

app.py: Streamlit graphical interface and coordination of the application workflow.

respostas.py: recognition of simple definition questions and construction of direct answers.

perfis.py: definition of assistant behavior profiles.

ollama.py: communication with the local language model.

config.py: centralization of application settings.

embeddings.py: generation of text embeddings.

documentos.py: document reading, splitting, and organization.

base_conhecimento.py: construction of the knowledge base.

busca.py: semantic and hybrid retrieval of document passages.

busca_lexical.py: lexical search processing and scoring.

Directories and Supporting Files

Documentos/: documents used as the knowledge base.

images/: images used in the project documentation.

.streamlit/: graphical interface configuration.

requirements.txt: Python dependencies required to run the project.

.gitignore: definition of files and directories that should not be uploaded to the repository.

## 5. Criteria for Considering Version 1.0 Complete

Version 1.0 will be considered complete when:

The project can be installed and executed by following the documented instructions.

The assistant runs locally with Ollama and the configured model.

The graphical interface allows users to interact with the assistant.

Example documents are loaded and processed correctly.

The retrieval system can locate relevant passages for questions included in the tests.

Simple definition questions can receive answers directly supported by the document.

Questions requiring elaboration can be forwarded to the model along with the retrieved context.

The system recognizes situations where the knowledge base does not contain enough information.

Conversation history works during a session and can be cleared.

Profile selection works correctly.

The main workflows have been tested and known issues have been documented.

The repository includes basic documentation so that others can understand and run the project.

The interface receives the planned basic visual customization without compromising existing workflows. Completed: Elio identity and the Dark 2 — Deep Blue palette have been applied.

Testing should include literal questions, paraphrased questions, questions whose answers are absent from the documentation, and questions that depend on conversation history.

## 6. Out of Scope for Version 1.0

To keep the first release feasible and avoid premature complexity, the following items are reserved for future evaluation:

Dedicated vector database and advanced embedding persistence.

Automatic document updates and continuous monitoring.

Automatic decomposition of complex questions into multiple queries.

Advanced automated response quality evaluation pipeline.

Sophisticated reranking and retrieval mechanisms.

Authentication, multiple users, and enterprise access control.

Integrations with external tools and services.

Server deployment or public availability as a service.

AI features for NPCs or game integration.

These items are not requirements for considering the initial proof of concept functional. They may be prioritized later according to actual needs identified during development.

## 7. Post-Version 1.0 Evolution (Post-POC)

With V1.0 completed, Elio's evolution will take place in incremental stages. The initial post-POC priority will be to further develop the interface; afterward, the focus will shift to improvements in the assistant's internal functionality.

### 7.1. First Stage — Interface Improvements

Explore new color palettes while keeping Dark 2 — Deep Blue as the initial default. The idea is to offer clearly identified alternatives, such as Dark 1, Dark 2, Dark 3, and light themes.

Allow users to choose the visual theme.

Evaluate persistence of theme preferences between sessions.

Improve the layout, sidebar organization, and overall user experience.

Evaluate improvements to the presentation and organization of conversation history.

### 7.2. Second Stage — Assistant Improvements

After the interface stage, evaluate and prioritize functional and technical improvements, such as:

Response streaming in the interface, displaying text progressively as it is generated.

Improvements to RAG retrieval quality and accuracy.

Vector database persistence to reduce startup time.

More practical document management.

Display and organization of the sources used in responses.

Additional profiles and knowledge bases.

Systematic evaluation of retrieval and generation.

Performance improvements and additional reliability controls.

Evaluation of support for queries in different languages, including strategies for retrieving Portuguese documents from questions written in other languages.

Each improvement should be considered according to its benefits, complexity, and contribution to the project's objectives. The order may change based on lessons learned and needs identified during the post-POC phase.

## 8. Development Principles

The following principles will guide the development of version 1.0:

Learning: the code and technical decisions should be understood by the developer.

Incremental development: implement and test one change at a time whenever possible.

Simplicity: avoid abstractions and dependencies that are not necessary.

Accuracy: prioritize responses supported by documents and acknowledge limitations.

Modularity: keep each part of the system focused on a clear responsibility.

Controlled scope: record interesting improvements for later instead of automatically incorporating them into the first version.

Definition of Success: version 1.0 is not intended to be a complete enterprise assistant or a competing product to major AI services. Its success lies in delivering a functional local application with a graphical interface that clearly demonstrates how a RAG-based assistant works and makes its architecture understandable and open to further development.