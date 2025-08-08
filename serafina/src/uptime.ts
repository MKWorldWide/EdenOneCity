/**
 * Heartbeat loop to maintain presence and keep the bot process active on free tiers.
 * Runs every 15 minutes to update Discord presence.
 */
import { Client } from 'discord.js';

export function startHeartbeat(client: Client) {
  async function beat() {
    try {
      await client.user?.setPresence({
        activities: [{ name: 'whispering across realms' }],
        status: 'online',
      });
    } catch (err) {
      console.error('Presence heartbeat failed:', err);
    } finally {
      setTimeout(beat, 15 * 60 * 1000); // 15 minutes
    }
  }
  beat();
}
