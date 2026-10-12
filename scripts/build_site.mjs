// Assembles dist/: the self-contained static site served locally and
// deployed to GitHub Pages. Combines the hand-authored site/index.html and
// site/covers/ with freshly built data/*.json.
import { execFileSync } from "node:child_process";
import { cpSync, mkdirSync, rmSync } from "node:fs";
import { join } from "node:path";
import { ROOT } from "./_lib.mjs";

const DIST = join(ROOT, "dist");

execFileSync("node", [join(ROOT, "scripts", "build_gv100.mjs")], { stdio: "inherit" });

rmSync(DIST, { recursive: true, force: true });
mkdirSync(DIST);

cpSync(join(ROOT, "site", "index.html"), join(DIST, "index.html"));
cpSync(join(ROOT, "site", "covers.json"), join(DIST, "covers.json"));
cpSync(join(ROOT, "site", "jaapleest.json"), join(DIST, "jaapleest.json"));
cpSync(join(ROOT, "site", "covers"), join(DIST, "covers"), { recursive: true });
for (const name of ["gv100_long.json", "gv100_editions.json"]) {
  cpSync(join(ROOT, "data", name), join(DIST, name));
}

console.log("dist/ ready");
