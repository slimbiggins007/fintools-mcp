# Fintools Vision

Fintools is agent-native market analysis infrastructure.

The goal is simple: give AI assistants computed market-context tools so they do not invent prices, levels, trend context, options context, sizing math, or setup quality.

Fintools is not an AI hedge fund. It is not a signal service. It is not a broker. It is not a raw financial data vendor. It is a read-only tool layer that lets traders and AI assistants ask market questions and get answers grounded in tool output.

## Product Shape

Fintools MCP is the product: a local, read-only market-analysis toolbelt for Claude, Codex, Cursor, and other MCP-compatible assistants.

The public repository provides a small connector and documentation hub. It proves the MCP wiring works and gives people a safe way to inspect the project.

The paid Fintools MCP package contains the complete desk:

- market snapshots and day-context gates
- trend scores and technical context
- support/resistance
- breakout discovery
- custom screens
- ticker comparison
- options-chain context
- position sizing and ATR sizing
- trade-stat calculations
- winner-similarity candidate ranking
- playbooks, templates, sample reports, and methodology

There is no separate AI trader and no separate broker product. Fintools is the local market-analysis layer. Trader judgment stays with the user.

## Principles

- The AI never invents market or technical numbers.
- Every market or technical figure should come from tool output.
- Read-only by design.
- No broker execution.
- No trade recommendations.
- No raw data resale.
- Bring your own data access or credentials where needed.
- Explicit "not checked" caveats are a feature, not a weakness.
- Trader judgment stays with the user.

## Broker Boundary

Fintools is broker-agnostic. It can sit next to a user's own broker API, broker MCP, or account system. That lets the user's AI assistant combine Fintools market context with broker-side account truth, live executable quotes, positions, fills, and order-routing capability if the user has built or connected that layer.

Use Fintools for:

- historical bars
- trend and chart context
- scans and ranking
- market snapshots
- options research context
- sizing math
- report structure

Use a broker API, broker MCP, or account system for:

- account equity
- positions
- live executable quotes
- order routing
- fills and realized P&L

Fintools does not ship that broker layer and does not place trades. It supplies the market-analysis context that can be layered beside broker truth.

## Operating Model

The model is not "AI makes the trade." The model is:

1. The trader asks a market question.
2. The AI calls read-only Fintools tools.
3. The tools compute the numbers.
4. The AI explains what was checked, what was not checked, and what the data says.
5. The trader decides.
