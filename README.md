# GV100 analysis

Structured data for **De Grote Vriendelijke 100**, the yearly reader-voted list of favourite children's and YA books. The list is run by [De Grote Vriendelijke Podcast](https://degrotevriendelijkepodcast.nl) together with [Hebban](https://www.hebban.nl/gv100).

## Data

| File | Grain | Notes |
|---|---|---|
| `data/gv100_books.json` | one record per distinct book | `work_key, title, authors, goodreads_id, cover, jaapleest, age_rating, publisher, illustrator, translator, publication_year, original_language, editions: [{year, rank, source}, ...]` |
| `data/gv100_editions.json` | one record per edition | voter counts, dates, source, completeness |

`work_key` is a normalised title + author surname. It links the same book across years, because sources often point to different editions of the same book.

`gv100_books.json` is the single canonical file — one book per entry, with its full rank history nested in `editions` — and it's **hand-maintained directly**, not generated. Correcting a title, adding a co-author, sourcing a cover, adding a year — all of it means editing `data/gv100_books.json` itself. `scripts/validate.mjs` (run automatically by `pnpm run build`) checks it for the mistakes hand-editing risks: every year having exactly ranks 1–100 with no duplicate `work_key`, and `gv100_editions.json` covering exactly the same years.

`translator` only applies to books with `original_language` set (i.e. confirmed translated into Dutch). It holds either a name, `null` (not researched, or genuinely undetermined — e.g. it's unclear which of several historical Dutch editions this entry represents), or the literal string `"unknown"` for a book that's been actively researched with no findable credit. The distinction keeps a dead end from getting re-researched. The site's modal treats `"unknown"` the same as absent — it's bookkeeping for the data file, not something shown to visitors.

### Sources and caveats

- [jaapleest.nl](https://jaapleest.nl), run by one of the people behind De Grote Vriendelijke Podcast and the chart itself, is the closest thing this project has to a primary source — reviews there carry `age_rating`, `publisher`, `illustrator`, and `translator` where shown. It only reviews new releases as they come out, not the backlist, so it has reviewed 110 of 189 works and that won't change on its own with time — everything else is sourced from Dutch retailer/library sites (bol.com, kinderboeken.nl, bibliotheek.nl, the Koninklijke Bibliotheek catalog, publishers' own pages) or Goodreads. Watch for omnibus/trilogy reviews surfacing under a different title than the one being checked — a review of a bundled edition shouldn't be applied to a standalone entry it doesn't actually describe.

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

- [ ] Check if all co-authors are correct

## License

MIT for the code. See [LICENSE](LICENSE) — the data and cover images are handled differently than the code; that file explains how.
