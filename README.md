# GV100 analysis

Structured data for **De Grote Vriendelijke 100**, the yearly reader-voted list of favourite children's and YA books. The list is run by [De Grote Vriendelijke Podcast](https://degrotevriendelijkepodcast.nl) together with [Hebban](https://www.hebban.nl/gv100).

## Data

| File | Grain | Notes |
|---|---|---|
| `data/gv100_long.csv` | one row per edition × rank | `year, rank, title, series, author, work_key, goodreads_id, source` |
| `data/gv100_wide.csv` | one row per book | `rank_2021` … `rank_2025`, `editions_present`, `best_rank` |
| `data/gv100_editions.csv` | one row per edition | voter counts, dates, source, completeness |

`work_key` is a normalised title + author surname. It links the same book across years, because sources often point to different editions of the same book.

### Coverage

| Edition | Entries | Status |
|---|---|---|
| 2021 | 100 | complete |
| 2022 | 13 | **partial**: top 10 plus ranks 12, 14 and 15 |
| 2023 | 100 | complete |
| 2024 | 100 | complete |
| 2025 | 100 | complete |

### Sources and caveats

- The official lists are hosted on Hebban, which doesn't allow automated access. The complete editions are taken from reader-maintained Goodreads copies (links in `gv100_editions.csv`). Their top-10s and previous-year positions were cross-checked against press coverage from Tzum, NBD Biblion and nieuws.nl.
- The Goodreads copy of the 2022 list is broken, so 2022 comes from a bookshop write-up and is incomplete.
- Only the first author is recorded, so co-authors and illustrators are missing.
- Some entries may refer to the same work under different titles and might need to be merged by hand. Examples: *Hier is de boze heks* (2021–22) vs *De grote boze heks* (2023+), and *Heksenkind* vs *De Heksenkind trilogie*.

## Rebuilding

```bash
python3 scripts/build_gv100.py   # stdlib only; rewrites data/*.csv
```

The list data is embedded in the script. To correct or add a year, edit it there and rerun the script. `notebooks/01_explore.ipynb` contains a few starter analyses (needs `pandas`).

## TODO

- [ ] Complete the 2022 edition (Hebban list or poster)
- [ ] Add 2026 once it is announced (November 2026)
- [ ] Enrich with publication year, original language, age category, and author gender/nationality
