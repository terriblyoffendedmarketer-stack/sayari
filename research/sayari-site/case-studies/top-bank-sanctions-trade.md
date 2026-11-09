# Top Bank Sanctions Trade

Source: https://sayari.com/resources/case-studies/top-bank-sanctions-trade/
Published: 2026-05-05
Type: case-study (anonymized)

## Top 3 U.S. Bank

Graph-based entity resolution cut wasted analyst time on false positives; every cleared alert now carries a documented evidence chain.
90-95% Analyst time on false positives (industry benchmark) · $1.5B OFAC penalties in 2023 · 10.6B+ Source records

## The challenge

Global sanctions enforcement entered a new era after 2022. Coordinated Western sanctions on Russia, expanded OFAC designations, and secondary sanctions on intermediary jurisdictions created an exponential increase in screening obligations. For the largest banks, the math broke: more entities on more lists, multiplied by more transactions, produced more alerts than any team could process.

The vast majority of analyst time (by widely cited industry benchmarks, 90 to 95%) went to clearing false positives. Analysts spent their days confirming that a shipping company in Singapore was not, in fact, a sanctioned individual in Tehran. The work was manual, repetitive, and increasingly unsustainable as list volumes grew.

- Coordinated Russia sanctions + expanded OFAC + secondary sanctions = exponential alert growth
- 90-95% of analyst time clearing false positives, not investigating actual risk
- Legacy keyword-matching could not disambiguate complex entity structures
- Either double headcount or accept material risk of a missed sanctions hit

## The solution

Thesis: resolving entities against a connected graph of 10.6B+ source records (corporate registries, ownership chains, sanctions lists across 250+ jurisdictions) can disambiguate entities that keyword matching cannot. Evaluated on resolution accuracy, source transparency for audit documentation, and API throughput; a structured pilot tested the highest-volume alert categories.

## Results

Analysts who spent their time confirming false positives now focus on actual risk analysis. Every match, and every non-match, carries a documented evidence chain. The operation scales with sanctions list growth rather than against it.

> "When the next wave of designations hits, the team has the resolution infrastructure to absorb the volume without breaking." (Head of Sanctions Compliance, Top 3 U.S. Bank)
