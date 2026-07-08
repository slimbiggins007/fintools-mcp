# Media Kit

Use this checklist for GitHub attachments, Lemon Squeezy product media, and X/LinkedIn launch posts.

Do not record private account information, broker/account output, scan-log paths, private research files, or anything from a live trading account.

## Assets To Capture

### 1. GitHub / Public Connector

Capture:

- GitHub repo landing page
- PyPI page showing the latest `fintools-mcp` version
- terminal install: `pip install fintools-mcp`
- assistant prompt: `Check the Fintools connection.`
- assistant prompt: `Get a basic quote for SPY.`
- assistant prompt that hits the paid-package boundary: `What's SPY's trend score?`

Message:

```text
The public connector proves the MCP connection works and refuses to invent analysis it does not include.
```

### 2. Fintools MCP Desk

Capture from a clean, non-prod demo environment:

- Fintools MCP zip contents
- `START_HERE.md`
- playbooks folder
- one Fintools MCP output showing computed trend/day/candidate context
- one Fintools MCP output showing a clear `Not checked` section

Message:

```text
Fintools MCP is the local market-context desk: computed numbers, explicit caveats, no trade recommendations.
```

### 3. Lemon Squeezy

Recommended product image size:

```text
1600 x 1200
```

Ready asset:

```text
docs/assets/fintools-mcp-card.png
```

Good frames:

- product card: Fintools MCP
- zip contents
- `START_HERE.md`
- paid-package boundary
- sample report excerpt with numbers visible and account/private fields absent

### 4. X / LinkedIn

Good launch assets:

- one screenshot of the public connector returning `upgrade_required`
- one screenshot of Fintools MCP answering with tool-grounded analysis
- one screenshot of the playbook folder
- one short clip from install to first report

Avoid:

- performance claims
- account screenshots
- broker screenshots
- performance promises
- trade-instruction language

## Demo Clip Structure

Keep the first clip under 45 seconds.

1. Install the public connector.
2. Ask for a basic quote.
3. Ask for a full-desk workflow.
4. Show the honest paid-package boundary.
5. Show Fintools MCP running the same kind of request with computed output.
6. End on the Lemon Squeezy checkout link and `FOUNDING` code.

## Safe Demo Environment

Use a dedicated demo session. Do not use the production trading workspace.

For Fintools MCP recordings, use isolated demo configuration and disable or isolate scan logs. Do not show private research files or live account data.

## Launch Copy Guardrail

Use language like:

```text
Fintools turns AI assistants into a read-only market-analysis desk. The public connector proves the MCP connection works. The paid package contains the computed market-context tools and playbooks.
```

Do not use language like:

```text
This finds winning trades.
This tells you what to buy.
```
