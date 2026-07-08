# Watchlist Review

Use this workflow when you already have names and want to know what changed.

Watchlist review is a Fintools MCP workflow.

## Prompt

```text
Use Fintools MCP. Review this watchlist: SPY, QQQ, AMD, CRWD, HOOD, ANET, DDOG, FTNT. For each name, check trend context, day context, relevant levels, and candidate-quality flags. Group them into focus, watch, early, stand aside, or reject. Include a Not checked section.
```

## What Good Looks Like

A watchlist review should answer:

- Which names still deserve attention?
- Which names weakened?
- Which names are extended or messy?
- Which names need a clean reclaim or better level?
- Which checks were not run?

It should not tell the user what to buy or sell.

## Manual Diff

If you have yesterday's report, paste it with today's request:

```text
Use Fintools MCP. Compare today's watchlist review against the report pasted below. Tell me what changed, what improved, what deteriorated, and what was not checked.
```

That is the manual version of the future memory-backed workflow.
