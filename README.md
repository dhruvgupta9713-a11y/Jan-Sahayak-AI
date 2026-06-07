# Jan Sahayak AI

A smart chatbot that helps you understand Indian government schemes. Upload scheme PDFs, ask questions in plain language, and get accurate answers backed by real document sources.

Built with Retrieval-Augmented Generation (RAG) — every answer comes from the actual documents, not from AI guessing.

## What It Does

- Upload government scheme PDFs and index them automatically
- Ask questions in natural language about any scheme
- Get answers grounded strictly in the uploaded documents
- See exactly which document and page the answer came from
- Pre-loaded with 3 demo schemes to try instantly

## Demo Schemes Included

| Scheme | What It Covers |
|--------|---------------|
| Pradhan Mantri Jan Dhan Yojana | Zero-balance bank accounts, RuPay cards, insurance |
| PM Kisan Samman Nidhi | Direct income support of ₹6,000/year for farmers |
| Ayushman Bharat (PM-JAY) | ₹5 Lakh cashless health coverage for families |

## Tech Stack

- **Frontend**: Streamlit with custom dark theme
- **AI Model**: Google Gemini 2.0 Flash
- **Embeddings**: Gemini Embedding 001
- **Vector DB**: ChromaDB
- **Framework**: LangChain
- **PDF Parsing**: PyPDF

## How It Works

```
PDF Upload → Text Extraction → Chunking (1000 chars) → Embedding → ChromaDB Storage
                                                                          ↓
User Question → Semantic Search → Top-K Retrieval → Gemini Generates Answer
```

1. PDFs are split into overlapping chunks of 1000 characters
2. Each chunk is converted into a 768-dimensional vector using Gemini embeddings
3. Vectors are stored in ChromaDB for fast similarity search
4. When you ask a question, it finds the most relevant chunks
5. Gemini reads those chunks and writes a grounded answer

## Setup

```bash
# Clone the repo
git clone https://github.com/dhruvgupta9713-a11y/Jan-Sahayak-AI.git
cd Jan-Sahayak-AI

# Install dependencies
pip install -r requirements.txt

# Add your Gemini API key
# Create a .env file with:
GOOGLE_API_KEY=your_api_key_here

# Generate demo scheme PDFs
python generate_dummy_assets.py

# Run the app
streamlit run app.py
```

Get your free Gemini API key from [Google AI Studio](https://aistudio.google.com/apikey).

## Project Structure

```
Jan-Sahayak-AI/
├── app.py                    # Main Streamlit application
├── chatbot.py                # RAG logic and Gemini integration
├── vector_store.py           # ChromaDB operations
├── pdf_processor.py          # PDF text extraction and chunking
├── utils.py                  # File handling utilities
├── generate_dummy_assets.py  # Creates demo scheme PDFs
├── requirements.txt          # Python dependencies
├── .streamlit/config.toml    # Dark theme configuration
└── uploads/                  # Stored PDF documents
```

## Screenshots

The app features a dark theme with three main tabs:
- **Chat** — Ask questions and get sourced answers
- **Schemes & Questions** — Browse available schemes and preset questions
- **How to Use** — Tutorial video and step-by-step guide

## License

MIT
