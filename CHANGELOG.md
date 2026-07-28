# Changelog

## 0.6.2

- Route paid-tool upgrade responses to the live Fintools MCP page on Whop.
- Match the public paid-tool stub signatures to Fintools MCP 1.0.1.
- Return a clean JSON error for unknown tickers or quote-provider failures.
- Pin the MCP SDK below version 2 to preserve the current FastMCP import path.

## 0.6.1

- Point paid-tool responses at the live Fintools MCP checkout.
- Include the founding discount code in paid-tool responses.

## 0.6.0

- Make the public package a lightweight Fintools connector.
- Keep public runtime functionality to connection check, product info, basic quote, and data/cache status.
- Add hard `upgrade_required` stubs for the market-context tools that ship in the paid Fintools MCP package.
- Remove the analysis and indicator implementations from the public package.
- Rewrite README and VISION around the public connector / paid package boundary.
- Add CLI `--version` and `--about` checks.

## 0.5.0

- Reframe the public package as the open-source Fintools MCP foundation.
- Add the public vision document and product guardrails.
- Keep the public package limited to the already-public basic analysis tools.
- Add optional Public.com daily-bar support via user-supplied credentials.
- Add file-backed caching and provider request counters.
- Add batched yfinance bar fetches for faster screening and comparison workflows.
- Remove personal credential-path fallback from the public package.
- Remove an unavailable unused dependency from package metadata so fresh installs work.
