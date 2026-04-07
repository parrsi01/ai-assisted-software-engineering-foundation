# Capstone Project Ideas

---

## 1. CLI Expense Tracker
Store expenses (category, amount, date, note) in a JSON file. Commands: `add`, `list`, `summary` (by category/month), `export csv`. Test with unittest.

## 2. URL Shortener Service
FastAPI backend: POST `/shorten` returns a short code, GET `/{code}` redirects. Store in SQLite. Include expiry, hit counter, and basic auth.

## 3. Log Analyzer
Parse Apache/Nginx access logs. Report: top IPs, top paths, status code distribution, requests per hour, potential brute-force detection (>100 reqs/min from single IP).

## 4. Task Queue
Thread-safe priority task queue. Workers consume tasks concurrently. Supports: priority levels, task cancellation, retry on failure, progress reporting.

## 5. Mini Key-Value Store
TCP server accepting GET/SET/DEL/KEYS commands. Persistence: append-only log file + compaction. Configurable in-memory LRU cache layer.

## 6. Data Pipeline
Read CSV → validate → transform (normalize, enrich) → write Parquet/JSON. Configurable transforms via YAML. Error rows written to separate file with reason.

## 7. Web Scraper with Rate Limiting
asyncio + aiohttp scraper with configurable concurrency, retry logic, and politeness delay. Output: structured JSON per page.

## 8. Binary Protocol Parser
Parse a custom binary protocol (TLV format). Encoder and decoder. Fuzzer that generates random valid and invalid packets. Suitable for IPC or network protocol design.

## 9. Distributed Task Scheduler (Simulated)
Multiple worker processes coordinated via multiprocessing queues. Master assigns tasks, workers report results, master aggregates. Fault tolerance: dead worker detection and task reassignment.

## 10. Compiler Front-End (Mini Language)
Lexer → parser → AST → interpreter for a simple expression language supporting variables, arithmetic, if/else, and while loops. AST pretty-printer included.
