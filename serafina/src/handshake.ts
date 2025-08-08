/**
 * Architectural preamble:
 * Defines a lightweight handshake protocol so sibling services can announce
 * themselves and exchange capability data. Serafina will both expose a
 * /handshake endpoint for inbound requests and actively contact peers on boot
 * to form a mesh.
 */

import fetch from 'node-fetch';
import express from 'express';

const NAME = process.env.REPO_NAME || 'Serafina';
const CAPABILITIES = ['discord-router', 'unity-bridge'];
const PEERS = (process.env.HANDSHAKE_PEERS || '')
  .split(',')
  .map((s) => s.trim())
  .filter((s) => s.length);

/** Perform handshakes with configured peers */
export async function performHandshakes() {
  for (const peer of PEERS) {
    try {
      const res = await fetch(`${peer}/handshake`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: NAME, capabilities: CAPABILITIES }),
      });
      const data = await res.json().catch(() => ({}));
      console.log(`[handshake] ${peer} ->`, data);
    } catch (err) {
      console.error(`[handshake] failed with ${peer}:`, err);
    }
  }
}

/**
 * Create an Express router hosting the /handshake endpoint.
 * Other services POST { name, capabilities } and receive our details in return.
 */
export function createHandshakeRouter() {
  const app = express();
  app.use(express.json());
  app.post('/handshake', (req, res) => {
    // Basic logging for visibility; in production consider rate limits/auth
    console.log('[handshake] received from', req.body?.name);
    res.json({ name: NAME, capabilities: CAPABILITIES });
  });
  return app;
}
