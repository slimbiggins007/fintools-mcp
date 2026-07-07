# Fintools Vision

Fintools is agent-native market analysis infrastructure.

The goal is simple: give AI assistants computed market-analysis tools so they do not invent prices, indicators, levels, options context, sizing math, or trend statistics.

Fintools is not an AI hedge fund. It is not a signal service. It is not a broker. It is not a raw financial data vendor. It is a read-only tool layer that lets traders and AI assistants ask market questions and get answers grounded in tool output.

## Core And Pro

Fintools has two product surfaces:

- **Fintools Core**: the free, open-source MCP server in this repository. Core proves the tool layer works and provides basic local market-analysis primitives.
- **Fintools Pro**: the paid local market desk layer. Pro contains the private judgment tools, playbooks, and future engines for deeper daily analysis.

Core should stay useful, stable, and trustworthy. Pro is where advanced workflow logic, market-desk judgment, memory, calibration, and future paid engines belong.

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

Core gives MCP-compatible assistants a basic local financial-analysis toolbelt:

- quotes and historical bars
- technical indicators
- trend scores
- support and resistance
- screening
- ticker comparison
- options chain context
- position-sizing math
- trade-stat calculations
- data-source and cache visibility

Core is deliberately limited. It is the foundation and public trust layer, not the full market desk.

## What Fintools Is Building Toward

The long-term direction is an AI-native market analysis operating layer: local tools, structured workflows, watchlist context, calibration logs, report memory, and guardrails that keep AI assistants honest.

The model is not "AI makes the trade." The model is:

1. The trader asks a market question.
2. The AI calls read-only Fintools tools.
3. The tools compute the numbers.
4. The AI explains what was checked, what was not checked, and what the data says.
5. The trader decides.
