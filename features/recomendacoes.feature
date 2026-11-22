# language: pt
Funcionalidade: Recomendações com LLM e fallback
  Como sistema de balcão
  Quero recomendar livros ao sócio
  Para sugerir títulos com Ollama ou fallback determinístico

  Cenário: Recomendação com origem ollama quando o modelo responde
    Dado que existe sócio "ana.silva@biblioteca.example.com"
    E que o Ollama responde JSON válido de recomendações
    Quando solicitar recomendações com limite 3
    Então a resposta deve ter status 200
    E a origem deve ser "ollama"

  Cenário: Fallback determinístico quando Ollama falha
    Dado que existe sócio "ana.silva@biblioteca.example.com"
    E que o Ollama está indisponível ou em timeout
    Quando solicitar recomendações com limite 3
    Então a resposta deve ter status 200
    E a origem deve ser "fallback_deterministico"

  Cenário: Sócio inexistente em recomendações
    Quando solicitar recomendações para sócio inexistente
    Então a resposta deve ter status 404
