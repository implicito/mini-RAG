"""
Test script for Mini RAG backend
Run: python test_ingest.py
"""

print(">>> test_ingest.py started <<<", flush=True)

import requests
import time
import sys

print("Python:", sys.version, flush=True)

BACKEND_URL = "http://localhost:8000"

SAMPLE_DOC = """
Computer architecture defines the structure and behavior of a computer system.
The CPU consists of the ALU, control unit, and registers.
Cache memory improves performance by storing frequently accessed data close to the CPU.
L1, L2, and L3 caches differ in size and speed.
Virtual memory allows programs to use more memory than physically available.
Paging and segmentation are memory management techniques.
The operating system manages process scheduling and resource allocation.
Context switching enables multitasking.
Interrupts allow hardware devices to signal the CPU.
Pipelining increases instruction throughput.
"""

QUESTIONS = [
    "What is the role of cache memory in computer architecture?",
    "What is virtual memory?",
    "What does an operating system do?",
    "What is context switching?",
    "How does pipelining improve CPU performance?",
]


def test_ingest():
    print("\n[INGEST]", flush=True)

    r = requests.post(
        f"{BACKEND_URL}/ingest",
        data={
            "text": SAMPLE_DOC,
            "source": "arch-os-doc",
        },
        timeout=30,
    )

    print("Status:", r.status_code, flush=True)
    print("Response:", r.text[:200], flush=True)

    r.raise_for_status()
    return r.json()


def test_query(q: str):
    print(f"\n[QUERY]\nQ: {q}", flush=True)

    client_start = time.time()

    r = requests.post(
        f"{BACKEND_URL}/query",
        json={"q": q},
        timeout=60,
    )

    client_latency = (time.time() - client_start) * 1000

    print("Status:", r.status_code, flush=True)
    r.raise_for_status()

    result = r.json()

    print("✓ Answer (preview):")
    print(result["answer"][:200] + "...", flush=True)

    print("\nMetrics:", flush=True)
    print("  Latency (backend):", result.get("latency_ms"), "ms", flush=True)
    print("  Latency (client): ", round(client_latency, 2), "ms", flush=True)
    print("  Token estimate:   ", result.get("token_estimate"), flush=True)
    print("  Retrieved chunks: ", len(result.get("retrieved_ids", [])), flush=True)
    print("  Citations:        ", len(result.get("citations", [])), flush=True)


if __name__ == "__main__":
    try:
        print("\nMini RAG Test Script", flush=True)
        print("=" * 50, flush=True)

        ingest_result = test_ingest()
        print("✓ Ingested chunks:", ingest_result["count"], flush=True)
        print("✓ Collection:", ingest_result["collection_name"], flush=True)

        for q in QUESTIONS:
            test_query(q)

        print("\n✓ TEST COMPLETED SUCCESSFULLY", flush=True)

    except Exception as e:
        print("\n✗ TEST FAILED:", repr(e), flush=True)
        raise
