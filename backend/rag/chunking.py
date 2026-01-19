"""
Sentence-aware chunking with configurable size and overlap.
Chunks are 800-1200 tokens with 10-15% overlap.
"""
import tiktoken
from typing import List, Dict, Any
import re


class SentenceAwareChunker:
    """
    Chunks text using sentence boundaries while respecting token limits.
    Target: 800-1200 tokens per chunk, 10-15% overlap.
    """
    
    def __init__(
        self,
        min_tokens: int = 800,
        max_tokens: int = 1200,
        overlap_ratio: float = 0.12  # 12% overlap (middle of 10-15%)
    ):
        self.min_tokens = min_tokens
        self.max_tokens = max_tokens
        self.overlap_ratio = overlap_ratio
        # Use cl100k_base encoding (GPT-4 tokenizer)
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def _count_tokens(self, text: str) -> int:
        """Count tokens in text."""
        return len(self.encoding.encode(text))
    
    def _split_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences using regex.
        Handles common sentence endings: . ! ? followed by space or newline.
        """
        # Pattern: sentence ending followed by whitespace or end of string
        pattern = r'([.!?]+)\s+'
        sentences = re.split(pattern, text)
        
        # #region agent log
        import json
        import time
        with open(r'e:\miniRAG\.cursor\debug.log', 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"V","location":"chunking.py:32","message":"After regex split","data":{"text_length":len(text),"split_count":len(sentences),"split_preview":sentences[:5] if sentences else []},"timestamp":int(time.time()*1000)})+"\n")
        # #endregion
        
        # Recombine sentences with their punctuation
        result = []
        for i in range(0, len(sentences) - 1, 2):
            if i + 1 < len(sentences):
                result.append(sentences[i] + sentences[i + 1])
            else:
                result.append(sentences[i])
        
        # Handle last sentence if odd number of splits
        if len(sentences) % 2 == 1:
            result.append(sentences[-1])
        
        final_result = [s.strip() for s in result if s.strip()]
        
        # #region agent log
        with open(r'e:\miniRAG\.cursor\debug.log', 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"W","location":"chunking.py:53","message":"After sentence recombination","data":{"result_count":len(final_result),"result_preview":final_result[:3] if final_result else []},"timestamp":int(time.time()*1000)})+"\n")
        # #endregion
        
        return final_result
    
    def chunk(
        self,
        text: str,
        source: str = "unknown",
        title: str = "unknown",
        section: str = "unknown"
    ) -> List[Dict[str, Any]]:
        """
        Chunk text into overlapping segments with metadata.
        
        Args:
            text: Input text to chunk
            source: Source identifier (filename, URL, etc.)
            title: Document title
            section: Section identifier
        
        Returns:
            List of chunk dictionaries with text and metadata
        """
        # #region agent log
        import json
        import time
        with open(r'e:\miniRAG\.cursor\debug.log', 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"Q","location":"chunking.py:55","message":"Chunk entry","data":{"text_length":len(text) if text else 0,"text_stripped_length":len(text.strip()) if text else 0,"text_is_none":text is None},"timestamp":int(time.time()*1000)})+"\n")
        # #endregion
        
        if not text.strip():
            # #region agent log
            with open(r'e:\miniRAG\.cursor\debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"R","location":"chunking.py:77","message":"Text is empty after strip","data":{},"timestamp":int(time.time()*1000)})+"\n")
            # #endregion
            return []
        
        sentences = self._split_sentences(text)
        
        # #region agent log
        with open(r'e:\miniRAG\.cursor\debug.log', 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"S","location":"chunking.py:79","message":"After split_sentences","data":{"sentences_count":len(sentences) if sentences else 0,"sentences_is_none":sentences is None,"sentences_is_empty":sentences == []},"timestamp":int(time.time()*1000)})+"\n")
        # #endregion
        
        if not sentences:
            # #region agent log
            with open(r'e:\miniRAG\.cursor\debug.log', 'a', encoding='utf-8') as f:
                f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"T","location":"chunking.py:80","message":"No sentences after split","data":{},"timestamp":int(time.time()*1000)})+"\n")
            # #endregion
            return []
        
        chunks = []
        current_chunk = []
        current_tokens = 0
        chunk_position = 0
        
        for sentence in sentences:
            sentence_tokens = self._count_tokens(sentence)
            
            # If adding this sentence would exceed max_tokens
            if current_tokens + sentence_tokens > self.max_tokens and current_chunk:
                # Save current chunk if it meets minimum size
                if current_tokens >= self.min_tokens:
                    chunk_text = " ".join(current_chunk)
                    chunks.append({
                        "text": chunk_text,
                        "source": source,
                        "title": title,
                        "section": section,
                        "position": chunk_position,
                        "token_count": current_tokens
                    })
                    chunk_position += 1
                    
                    # Calculate overlap: keep last N sentences that fit in overlap window
                    overlap_tokens = int(current_tokens * self.overlap_ratio)
                    overlap_sentences = []
                    overlap_count = 0
                    
                    # Build overlap from end of current chunk
                    for s in reversed(current_chunk):
                        s_tokens = self._count_tokens(s)
                        if overlap_count + s_tokens <= overlap_tokens:
                            overlap_sentences.insert(0, s)
                            overlap_count += s_tokens
                        else:
                            break
                    
                    # Start new chunk with overlap
                    current_chunk = overlap_sentences
                    current_tokens = overlap_count
                else:
                    # Chunk too small, continue building
                    pass
            
            # Add sentence to current chunk
            current_chunk.append(sentence)
            current_tokens += sentence_tokens
        
        # Add final chunk - always include it even if below min_tokens (to avoid losing content)
        if current_chunk and current_tokens > 0:
            chunk_text = " ".join(current_chunk)
            chunks.append({
                "text": chunk_text,
                "source": source,
                "title": title,
                "section": section,
                "position": chunk_position,
                "token_count": current_tokens
            })
        
        # #region agent log
        with open(r'e:\miniRAG\.cursor\debug.log', 'a', encoding='utf-8') as f:
            f.write(json.dumps({"sessionId":"debug-session","runId":"run1","hypothesisId":"U","location":"chunking.py:141","message":"Before return chunks","data":{"chunks_count":len(chunks),"current_chunk_exists":current_chunk is not None and len(current_chunk) > 0,"current_tokens":current_tokens,"min_tokens":self.min_tokens,"meets_min":current_tokens >= self.min_tokens if current_chunk else False},"timestamp":int(time.time()*1000)})+"\n")
        # #endregion
        
        return chunks
