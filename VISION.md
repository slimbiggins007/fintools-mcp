# Fintools Vision

Fintools is agent-native market analysis infrastructure.

The goal is simple: give AI assistants computed market-context tools so they do not invent prices, levels, trend context, options context, sizing math, or setup quality.

Fintools is not an AI hedge fund. It is not a signal service. It is not a broker. It is not a raw financial data vendor. It is a read-only tool layer that lets traders and AI assistants ask market questions and get answers grounded in tool output.

## Core And Pro

Fintools has two product surfaces:

- **Fintools Core**: the free, open-source MCP connector in this repository. Core proves the local MCP connection works and provides basic quote/status functionality.
- **Fintools Pro**: the paid local market-context and research layer. Pro contains the tools and playbooks meant for real trader workflows.

Core is deliberately small. It should stay stable, trustworthy, and useful for verifying the installation. It is not the market desk.

Pro is where Fintools' analysis work belongs: trend gates, day context, breakout discovery, custom screens, support/resistance, options context, sizing math, candidate ranking, playbooks, future memory, and future calibration.

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

## What Core Is For

Core gives MCP-compatible assistants a small free connector:

- connection check
- product and edition info
- basic stock quote
- data-source and cache visibility
- clear `upgrade_required` boundaries for Pro tools

Core exists so a user can confirm that Fintools works in their AI assistant before deciding whether they want the full desk.

## What Pro Is For

Pro is the market-context and research layer:

- trend score
- technical indicators and chart context
- support/resistance
- breakout discovery
- custom screens
- ticker comparison
- options-chain context
- position sizing and ATR sizing
- market snapshot and day-context gates
- winner-similarity candidate ranking
- desk playbooks and report workflows

The model is not "AI makes the trade." The model is:

1. The trader asks a market question.
2. The AI calls read-only Fintools tools.
3. The tools compute the numbers.
4. The AI explains what was checked, what was not checked, and what the data says.
5. The trader decides.
