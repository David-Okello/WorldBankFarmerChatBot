# Sample RAG prototype: vectorize simple soil-health docs, retrieve top-3, build prompt.

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# 1. Sample “soil-health” documents (simulating indexed World Bank reports)
docs = [
    "Soil organic matter improves water retention and nutrient supply in farms.",
    "pH levels between 6.0 and 7.5 are optimal for most crops to access nutrients.",
    "Cover cropping reduces erosion and boosts soil biodiversity over time.",
    "Regular soil testing reveals nitrogen, phosphorus, and potassium deficiencies.",
    "Compost application increases microbial activity and soil structure quality."
]

# 2. Build TF-IDF embeddings & NearestNeighbors index
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(docs)
'''
TF-IDF converts each document into a numerical “fingerprint” (a vector) 
that captures which words are important in that doc relative to the whole collection.

Now each snippet lives as a point in a multi-dimensional space.
'''

nn = NearestNeighbors(n_neighbors=3, metric='cosine').fit(X)
'''
Here I'm telling the index: “When I give you a new vector, find the 3 most similar existing vectors by cosine similarity.”
In a real RAG system I'd use a faster, scalable store like FAISS or Pinecone—but the idea is the same.
'''

def ask_farming_bot(query):
    # 3. Embed query
    q_vec = vectorizer.transform([query])
    # 4. Retrieve top-3 docs
    distances, indices = nn.kneighbors(q_vec)
    retrieved = [docs[i] for i in indices[0]]
    # 5. Compose prompt
    system_msg = "You are an agricultural expert chatbot. Use the following contexts to answer:"
    context_block = "\n\n".join(f"{i+1}. {d}" for i, d in enumerate(retrieved))
    prompt = f"{system_msg}\n\n{context_block}\n\nUser: {query}\nBot:"
    # 6. Show results
    print("=== Retrieved Passages ===")
    for i, d in enumerate(retrieved, 1):
        print(f"{i}. {d}")
    print("\n=== Generated Prompt ===")
    print(prompt)

# 7. Test with a sample query
ask_farming_bot("What soil health indicators should a farmer monitor?")



'''
A little Note:
Why This Matters
Precision: By only feeding the LLM the most relevant text, you avoid “hallucinations” or off-topic ramblings.

Explainability: You can inspect exactly which source passages the model used.

Scalability: Swap TF-IDF + NearestNeighbors for FAISS + embeddings and you have a production-ready RAG pipeline.
'''


'''
POSSIBLE OPTIMISATIONS
1. Move from TF-IDF to Dense Embeddings + FAISS
Why: TF-IDF only captures keyword overlap. Dense embeddings (e.g. from sentence-transformers) 
give real semantic similarity, so you’ll retrieve more relevant passages.

2. Chunk Long Documents with Overlap
Why: Real World Bank reports can be hundreds of pages. Break them into, say, 500-token chunks 
with 100-token overlap so you don’t split key facts at the wrong boundary.

def chunk_text(text, chunk_size=500, overlap=100):
    tokens = text.split()
    chunks = []
    for i in range(0, len(tokens), chunk_size - overlap):
        chunks.append(" ".join(tokens[i:i+chunk_size]))
    return chunks

3. Add Caching & Latency Monitoring
Why: In real apps you don’t want to re-compute embeddings on every query. 
Cache embeddings in Redis or local file. Log retrieval and generation times so you can spot bottlenecks.

4. Metadata Filtering
Why: If reports are tagged by region, crop, or date, filter your index by metadata before retrieval.
e.g., only retrieve docs where doc['region']=='East Africa'

filtered_index = [d for d in all_docs if d.meta['region']=='EA']

'''