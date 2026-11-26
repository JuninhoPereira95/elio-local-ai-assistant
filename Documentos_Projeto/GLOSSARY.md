# Glossary

This glossary brings together technical concepts used in the development of Elio, a local AI assistant built with Python, Ollama, Streamlit, and RAG.

Each entry provides the meaning of the term, a plain-language explanation, and its practical application in the project.

## How This Glossary Is Organized

Whenever possible, each term includes:

1. **Meaning:** technical definition.
2. **In simple terms:** an accessible explanation or analogy.
3. **In the project:** where the concept appears and what its purpose is.

The goal is not to collect isolated definitions copied from other sources, but to explain the concepts we actually encounter and use while building the assistant.

---

## 1. RAG — Retrieval-Augmented Generation

**Meaning:** A technique that combines information retrieval from an external source with text generation by a language model.

**In simple terms:** Before answering, the assistant searches reference documents for information. It then sends the retrieved passages to the model to help formulate the response.

**In the project:** The assistant searches passages in files stored in the `Documentos/` directory and uses the results as context for Gemma. For some simple definition questions, Python returns the document text directly.

## 2. LLM — Large Language Model

**Meaning:** A large language model trained to process and generate text.

**In simple terms:** It is the AI model that interprets messages and produces responses in natural language.

**In the project:** We use Gemma 3 1B through Ollama to generate responses that require elaboration, summarization, or interpretation.

## 3. Embedding

**Meaning:** A numerical representation of text in the form of a vector, constructed so that relationships in meaning can be compared mathematically.

**In simple terms:** It is a way of converting text into numbers so the program can compare the approximate meaning of questions and passages.

**In the project:** The `nomic-embed-text` model generates embeddings for document passages and questions. These vectors are used in semantic search.

## 4. Semantic Search

**Meaning:** A retrieval method that compares vector representations to find semantically related content, even when different words are used.

**In simple terms:** It tries to find passages that discuss the same idea, rather than only passages that repeat the words used in the question.

**In the project:** Semantic search compares the question embedding with the embeddings of passages in the knowledge base.

## 5. Lexical Search

**Meaning:** A retrieval method based on matching words or terms found in a query with the content being searched.

**In simple terms:** It checks whether important words from the question appear in the passage or section title.

**In the project:** The `busca_lexical.py` module extracts words from the question and calculates a matching score against the content and titles of document passages.

## 6. Hybrid Search

**Meaning:** The combination of more than one retrieval method to take advantage of their complementary characteristics.

**In simple terms:** It combines meaning-based search with word-matching search.

**In the project:** The hybrid score currently uses 70% semantic similarity and 30% lexical relevance:

`hybrid_relevance = 0.70 × semantic_similarity + 0.30 × lexical_relevance`

## 7. Cosine Similarity

**Meaning:** A mathematical measure that compares the orientation of two vectors. It is frequently used to estimate the similarity between embeddings.

**In simple terms:** It compares the direction of two vectors to estimate how closely their contents are related.

**In the project:** It is used in `busca.py` to compare the question embedding with the embeddings of document passages.

## 8. Chunk / Chunking

**Meaning:** A chunk is a passage of text; chunking is the process of splitting a document into smaller parts for processing and retrieval.

**In simple terms:** Instead of searching an entire document at once, the assistant works with smaller pieces.

**In the project:** `documentos.py` splits documents into passages and preserves metadata such as titles and hierarchy.

## 9. Threshold

**Meaning:** A minimum value used as a criterion for accepting or rejecting a result.

**In simple terms:** It is a cutoff score. If a result does not reach the minimum value, it is not considered relevant enough.

**In the project:** Hybrid search currently uses 0.50 as its default threshold.

## 10. Prompt Injection

**Meaning:** An attempt to manipulate a model's behavior through instructions inserted into messages, documents, or other content processed by the model.

**In simple terms:** It happens when a piece of text tries to give the AI commands to ignore the instructions it is supposed to follow.

**In the project:** Documents are treated as untrusted reference data. The system instructions guide Gemma not to obey commands found within document content.

## 11. Metadata

**Meaning:** Additional information that describes or provides context for other data, without necessarily being part of its main content.

**In simple terms:** Metadata helps identify, organize, or better understand a passage of text.

**In the project:** Each chunk retains information such as the document name, section level, title, and hierarchy. This metadata is preserved in the knowledge base and can be used to display sources and expand context.

## 12. Document Hierarchy

**Meaning:** The organization of content into related levels, such as headings, subheadings, and subordinate sections.

**In simple terms:** It is the chapter and subchapter structure of a document, indicating which topics belong to others.

**In the project:** `documentos.py` identifies Markdown headings and records the hierarchy of sections. `busca.py` uses this structure to include descendant sections related to a retrieved passage.

## 13. Hierarchical Expansion

**Meaning:** The inclusion of passages related to a document's hierarchical structure, starting from a passage retrieved directly.

**In simple terms:** When a relevant section is found, the system can also retrieve subordinate sections to provide additional context.

**In the project:** `expandir_contexto_hierarquico()` in `busca.py` searches for descendant sections in the same document that match the hierarchy of the retrieved result. The added passages are identified as hierarchical expansion, not as results directly scored by the search process.

## 14. Stopwords

**Meaning:** Words frequently removed from queries or texts because, in a given retrieval method, they contribute little to distinguishing content.

**In simple terms:** These are common words, such as certain articles, prepositions, and conjunctions, that can be ignored to focus the comparison on more informative terms.

**In the project:** `busca_lexical.py` maintains a manually defined list of Portuguese stopwords, which are removed during word extraction. The list is simple and may be expanded or refined in the future.

## 15. Streamlit

**Meaning:** A Python framework used to create interactive applications, especially interfaces for data tools and prototyping.

**In simple terms:** It makes it possible to turn a Python program into a browser-accessible interface with elements such as text fields, buttons, and display areas.

**In the project:** It is used in `app.py` to present the assistant, allow profile selection, display conversation history, send questions, clear the conversation, and show retrieved passages and sources.

---

## Terms to Add as the Project Evolves

- API
- HTTP and Request/Response
- JSON
- Token
- Context Window
- System Prompt
- Conversation History
- Contextual Retrieval
- Vector
- Text Normalization
- Persistence
- Vector Database
- Model Hallucination

> The terms in this list do not necessarily represent implemented features. They will be explained when they become relevant to the project.