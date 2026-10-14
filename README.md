# GV100 analysis

Structured data for **De Grote Vriendelijke 100**, the yearly reader-voted list of favourite children's and YA books. The list is run by [De Grote Vriendelijke Podcast](https://degrotevriendelijkepodcast.nl) together with [Hebban](https://www.hebban.nl/gv100).

## Data

| File | Grain | Notes |
|---|---|---|
| `data/gv100_books.json` | one record per distinct book | `work_key, title, authors, goodreads_id, cover, jaapleest, age_rating, publisher, illustrator, translator, publication_year, original_language, editions: [{year, rank, source}, ...]` |
| `data/gv100_editions.json` | one record per edition | voter counts, dates, source, completeness |

`work_key` is a normalised title + author surname. It links the same book across years, because sources often point to different editions of the same book.

`gv100_books.json` is the single canonical file — one book per entry, with its full rank history nested in `editions` — and it's **hand-maintained directly**, not generated. Correcting a title, adding a co-author, sourcing a cover, adding a year — all of it means editing `data/gv100_books.json` itself. `scripts/validate.mjs` (run automatically by `pnpm run build`) checks it for the mistakes hand-editing risks: every year having exactly ranks 1–100 with no duplicate `work_key`, and `gv100_editions.json` covering exactly the same years.

A handful of books (9 of 189) have a different `goodreads_id` per edition in reality — different print runs linked from different years' source pages — but only one value is kept per book here (first one encountered, in year order). The site only ever shows one Goodreads link per book regardless, so the extra fidelity wasn't worth the complexity.

