# Changelog

## 0.6.0

- Demote Fintools Core to a free connector/demo tier.
- Keep Core runtime functionality to connection check, product info, basic quote, and data/cache status.
- Add hard `upgrade_required` stubs for the market-context tools that now belong in Fintools Pro.
- Remove the analysis and indicator implementations from the public Core package.
- Rewrite README and VISION around the Core/Pro split.
- Add CLI `--version` and `--about` checks.

## 0.5.0

- Reframe the public package as Fintools Core: the free, open-source MCP foundation.
- Add the public vision document and product guardrails.
- Keep Core limited to the already-public basic analysis tools.
- Add optional Public.com daily-bar support via user-supplied credentials.
- Add file-backed caching and provider request counters.
- Add batched yfinance bar fetches for faster screening and comparison workflows.
- Remove personal credential-path fallback from the public Core package.
- Remove an unavailable unused dependency from package metadata so fresh installs work.
