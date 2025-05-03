# World Bank Farmer Chat

## Overview of Files in Directory
A brief overview of all folders and files in the directory, what they do, what they contain, how to run them.

### .venv
Virtual environment so as to avoid version conflicts when installing packages. e.g: FAISS requires a lower version of numpy in order to not conflict

### reports
Generated txt files with sample data for the RAG

### create_reports.py
Script to generate reports directory and sample data txt files

### improved.py
An improved version of the RAG prototype.
Think of main.py as RAG version 1 and improved.py as RAG version 1.1

SentenceTransformer gives you dense semantic embeddings (vs. TF-IDF’s keyword overlap).

FAISS is the industry standard for fast, approximate nearest-neighbor retrieval at scale.

a) Document Loading & Chunking
- Why chunk? LLMs have context-window limits. Breaking large reports into overlapping 500-token snippets preserves continuity at boundaries.

- Metadata (e.g. source=file.name) lets you filter by region, date, or document type at retrieval time.

b) Embedding & Indexing
- “all-MiniLM-L6-v2” balances speed vs. semantic power.

- L2 normalization + Inner-Product is mathematically equivalent to cosine similarity, which works well for nearest-neighbor retrieval.

- IndexFlatIP is the simplest FAISS index; for millions of docs you’d swap in an IVF or HNSW variant.

c) Retrieval + Prompt Composition
1. Embed the user query into the same semantic space.

2. Search the FAISS index for the top-k closest chunks.

3. Optional metadata filtering ensures, for example, only “East Africa” docs are returned.

4. Build a system + context prompt:

    - A clear “You are …” system instruction locks the chatbot’s persona.

    - Numbered contexts let you—and the LLM—trace back which passages informed the answer.

    - Appending User: … Bot: sets the stage for an LLM call (e.g. openai.ChatCompletion.create(prompt=prompt)).

High-Level Takeaways
1. Modularity: each function has a single responsibility (chunking, embedding, indexing, retrieval, prompting).

2. Scalability path:

    - Swap TF-IDF → dense embeddings for better semantic recall.

    - Scale FAISS → distributed IVF/HNSW for millions of docs.

    - Add caching of embeddings & prompts for low-latency.

3. Explainability: humans can inspect “which snippet #2 came from file X” to audit and debias the system.

4. Security: RAG prototypes should run over sanitized, internally hosted document stores behind VPCs to avoid exposing sensitive reports.

### main.py
Sample RAG prototype: vectorize simple soil-health docs, retrieve top-3, build prompt.

1. Sample “soil-health” documents (simulating indexed World Bank reports)
2. Build TF-IDF embeddings & NearestNeighbors index
3. Embed query
4. Retrieve top-3 docs
5. Compose prompt
6. Show results

output generated: 
```
(.venv) C:\Users\User\Desktop\WorldBankFarmerChat>python main.py
=== Retrieved Passages ===
1. Regular soil testing reveals nitrogen, phosphorus, and potassium deficiencies.
2. Compost application increases microbial activity and soil structure quality.
3. Cover cropping reduces erosion and boosts soil biodiversity over time.

=== Generated Prompt ===
You are an agricultural expert chatbot. Use the following contexts to answer:

1. Regular soil testing reveals nitrogen, phosphorus, and potassium deficiencies.

2. Compost application increases microbial activity and soil structure quality.

3. Cover cropping reduces erosion and boosts soil biodiversity over time.

User: What soil health indicators should a farmer monitor?
Bot:

```


### README.md

### churnpred.py
Code for customer churn prediction model

output generated: 
```
(.venv) C:\Users\User\Desktop\WorldBankFarmerChat>python churnpred.py
Best ROC AUC: 1.0
Best params: {'clf__max_depth': 5, 'clf__n_estimators': 100}
Sample risk scores: [0.07642917 0.08650294 0.05018108]
```

### generate_customer_data.py
Script to generate dummy customer data for the churn prediction model
Generates a csv with over 1000 rows

### requirements.txt
In worldbankfarmerchat directory, run: 

```
python -m venv .venv

.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt 
```

After the virtual env is activated and all requirements installed:
```
python create_reports.py
python generate_customer_data.py
python main.py
python improved.py
python churnpred.py
```


