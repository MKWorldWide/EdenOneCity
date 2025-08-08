/**
 * Architectural preamble:
 * Entrypoint for Serafina, the Discord router. Handles slash commands, message
 * parsing, and bridges dispatches into the Unity guardian bus via HTTP.
 * Follows a modular, event-driven design so new command modules can drop in
 * without polluting core logic.
 */

import 'dotenv/config';
import {
  Client,
  GatewayIntentBits,
  Partials,
  REST,
  Routes,
  InteractionType,
} from 'discord.js';
import fetch from 'node-fetch';
import { sendCouncilReport, scheduleNightlyCouncilReport } from './nightlyReport.js';
import { createHandshakeRouter, performHandshakes } from './handshake.js';
import { startHeartbeat } from './uptime.js';

const TOKEN = process.env.DISCORD_TOKEN!;
const GUILD_ID = process.env.GUILD_ID!;
const BUS_URL = process.env.BUS_URL || 'http://localhost:8080';
const BUS_TOKEN = process.env.BUS_TOKEN; // shared secret for Unity relay
const PORT = Number(process.env.PORT || 3000); // HTTP server port for handshake

/** Post a whisper to the Unity bus */
async function relayToUnity(to: string, message: string, from = 'Serafina') {
  try {
    await fetch(`${BUS_URL}/whisper`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(BUS_TOKEN ? { Authorization: `Bearer ${BUS_TOKEN}` } : {}),
      },
      body: JSON.stringify({ from, to, message }),
    });
  } catch (err) {
    console.error('Failed to relay to Unity bus:', err);
  }
}

// Discord client with guild message and interaction intents
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
  ],
  partials: [Partials.Channel],
});

// Start handshake HTTP server immediately so peers can reach us
const handshakeServer = createHandshakeRouter();
handshakeServer.listen(PORT, () =>
  console.log(`Handshake server listening on ${PORT}`)
);

client.once('ready', async () => {
  console.log(`Serafina online as ${client.user?.tag}`);
  scheduleNightlyCouncilReport(client);
  startHeartbeat(client);
  await performHandshakes();
});

// Register slash command
const rest = new REST({ version: '10' }).setToken(TOKEN);
async function registerCommands() {
  await rest.put(Routes.applicationGuildCommands(client.user!.id, GUILD_ID), {
    body: [
      {
        name: 'councilreport',
        description: 'Send the ShadowFlower council report now',
      },
    ],
  });
}

client.on('interactionCreate', async (interaction) => {
  if (interaction.type !== InteractionType.ApplicationCommand) return;
  if (interaction.commandName === 'councilreport') {
    await interaction.deferReply({ ephemeral: true });
    await sendCouncilReport(client);
    await interaction.editReply('Council report dispatched.');
  }
});

client.on('messageCreate', async (msg) => {
  // ignore bot messages
  if (msg.author.bot) return;

  // pattern: !to GuardianName message
  const match = msg.content.match(/^!to\s+(\w+)\s+(.+)/);
  if (match) {
    const [, guardian, text] = match;
    await relayToUnity(guardian, text, msg.author.username);
  }
});

client.login(TOKEN).then(() => registerCommands());
