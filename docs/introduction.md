# Introduction

Fintools is agent-native market-analysis tooling for traders who use AI assistants.

The point is simple: an AI assistant should not invent prices, levels, trend context, options context, sizing math, or setup quality. It should call tools, use the computed output, and state clearly what was not checked.

Fintools is not a broker. It does not place trades. It does not connect to an account. It does not provide buy, sell, or hold recommendations. Trader judgment stays with the user.

## The Product

Fintools MCP is a paid local MCP package. It gives Claude, Codex, Cursor, and other MCP-compatible assistants read-only market-analysis tools:

- quotes and day context
- trend scores
- technical indicators
- support/resistance
- screens and breakout discovery
- winner-similarity ranking
- ticker comparison
- options-chain context
- sizing math
- trade-stat review
- playbooks and report structure

The public package in this repository is only the connector and documentation surface. It proves the MCP connection works and returns a basic quote. The full desk ships in the paid Fintools MCP download.

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