`translator` only applies to books with `original_language` set (i.e. confirmed translated into Dutch). It holds either a name, `null` (not researched, or genuinely undetermined — e.g. it's unclear which of several historical Dutch editions this entry represents), or the literal string `"unknown"` for a book that's been actively researched with no findable credit. The distinction keeps a dead end from getting re-researched. The site's modal treats `"unknown"` the same as absent — it's bookkeeping for the data file, not something shown to visitors.

### Coverage

| Edition | Entries | Status |
|---|---|---|
| 2021 | 100 | complete |
| 2022 | 100 | complete |
| 2023 | 100 | complete |
| 2024 | 100 | complete |
| 2025 | 100 | complete |

Every book has a `cover`, `goodreads_id` (except 2, see below), `publication_year`, `publisher`, and `age_rating`. `translator` is filled in for all 47 books it applies to. `original_language` and `illustrator` are populated only where a source states them explicitly, rather than assumed — 47 and 89 of 189 books respectively. `authors` supports co-authors but only 5 of 189 books currently record more than one.

### Sources and caveats

- The official lists are hosted on Hebban, which doesn't allow automated access. The 2021/2023/2024/2025 editions are taken from reader-maintained Goodreads copies (links in `gv100_editions.json`), cross-checked against press coverage from Tzum, NBD Biblion and nieuws.nl. The 2022 edition comes from a manually saved copy of the official Hebban page instead, since the Goodreads copy of that year was broken/misordered.
- `goodreads_id` is blank for 2 omnibus/compilation titles confirmed to have no dedicated Goodreads entry — *Het tegendeel van zorgen* (a Querido bundling of two older Lindelauf novels) and *Een jaar bij Kikker en Pad* (a Ploegsma Frog-and-Toad compilation). Their `publisher`/`publication_year` came from Hebban's own "eerste editie" listing instead.
- Some entries may refer to the same work under different titles and might need to be merged by hand. Examples: *Hier is de boze heks* (2021–22) vs. *De grote boze heks* (2023+), and *Heksenkind* vs. *De Heksenkind trilogie*.
- [jaapleest.nl](https://jaapleest.nl), run by one of the people behind De Grote Vriendelijke Podcast and the chart itself, is the closest thing this project has to a primary source — reviews there carry `age_rating`, `publisher`, `illustrator`, and `translator` where shown. It only reviews new releases as they come out, not the backlist, so it has reviewed 110 of 189 works and that won't change on its own with time — everything else is sourced from Dutch retailer/library sites (bol.com, kinderboeken.nl, bibliotheek.nl, the Koninklijke Bibliotheek catalog, publishers' own pages) or Goodreads. Watch for omnibus/trilogy reviews surfacing under a different title than the one being checked — a review of a bundled edition shouldn't be applied to a standalone entry it doesn't actually describe. One oddity: its review of *Terra ultima* credits a fictional in-story narrator as "Auteur" and the real author (Raoul Deleo, correctly credited here) only as illustrator.
- `publication_year` and `original_language` are pulled from each book's Goodreads page ("First published …") or a translator/original-title signal. `original_language` is left blank by design wherever a source doesn't say so explicitly — e.g. *De Gruffalo* and *De ruïnes van Gorlan* read as obvious English translations but carry no such signal on Goodreads, so they stay unguessed rather than assumed.
- A couple of sites redirect any URL slug to a generic page rather than 404ing (leopold.nl and unieboekspectrum.nl were both caught doing this) — worth testing with a nonsense slug before trusting a "match" from either.

## Editing the data

Edit `data/gv100_books.json` directly, then run:

```bash
node scripts/validate.mjs   # no dependencies; checks ranks and work_keys are consistent
```

Adding a new year (e.g. 2026) means: appending an `{year, rank, source}` entry to `editions` for every returning book, creating a new book entry for anything appearing for the first time, and adding the year to `gv100_editions.json`. There's no shortcut for the ~100 rank assignments that come with a new edition — that tradeoff was made deliberately, in exchange for not having a second, build-generated file to reconcile against.

## Site

A small static site in `site/`, in Dutch — an Editions browser (top 100 per year, with filters, per-edition stats, and a per-book modal showing cover, author and a rank-history chart) and an Insights tab (a year-by-year bubble chart — books clustered by a chosen lens, with an animated re-cluster on every lens switch — plus a handful of small-multiple cards). The whole pipeline is Node-only, no Python required.

```bash
pnpm install
pnpm run serve   # builds dist/ and serves it at http://localhost:5173
```

`pnpm run build` validates `data/gv100_books.json` (see above), then assembles `dist/` from `site/index.html`, `site/covers/`, `data/gv100_books.json` and `gv100_editions.json` — that's the one folder that gets deployed. Pushing to `main` runs the same build in `.github/workflows/pages.yml` and publishes `dist/` to GitHub Pages (enable Pages → *Build and deployment: GitHub Actions* in the repo settings once, first time).

Covers are plain committed files in `site/covers/`; each book's path to its own file lives in its `cover` field in `data/gv100_books.json`. There's no script that (re)produces any of this — add a new cover by dropping the file in `site/covers/` and setting `cover` on the matching book by hand. The modal also shows publisher, age rating, first-published year, original language, illustrator, and translator wherever those fields are set, plus a jaapleest.nl link next to the Goodreads one.

## TODO

- [ ] Add 2026 once it is announced (November 2026)
- [ ] Enrich with author nationality — not on jaapleest.nl or in Goodreads' usual fields; a per-author lookup (e.g. Wikipedia), not per-book, and worth extra care since it's a claim about a real person
- [ ] Backfill co-authors for the 184 of 189 books still recording only a single author (schema already supports it; see `authors` in `data/gv100_books.json`)
- [ ] Keep closing the `original_language` gap for translated works whose source doesn't explicitly say so — e.g. *De Gruffalo*, *De ruïnes van Gorlan* need a source beyond Goodreads' translator/original-title fields, or careful manual judgment
- [ ] Look into whether illustrators are worth surfacing more — e.g. an "illustrators" insight card, or filtering/grouping by illustrator like publisher. Coverage is 89 of 189 books, so check whether that's enough before investing more
- [ ] Consider a small-multiples version of the bubble chart (one mini chart per edition, side by side) as an alternative to the year-pill selector — worth it for the binary lenses (Translated/Mainstay/Newcomer) but the Publisher/Age-rating lenses' dominant "Other/Unknown" cluster would get cramped at 1/5 width
- [ ] Keep an eye out for further `publisher` spelling/casing variants of the same publisher, and for correctness generally (e.g. the unusual compound entry "Holland / Lemniscaat (Paul Biegel Bibliotheek)")

## License

MIT for the code. See [LICENSE](LICENSE) — the data and cover images are handled differently than the code; that file explains how.
