# Guardrails

Fintools is built around one rule: AI assistants should not invent market numbers.

## Principles

- Every market or technical figure should come from tool output.
- If something was not checked, say it was not checked.
- The tools are read-only.
- The tools do not place trades.
- The tools do not route orders.
- The tools do not manage accounts.
- The tools do not provide buy, sell, or hold recommendations.
- Trader judgment stays with the user.

## Not Checked Is A Feature

A market report is safer when it clearly says what was not verified.

Examples:

- earnings date not checked
- live options quality not checked
- news not checked
- account position not checked
- broker tradability not checked

That is not weakness. It is the system refusing to pretend.

## Data Boundary

Fintools is not a raw-data vendor. It computes market context from the buyer's local setup and available data sources.

If a user needs licensed institutional data, they should bring that data through their own permitted setup. Fintools should not be used to resell or redistribute raw market data.

## Trading Boundary

Fintools is research software. It is not broker truth.

You can layer your own broker API, broker MCP, or account system into the same AI assistant workflow, but that layer is separate from Fintools. Use it for:

- account balances
- open positions
- live executable quotes
- order routing
- fills
- options execution quality

Use Fintools for computed market context and structured research. Fintools itself remains read-only and does not route orders.
