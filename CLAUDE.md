# channel-videos

Pipeline for the YouTube channel **Md Juman Hussan JP** (`@md.jumanhussan3821`).
One animated explainer video per day, built here and published through Metricool.
The owner (Juman) checks YouTube about once a week, so runs are unattended. Nobody reviews a video before it goes live. Act accordingly: accuracy and restraint matter more than volume.

## Layout

- `pipeline/engine.py` — drawing helpers, narration (Kokoro TTS), renderer.
- `pipeline/setup.sh` — installs the voice engine and downloads its models. Run once per session.
- `episodes/YYYY-MM-DD-slug.py` — one file per video: narration lines + one draw function per scene.
- `learnings.md` — running notes on what works in viral educational videos and on this channel. Read and add to it every run.
- `topics.md` — log of every video made. Read it before picking a topic. Append after scheduling.
- `videos/` — published video files (public links for Metricool).
- `build/` — scratch output, git-ignored.
- `quranic/` — separate pipeline for the Quranic Story Facebook page. Not part of the YouTube run; see `quranic/RUNBOOK.md`.

## Daily run

1. **Check last run.** Call Metricool `getScheduledPosts` (blogId `7328099`) for the past 3 days and next 7 days. Ignore Facebook posts (they belong to the Quranic Story job). Note any YouTube post that failed to publish; mention it in the final report. If 3 or more long YouTube videos are already queued for future days, stop and report — do not pile up more.
1b. **Learn from what is working (15–20 minutes, every run).** Read `learnings.md` first. Then study 3–5 educational videos or Shorts that are performing unusually well right now (WebSearch/WebFetch: trending explainers, "most viewed this week" lists, creator breakdowns, and any transcript or description you can open). You cannot watch or hear video, so work from what is readable: title wording, thumbnail description, the first lines of the script, length, structure, pacing notes, and what commentators say about the visuals and sound. For each one note what it does in four areas: **content** (hook, structure, payoff), **visuals** (framing, motion, colour), **graphic design** (thumbnail, type, layout), **sound** (music, effects, voice pacing).
   Then: append 2–4 dated, specific, sourced lessons to `learnings.md`; choose **one** lesson and apply it in today's video; write which one under "Applied" in `learnings.md`. If a lesson needs an engine change, make it small, test it on stills, and keep the old behaviour as the default if unsure. Learn patterns only. Never copy another creator's script, wording, footage, music, thumbnail or characters.
   Once a week (Sundays), also pull the channel's own numbers with Metricool analytics (views, watch time, per-video results) and record in `learnings.md` which topics and hooks did best. Lean topic choice toward those.
2. **Pick a topic.** Read `topics.md`. Never repeat a topic. Rotate across: science, technology/AI, money and everyday economics, health basics, how-things-work, psychology of learning. Use WebSearch to see what people are asking about right now, then pick one question with broad curiosity and a clear, settled answer.
3. **Write the script.** 350–450 words, 8–10 scenes, 2.5–4 minutes. Rules:
   - Hook in the first 5 seconds: a question or a surprising true statement.
   - Short sentences. Plain words. One idea per line. A relatable everyday example in every scene.
   - End with a 3-point recap and a subscribe line.
4. **Fact-check before rendering.** Verify every factual claim against at least one reliable source with WebSearch/WebFetch. If a claim cannot be verified, cut it. Any number or chart that is invented for teaching must be labelled on screen ("Illustrative").
5. **Write the episode file.** Copy the structure of `episodes/2026-10-09-how-ai-chatbots-actually-work.py`. Each scene is `(chapter label, [narration lines], draw_fn)`; `draw_fn(c, T, t)` where `T(i)` is seconds since narration line `i` started and `t` is seconds since the scene started. Draw new visuals for the topic — do not reuse another episode's scenes with new words. Keep the same visual style (colours, fonts, caption bar).
   The engine adds the cinematic look by itself: glow, drifting light and bokeh, vignette, slow camera push-in, word-by-word highlighted captions, a soft music bed and scene whooshes. In the episode file also set:
   - `HITS = [(scene, line, offset_s), ...]` — 2–3 deep sound hits on the biggest reveals (title card, the key answer).
   - `THUMB = ['LINE ONE', 'LINE TWO', 'PAYOFF']` — 2–3 short upper-case lines for the thumbnail; optional `thumb_art(c)` draws a simple picture in the right third (x 1150–1850).
   - Keep scene drawings above y = 880 so captions never cover them. Use strong colour on the one thing that matters in each scene.
