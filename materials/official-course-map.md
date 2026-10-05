# learn-business-chinese-basic-with-phoebe - source map

Internal build document. Not linked from any audience-facing page.

Bucket `comm`, difficulty 1, audience both, 6 sessions, single track, no code. Sibling:
`learn-business-chinese-advanced-with-phoebe`. Facts shared by both courses live HERE; the
Advanced map points to this file for them and never restates them.

Built 2026-10-05. Sources checked by the source-checker agent on 2026-10-05 (tiers as returned).

---

## Scope (approved by Phoebe 2026-10-05)

Complete beginners to roughly the 2021 standard's elementary stage, for work. Simplified
characters with pinyin, Mainland norm, Singapore differences noted where they exist.
**Every Chinese term on every page carries (pinyin, English) at every occurrence** (Phoebe's
choice for these two courses; `materials/gloss.py` applies it outside figures, and figure labels
are restructured by hand so the next label opens with the bracket).

Running case (constructed, said once per page): **Lumen Logistics**, an invented Singapore freight
company, 鲁门物流 (Lǔmén Wùliú), opening a partnership with a Shanghai distributor. The learner is
the person they send. Basic ends with a first meeting and a WeChat follow-up; Advanced takes the
same partnership to a negotiation and a formal email.

Seams: `learn-communication-with-phoebe` owns presenting and influence in general;
`learn-business-english-with-phoebe` (planned) is the English-language sibling. Nothing here
teaches HSK exam technique; the official exam pages own that.

---

## Verified facts and their tiers

| Fact | Tier | Use |
|---|---|---|
| GF0025-2021, 国际中文教育中文水平等级标准 (Chinese Proficiency Grading Standards for International Chinese Language Education), Ministry of Education and State Language Commission, issued March 2021, effective 1 July 2021: three stages, nine levels | Primary (text copy) for structure; secondary for dates | landing, session 1 |
| Cumulative counts, 2021 standard: L1 500 words / 300 chars; L2 1,272 / 600; L3 2,245 / 900; L4 3,245 / 1,200; L5 4,316 / 1,500; L6 5,456 / 1,800; L7-9 11,092 / 3,000 | Primary (text copy) | landing only, labelled "the 2021 standard" |
| **The HSK exam itself moves to a revised syllabus (Nov 2025) with an official launch on 13 December 2026** (CTI announcement, relayed by Shanghai Municipal Education Commission, 15 Sep 2026). Many guides still say July 2026 | Secondary (official body relayed) | landing note: "check chinesetest.cn before booking" |
| HSK 2.0 had six levels: 150 / 300 / 600 / 1,200 / 2,500 / 5,000 words | Secondary | not needed |
| BCT (商务汉语考试, Business Chinese Test): BCT (A) basic business, BCT (B) complex business, BCT (oral); run by Chinese Testing International; NTU Confucius Institute is Singapore's centre | Primary (CTI brochure, 2017) + secondary | Advanced landing |
| Tone values T1 55, T2 35, T3 214, T4 51 | Primary (Lee-Schoenfeld and Kandybowicz 2008, citing Chao); Chao 1930 "A system of tone letters", Le Maître Phonétique 45, reported | session 1, bench |
| Third-tone change (3+3 → 2+3) and the half third tone | Primary (Lee-Schoenfeld and Kandybowicz 2008) | sessions 1, 3 |
| 不 before 4 → bú; 一 before 4 → yí, before 1-3 → yì, stays yī as a number | Secondary (standard descriptions) | sessions 1, 3; marked ◐ |
| GB/T 16159-2012 §6.5.1: the tone mark goes on the main vowel; iu and ui on the second letter. **"a or e first, ou's o, else last vowel" is a teaching shortcut, not the standard's wording** | Primary | session 1 |
| GB/T 16159-2012 §6.5.2: 一 and 不 are written with their original tones; the changed tone may be written in teaching | Primary | session 1: word lists show changed tones and say so |
| 汉语拼音方案 (Scheme for the Chinese Phonetic Alphabet), approved 11 Feb 1958 | Primary | session 1 |
| YIN pitch estimator: de Cheveigné and Kawahara, JASA 111(4), 1917-1930, 2002 | Primary | bench |
| Speaking F0: male about 85-155 Hz, female about 165-255 Hz (Baken 1987 / 2000) | Secondary; **never print "85-180" or attribute to Titze** | bench speakers are chosen inside these |
| Two-handed card exchange, Chinese side facing the recipient; address by surname + title, 王经理 (Wáng jīnglǐ, Manager Wang) | Secondary (Columbia LRC Business Chinese; Open University OpenLearn) | session 2 |
| **王总 (Wáng zǒng, President Wang) is not documented in either source**; it is very widely heard | Unverified | session 2 says "widely heard, no style guide found" |
| Singapore Mandarin: 巴刹 (bāshā, market), 德士 (déshì, taxi) from the Singapore Mandarin Database (Speak Mandarin Campaign) | Primary | one Singapore note; these are not business terms |
| Web Speech API voices are user-agent dependent; a zh-CN voice is not guaranteed | Primary (W3C spec) | the trainer uses its own synthetic hum, not speechSynthesis |

