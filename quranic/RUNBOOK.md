# Quranic Story — daily Facebook Reel runbook

Facebook page **Quranic Story** (Juman's page). One vertical Reel per day, built here and published through Metricool.
Juman does not review videos before they go live. Religious accuracy matters more than anything else. When unsure, leave it out.

This is separate from the YouTube channel job (root `CLAUDE.md`). Never post these videos to YouTube. Never post YouTube explainers to this page.

## Layout

- `quranic/engine.py` — vertical 1080x1920 engine: painted layers, parallax camera, glow, particles, word-by-word captions, verse cards, eight-point-star transitions, Kokoro narration (voice `bm_george`), soft ambience. No music.
- `quranic/data/quran.json` — exact Uthmani Arabic + Saheeh International English for all 6236 verses (source: npm `quran-json` 3.1.2 → quranenc.com and tanzil.net). The only source for quoted verses.
- `quranic/fonts/` — Amiri (OFL) for Arabic.
- `quranic/series.md` — the story order and status. Take the first row with an empty "Built" column.
- `quranic/episodes/NNN-slug.py` — one file per episode. Copy the structure of `001-adam.py`.
- `quranic/log.md` — one line per published episode.
- `videos/quranic/` — published files (public links for Metricool).

## Daily run

1. **Check Metricool.** `getBrandSettings`: the brand (blogId `7328099`) must list a Facebook page in `networksData`. If Facebook is not connected, stop and report: "Connect the Quranic Story Facebook page in Metricool." Then `getScheduledPosts` for the past 3 and next 7 days. Report any failed Facebook post. If 3 or more Facebook Reels are already queued for future days, stop and report.
1a. **Study what is viral today.** Run 2–3 WebSearches on what is working in Reels right now (hooks, formats, editing, sound, and Islamic or faith story pages in particular). You cannot watch videos, so read articles, creator breakdowns, and look at thumbnails/covers with image search. Add one dated finding with its source link to the bottom of `VIRAL-PLAYBOOK.md`. Skip anything that would break the accuracy or visual rules.
1b. **Learn from the last Reels, then improve one thing.** Read `quranic/improvements.md`. Use Metricool analytics (`getAnalyticsAvailableMetrics`, then `getAnalyticsDataByMetrics` for facebook) to get views, plays, average watch time, reactions, comments and shares for every published Reel. Add today's numbers to the table in `improvements.md`. Compare: which Reel held people longest, which got shared most? Pick **one concrete improvement** for today's episode and write it down before building, for example: a sharper first 2 seconds, a shorter script, faster pacing, a stronger emotional peak, a new scenery helper, richer colours or lighting, bigger caption pops, a better end card, a better caption hook. Make the improvement in the episode or in `engine.py` (engine changes apply to all future Reels, so check stills carefully). Never trade accuracy or the visual rules for engagement. Once a change clearly helps, list it under "Keep doing".
2. **Pick the story.** If a row is Built but not Scheduled and its file is in `videos/quranic/`, skip to step 8 and schedule that one (its caption is `CAPTION` and title is `TITLE` in the episode file). Build nothing new that day. Otherwise take the first row in `series.md` with an empty "Built" column. Do not skip ahead, do not repeat.
3. **Research.** Read every verse of the story in `data/quran.json` (Python: `json.load(open('quranic/data/quran.json'))['verses']['2:30']`). For hadith episodes, open the hadith on sunnah.com with WebFetch and confirm: collection is Sahih al-Bukhari or Sahih Muslim, the number, and the English wording. If it cannot be confirmed, skip that story (mark it "skipped: could not verify" in `series.md`) and take the next one.
4. **Write the script.** Follow `VIRAL-PLAYBOOK.md`. 120–170 words, 9–11 scenes, 45–65 seconds (the engine refuses outside 115–185 words). If the story cannot be told well in that length, split it into Part 1 / Part 2 on consecutive days (add the extra row to `series.md`) and end Part 1 on a true cliffhanger. Note: `001-adam.py` predates these rules (104 s); copy its structure, not its length.
   - Set `HITS = [(scene, line, offset_s)]` for 1–2 deep hits on the emotional peak (the title already gets one). Use `pause=0.5` on the scene before the biggest line.
   - Scene 1 is a title card with a hook line that makes people stop scrolling (a question or a striking true moment from the story).
   - Short sentences. Simple, warm, emotional. One idea per line.
   - Every event must come from the Quran verses (or the verified hadith). No Israiliyyat, no invented dialogue, no details from weak reports, no names the Quran does not give (say "the two sons of Adam", "his wife").
   - Quoted words of Allah use the Saheeh International wording, exactly, via a verse card. Paraphrase in narration only when it is clearly narration, never inside quotation.
   - Say "peace be upon him" after a prophet's name once per episode. For the Prophet Muhammad say "peace and blessings be upon him".
   - End with one lesson from the story in plain words, then: "Share this with someone who … And follow for a new story from the Quran every day."
5. **Visual rules (strict).**
   - Never draw any prophet, any companion, angels, Iblees, or Allah in any form — no faces, no silhouettes, no figures, no light-shaped "person". Show places, nature, light, sky, objects (the Ark, the well, the fire, the sea, the Kabah, the whale, the cave) and symbolism instead.
   - No ordinary human figures either. Keep every scene landscape, object or symbol.
   - No music or instruments. Voice + the engine's soft ambience only.
   - Each episode paints its own scenes with the engine's helpers (`sky`, `dunes`, `mountains`, `sea`, `cloud_bank`, `clouds`, `rays`, `moon`, `sun`, `stars`, `mosque`, `city`, `palm`, `tree`, `kaaba`, `ark`, `whale`, `well`, `fire`, `cave_frame`, `pyramids`, `lantern`, `crow`). Add a new helper when a story needs a new object. Use fresh colour palettes per story.
   - Verse cards sit in the upper half (`y` around 600–650). Captions sit at the lower third. Keep important art in the middle.
6. **Build.**
   ```bash
   bash pipeline/setup.sh
   python3 quranic/engine.py quranic/episodes/NNN-slug.py audio      # also runs the verse check; fails on any non-exact quote
   python3 quranic/engine.py quranic/episodes/NNN-slug.py still 1.5 ...   # one or two stills per scene
   ```
   Look at the stills with the Read tool (make a contact sheet). Fix clipped text, overlaps, ugly shapes, anything that looks like a person. Then render with a 50-minute timeout (about 25 minutes on 2 CPUs):
   ```bash
   python3 quranic/engine.py quranic/episodes/NNN-slug.py render     # writes build/quranic/NNN-slug/video.mp4
   ```
   Confirm with `ffprobe`: 1080x1920, has audio, 80–110 seconds.
7. **Publish the file.** Copy to `videos/quranic/NNN-slug.mp4`, commit with the episode file, push to `main`. Public link:
   `https://raw.githubusercontent.com/mdjumanhussan/channel-videos/main/videos/quranic/NNN-slug.mp4` — check HTTP 200 with `curl -sIL`. Delete `videos/quranic/*.mp4` older than 7 days.
8. **Schedule.** Metricool `createScheduledPost`, blogId `7328099`, providers `[{"network":"facebook"}]`, `facebookData: {"type":"REEL","title":<title>}`, timezone `Australia/Sydney`, `autoPublish: true`, at **21:45 Sydney** on the first day from today with no Facebook post (if less than 1 hour away, start tomorrow). Once the page has 30+ days of data, use `getBestTimeToPostByNetwork` for facebook instead. Never boost, never spend money.
   Also set `firstCommentText` to a soft question inviting comments plus the full references (and "Part 2 tomorrow, in sha Allah" when split). Caption (the `text`): a 1-line hook, 3–5 short lines telling the heart of the story with one verse quoted exactly with its reference, a 1-line lesson, a sources line ("📖 Sources: Quran …, Saheeh International"), "Share this with someone who needs it. Follow for a new story every day.", then 3 hashtags (#QuranicStories #Prophet<Name> #IslamicReminder).
9. **Log.** Note the improvement and whether it was kept in `improvements.md`. Fill in "Built" and "Scheduled" in `series.md`, append to `log.md` (date, number, title, scheduled time, references). Commit and push.
10. **Report.** Short plain-English report: story, scheduled time, the one improvement made today, yesterday's views, anything that failed or needs Juman.

## Hard limits

- One Reel per day. Never more.
- Quran quotes only from `data/quran.json`. Hadith only Sahih al-Bukhari / Sahih Muslim, confirmed on sunnah.com. No fiqh rulings, no fatwas, no sectarian or political topics, no current events.
- No depictions of prophets, companions, angels, jinn/Iblees or Allah. No music.
- If any step fails (voice engine, render, push, Metricool, Facebook not connected), stop. Do not publish a partial or unchecked video.
