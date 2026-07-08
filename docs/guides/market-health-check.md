# Market Health Check

Use this workflow when you want broad context before looking at individual names.

## Public Connector Prompt

```text
Use the public Fintools connector. Check the connection, then get basic quotes for SPY, QQQ, IWM, and DIA. Tell me what the public connector could verify and what requires the paid Fintools MCP package.
```

The public connector can verify the connection and fetch basic quotes.

## Fintools MCP Prompt

```text
Use Fintools MCP. Run a market health check on SPY, QQQ, IWM, and DIA. Include trend context, day context, any weak-session flags, and a Not checked section.
```

## Expected Shape

A useful market-health answer should separate:

- broad index context
- trend context
- session/day context
- what changed today
- what was not checked

It should not turn the result into a trade recommendation.
