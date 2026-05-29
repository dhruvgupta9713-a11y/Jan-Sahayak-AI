import os
import time
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI

# Model fallback chain — if primary model hits rate limits, try alternatives
GEMINI_MODELS = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-2.5-flash",
]

def retrieve_relevant_chunks(vector_store, query: str, k: int = 4):
    """
    Retrieves the top k most relevant chunks along with their similarity scores.
    Uses ChromaDB similarity search with relevance scores.
    """
    try:
        # returns list of tuples: (Document, score)
        # Chroma relevance scores are typically mapped to [0, 1] range.
        results = vector_store.similarity_search_with_relevance_scores(query, k=k)
        return results
    except Exception as e:
        print(f"Error during document retrieval: {e}")
        return []

def generate_answer(query: str, retrieved_chunks: list, google_api_key: str) -> dict:
    """
    Generates a response from Google Gemini strictly grounded in the retrieved chunks.
    If the context is insufficient, returns: "The information is not available in the uploaded documents."
    Automatically retries with fallback models if rate limits are hit.
    """
    fallback_response = "The information is not available in the uploaded documents."
    
    # If no chunks were returned, we can't answer the question
    if not retrieved_chunks:
        return {
            "answer": fallback_response,
            "sources": []
        }
    
    # 1. Format context and collect metadata for the user interface
    context_parts = []
    sources_info = []
    
    for i, (doc, score) in enumerate(retrieved_chunks):
        # Format the score as a percentage confidence value (clamp between 0 and 100)
        confidence = max(0.0, min(1.0, score)) * 100
        
        # Source filename
        source_name = os.path.basename(doc.metadata.get('source', 'Unknown Document'))
        page_num = doc.metadata.get('page', 0) + 1
        
        # Context block passed to LLM
        context_parts.append(
            f"--- [SOURCE {i+1}]: {source_name} (Page {page_num}) ---\n"
            f"{doc.page_content}"
        )
        
        # Details displayed in Streamlit UI
        sources_info.append({
            "id": i + 1,
            "content": doc.page_content,
            "source": source_name,
            "page": page_num,
            "score": round(confidence, 2)
        })
        
    context_text = "\n\n".join(context_parts)
    
    # 2. Construct prompt restricting Gemini to the provided context
    system_prompt = (
        "You are an expert AI assistant specializing in Government Schemes.\n"
        "You must answer the user's question STRICTLY based on the provided document context below.\n\n"
        f"--- CONTEXT START ---\n"
        f"{context_text}\n"
        f"--- CONTEXT END ---\n\n"
        "Strict Guidelines:\n"
        "1. Answer the question using ONLY the facts explicitly mentioned in the context above.\n"
        "2. Do NOT use any pre-existing training knowledge, external facts, or assumptions to answer.\n"
        "3. If the context does not contain the answer, or is unrelated to the question, you MUST answer EXACTLY with: \n"
        "   \"The information is not available in the uploaded documents.\"\n"
        "   Do not add any explanations, greetings, or other words if this is the case.\n"
        "4. Be objective, factual, and direct. Do not say things like 'based on the context' or 'according to source 1'."
    )
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=query)
    ]
    
    # 3. Try each model in the fallback chain
    last_error = None
    for model_name in GEMINI_MODELS:
        try:
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=google_api_key,
                temperature=0.0  # Zero temperature for deterministic, factual responses
            )
            
            response = llm.invoke(messages)
            content = response.content
            
            # Parse list-based content (some versions of the package return structured blocks)
            if isinstance(content, list):
                text_parts = []
                for part in content:
                    if isinstance(part, dict) and "text" in part:
                        text_parts.append(part["text"])
                    elif hasattr(part, "text"):
                        text_parts.append(part.text)
                    elif isinstance(part, str):
                        text_parts.append(part)
                answer = "".join(text_parts).strip()
            else:
                answer = str(content).strip()
            
            # 4. Enforce exact fallback message if the LLM generated a generic refusal
            lower_answer = answer.lower()
            refusal_keywords = [
                "not mentioned", "not found", "does not contain", "no information", 
                "not provide", "not available in the provided", "cannot answer",
                "insufficient information", "do not have information"
            ]
            
            # If the answer is thin or represents a refusal, normalize it to the required prompt response
            if any(keyword in lower_answer for keyword in refusal_keywords) or len(answer) < 5:
                answer = fallback_response
                
            return {
                "answer": answer,
                "sources": sources_info
            }
            
        except Exception as e:
            last_error = e
            error_str = str(e).upper()
            # If rate limited or model not found, try next model after a short pause
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in error_str or "RATE" in error_str or "404" in str(e) or "NOT_FOUND" in error_str:
                print(f"Error on {model_name} ({type(e).__name__}), trying next model...")
                time.sleep(2)
                continue
            else:
                # Non-retryable error — don't try other models
                return {
                    "answer": f"Error running Gemini API: {str(e)}",
                    "sources": []
                }
    
    # All models exhausted
    return {
        "answer": f"⚠️ All Gemini models are currently rate-limited. Please wait 1-2 minutes and try again.\n\n_Technical details: {str(last_error)}_",
        "sources": []
    }

