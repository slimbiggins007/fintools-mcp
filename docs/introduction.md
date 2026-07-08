# Introduction

Fintools is agent-native market-analysis tooling for traders who use AI assistants.

The point is simple: an AI assistant should not invent prices, levels, trend context, options context, sizing math, or setup quality. It should call tools, use the computed output, and state clearly what was not checked.

Fintools is not a broker. It does not place trades. It does not connect to an account. It does not provide buy, sell, or hold recommendations. Trader judgment stays with the user.

## The Product Shape

Fintools has two surfaces.

| Surface | Role |
|---|---|
| Fintools Core | Free public MCP connector. It verifies the install and provides basic quote/status tools. |
| Fintools Pro | Paid local market-context desk. It contains the tools and playbooks for real research workflows. |

Core is intentionally small. It is the public doorway.

Pro is the desk: trend gates, chart context, support/resistance, screens, breakout discovery, market snapshots, day-context flags, options context, sizing math, candidate ranking, and playbooks.

## Why It Exists

AI assistants are useful for synthesis, but market work has a hard failure mode: plausible prose around invented numbers.

Fintools exists to make the assistant show its work:

1. The user asks a market question.
2. The assistant calls read-only tools.
3. The tools compute the market figures.
4. The assistant explains what was checked, what was not checked, and what the data says.
5. The user decides.

## What This Is Not

Fintools is not:

- a hedge fund
- a signal service
- a broker
- a managed account product
- a raw-data resale API
- a promise of trading performance
- a replacement for trader judgment

It is a local tool layer for computed market context.
