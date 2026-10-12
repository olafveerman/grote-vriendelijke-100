// Assembles dist/: the self-contained static site served locally and
// deployed to GitHub Pages. Combines the hand-authored site/index.html and
// site/covers/ with the hand-maintained data/*.json — nothing here generates
// the data, see scripts/validate.mjs for the integrity check that runs first.
import { cpSync, mkdirSync, rmSync } from "node:fs";
import { join } from "node:path";
import { ROOT } from "./_lib.mjs";

const DIST = join(ROOT, "dist");

rmSync(DIST, { recursive: true, force: true });
mkdirSync(DIST);

cpSync(join(ROOT, "site", "index.html"), join(DIST, "index.html"));
cpSync(join(ROOT, "site", "covers"), join(DIST, "covers"), { recursive: true });
for (const name of ["gv100_books.json", "gv100_editions.json"]) {
  cpSync(join(ROOT, "data", name), join(DIST, name));
}

console.log("dist/ ready");