**Never print:** the 2021 counts as the exam's current vocabulary; "July 2026" as the HSK 3.0
launch; the a/e/ou rule as the standard's text; 85-180 Hz or Titze for voice ranges; 王总 as
documented.

---

## The bench (`assets/tone-live.js`)

YIN pitch tracking on 40 ms frames (10 ms hop), syllables split on unvoiced runs, onsets and
offsets trimmed 15 percent, contours resampled to 10 points and scored by distance to the Chao
shapes (T1 55, T2 35, T3 214, half third 21, T4 51). Four synthetic speakers (hums following each
tone shape; not recordings): higher 220 Hz / 10 st, lower 115 / 10, narrow 170 / 5, wide 190 / 14.
Twelve business phrases, said with their surface tones, then again with one tone wrong.

Canon, verified headlessly in node 2026-10-05 (right tones heard right, of 23; mistakes caught, of 12):

| Method | Higher | Lower | Narrow | Wide |
|---|---|---|---|---|
| ANTI: raw Hz against one template voice | 23 · 12 | **6 · 7** | **6 · 7** | 23 · 12 |
| Semitones from your own middle | 23 · 12 | 23 · 12 | 19 · 12 | 23 · 12 |
| **Relative, scaled to your range, calibrated** | **23 · 12** | **23 · 12** | **23 · 12** | **23 · 12** |
| Same, judging each phrase on its own (no calibration) | 21 · 12 | 21 · 12 | 21 · 12 | 21 · 12 |
| ANTI: calibrated, but scored against dictionary tones | 18 · 12 | 18 · 12 | 18 · 12 | 18 · 12 |

With noise 0.15 added, lower voice, five runs: 115 / 115.

Findings: raw Hz punishes lower and narrow voices (6 of 23); calibration is what lets a one-level
word, 公司 (gōngsī, company), be scored at all (21 → 23); scoring dictionary tones marks five correct
tone-changed syllables wrong (18 of 23). The bench claims the ORDERING and the mechanism, never an
accuracy for real human speech; a real voice adds vowels, consonants and creak the hum lacks.

---

## Sessions

| # | Title | File |
|---|---|---|
| 1 | Sounds and tones | 01-sounds-and-tones.html |
| 2 | Names, titles and business cards | 02-names-titles-and-cards.html |
| 3 | The tone trainer | 03-the-tone-trainer.html |
| 4 | Numbers, money, dates and times | 04-numbers-money-dates.html |
| 5 | Meetings, calls and WeChat basics | 05-meetings-calls-and-wechat.html |
| 6 | The first meeting, and the follow-up | 06-the-first-meeting.html |

## Design

Palette cinnabar and jade: deep #7A1420, primary #A61B29, mid #B42A37, soft #F4C6CB, tint #FDF2F3,
ink #2A1216, muted #6E4B50, faint #E6CDD0, hairline #F1E1E3, jade #0E6655, jade ink #0A4A3E, jade
tint #E3F3EF, paper #FFFCFC. 23 pairs checked before the first page, lowest 4.91; the estate
sweep's pair check is clean on the stylesheet. Hand-drawn figure grammar as in the
asking-right-questions courses; Chinese glyphs in figures use the plain `sans-serif` stack so the
system CJK font renders them. `PASSPORT_KEY` = `lwp-passport:business-chinese-basic`.
