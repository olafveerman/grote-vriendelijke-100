// Copies cover images out of the saved 2022 Hebban page into site/covers/.
//
// Hebban blocks automated access, so these come from a manually saved copy of
// the 2022 list page (gitignored, under drop/). The page's rank order matches
// EDITIONS[2022] in build_gv100.mjs exactly, so rank -> work_key comes
// straight from gv100_long.json. Covers only exist for the 2022 edition;
// other works are left without one.
//
// Run after build_gv100.mjs. Writes site/covers/<slug>.jpg and
// site/covers.json (work_key -> relative path), both committed to the repo.
import { existsSync, mkdirSync, copyFileSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { ROOT, norm } from "./_lib.mjs";

const DROP_HTML = join(ROOT, "drop", "De Grote Vriendelijke 100 van 2022 _ Hebban.nl.html");
const COVERS_DIR = join(ROOT, "site", "covers");

function slugify(workKey) {
  return norm(workKey).replace(/ /g, "-");
}

function main() {
  if (!existsSync(DROP_HTML)) {
    console.log(`skip: ${DROP_HTML} not found (nothing to sync)`);
    return;
  }

  const html = readFileSync(DROP_HTML, "utf-8");
  const books = [...html.matchAll(/<img src="([^"]+)" alt="([^"]+)"/g)]
    .filter(([, , alt]) => alt.includes(" - "))
    .map(([, src]) => src);
  if (books.length !== 100) {
    throw new Error(`expected 100 cover images in the saved page, found ${books.length}`);
  }

  const longRows = JSON.parse(readFileSync(join(ROOT, "data", "gv100_long.json"), "utf-8"));
  const rankToWorkKey = Object.fromEntries(
    longRows.filter((r) => r.year === 2022).map((r) => [r.rank, r.work_key])
  );
  if (Object.keys(rankToWorkKey).length !== 100) throw new Error("expected 100 rows for 2022");

  mkdirSync(COVERS_DIR, { recursive: true });
  const mapping = {};
  books.forEach((src, i) => {
    const rank = i + 1;
    const workKey = rankToWorkKey[rank];
    const sourcePath = join(dirname(DROP_HTML), src.replace(/^\.\//, ""));
    const slug = slugify(workKey);
    copyFileSync(sourcePath, join(COVERS_DIR, `${slug}.jpg`));
    mapping[workKey] = `covers/${slug}.jpg`;
  });

  writeFileSync(join(ROOT, "site", "covers.json"), JSON.stringify(mapping, null, 2));
  console.log(`${Object.keys(mapping).length} covers copied to ${COVERS_DIR}`);
}

main();
