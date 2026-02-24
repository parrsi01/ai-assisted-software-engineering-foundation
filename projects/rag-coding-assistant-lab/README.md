# RAG Coding Assistant Lab

## Focus Areas

- code/document chunking strategy
- metadata (path, symbol, language, recency)
- retrieval quality vs context budget
- citation requirements
- stale code and index drift risks

## Architecture Pattern

Query -> retriever -> ranked chunks -> prompt assembly -> model -> citations -> verification