6. **Build.**
   ```bash
   bash pipeline/setup.sh
   python3 pipeline/engine.py episodes/NAME.py audio
   python3 pipeline/engine.py episodes/NAME.py still 5 20 40 ...   # 2 stills per scene
   ```
   Look at the stills with the Read tool. Fix overlaps, clipped text, typos. Then:
   ```bash
   python3 pipeline/engine.py episodes/NAME.py render   # writes build/NAME/video.mp4 and thumb.jpg
   ```
   Then build the vertical Short (first scenes, up to 55 s, inside a branded frame). Set `SHORT_HOOK` in the episode file to a short question (under 40 characters):
   ```bash
   python3 pipeline/engine.py episodes/NAME.py short    # writes build/NAME/short.mp4 (1080x1920)
   ```
   `render` takes about 30–40 minutes for a 3-minute video. Start it in the background (`nohup ... > build/render.log 2>&1 &`) and poll the log for the line starting `DONE`. Never wait on it with `pgrep -f`, which matches its own shell. Confirm with `ffprobe` that the file is 1920x1080, has audio, and runs 2–5 minutes.
7. **Publish the files.** Copy `build/NAME/video.mp4` to `videos/NAME.mp4` and `build/NAME/short.mp4` to `videos/NAME-short.mp4`, commit with the episode file, push to `main`. The public link is
   `https://raw.githubusercontent.com/mdjumanhussan/channel-videos/main/videos/NAME.mp4`. Check it returns HTTP 200 with `curl -sIL`.
   Then delete `videos/*.mp4` files older than 7 days in the same or a follow-up commit (Metricool keeps its own copy once a post is scheduled).
8. **Schedule.** Metricool `createScheduledPost`, blogId `7328099`, provider `youtube`, timezone `Australia/Sydney`, at **18:00 on the first day from today that has no post yet** (if today 18:00 is less than 1 hour away, start from tomorrow). Use `type: video`, `privacy: public`, `category: EDUCATION` (or `SCIENCE_TECHNOLOGY`), `madeForKids: false`, `autoPublish: true`. Thumbnail: commit `build/NAME/thumb.jpg` as `videos/NAME.jpg` and pass its raw link as `videoThumbnailUrl`; if Metricool rejects the post because of the thumbnail, resend without it.
8b. **Promote.** Call Metricool `getBrandSettings`. For every other network connected there (linkedin, instagram, tiktok, twitter), schedule the same video as a native post 30 minutes after the YouTube time. **Never post YouTube videos to Facebook, even if it is connected — the owner said no.** (The Facebook page "Quranic Story" is run by a separate daily job: `quranic/RUNBOOK.md`. Leave its posts alone.) Caption: the hook line, 2 lines on what the viewer learns, then "More on YouTube: https://youtube.com/@md.jumanhussan3821". If no other network is connected, skip this step and say so in the report. Never spend money: no boosts, no ads.
8c. **Short.** Schedule `videos/NAME-short.mp4` on YouTube 1 hour after the long video (19:00), `type: short`, same privacy/category/madeForKids settings. Title: the hook question plus ` #Shorts` (under 60 characters). Description: one line on the answer, then "Full video on the channel."
9. **Log.** Append one line to `topics.md`: date, title, category, scheduled time, sources used. Commit and push.
10. **Report** in the final message: title, scheduled time, and anything that failed.

## Titles and descriptions

- Title under 60 characters. Promise exactly what the video delivers. No fake urgency, no false claims, no ALL CAPS.
- Description: 2-sentence summary, bullet list of what is covered, sources as plain links, 3 hashtags.

## Hard limits

- **One video per run: one long video plus its one Short. Never more than that per day.** Bulk posting risks the channel being flagged as mass-produced content.
- **Do not make videos on:** religion or religious stories, politics, elections, wars and current conflicts, medical diagnosis or treatment advice, legal advice, specific investment advice, named private individuals, or breaking news. The channel carries the owner's name and his Justice of the Peace title; these need his eyes first. If a topic idea falls here, pick another.
- No copyrighted music, footage, logos, or characters. Everything on screen is drawn by the engine.
- If any step fails (voice engine, render, push, Metricool), stop. Do not publish a partial or unchecked video. Report what failed.
- Only post to networks that `getBrandSettings` lists as connected. At setup time that was YouTube only.
