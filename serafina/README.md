# Serafina Router

TypeScript Discord bot coordinating guardians and nightly council report. Bridges
Discord chat into the Unity guardian bus via an authenticated HTTP relay.

## Setup

```bash
cd serafina
npm install
cp .env.example .env
npm run build && npm start
```

### Slash Commands
- `/councilreport` – send council report immediately.

### Environment Variables
See `.env.example` for the full list. At minimum supply `DISCORD_TOKEN`,
`GUILD_ID`, `CHN_COUNCIL`, `MCP_URL`, `BUS_URL` and a matching `BUS_TOKEN` used by
the Unity `HttpWhisperReceiver`.

### Bridging Messages

In Discord, send `!to GuardianName message` to whisper to a Unity guardian. The
router posts the payload to `BUS_URL/whisper` with the bearer `BUS_TOKEN` so only
trusted sources can inject messages.

### Handshake Mesh

On startup Serafina contacts any peers listed in `HANDSHAKE_PEERS` with a simple
HTTP `POST /handshake` request, advertising its capabilities and receiving the
same in response. An embedded Express server also listens on `PORT` for incoming
handshakes so sibling services can discover this node.

### Uptime Hardening

`npm start` launches `scripts/start.js`, which respawns the bot with exponential
backoff if it crashes. A background heartbeat updates Discord presence every 15
minutes to keep the process active on free tiers. For Render deployments, see
the repository's `keepalive` GitHub Action which triggers redeploys via deploy
hooks.

