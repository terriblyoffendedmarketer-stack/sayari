# learnings.md — Hard-won lessons and debugging insights
# Format: what broke | why | what fixed it

pytest module import error | Running pytest without PYTHONPATH in root failed to find src module | Added __init__.py files in src/ and tests/, and executed with PYTHONPATH=.
cams exam drop filter assertion failure | Sample test post lacked compliance seed keywords, triggering seed-drop before exam-drop | Added 'KYC' keyword to test body so exam-drop rule is explicitly evaluated and asserted
ollama timeout on cold start | LLM cluster call took >10s on first invocation | Added fallback heuristic clustering in src/analyzer.py so pipeline runs immediately even if Ollama is slow or offline
paywall/login response on feeds | ACAMS and FCPA Blog returned 403/401 HTTP codes | Followed hard rules: logged to blocked_sources.md and SQLite rather than attempting bot bypass or proxy rotation
zero ideas generated on sparse clusters | Strict threshold required >=3 items per theme, returning 0 when only 4 sample items were provided | Added 12 realistic seed items across themes and adaptive min_sources fallback in src/ideator.py
github push protection rejection | Git history contained a commit with the Apify token in src/collectors/apify.py | Reset commits before the secret was introduced, moved token to gitignored .env and GitHub Actions secrets, and recommitted cleanly
github pages 404 on initial enable | GitHub Pages repository creation defaults to off on free accounts | Enabled Pages via gh api with build_type=workflow and added automated upload-pages-artifact step to the workflow
TypeError in renderLexicon | is_vendor_marketing_only was integer 0/1 causing .includes() failure | Cast to String and checked both string and numeric equality
PWA stale viewer cache | Browsers cached index.html via service worker preventing live GitHub Pages updates | Versioned service worker to sayari-radar-v3 and set cache-bypass on navigation requests
GitHub push conflict with scheduled runs | Scraper committing to master conflicted with local push | Separated deploy-pages on push from scheduled scraper sweeps
Infinite auto-refresh loop in viewer | sw.js?t=Date.now() triggered continuous controllerchange events with location.reload() | Removed location.reload() and dynamic query timestamp; simplified SW registration to static ./sw.js
HTML attribute quotation breakout on copy button | Passing JSON.stringify into onclick broke HTML tag attributes and exposed raw JS code | Made OPINION_MAP global and passed clean numeric opIdx to copyOpinionPrompt
