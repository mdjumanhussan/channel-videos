# channel-videos

Pipeline for the YouTube channel **Md Juman Hussan JP** (`@md.jumanhussan3821`).
One animated explainer video per day, built here and published through Metricool.
The owner (Juman) checks YouTube about once a week, so runs are unattended. Nobody reviews a video before it goes live. Act accordingly: accuracy and restraint matter more than volume.

## Layout

- `pipeline/engine.py` — drawing helpers, narration (Kokoro TTS), renderer.
- `pipeline/setup.sh` — installs the voice engine and downloads its models. Run once per session.
- `episodes/YYYY-MM-DD-slug.py` — one file per video: narration lines + one draw function per scene.
- `topics.md` — log of every video made. Read it before picking a topic. Append after scheduling.
- `videos/` — published video files (public links for Metricool).
- `build/` — scratch output, git-ignored.

## Daily run

1. **Check last run.** Call Metricool `getScheduledPosts` (blogId `7328099`) for the past 3 days and next 7 days. Note any post that failed to publish; mention it in the final report. If 3 or more videos are already queued for future days, stop and report — do not pile up more.
2. **Pick a topic.** Read `topics.md`. Never repeat a topic. Rotate across: science, technology/AI, money and everyday economics, health basics, how-things-work, psychology of learning. Use WebSearch to see what people are asking about right now, then pick one question with broad curiosity and a clear, settled answer.
3. **Write the script.** 350–450 words, 8–10 scenes, 2.5–4 minutes. Rules:
   - Hook in the first 5 seconds: a question or a surprising true statement.
   - Short sentences. Plain words. One idea per line. A relatable everyday example in every scene.
   - End with a 3-point recap and a subscribe line.
4. **Fact-check before rendering.** Verify every factual claim against at least one reliable source with WebSearch/WebFetch. If a claim cannot be verified, cut it. Any number or chart that is invented for teaching must be labelled on screen ("Illustrative").
5. **Write the episode file.** Copy the structure of `episodes/2026-10-09-how-ai-chatbots-actually-work.py`. Each scene is `(chapter label, [narration lines], draw_fn)`; `draw_fn(c, T, t)` where `T(i)` is seconds since narration line `i` started and `t` is seconds since the scene started. Draw new visuals for the topic — do not reuse another episode's scenes with new words. Keep the same visual style (colours, fonts, caption bar).
6. **Build.**
   ```bash
   bash pipeline/setup.sh
   python3 pipeline/engine.py episodes/NAME.py audio
   python3 pipeline/engine.py episodes/NAME.py still 5 20 40 ...   # 2 stills per scene
   ```
   Look at the stills with the Read tool. Fix overlaps, clipped text, typos. Then:
   ```bash
   python3 pipeline/engine.py episodes/NAME.py render   # ~5 min, writes build/NAME/video.mp4 and thumb.png
   ```
   Run `render` with a 10-minute timeout. Confirm with `ffprobe` that the file is 1920x1080, has audio, and runs 2–5 minutes.
7. **Publish the file.** Copy `build/NAME/video.mp4` to `videos/NAME.mp4`, commit with the episode file, push to `main`. The public link is
   `https://raw.githubusercontent.com/mdjumanhussan/channel-videos/main/videos/NAME.mp4`. Check it returns HTTP 200 with `curl -sIL`.
   Then delete `videos/*.mp4` files older than 7 days in the same or a follow-up commit (Metricool keeps its own copy once a post is scheduled).
8. **Schedule.** Metricool `createScheduledPost`, blogId `7328099`, provider `youtube`, timezone `Australia/Sydney`, at **18:00 on the first day from today that has no post yet** (if today 18:00 is less than 1 hour away, start from tomorrow). Use `type: video`, `privacy: public`, `category: EDUCATION` (or `SCIENCE_TECHNOLOGY`), `madeForKids: false`, `autoPublish: true`. Do not send a thumbnail field unless a previous run proved it works.
9. **Log.** Append one line to `topics.md`: date, title, category, scheduled time, sources used. Commit and push.
10. **Report** in the final message: title, scheduled time, and anything that failed.

## Titles and descriptions

- Title under 60 characters. Promise exactly what the video delivers. No fake urgency, no false claims, no ALL CAPS.
- Description: 2-sentence summary, bullet list of what is covered, sources as plain links, 3 hashtags.

## Hard limits

- **One video per run. Never more than one scheduled per day.** Bulk posting risks the channel being flagged as mass-produced content.
- **Do not make videos on:** religion or religious stories, politics, elections, wars and current conflicts, medical diagnosis or treatment advice, legal advice, specific investment advice, named private individuals, or breaking news. The channel carries the owner's name and his Justice of the Peace title; these need his eyes first. If a topic idea falls here, pick another.
- No copyrighted music, footage, logos, or characters. Everything on screen is drawn by the engine.
- If any step fails (voice engine, render, push, Metricool), stop. Do not publish a partial or unchecked video. Report what failed.
- Facebook is not connected in Metricool yet. YouTube only until `getBrandSettings` shows a Facebook page.
