# GV100 analysis

Structured data for **De Grote Vriendelijke 100**, the yearly reader-voted list of favourite children's and YA books. The list is run by [De Grote Vriendelijke Podcast](https://degrotevriendelijkepodcast.nl) together with [Hebban](https://www.hebban.nl/gv100).

## Data

| File | Grain | Notes |
|---|---|---|
| `data/gv100_long.json` | one record per edition × rank | `year, rank, title, series, author, work_key, goodreads_id, source` |
| `data/gv100_editions.json` | one record per edition | voter counts, dates, source, completeness |

`work_key` is a normalised title + author surname. It links the same book across years, because sources often point to different editions of the same book. The per-book "rank in every edition" view (what used to be a generated `gv100_wide.json`) is now a pivot of `long` computed on the fly, client-side in the site's JS, rather than a second file that could drift from it.

### Coverage

| Edition | Entries | Status |
|---|---|---|
| 2021 | 100 | complete |
| 2022 | 100 | complete |
| 2023 | 100 | complete |
| 2024 | 100 | complete |
| 2025 | 100 | complete |

### Sources and caveats

- The official lists are hosted on Hebban, which doesn't allow automated access. The 2021/2023/2024/2025 editions are taken from reader-maintained Goodreads copies (links in `gv100_editions.json`). Their top-10s and previous-year positions were cross-checked against press coverage from Tzum, NBD Biblion and nieuws.nl.
- The Goodreads copy of the 2022 list was broken/misordered, so 2022 comes from a manually saved copy of the official Hebban page instead. `goodreads_id` is backfilled from matching works in other editions where possible; it's blank for the ~13 titles unique to 2022 that weren't looked up individually.
- `authors` supports co-authors, but they're only populated for the 2022 edition, where the source was scraped directly (2 of its titles have one). The other four editions were hand-curated with a single author per book historically; backfilling their co-authors is a TODO, same as publisher/pub-date. `work_key` is always anchored on the first-listed author, so adding co-authors to a row never changes which editions it links to.
- Some entries may refer to the same work under different titles and might need to be merged by hand. Examples: *Hier is de boze heks* (2021–22) vs *De grote boze heks* (2023+), and *Heksenkind* vs *De Heksenkind trilogie*.
- [jaapleest.nl](https://jaapleest.nl) is run by one of the people behind De Grote Vriendelijke Podcast and the GV100 chart itself — likely the best source for the enrichment TODOs below (nationality, age rating, publisher, pub date), closer to primary than the Goodreads mirrors.

## Rebuilding the data

```bash
node scripts/build_gv100.mjs   # no dependencies; rewrites data/*.json
```

The list data is embedded in the script. To correct or add a year, edit it there and rerun the script.

## Site

A small static site in `site/` — an Editions browser (top 100 per year, with a per-book modal showing cover, author and its rank in every edition) and an Insights tab (placeholder for now). The whole pipeline is Node-only, no Python required.

```bash
pnpm install
pnpm run serve   # builds dist/ and serves it at http://localhost:5173
```

`pnpm run build` assembles `dist/` from `site/index.html`, `site/covers/` and a freshly rebuilt `data/gv100_long.json` + `gv100_editions.json` — that's the one folder that gets deployed. Pushing to `main` runs the same build in `.github/workflows/pages.yml` and publishes `dist/` to GitHub Pages (enable Pages → *Build and deployment: GitHub Actions* in the repo settings once, first time).

Covers only exist for the 2022 edition's 100 titles (`scripts/sync_covers.mjs`, sourced from a manually saved copy of the Hebban page — see caveats above); other books show a placeholder in the modal.

## TODO

- [ ] Add 2026 once it is announced (November 2026)
- [ ] Look up `goodreads_id` for the 11 titles unique to 2022 that are still blank in `EDITIONS[2022]` (ranks 32, 33, 44, 68, 78, 82, 90, 93, 94, 97, 98 in `scripts/build_gv100.mjs`)
- [ ] Enrich with publication year and original language
- [ ] Enrich with author nationality and age rating (likely from jaapleest.nl — see Sources)
- [ ] Add a jaapleest.nl link per book, next to the Goodreads one, where available
- [ ] Source covers for the 89 works outside the 2022 edition that don't have one yet
- [ ] Backfill co-authors for the 2021/2023/2024/2025 editions (schema already supports it; see `authors` in `data/gv100_long.json`)

## License

MIT for the code. See [LICENSE](LICENSE) — the data and cover images are handled differently than the code; that file explains how.
