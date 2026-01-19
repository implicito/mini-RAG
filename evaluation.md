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

**Answer Given:**
The core problem the paper aims to address in insect pest classification is the challenge posed by limited labelled data and severe class imbalance [1][2][3][4].

---

### Q2.  
**Question:** What is Cost-Focal FixMatch and how does it extend FixMatch?

**Ground Truth (GT):**  
Cost-Focal FixMatch extends FixMatch by introducing class-aware weighting and focal loss to improve minority-class learning under severe imbalance.

**Answer Given:**
Cost-Focal FixMatch is an SSL technique designed to address data imbalance in scenarios with scarce label availability. It extends the FixMatch framework by incorporating class-balanced weighting and focal loss [1][2]. This pipeline enhances the contribution of underrepresented classes while mitigating the dominance of majority classes [3][4].

---

### Q3.  
**Question:** Which datasets are used for evaluation and how are they structured?

**Ground Truth (GT):**  
The study uses Repurposed IP102 (4 life stages) and Mixed IP102 (167 combined species–stage classes), with validation data treated as labeled and training data as unlabeled.

**Answer Given:**
The Mixed IP102 dataset is used for evaluation, comprising 38,171 training images, 6,320 validation images, and 19,839 test images across 167 classes [1][2]. The test subset is preserved to enable unbiased model evaluation. The validation subset is used as the primary labelled data, and the original training subset is designated as the unlabelled dataset to simulate limited annotation scenarios [1][2]. The Mixed IP102 dataset is structured with a 6:1:3 partition between the subsets, with the validation subset used for training and the original training subset used as unlabelled data [1][2].

---

### Q4.  
**Question:** What evaluation metrics are used to assess model performance?

**Ground Truth (GT):**  
Accuracy, Precision, Recall, and F1-score computed from TP, FP, FN, and TN.

**Answer Given:**

The evaluation metrics used to assess model performance are Accuracy [1][2], Precision [1][2], Recall [1][2], and F1-score [1][2][3].
---

### Q5.  
**Question:** How does the proposed method improve performance on minority classes?

**Ground Truth (GT):**  
It significantly improves recall for minority classes (e.g., Larva, Pupa, Egg) by generating higher-quality pseudo-labels and focusing learning on hard examples.

**Answer Given:**

The proposed method improves performance on minority classes by employing a cost-sensitive focal loss for unlabelled data, which suppresses the influence of noisy pseudo-labels and enables more effective model training [3]. This approach also indirectly benefits minority classes by lowering mislabelling errors [3]. Additionally, the method uses a dual-loss strategy, which guides supervised learning from labelled data and emphasises learning from hard-to-classify unlabelled examples [3].
---

## Precision and Recall Calculation

For each query:

- **Relevant Chunks (R):** Chunks that truly contain information needed to answer the query.
- **Retrieved Chunks (K):** Chunks returned by the retriever.
- **Correctly Retrieved (C):** Retrieved chunks that are relevant.

### Precision
\[
\text{Precision} = C/K
\]

Measures how much of the retrieved information is relevant.

---

### Recall
\[
\text{Recall} = C/R
\]

Measures how much of the relevant information was successfully retrieved.

- High recall indicates effective semantic retrieval from the vector store.
- Precision depends on chunking granularity and reranking quality.
- Errors typically arise from overlapping methodological sections or dense mathematical descriptions.

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

##  Evaluation Metrics Obtained

| Query | Retrieved Chunks | Relevant Chunks | Precision@k | Recall |
|------|------------------|-----------------|-------------|----------------|
| Q1   | 4                | 2               | 0.50        | 1.00           |
| Q2   | 4                | 2               | 0.50        | 1.00           |
| Q3   | 4                | 1               | 0.25        | 1.00           |
| Q4   | 4                | 1               | 0.25        | 1.00           |
| Q5   | 4                | 1               | 0.25        | 1.00           |


---

## Conclusion

The Mini RAG system demonstrates strong document grounding and recall on technical academic content. Performance is robust for conceptual and methodological queries, validating its suitability for research-oriented question answering.
