# Gold Q/A Pairs for Evaluation

These are 5 gold question-answer pairs for evaluating the Mini RAG system. 
After ingesting the test document (see `test_ingest.py`), these questions should produce accurate answers with proper citations.

## Test Document Context
The test document covers: AI/ML basics, LLMs, RAG systems, vector databases, and the RAG pipeline.

---

## Q/A Pair 1

**Question:** What is Retrieval-Augmented Generation?

**Expected Answer:** Retrieval-Augmented Generation (RAG) combines the power of Large Language Models (LLMs) with external knowledge bases to provide more accurate and up-to-date answers. It involves retrieving relevant documents from a knowledge base and using them as context for the LLM to generate answers.

**Expected Citations:** Should cite the section discussing RAG systems.

**Precision/Recall Note:** High precision expected as RAG is explicitly defined. Should retrieve the chunk containing "Retrieval-Augmented Generation (RAG) combines..."

---

## Q/A Pair 2

**Question:** What are vector databases used for in RAG systems?

**Expected Answer:** Vector databases are essential for RAG systems as they enable efficient similarity search over embeddings. They use cosine similarity or other distance metrics to find relevant documents.

**Expected Citations:** Should cite the section about vector databases.

**Precision/Recall Note:** Should retrieve chunks mentioning "Vector databases" and "similarity search". May need to combine information from related chunks.

---

## Q/A Pair 3

**Question:** What are the steps in the RAG pipeline?

**Expected Answer:** The RAG pipeline typically involves: document ingestion, chunking, embedding generation, vector storage, retrieval, reranking, and answer generation. Each step is crucial for building an effective question-answering system.

**Expected Citations:** Should cite the section listing the RAG pipeline steps.

**Precision/Recall Note:** High recall needed to capture all pipeline steps. Should retrieve the chunk with the complete list.

---

## Q/A Pair 4

**Question:** What is the relationship between machine learning and deep learning?

**Expected Answer:** Machine learning is a subset of AI that enables computers to learn from data without explicit programming. Deep learning uses neural networks with multiple layers to process complex patterns, and is a subset of machine learning.

**Expected Citations:** Should cite sections about machine learning and deep learning.

**Precision/Recall Note:** May require combining information from multiple chunks about ML and deep learning. Should maintain accuracy about the hierarchical relationship.

---

## Q/A Pair 5

**Question:** Name some popular vector databases.

**Expected Answer:** Popular vector databases include Qdrant, Pinecone, and Weaviate.

**Expected Citations:** Should cite the section listing vector databases.

**Precision/Recall Note:** High precision needed for exact names. Should retrieve the chunk containing the list of vector databases.

---

## Evaluation Metrics

**Precision:** Measures how many retrieved chunks are relevant to the question.
- Target: >80% for factual questions (Q1, Q2, Q5)
- Target: >70% for multi-part questions (Q3, Q4)

**Recall:** Measures how many relevant chunks were retrieved.
- Target: >75% for single-concept questions
- Target: >60% for questions requiring multiple chunks

**Answer Quality:** 
- Answers should be grounded in retrieved chunks only
- Citations should be accurate and traceable
- No hallucinated information
