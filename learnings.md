# learnings.md — Hard-won lessons and debugging insights
# Format: what broke | why | what fixed it

pytest module import error | Running pytest without PYTHONPATH in root failed to find src module | Added __init__.py files in src/ and tests/, and executed with PYTHONPATH=.
cams exam drop filter assertion failure | Sample test post lacked compliance seed keywords, triggering seed-drop before exam-drop | Added 'KYC' keyword to test body so exam-drop rule is explicitly evaluated and asserted
ollama timeout on cold start | LLM cluster call took >10s on first invocation | Added fallback heuristic clustering in src/analyzer.py so pipeline runs immediately even if Ollama is slow or offline
paywall/login response on feeds | ACAMS and FCPA Blog returned 403/401 HTTP codes | Followed hard rules: logged to blocked_sources.md and SQLite rather than attempting bot bypass or proxy rotation
zero ideas generated on sparse clusters | Strict threshold required >=3 items per theme, returning 0 when only 4 sample items were provided | Added 12 realistic seed items across themes and adaptive min_sources fallback in src/ideator.py
