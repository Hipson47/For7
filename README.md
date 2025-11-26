# 🤖 RAG Knowledge Assistant v2.0

Inteligentny asystent wiedzy z interfejsem graficznym, który łączy wyszukiwanie semantyczne w bazie wiedzy z modelami AI przez OpenRouter.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

## ✨ Funkcje

- 🔍 **Inteligentne wyszukiwanie** - TF-IDF + cosine similarity
- 🤖 **Integracja z AI** - OpenRouter (Claude, GPT-4, Gemini, Llama...)
- 💬 **Język naturalny** - pisz pytania jak do człowieka
- 📚 **Wiele formatów** - PDF, MD, TXT, JSON
- 🎨 **Nowoczesne GUI** - ciemny motyw, responsywny design
- 📊 **Streaming** - odpowiedzi w czasie rzeczywistym
- 🔧 **Konfigurowalny** - wybór modelu, temperatura, liczba wyników

## 🚀 Szybki start

### 1. Instalacja

```bash
# Klonuj repozytorium
git clone <https://github.com/Hipson47/For7>
cd For7

# Zainstaluj zależności
pip install -r requirements.txt
```

### 2. Uruchomienie

```bash
python run.py
```

Aplikacja otworzy się w przeglądarce pod adresem `http://localhost:8501`

### 3. Konfiguracja

1. Uzyskaj klucz API na https://openrouter.ai/keys
2. Wprowadź klucz w panelu bocznym aplikacji
3. Wybierz model AI
4. Zadaj pytanie!

## 🎯 Dostępne modele AI

| Model | Dostawca | Kontekst | Tier | Koszt |
|-------|----------|----------|------|-------|
| Claude 3.5 Sonnet | Anthropic | 200K | Premium | $3/$15 per 1M |
| Claude 3 Haiku | Anthropic | 200K | Fast | $0.25/$1.25 |
| GPT-4o | OpenAI | 128K | Premium | $2.50/$10 |
| GPT-4o Mini | OpenAI | 128K | Fast | $0.15/$0.60 |
| Gemini 2.0 Flash | Google | 1M | Free | Darmowy |
| Gemini Pro 1.5 | Google | 2M | Premium | $1.25/$5 |
| Llama 3.1 70B | Meta | 128K | Open | $0.35/$0.40 |
| Llama 3.1 8B | Meta | 128K | Fast | $0.06/$0.06 |
| Mistral Large | Mistral | 128K | Premium | $2/$6 |
| DeepSeek Chat | DeepSeek | 64K | Budget | $0.14/$0.28 |

## 📁 Struktura projektu

```
📦 RAG Knowledge Assistant
├── 🚀 run.py              # Launcher aplikacji
├── 🎨 app.py              # Główna aplikacja Streamlit
├── 📋 requirements.txt    # Zależności Python
├── 📖 README.md           # Dokumentacja
│
├── 📂 src/                # Moduły źródłowe
│   ├── __init__.py
│   ├── config.py          # Konfiguracja i modele
│   ├── rag_engine.py      # Silnik RAG
│   ├── ai_client.py       # Klient OpenRouter
│   └── server.py          # API HTTP (opcjonalne)
│
├── 📂 .cursor/knowledge/  # Baza wiedzy (dokumenty)
│   ├── *.pdf
│   ├── *.md
│   └── *.json
│
└── 📂 logs/               # Logi aplikacji
    └── server.log
```

## 💡 Jak używać

### Przykładowe pytania:

```
"Jakie są najlepsze praktyki Docker w 2025?"
"Opisz architekturę backend aplikacji"
"Jak skonfigurować CI/CD w Google Cloud?"
"Pokaż przykłady async/await w Pythonie"
"Co to jest RAG i jak działa?"
```

### Tryby pracy:

- **🤖 AI + RAG** - Wyszukaj kontekst i wygeneruj odpowiedź AI
- **🔍 Tylko RAG** - Pokaż tylko wyniki wyszukiwania bez AI
- **📡 Streaming** - Odpowiedzi w czasie rzeczywistym

## ⚙️ Konfiguracja zaawansowana

### Zmienne środowiskowe

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
```

### Plik konfiguracyjny

Konfiguracja zapisywana jest w `~/.rag_assistant/config.json`:

```json
{
  "openrouter_api_key": "sk-or-v1-...",
  "default_model": "anthropic/claude-3.5-sonnet",
  "temperature": 0.7,
  "max_tokens": 4000,
  "top_k_results": 5
}
```

## 🔧 API Server (opcjonalne)

Dla integracji z innymi aplikacjami:

```bash
python -m src.server
```

Endpoints:
- `GET /health` - Status serwera
- `POST /search` - Wyszukiwanie
- `POST /context` - Kontekst dla AI
- `GET /files` - Lista plików
- `GET /stats` - Statystyki

## 📊 Dodawanie dokumentów

1. Dodaj pliki do `.cursor/knowledge/`
2. Obsługiwane formaty: PDF, MD, TXT, JSON
3. Uruchom ponownie aplikację (indeks zostanie przebudowany)

## 🐛 Troubleshooting

### "Brak modułu sklearn"
```bash
pip install scikit-learn
```

### "Błąd połączenia z OpenRouter"
- Sprawdź klucz API
- Sprawdź połączenie internetowe
- Sprawdź limity na koncie OpenRouter

### "Brak dokumentów w bazie"
- Upewnij się, że folder `.cursor/knowledge/` istnieje
- Dodaj pliki PDF/MD do folderu
- Usuń `rag_index.json` aby wymusić przebudowę

## 📝 Changelog

### v2.0.0
- 🎨 Nowe nowoczesne GUI
- 🤖 Integracja z OpenRouter
- 📊 Streaming odpowiedzi
- 🔧 System konfiguracji
- 📁 Lepsza obsługa wielu formatów
- 🧹 Czysty kod i struktura

### v1.0.0
- Podstawowy system RAG
- CLI interface

## 📄 Licencja

MIT License - używaj jak chcesz!

---

**🎉 Gotowe!** Twój inteligentny asystent wiedzy jest uruchomiony i gotowy do pomocy.

