"""
Question-answering using retrieved chunks.
LLM: Groq (LLaMA 3.1)
Strictly grounded answers with explicit citations.
"""

import os
import re
from typing import List, Dict, Any
from groq import Groq


class QAGenerator:
    """
    Generates answers from retrieved chunks using Groq.
    Enforces grounding and structured citations.
    """

    def __init__(self, api_key: str = None):
        api_key = api_key or os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set")

        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-8b-instant"

    def generate_answer(
        self,
        query: str,
        chunks: List[Dict[str, Any]]
    ) -> Dict[str, Any]:

        # ---- SAFETY ----
        if not chunks:
            return {
                "answer": "No answer found in provided documents.",
                "citations": [],
                "sources": []
            }

        # ---- INDEX CHUNKS EXPLICITLY ----
        indexed_chunks = []
        for i, chunk in enumerate(chunks, start=1):
            indexed_chunks.append({
                "chunk_index": i,
                "text": chunk["text"],
                "source": chunk["source"],        
                "section": chunk.get("section", "unknown"),
                "position": chunk.get("position", -1),
            })


        # ---- BUILD CONTEXT ----
        context_blocks = []
        for c in indexed_chunks:
            context_blocks.append(
                f"[{c['chunk_index']}] {c['text']}"
            )

        context = "\n\n".join(context_blocks)

        # ---- PROMPTS ----
        system_prompt = ("""
          You are a retrieval-grounded assistant.

            STRICT RULES:
            1. Use ONLY the provided chunks as evidence.
            2. Do NOT copy references, citations, or bracketed numbers that appear inside the source text. The ONLY allowed citations are chunk numbers you add yourself: [1], [2], [3], etc.
            3. When you use information from chunk i, cite it ONLY as [i].
            4. If multiple chunks support a sentence, use multiple citations like [1][2].
            5. Paraphrase where possible; do not quote long passages verbatim.
            6. If the answer is not at all contained /related to text in the chunks, say:
            "No answer found in provided documents.
            """


        )

        user_prompt = (
            f"Context:\n{context}\n\n"
            f"Question: {query}\n\n"
            "Answer concisely with inline citations."
        )

        # ---- LLM CALL ----
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,
        )

        answer = response.choices[0].message.content.strip()

        # ---- EXTRACT CITATION NUMBERS ----
        citation_numbers = sorted(
            set(int(n) for n in re.findall(r"\[(\d+)\]", answer))
        )

        citations = []
        sources = []
        seen_sources = set()

        # ---- BUILD CITATIONS ----
        for num in citation_numbers:
            chunk = next(
                (c for c in indexed_chunks if c["chunk_index"] == num),
                None
            )
            if not chunk:
                continue

            citations.append({
                "number": num,
                "chunk_index": chunk["chunk_index"],
                "source": chunk["source"],
                "section": chunk["section"],
                "position": chunk["position"],
                "excerpt": chunk["text"][:300].strip() + "..."
            })

            src_key = (chunk["source"], chunk["section"], chunk["position"])
            if src_key not in seen_sources:
                seen_sources.add(src_key)
                sources.append({
                    "source": chunk["source"],
                    "section": chunk["section"],
                    "position": chunk["position"]
                })

        # ---- GUARANTEED SCHEMA ----
        return {
            "answer": answer,
            "citations": citations,   
            "sources": sources        
        }
