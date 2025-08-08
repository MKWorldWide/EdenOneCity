/**
 * Architectural preamble:
 * This module centralizes creation and dispatch of the ShadowFlower Council report.
 * It exposes both a scheduler for daily automatic delivery and a direct send function
 * that other modules (e.g., slash commands) can invoke. Network calls are isolated so
 * future transports (GraphQL, gRPC) can swap easily.
 */

import 'dotenv/config';
import fetch from 'node-fetch';
import { EmbedBuilder, TextChannel, Client } from 'discord.js';
import cron from 'node-cron';

const MCP = process.env.MCP_URL!; // MCP server for system status
const COUNCIL_CH = process.env.CHN_COUNCIL!; // Discord channel ID for council messages
const LILY_WEBHOOK = process.env.WH_LILYBEAR; // optional webhook for Lilybear persona
const GH_REPOS = (process.env.NAV_REPOS || '')
  .split(',')
  .map((s) => s.trim())
  .filter(Boolean);

/** Lightweight query to MCP for a one-line status */
async function getMcpStatus(): Promise<string> {
  try {
    const r = await fetch(`${MCP}/ask-gemini`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: 'Summarize system health in one sentence.' }),
    });
    const j = (await r.json().catch(() => ({ response: '(no data)' }))) as any;
    return j.response || '(no data)';
  } catch {
    return '(MCP unreachable)';
  }
}

/** Query GitHub for recent commits; avoids auth by using public API */
async function getRepoDigest(repo: string): Promise<string> {
  const since = new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString();
  const url = `https://api.github.com/repos/${repo}/commits?since=${encodeURIComponent(
    since,
  )}&per_page=5`;
  try {
    const r = await fetch(url, {
      headers: { Accept: 'application/vnd.github+json' },
    });
    if (!r.ok) return `• ${repo}: no recent commits`;
    const commits = (await r.json()) as any[];
    if (!commits.length) return `• ${repo}: 0 commits in last 24h`;
    const lines = commits.map(
      (c) => `• ${repo}@${(c.sha || '').slice(0, 7)} — ${c.commit.message.split('\n')[0]}`,
    );
    return lines.join('\n');
  } catch {
    return `• ${repo}: (error fetching commits)`;
  }
}

/** Compose the report embed for reuse */
async function buildReportEmbed(): Promise<EmbedBuilder> {
  const mcp = await getMcpStatus();
  const repoLines = GH_REPOS.length
    ? (await Promise.all(GH_REPOS.map(getRepoDigest))).join('\n')
    : '—';

  return new EmbedBuilder()
    .setTitle('🌙 Nightly Council Report')
    .setDescription('Summary of the last 24h across our realm.')
    .setColor(0x9b59b6)
    .addFields(
      { name: 'System Health (MCP)', value: mcp.slice(0, 1024) || '—' },
      { name: 'Recent Commits', value: repoLines.slice(0, 1024) || '—' },
    )
    .setFooter({ text: 'Reported by Lilybear' })
    .setTimestamp(new Date());
}

/** Send the report immediately to the council channel or webhook */
export async function sendCouncilReport(client: Client): Promise<void> {
  const embed = await buildReportEmbed();
  if (LILY_WEBHOOK) {
    await fetch(LILY_WEBHOOK, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ embeds: [embed.toJSON()] }),
    });
  } else {
    const ch = client.channels.cache.get(COUNCIL_CH) as TextChannel | undefined;
    await ch?.send({ embeds: [embed] });
  }
}

/** Schedule the nightly report at 08:00 UTC */
export function scheduleNightlyCouncilReport(client: Client): void {
  cron.schedule(
    '0 8 * * *',
    async () => {
      try {
        await sendCouncilReport(client);
      } catch (e) {
        console.error('Nightly report error:', e);
      }
    },
    { timezone: 'UTC' },
  );
}
