# GV100 analysis

Structured data for **De Grote Vriendelijke 100**, the yearly reader-voted list of favourite children's and YA books. The list is run by [De Grote Vriendelijke Podcast](https://degrotevriendelijkepodcast.nl) together with [Hebban](https://www.hebban.nl/gv100).

## Data

| File | Grain | Notes |
|---|---|---|
| `data/gv100_books.json` | one record per distinct book | `work_key, title, authors, goodreads_id, cover, jaapleest, age_rating, publisher, illustrator, translator, publication_year, original_language, editions: [{year, rank, source}, ...]` |
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
- The Goodreads copy of the 2022 list was broken/misordered, so 2022 comes from a manually saved copy of the official Hebban page instead. `goodreads_id` is backfilled from matching works in other editions, or looked up directly on Goodreads where a title is unique to 2022; it's blank for 2 omnibus/compilation titles confirmed to have no dedicated Goodreads entry (*Het tegendeel van zorgen*, a Querido bundling of two older Lindelauf novels; *Een jaar bij Kikker en Pad*, a Ploegsma Frog-and-Toad compilation) — publisher and publication year for both came from Hebban's own "eerste editie" listing instead, since Goodreads had nothing to pull from.
- `authors` supports co-authors. Populated for: the 2022 edition (scraped directly, 2 titles have one), plus 2 more works found via jaapleest.nl (*Misjka*, *Tori* — both missing a second author across every edition they appear in). The other 185 of 189 books still record only a single author; backfilling the rest is a TODO. `work_key` is always anchored on the first-listed author, so adding co-authors to a book never changes which editions it links to.
- Some entries may refer to the same work under different titles and might need to be merged by hand. Examples: *Hier is de boze heks* (2021–22) vs *De grote boze heks* (2023+), and *Heksenkind* vs *De Heksenkind trilogie*.
- [jaapleest.nl](https://jaapleest.nl) is run by one of the people behind De Grote Vriendelijke Podcast and the GV100 chart itself. A one-time research sweep (October 2026) matched 103 of the 189 distinct works there by title+author and pulled a review link, age rating, publisher, and illustrator where shown, plus 55 extra cover images and 2 missing co-authors (cross-checking its `Auteur:` field against what we had) — all now folded into `data/gv100_books.json`. It skews toward reviewing newer releases, so classics (Harry Potter, Matilda, Pippi Langkous, Astrid Lindgren's books, etc.) mostly came back unmatched — and it doesn't carry publication year, original language, or author nationality at all, so those stay open regardless of how many more titles it ends up reviewing. One oddity found along the way: its review of *Terra ultima* credits a fictional in-story narrator as "Auteur" and the real author (Raoul Deleo, who we already have right) only as illustrator — left unchanged, noted here in case it's confusing later.
- The remaining 2 unresolved `goodreads_id`s and the full cover set were finished off with a direct per-title Goodreads lookup (same sweep) rather than jaapleest — Goodreads blocks plain fetches with a bot challenge, worked around via a text-rendering proxy reading the page's `og:image`/`og:title` tags.
- `publication_year` and `original_language` (October 2026, first sweep): pulled from each book's Goodreads page ("First published …"). A second pass closed out `publication_year` to 189/189 — *Zoef!* (dead Goodreads page) confirmed as 2024 via Hebban, the 2 goodreads_id-less titles above backfilled from Hebban's "eerste editie" field. `original_language` is populated for 47 books where a source stated it explicitly (a translator credit, or a differing original title) — including the 4 Harry Potter titles, previously blank despite having a Goodreads page, once their Dutch editions' translator credits were checked directly. Still left blank by design everywhere a source doesn't explicitly say so — e.g. *De Gruffalo* and *De ruïnes van Gorlan* read as obvious English translations but neither Goodreads page carries a translator field or original-title field, so they stay unguessed.
- jaapleest.nl re-check (October 2026): the 86 works jaapleest hadn't reviewed as of the original sweep were checked again — it's added reviews since, closing jaapleest coverage to 109 of 189. 6 new matches (*Alice in Wonderland*, *De Gorgels*, *Een groene bloem trilogie*, *Iep!*, *Missie afbreken*, *Nederland*), which also brought `publisher` and `age_rating` forward and introduced the `translator` field (from jaapleest's `Vertaler:` label where shown) — populated for 1 book so far (*Alice in Wonderland*, translated by Sofia Engelsman). Two apparent matches were deliberately **not** applied: reviews of the Furlong "Heksenkind" and Beckman "Thule" trilogies turned up again under the standalone titles *Heksenkind* and *Kinderen van Moeder Aarde* — but those reviews cover the 3-in-1 omnibus editions, which this dataset already represents correctly as their own separate entries (*De Heksenkind trilogie*, *Het Gulden Vlies van Thule*) from the original sweep. Applying the omnibus review's metadata to the standalone title would have been wrong, not just redundant.
- `publisher`/`age_rating` general sweep (October 2026): the 90 books still missing one or both after the jaapleest passes were looked up directly — Dutch retailer/library sites (bol.com, kinderboeken.nl, bibliotheek.nl, publishers' own sites) rather than jaapleest this time. Closed `publisher` to 179/189 and `age_rating` to 157/189. Deliberately skipped rather than guessed: *Alleen op de wereld* and *De Kronieken van Narnia* (several distinct Dutch editions/translations circulate for each, with different publishers and age-recs, and which one matches our entry couldn't be confirmed) and age ratings for roughly two dozen titles where sources disagreed across editions/retailers widely enough (e.g. a 6-year spread) that picking one would have been a guess, not a finding. 7 titles (*Polleke*, *Prutje*, *Robin: alle verhalen*, *Sinterklaas*, *Spijt*, *Winnie de Poeh: De complete verzameling verhalen en gedichten*, *Winterijs*) came back with nothing confirmable at all — some sites issue blanket redirects for any URL slug (leopold.nl, unieboekspectrum.nl), which look like confirmation but aren't; worth knowing about if re-attempting these.

## Editing the data

Edit `data/gv100_books.json` directly, then run:

```bash
node scripts/validate.mjs   # no dependencies; checks ranks and work_keys are consistent
```

Adding a new year (e.g. 2026) means: appending an `{year, rank, source}` entry to `editions` for every returning book, creating a new book entry for anything appearing for the first time, and adding the year to `gv100_editions.json`. There's no shortcut for the ~100 rank assignments that come with a new edition — that tradeoff was made deliberately, in exchange for not having a second, build-generated file to reconcile against.

## Site

A small static site in `site/` — an Editions browser (top 100 per year, with filters, per-edition stats, and a per-book modal showing cover, author and a rank-history chart) and an Insights tab (a year-by-year bubble chart — books clustered by a chosen lens, with an animated re-cluster on every lens switch — plus a handful of small-multiple cards). The whole pipeline is Node-only, no Python required.

```bash
pnpm install
pnpm run serve   # builds dist/ and serves it at http://localhost:5173
```

`pnpm run build` validates `data/gv100_books.json` (see above), then assembles `dist/` from `site/index.html`, `site/covers/`, `data/gv100_books.json` and `gv100_editions.json` — that's the one folder that gets deployed. Pushing to `main` runs the same build in `.github/workflows/pages.yml` and publishes `dist/` to GitHub Pages (enable Pages → *Build and deployment: GitHub Actions* in the repo settings once, first time).

Every one of the 189 distinct works has a cover now: the 2022 edition's 100 titles (from a manually saved copy of the Hebban page), 55 more from matched jaapleest.nl reviews, and the last 34 pulled directly from Goodreads (see caveats above). The images themselves are plain committed files in `site/covers/`; each book's path to its own file lives in its `cover` field in `data/gv100_books.json`. There's no script that (re)produces any of this — add a new cover by dropping the file in `site/covers/` and setting `cover` on the matching book by hand. The modal also shows publisher, age rating, first-published year, original language, and illustrator wherever those fields are set, plus a jaapleest.nl link next to the Goodreads one.

## TODO

- [ ] Add 2026 once it is announced (November 2026)
- [ ] Enrich with author nationality — not on jaapleest.nl or in Goodreads' usual fields; a per-author lookup (e.g. Wikipedia), not per-book, and worth extra care since it's a claim about a real person
- [ ] Backfill co-authors for the 185 of 189 books still recording only a single author (schema already supports it; see `authors` in `data/gv100_books.json`)
- [ ] Keep closing the `original_language` gap for translated works whose source doesn't explicitly say so — e.g. *De Gruffalo*, *De ruïnes van Gorlan* (checked October 2026, no explicit signal found yet; needs a source beyond Goodreads' translator/original-title fields, or careful manual judgment)
- [ ] Look into whether illustrators are worth surfacing more — e.g. an "illustrators" insight card, or filtering/grouping by illustrator like publisher. Coverage is thin: `illustrator` is set for only 61 of 189 books (populated via the jaapleest.nl sweeps), so check whether that's enough before investing more
- [ ] Consider a small-multiples version of the bubble chart (one mini chart per edition, side by side) as an alternative to the year-pill selector — worth it for the binary lenses (Translated/Mainstay/Newcomer) but the Publisher/Age-rating lenses' dominant "Other/Unknown" cluster would get cramped at 1/5 width
- [ ] Add a link/button to quickly reset the Editions table filters (search text, age rating, publisher, Newcomers/Mainstays toggle) back to their defaults in one click, instead of clearing each one individually
- [ ] Bucket the "Filter by age rating" dropdown in the Editions tab onto the same jaapleest.nl scale (1+/4+/8+/10+/12+/15+) already used for the Insights "Leeftijdsadvies" histogram — it currently lists every distinct `age_rating` value as its own option (15 of them), which isn't a useful filter at that granularity
- [ ] Fill in `age_rating` for the 17 of 189 books still missing one (down from 27 after an October 2026 sweep closed 8, via Lemniscaat's own publisher pages and bibliotheek.nl/NBD catalog records, plus *Spijt* and *Winnie de Poeh: De complete verzameling verhalen en gedichten* confirmed directly by Olaf) — a chunk of the remainder are genuine "sources disagree" cases, not "no source found" (*Minoes* and *Matilda* have inconsistent NUR codes across printings; *Dwars & Co* only has separate read-aloud vs. read-yourself ages, not one value) — so a confident single value may not exist for every title no matter how much more is looked up
- [ ] Fill in `translator` for the 9 of 47 translated-from-foreign-language books still missing one (down from 19 after an October 2026 sweep closed 10, via Koninklijke Bibliotheek catalog records, Dutch Wikipedia infoboxes, and corroborating retailer sources) — the remainder split into: no credit found anywhere despite two independent sweeps (*Alle verhalen van Kikker en Pad*, *Over een kleine mol die wil weten wie er op zijn kop gepoept heeft*, *Wij gaan op berenjacht*); a low-confidence Wikipedia-only credit a second sweep still couldn't corroborate (*Rupsje Nooitgenoeg* — "Denis Courtney"); a credit whose cited publication year still doesn't match this dataset's after a second look (*Ronja de roversdochter*); an editorial choice between the on-cover credited name and the actual (ghost-)translator per Wikipedia (*Sjakie en de chocoladefabriek* — "Harriët Freezer" credited, "Huberte Vriesendorp" the real translator); and classics with multiple historical Dutch translations/editions where it's unclear which this entry represents (*Alleen op de wereld*, *Pippi Langkous*, *Winnie de Poeh: De complete verzameling verhalen en gedichten*)

## License

MIT for the code. See [LICENSE](LICENSE) — the data and cover images are handled differently than the code; that file explains how.
