# ==========================================
# MODULO: CONFIGURACOES DO ASSISTENTE
# ==========================================

# Endereco da API do Ollama
URL_OLLAMA = "http://localhost:11434/api/chat"

# Modelo de IA utilizado pelo assistente
MODELO_IA = "gemma3:1b"

# Tempo máximo de espera pela resposta do Ollama (segundos)
TIMEOUT_OLLAMA = 180

# Modelo utilizado para gerar embeddings
MODELO_EMBEDDING = "nomic-embed-text"

# Endereco da API de embeddings do Ollama
URL_EMBEDDING = "http://localhost:11434/api/embed"