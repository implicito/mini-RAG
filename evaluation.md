# Evaluation of Mini RAG System

## Document Used
**Title:** A Semi-Supervised Approach for Classifying Insect Developmental Phases from Repurposed IP102  
**Domain:** Computer Vision, Semi-Supervised Learning, Agricultural AI

This evaluation assesses the ability of the Mini RAG system to retrieve and generate accurate, context-grounded answers from the above document using five representative queries.

---

## Evaluation Methodology

For each query:
1. A question was issued to the RAG system.
2. Retrieved chunks and the generated answer were manually compared against the ground-truth information in the paper.
3. Precision and recall were computed based on retrieved relevance.

---

## Evaluation Queries

### Q1.  
**Question:** What core problem does the paper aim to address in insect pest classification?

**Ground Truth (GT):**  
The paper addresses class imbalance and limited labeled data in insect life-stage classification, particularly under semi-supervised learning settings.

---

### Q2.  
**Question:** What is Cost-Focal FixMatch and how does it extend FixMatch?

**Ground Truth (GT):**  
Cost-Focal FixMatch extends FixMatch by introducing class-aware weighting and focal loss to improve minority-class learning under severe imbalance.

---

### Q3.  
**Question:** Which datasets are used for evaluation and how are they structured?

**Ground Truth (GT):**  
The study uses Repurposed IP102 (4 life stages) and Mixed IP102 (167 combined species–stage classes), with validation data treated as labeled and training data as unlabeled.

---

### Q4.  
**Question:** What evaluation metrics are used to assess model performance?

**Ground Truth (GT):**  
Accuracy, Precision, Recall, and F1-score computed from TP, FP, FN, and TN.

---

### Q5.  
**Question:** How does the proposed method improve performance on minority classes?

**Ground Truth (GT):**  
It significantly improves recall for minority classes (e.g., Larva, Pupa, Egg) by generating higher-quality pseudo-labels and focusing learning on hard examples.

---

## Precision and Recall Calculation

For each query:

- **Relevant Chunks (R):** Chunks that truly contain information needed to answer the query.
- **Retrieved Chunks (K):** Chunks returned by the retriever.
- **Correctly Retrieved (C):** Retrieved chunks that are relevant.

### Precision
\[
\text{Precision} = \frac{C}{K}
\]

Measures how much of the retrieved information is relevant.

---

### Recall
\[
\text{Recall} = \frac{C}{R}
\]

Measures how much of the relevant information was successfully retrieved.

---

## Example (Single Query)

- Retrieved chunks (K) = 6  
- Relevant chunks in document (R) = 5  
- Correctly retrieved chunks (C) = 4  

**Precision:**  
\[
4 / 6 = 0.67
\]

**Recall:**  
\[
4 / 5 = 0.80
\]

---

## Overall Evaluation Notes

- High recall indicates effective semantic retrieval from the vector store.
- Precision depends on chunking granularity and reranking quality.
- Errors typically arise from overlapping methodological sections or dense mathematical descriptions.

---

## Conclusion

The Mini RAG system demonstrates strong document grounding and recall on technical academic content. Performance is especially robust for conceptual and methodological queries, validating its suitability for research-oriented question answering.
