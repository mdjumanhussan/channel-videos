# Surah in 90 Seconds

Vertical Reels for Juman's "Surah in 90 Seconds" Facebook page (tagline: Understand, Memorize & Perfect).
Not automated yet: videos are made on request and posted by hand.

- `engine.py`: a copy of `quranic/engine.py` with a 160–240 word range (about 80–95 s), the page badge and end card, and output in `build/surah90/`.
- `data`, `fonts`: links to `quranic/data` and `quranic/fonts` (exact Quran text, Amiri).
- `episodes/NNN-surah.py`: one file per surah, numbered by surah.

Rules: same as `quranic/RUNBOOK.md` (Quran quotes only from `data/quran.json`, no people or prophets drawn, no music).
There is no recitation audio yet; the Arabic is shown on screen and the English voice explains.

Build:
    bash pipeline/setup.sh
    python3 surah90/engine.py surah90/episodes/112-al-ikhlas.py audio
    python3 surah90/engine.py surah90/episodes/112-al-ikhlas.py render
