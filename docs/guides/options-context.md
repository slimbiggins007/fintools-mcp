# Options Context

Use this workflow when the chart may look interesting but the options chain may not be usable.

Options context is a Fintools Pro workflow.

## Prompt

```text
Use Fintools Pro. For AMD, CRWD, and SCHW, check market context first, then options-chain context. Separate chart quality from options tradability. Include liquidity caveats and a Not checked section.
```

## What Good Looks Like

The assistant should separate:

- chart/trend context
- day/session context
- options-chain context
- liquidity caveats
- expiration assumptions
- what was not checked

Options-chain context is not an instruction to trade. It is one more filter in the research process.

## Broker Boundary

For executable quotes, account positions, fills, and order routing, use your broker or account system. Fintools does not place trades and does not replace broker truth.
