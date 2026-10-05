# Agent brief - learn-business-chinese-basic-with-phoebe

You are writing ONE static HTML session page. No servers, no npm. **If your target file already
exists on disk, do not write it; report that and stop.** Write the file in three or four tool
calls (Write the head through the end of Part 1, then append the rest with Bash heredocs
`cat >> file <<'EOF'`), each under ~220 lines. Return its path and one line of coverage, plus any
fact you could not support. No HTML in your reply.

## Read first, in this order

1. The template pages. Copy structure, classes, SVG grammar and quiz markup EXACTLY (four options
   per question): `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-business-chinese-basic-with-phoebe/courses/01-sounds-and-tones.html` (a concept session) and
   `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-business-chinese-basic-with-phoebe/courses/03-the-tone-trainer.html` (this course's bench session, for rhythm).
2. The source maps: `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-business-chinese-basic-with-phoebe/materials/official-course-map.md` (shared facts, tiers, the NEVER
   PRINT list) . Use ONLY their facts; never invent a statistic, a rule or an etiquette claim;
   if a fact is missing, teach it as common practice and say so, or leave it out.
3. Your page's outline: `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-business-chinese-basic-with-phoebe/materials/page-outlines.md`.
4. The stylesheet `:root` block: `/Users/phoebe.fu/Documents/claude_work/github_repo/learn-business-chinese-basic-with-phoebe/assets/style.css`.

## Page skeleton (keep every component)

As the template: toolbar (crumb EXACTLY `<a href="../index.html">learn-business-chinese-basic-with-phoebe</a> / Session N of 6`,
#toggle-all, #zoom-toggle) · masthead (eyebrow "Learn Business Chinese Basic with Phoebe · Session N of 6", h1 with one
`<span class="accent">`, .sub, .chip-row with level chip 🟢 Foundational, two audience chips, `45 min`,
.agenda a1-a4 flex 1/4/5/1) · section#intro (Part 0, .lede, .legend pills, .callout.win "★ What you
walk out with tonight.") · three Parts `section.section#part-N` (kicker klabel "Part N · covers ...",
h2, `.tag.concept "N min live"`), each with a .lede, ONE figure, `details.card` accordions
(`.mode.live` / `.mode.self`), and at least one `.callout.example` with `span.ex-pill` "Real world"
on the page · section#demo-1 build-along (`.tag.demo "★ 22 min · everyone says it"` or "everyone
writes", .lede, ONE figure, `.steps > .step` each with a `.prompt-box.good` and `span.label`) ·
section#exercise (ol, 4) · section#quiz (3 × `.quiz-q data-answer`, four `button.qopt` "A · ..",
`p.qwhy`; one `p.quiz-score`) · section#official, h2 EXACTLY "What this session teaches, and where it
came from", `.covered-row`s, then the `.mono` line EXACTLY "Every fact on this page, and its
verification tier, is recorded in the course's source map." · section.cheat#cheatsheet (h3 "Session
N cheat sheet <span>· pin this</span>", six .cheat-item) · `.callout.next` · footer.pagefoot ·
scripts `<script src="../assets/tone-live.js?v=1"></script> only if the page embeds #tone-practice, then <script src="../assets/app.js?v=1"></script>`. First `details.card` of Part 1 is `open`; no other. One `.tryrow` micro-try
on the page, as on the template.

## Hard rules (a violation is rework)

- **Every Chinese term carries (pinyin, English) at EVERY occurrence**, in prose, tables, prompt
  boxes, quiz options, cheat items and headings: `开会 (kāihuì, have a meeting)`. In SVG figures,
  either the next `<text>` element starts with "(pinyin, English)", or write pinyin only with no
  character. A whole sample message or email in Chinese is the one exception: print its English
  translation directly beneath it, in brackets, as the Advanced bench does.
- Check with `python3 /Users/phoebe.fu/Documents/claude_work/github_repo/learn-business-chinese-basic-with-phoebe/materials/gloss.py <your file>`: it must report "0 glosses added"
  and "figure labels to restructure by hand: none" (or only labels whose next element starts with a
  bracket). **Do not edit gloss.py**; other agents use it. If it lists an unknown term, gloss it
  inline yourself.
- Simplified characters; pinyin with tone marks. Word lists may show changed tones (bú shì,
  yídìng) and must say once that standard pinyin writes the original tone (GB/T 16159-2012).
- NEVER an em dash or en dash. Hyphen only. No cross marks (✕ ✗ ×) as bullets or labels.
- No meta text ("this course", "in this course"). Attribution "by Phoebe Fu". Never "lottery".
- Lumen Logistics, 鲁门物流 (Lǔmén Wùliú, Lumen Logistics), its people and every scenario are
  constructed; say so once in a `.callout.example` or a covered row.
- Etiquette and culture claims: only what the map supports (two-handed card exchange, surname +
  title address such as 王经理 (Wáng jīnglǐ, Manager Wang)). 王总 (Wáng zǒng, President Wang) is
  widely heard but undocumented in the sources found: say exactly that if you use it. Graham and
  Lam 2003 for face in negotiation; never paraphrase Hwang 1987 as a negotiation claim.
- HSK: the 2021 standard's counts describe the standard, not the exam; the HSK 3.0 exam's official
  launch is 13 December 2026 (not July). BCT: BCT (A), BCT (B), BCT (oral).
- 此致 敬礼 (cǐzhì jìnglǐ, with respect) is a convention, NOT part of GB/T 9704 or any standard.

## Figure grammar (hand-drawn, every figure)

Palette ONLY: `#7A1420` `#A61B29` `#B42A37` `#F4C6CB` `#FDF2F3` `#2A1216` `#6E4B50` `#E6CDD0` `#F1E1E3` `#0E6655` `#0A4A3E` `#E3F3EF` `#FFFCFC` · `#FFFFFF` · universal reds `#991B1B` `#FEF2F2` `#FCA5A5` for a wrong-way panel.
Same grammar as the template: `<figure class="zoomable">` > `<svg viewBox="0 0 880 H" role="img"
aria-label="...">`, a wobble filter `PSk`, a hachure `PHc`, an arrow `PAr`, all shapes in ONE
filtered `<g>`, all text outside it, unique prefix `s<session><letter>`, Chinese glyphs in figures
use `font: 800 22px sans-serif`. **Text must sit fully inside its box with 8px padding (budget
6.4px per character at 11px, 7px at 12px, and double that for Chinese characters); no line,
connector or tick may run through a label; no pen or arrow-like doodles; boxes never touch; on a
timeline put neighbouring milestone boxes on alternate sides of the axis.** The gate now checks
text-out-of-box and line-through-text automatically. Floor: one figure per Part plus one in the
build-along; draw the mechanism (who sits where, which tone goes where, how a number is grouped).

## Session titles and files

1. 01-sounds-and-tones.html · Sounds and tones (written)
2. 02-names-titles-and-cards.html · Names, titles and business cards
3. 03-the-tone-trainer.html · The tone trainer (written)
4. 04-numbers-money-dates.html · Numbers, money, dates and times
5. 05-meetings-calls-and-wechat.html · Meetings, calls and WeChat basics
6. 06-the-first-meeting.html · The first meeting, and the follow-up

Footer left: "Session N of 6 · learn-business-chinese-basic-with-phoebe · by Phoebe Fu &nbsp;·&nbsp; 📚 <a href="https://phoebefu6.github.io/learn-with-phoebe/">Learn with Phoebe ↗</a>"
Footer right: "← Prev: <title>" and "Next: <title> →" (session 1: "← Course home" first; session 6: "Course home" last).
