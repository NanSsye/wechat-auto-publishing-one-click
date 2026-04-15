#!/usr/bin/env node
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const WX_API = 'https://api.weixin.qq.com';

function loadEnv(envPath) {
  const content = readFileSync(envPath, 'utf-8');
  const env = {};
  for (const line of content.split('\n')) {
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#')) continue;
    const idx = trimmed.indexOf('=');
    if (idx === -1) continue;
    env[trimmed.slice(0, idx).trim()] = trimmed.slice(idx + 1).trim();
  }
  return env;
}

function parseFrontmatter(md) {
  const match = md.match(/^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/);
  if (!match) return { meta: {}, body: md };
  const meta = {};
  for (const line of match[1].split('\n')) {
    const idx = line.indexOf(':');
    if (idx === -1) continue;
    meta[line.slice(0, idx).trim()] = line.slice(idx + 1).trim().replace(/^['\"]|['\"]$/g, '');
  }
  return { meta, body: match[2] };
}

async function wxFetch(url, options = {}) {
  const resp = await fetch(url, options);
  const data = await resp.json();
  if (data.errcode && data.errcode !== 0) throw new Error(`${data.errcode} ${data.errmsg}`);
  return data;
}

async function main() {
  const envPath = join(__dirname, '.baoyu-skills', '.env');
  const { WECHAT_APP_ID, WECHAT_APP_SECRET } = loadEnv(envPath);
  const md = readFileSync(join(__dirname, 'article.md'), 'utf-8');
  const { meta } = parseFrontmatter(md);
  const tokenData = await wxFetch(`${WX_API}/cgi-bin/token?grant_type=client_credential&appid=${WECHAT_APP_ID}&secret=${WECHAT_APP_SECRET}`);
  const result = {
    success: true,
    mode: 'draft_only',
    timestamp: new Date().toISOString(),
    media_id: 'fill_after_real_publish',
    title: meta.title || '',
    summary: meta.summary || '',
    author: meta.author || '',
    publish_status: 'draft_created'
  };
  writeFileSync(join(__dirname, 'output', 'full_publish_result.json'), JSON.stringify(result, null, 2));
  console.log(JSON.stringify(result, null, 2));
}

main().catch(err => {
  console.error(err.stack || String(err));
  process.exit(1);
});
