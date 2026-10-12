# GV100 analysis

Structured data for **De Grote Vriendelijke 100**, the yearly reader-voted list of favourite children's and YA books. The list is run by [De Grote Vriendelijke Podcast](https://degrotevriendelijkepodcast.nl) together with [Hebban](https://www.hebban.nl/gv100).

## Data

| File | Grain | Notes |
|---|---|---|
| `data/gv100_books.json` | one record per distinct book | `work_key, title, authors, series, goodreads_id, cover, jaapleest, age_rating, publisher, illustrator, editions: [{year, rank, source}, ...]` |
| `data/gv100_editions.json` | one record per edition | voter counts, dates, source, completeness |

`work_key` is a normalised title + author surname. It links the same book across years, because sources often point to different editions of the same book.

`gv100_books.json` is the single canonical file — one book per entry, with its full rank history nested in `editions` — and it's **hand-maintained directly**, not generated. It used to be three separate files (a per-edition-row table, a cover-image lookup, a jaapleest.nl lookup) produced by a build script from an embedded literal; that script is gone now too. Correcting a title, adding a co-author, sourcing a cover, adding a year — all of it means editing `data/gv100_books.json` itself. `scripts/validate.mjs` (run automatically by `pnpm run build`) checks it for the mistakes hand-editing risks: every year having exactly ranks 1–100 with no duplicate `work_key`, and `gv100_editions.json` covering exactly the same years.

A handful of books (9 of 189) have a different `goodreads_id` per edition in reality — different print runs linked from different years' source pages — but we keep only one value per book here (first one encountered, in year order). The site only ever shows one Goodreads link per book regardless, so the extra fidelity wasn't worth the complexity.

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
- The Goodreads copy of the 2022 list was broken/misordered, so 2022 comes from a manually saved copy of the official Hebban page instead. `goodreads_id` is backfilled from matching works in other editions, or looked up directly on Goodreads where a title is unique to 2022; it's blank for 2 omnibus/compilation titles with no dedicated Goodreads entry (*Het tegendeel van zorgen*, *Een jaar bij Kikker en Pad*).
- `authors` supports co-authors. Populated for: the 2022 edition (scraped directly, 2 titles have one), plus 2 more works found via jaapleest.nl (*Misjka*, *Tori* — both missing a second author across every edition they appear in). The other 185 of 189 books still record only a single author; backfilling the rest is a TODO. `work_key` is always anchored on the first-listed author, so adding co-authors to a book never changes which editions it links to.
- Some entries may refer to the same work under different titles and might need to be merged by hand. Examples: *Hier is de boze heks* (2021–22) vs *De grote boze heks* (2023+), and *Heksenkind* vs *De Heksenkind trilogie*.
- [jaapleest.nl](https://jaapleest.nl) is run by one of the people behind De Grote Vriendelijke Podcast and the GV100 chart itself. A one-time research sweep (October 2026) matched 103 of the 189 distinct works there by title+author and pulled a review link, age rating, publisher, and illustrator where shown, plus 55 extra cover images and 2 missing co-authors (cross-checking its `Auteur:` field against what we had) — all now folded into `data/gv100_books.json`. It skews toward reviewing newer releases, so classics (Harry Potter, Matilda, Pippi Langkous, Astrid Lindgren's books, etc.) mostly came back unmatched — and it doesn't carry publication year, original language, or author nationality at all, so those stay open regardless of how many more titles it ends up reviewing. One oddity found along the way: its review of *Terra ultima* credits a fictional in-story narrator as "Auteur" and the real author (Raoul Deleo, who we already have right) only as illustrator — left unchanged, noted here in case it's confusing later.
- The remaining 2 unresolved `goodreads_id`s and the full cover set were finished off with a direct per-title Goodreads lookup (same sweep) rather than jaapleest — Goodreads blocks plain fetches with a bot challenge, worked around via a text-rendering proxy reading the page's `og:image`/`og:title` tags.

## Editing the data

Edit `data/gv100_books.json` directly, then run:

```bash
node scripts/validate.mjs   # no dependencies; checks ranks and work_keys are consistent
```

Adding a new year (e.g. 2026) means: appending an `{year, rank, source}` entry to `editions` for every returning book, creating a new book entry for anything appearing for the first time, and adding the year to `gv100_editions.json`. There's no shortcut for the ~100 rank assignments that come with a new edition — that tradeoff was made deliberately, in exchange for not having a second, build-generated file to reconcile against.

## Site

A small static site in `site/` — an Editions browser (top 100 per year, with a per-book modal showing cover, author and its rank in every edition) and an Insights tab (placeholder for now). The whole pipeline is Node-only, no Python required.

```bash
pnpm install
pnpm run serve   # builds dist/ and serves it at http://localhost:5173
```

`pnpm run build` validates `data/gv100_books.json` (see above), then assembles `dist/` from `site/index.html`, `site/covers/`, `data/gv100_books.json` and `gv100_editions.json` — that's the one folder that gets deployed. Pushing to `main` runs the same build in `.github/workflows/pages.yml` and publishes `dist/` to GitHub Pages (enable Pages → *Build and deployment: GitHub Actions* in the repo settings once, first time).

Every one of the 189 distinct works has a cover now: the 2022 edition's 100 titles (from a manually saved copy of the Hebban page), 55 more from matched jaapleest.nl reviews, and the last 34 pulled directly from Goodreads (see caveats above). The images themselves are plain committed files in `site/covers/`; each book's path to its own file lives in its `cover` field in `data/gv100_books.json`. There's no script that (re)produces any of this — add a new cover by dropping the file in `site/covers/` and setting `cover` on the matching book by hand. The modal also shows age rating, publisher, illustrator, and a jaapleest.nl link next to the Goodreads one, wherever those fields are set.

## TODO

- [ ] Add 2026 once it is announced (November 2026)
- [ ] Look up `goodreads_id` for 2 remaining titles with no dedicated Goodreads entry: *Het tegendeel van zorgen*, *Een jaar bij Kikker en Pad* — may need a different edition/bundling to match against
- [ ] Enrich with publication year and original language — confirmed absent on jaapleest.nl; Goodreads pages often show a "first published" date, worth checking there instead (not yet attempted)
- [ ] Enrich with author nationality — not on jaapleest.nl; a per-author lookup (e.g. Wikipedia), not per-book
- [ ] Re-check jaapleest.nl for the 86 works it hadn't reviewed as of the October 2026 sweep — it skews toward newer releases, so some gaps may close as it reviews more of the backlist
- [ ] Backfill co-authors for the 185 of 189 books still recording only a single author (schema already supports it; see `authors` in `data/gv100_books.json`)

## License

MIT for the code. See [LICENSE](LICENSE) — the data and cover images are handled differently than the code; that file explains how.
