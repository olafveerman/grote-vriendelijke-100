// Sanity-checks data/gv100_books.json (and its relationship to
// gv100_editions.json) before it gets built into the site. There's no
// generation step producing this data any more — it's hand-maintained — so
// this is what catches a typo'd rank or a duplicate work_key instead.
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { ROOT } from "./_lib.mjs";

const DATA = join(ROOT, "data");
const books = JSON.parse(readFileSync(join(DATA, "gv100_books.json"), "utf-8"));
const editions = JSON.parse(readFileSync(join(DATA, "gv100_editions.json"), "utf-8"));

const errors = [];

const seenKeys = new Set();
for (const b of books) {
  if (!b.work_key || !b.title || !Array.isArray(b.authors) || b.authors.length === 0) {
    errors.push(`book missing required fields: ${JSON.stringify(b.work_key ?? b.title)}`);
  }
  if (seenKeys.has(b.work_key)) errors.push(`duplicate work_key: ${b.work_key}`);
  seenKeys.add(b.work_key);
  if (!Array.isArray(b.editions) || b.editions.length === 0) {
    errors.push(`book has no editions: ${b.work_key}`);
  }
}

const rowsByYear = {};
for (const b of books) {
  for (const e of b.editions ?? []) {
    (rowsByYear[e.year] ??= []).push({ work_key: b.work_key, rank: e.rank });
  }
}

for (const [year, rows] of Object.entries(rowsByYear)) {
  const ranks = rows.map((r) => r.rank).sort((a, b) => a - b);
  const expected = Array.from({ length: 100 }, (_, i) => i + 1);
  if (JSON.stringify(ranks) !== JSON.stringify(expected)) {
    errors.push(`${year} does not have exactly ranks 1..100 (got ${ranks.length} rows)`);
  }
  const keys = rows.map((r) => r.work_key);
  const dupKeys = keys.filter((k, i) => keys.indexOf(k) !== i);
  if (dupKeys.length) errors.push(`duplicate work_key in ${year}: ${[...new Set(dupKeys)].join(", ")}`);
}

const bookYears = new Set(Object.keys(rowsByYear).map(Number));
const editionYears = new Set(editions.map((e) => e.year));
for (const y of bookYears) if (!editionYears.has(y)) errors.push(`year ${y} appears in books but not in gv100_editions.json`);
for (const y of editionYears) if (!bookYears.has(y)) errors.push(`year ${y} is in gv100_editions.json but no book has a ranking for it`);

if (errors.length) {
  console.error(`${errors.length} problem(s) found in data/gv100_books.json:`);
  for (const e of errors) console.error(`  - ${e}`);
  process.exit(1);
}

const totalEditions = Object.values(rowsByYear).reduce((n, rows) => n + rows.length, 0);
console.log(`OK: ${books.length} books, ${totalEditions} edition entries across ${bookYears.size} years`);
