// Shared helpers for the build scripts. No side effects on import.
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";

export const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");

export function norm(s) {
  return s
    .normalize("NFKD")
    .replace(/[^\x00-\x7F]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}

export function splitSeries(t) {
  const m = t.match(/^(.*?)\s*\(([^()]*#[^()]*)\)\s*$/);
  return m ? [m[1], m[2]] : [t, ""];
}

// The key is always anchored on the first-listed author, so adding co-authors
// to a row never changes which editions it links to.
export function workKey(title, authors) {
  const surname = authors[0].trim().split(/\s+/).pop();
  return norm(title) + " | " + norm(surname);
}
