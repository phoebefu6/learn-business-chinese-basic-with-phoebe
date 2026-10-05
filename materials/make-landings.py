"""Build the landing page and README for both Business Chinese courses from one structure.

One generator so the two landings cannot drift apart. The landing CSS block and the knowledge-map
renderer come from the asking-right-questions DA landing (the newest estate landing).
Run: python3 make-landings.py
"""
import json
import os
import re

GH = os.path.expanduser("~/Documents/claude_work/github_repo")
DA = f"{GH}/learn-asking-right-questions-as-da-with-phoebe/index.html"
STYLE_BLOCK = re.search(r"<style>.*?</style>", open(DA).read(), re.S).group(0)

COURSES = {
    "basic": dict(
        title="Learn Business Chinese Basic with Phoebe", accent="Business Chinese", tail="Basic",
        deep="#7A1420",
        desc="Six sessions from zero to a first business meeting in Mandarin: the sounds and the four tones, names, titles and business cards, numbers and money, meetings and WeChat, and a first meeting with its follow-up. A real pitch tracker in your browser scores your tones by shape, not height. Free, by Phoebe Fu.",
        og="A tone trainer that scores the shape of your pitch, not its height: raw hertz gets a lower voice right 6 times in 23, the calibrated method 23 in 23.",
        sub="In Mandarin, 买 (mǎi, buy) and 卖 (mài, sell) differ only in the shape of the pitch, and a buyer who says the second has offered to sell. Six sessions take a complete beginner to a first business meeting in Chinese: the sounds and the four tones, how to address people by title and exchange a card, numbers, money, dates and times, booking and confirming a meeting on WeChat, and the meeting itself with its follow-up. Every Chinese word on every page carries its pinyin and English. A real pitch tracker running in your browser listens to you and scores each tone by its shape against your own voice, so a deep voice and a high voice are judged the same way.",
        stats=[("6", "sessions"), ("4", "tones, plus neutral"), ("12", "business words drilled"), ("23", "of 23 on the bench"), ("45", "min per session")],
        sessions=[("01-sounds-and-tones.html", "Sounds and tones", "🔊", "#34D399", "foundational",
                   "How a syllable is built, pinyin and its tone marks, the four tones as shapes, why 买 (mǎi, buy) and 卖 (mài, sell) must never be confused, and the three tone changes."),
                  ("02-names-titles-and-cards.html", "Names, titles and business cards", "🪪", "#34D399", "foundational",
                   "Surname first, address by title, safe defaults when you do not know the title, and how a card is given and received with two hands."),
                  ("03-the-tone-trainer.html", "The tone trainer", "🎛️", "#F87171", "bench night",
                   "A pitch tracker scores four synthetic voices five ways: raw hertz fails a lower voice, calibration rescues a level word, dictionary tones mark correct speech wrong. Then your own voice."),
                  ("04-numbers-money-dates.html", "Numbers, money, dates and times", "🔢", "#FBBF24", "core",
                   "Counting in fours with 万 (wàn, ten thousand), prices, phone numbers, dates in Chinese order and meeting times."),
                  ("05-meetings-calls-and-wechat.html", "Meetings, calls and WeChat basics", "💬", "#FBBF24", "core",
                   "Polite requests, booking and confirming a meeting, and WeChat as the everyday business channel."),
                  ("06-the-first-meeting.html", "The first meeting, and the follow-up", "🤝", "#FB923C", "capstone",
                   "The first five minutes scripted, the numbers said and confirmed, the WeChat follow-up sent the same day. Final scorecard.")],
        concepts=[["One syllable, three parts", "Four shapes and a light one", "Why ní hǎo"],
                  ["Surname first", "Titles do the work", "Two hands, Chinese side up"],
                  ["Shape, not height", "Calibrate first", "Score the spoken tone"],
                  ["Counting in fours", "Ten or four", "Dates in Chinese order"],
                  ["Asking politely", "Booking a meeting", "WeChat at work"],
                  ["The first five minutes", "A polite repeat", "The same-day follow-up"]],
        paths=[("🧳 I fly to Shanghai next month", [1, 2, 6], "sounds, titles and cards, the meeting script"),
               ("🎧 My tones are the problem", [1, 3], "the shapes, then the trainer on your own voice"),
               ("🎯 The whole course", [1, 2, 3, 4, 5, 6], "from the first syllable to a first meeting and its follow-up")],
        honest=[("Every count on the tone trainer bench", "<strong>Really computed</strong> in your browser by a YIN pitch tracker on four synthetic voices; the bench claims the ordering of the scoring methods, not an accuracy for real speech"),
                ("The tone values 55, 35, 214, 51 and the third-tone change", "<strong>Confirmed</strong> in a published phonology paper citing Chao"),
                ("Where the tone mark goes", "<strong>Read at source</strong> in the 1958 pinyin scheme and GB/T 16159-2012; the familiar \"a or e first\" rule is taught as a shortcut, not as their wording"),
                ("Card exchange and address by title", "<strong>Reported</strong> from university business-Chinese guides; 王总 (Wáng zǒng, President Wang) is widely heard and not documented in them"),
                ("HSK levels", "<strong>The 2021 standard</strong> (GF0025-2021) for scope; the HSK exam's new version officially launches on 13 December 2026, so check chinesetest.cn before booking"),
                ("Lumen Logistics and its people", "<strong>Invented</strong> for the running case")],
        not_this=[("I already speak everyday Chinese and need the business register, formal writing and negotiation", "Business Chinese Advanced ↗", "https://phoebefu6.github.io/learn-business-chinese-advanced-with-phoebe/"),
                  ("I want to present and influence in English", "Communication ↗", "https://phoebefu6.github.io/learn-communication-with-phoebe/")],
        here="I start from zero and need to get through a first business meeting in Chinese.",
        sibling=("Business Chinese Advanced ↗", "https://phoebefu6.github.io/learn-business-chinese-advanced-with-phoebe/"),
        bench_line="The bench in session 3 (`assets/tone-live.js`) runs a YIN pitch tracker on four synthetic voices and five scoring methods. Raw pitch in hertz scores a lower voice 6 of 23; the calibrated, range-scaled method scores every voice 23 of 23; scoring dictionary tones marks five correct tone changes wrong.",
    ),
    "advanced": dict(
        title="Learn Business Chinese Advanced with Phoebe", accent="Business Chinese", tail="Advanced",
        deep="#16294D",
        desc="Six sessions on business Chinese for people who already speak it day to day: register, formal emails and WeChat, presenting numbers, negotiation and face, and business dining, with a formality checker that scores a draft against the channel it is going to. Free, by Phoebe Fu.",
        og="One message written five ways, scored against three channels: each draft fits one, and polishing everything into classical phrasing fits none.",
        sub="A message that is perfectly polite in an email is stiff on WeChat, and a word-for-word translation of polite English is too casual for both. Six sessions for people who already speak everyday Chinese and need it to work in business: register as a choice made per channel, the shape of a formal email and a business WeChat, presenting numbers with 同比 (tóngbǐ, year on year) and 环比 (huánbǐ, period on period), negotiation and face, and business dining. Every Chinese word on every page carries its pinyin and English. A formality checker in your browser finds the casual, formal and over-formal words in a draft and scores it against the band its channel expects.",
        stats=[("6", "sessions"), ("43", "markers in the checker"), ("3", "channels, three bands"), ("5", "drafts on the bench"), ("45", "min per session")],
        sessions=[("01-register.html", "Register: the same sentence, three ways", "🎚️", "#FBBF24", "core",
                   "Person, question form and company: the three levers that move a sentence from a colleague chat to a formal email, and written language versus speech."),
                  ("02-formal-emails-and-wechat.html", "Formal emails and WeChat", "✉️", "#FBBF24", "core",
                   "The blocks of a formal email, the shape of a business WeChat, subject lines, and why 此致 敬礼 (cǐzhì jìnglǐ, with respect) is a convention and not a standard."),
                  ("03-the-formality-checker.html", "The formality checker", "🎛️", "#F87171", "bench night",
                   "One message written five ways, scored against three channels. Each draft fits one; three swaps fix a literal translation; polishing everything overshoots even email."),
                  ("04-presenting-numbers.html", "Presenting numbers", "📊", "#FB923C", "advanced",
                   "同比 (tóngbǐ, year on year) and 环比 (huánbǐ, period on period) as the statistics bureau defines them, growth, decline and share, and a result always said with its comparison."),
                  ("05-negotiation-and-face.html", "Negotiation and face", "⚖️", "#FB923C", "advanced",
                   "Face as Graham and Lam describe it, reading an indirect no, and trading concessions toward a clear next step."),
                  ("06-dining-and-capstone.html", "Business dining, and the capstone", "🥂", "#FB923C", "capstone",
                   "Seating, toasts and polite refusal, then the full negotiation and both follow-ups, checked. Final scorecard.")],
        concepts=[["Three levers", "Written vs spoken", "Over-formal"],
                  ["Formal email blocks", "Business WeChat", "Subject lines"],
                  ["Bands per channel", "Three swaps", "The ceiling"],
                  ["Year on year", "Period on period", "Say the comparison"],
                  ["Face", "Indirect no", "Traded concessions"],
                  ["At the table", "Ritual refusal", "The full negotiation"]],
        paths=[("✉️ My emails sound wrong", [1, 2, 3], "register, the shape of each channel, the checker on your own drafts"),
               ("🤝 I have a negotiation coming", [3, 5, 6], "the checker, face and the indirect no, the capstone"),
               ("🎯 The whole course", [1, 2, 3, 4, 5, 6], "from register to a full negotiation with its follow-ups")],
        honest=[("Every index and fit on the formality checker", "<strong>Really computed</strong> in your browser from a printed list of 43 markers; the weights and channel bands are constructed and printed in full"),
                ("同比 (tóngbǐ, year on year) and 环比 (huánbǐ, period on period)", "<strong>Read at source</strong> from China's National Bureau of Statistics"),
                ("此致 敬礼 (cǐzhì jìnglǐ, with respect)", "<strong>A widely observed convention</strong>; it is not part of GB/T 9704 or any standard found"),
                ("Face in negotiation", "<strong>Graham and Lam, Harvard Business Review, 2003</strong>, taught as their argument; cultural generalisations are tendencies, not rules"),
                ("BCT, the Business Chinese Test", "<strong>From the official CTI brochure</strong>: BCT (A), BCT (B) and BCT (oral)"),
                ("Lumen Logistics, the drafts and the negotiation", "<strong>Invented</strong> for the running case")],
        not_this=[("I am starting from zero", "Business Chinese Basic ↗", "https://phoebefu6.github.io/learn-business-chinese-basic-with-phoebe/"),
                  ("I want to present and influence in English", "Communication ↗", "https://phoebefu6.github.io/learn-communication-with-phoebe/")],
        here="I speak everyday Chinese and need it to work in emails, meetings and negotiations.",
        sibling=("Business Chinese Basic ↗", "https://phoebefu6.github.io/learn-business-chinese-basic-with-phoebe/"),
        bench_line="The bench in session 3 (`assets/register-live.js`) scores one message written five ways against three channels. Each well-judged draft scores 100 in its own channel; a word-for-word translation is just too casual for WeChat (88); polishing everything into classical phrasing scores 76 even as a formal email and 4 on WeChat.",
    ),
}


def esc(s):
    return s.replace("&", "&amp;")


for k, c in COURSES.items():
    slug = f"learn-business-chinese-{k}-with-phoebe"
    url = f"https://phoebefu6.github.io/{slug}/"
    cards = []
    for i, (f, t, ic, dc, kind, blurb) in enumerate(c["sessions"]):
        pill = '<span class="pill amber">▶ Start here</span>' if i == 0 else ('<span class="pill amber">★ the bench</span>' if i == 2 else ('<span class="pill amber">🔒 final scorecard</span>' if i == 5 else ""))
        cards.append(f'''      <a class="course-card" href="courses/{f}" style="--diff:{dc}">
        <span class="cicon">{ic}</span>
        <span class="cnum">Session {i+1} · {kind}</span>
        <h3>{t}</h3>
        <p>{blurb}</p>
        <span class="meta">{pill}</span>
      </a>''')
    paths = []
    for label, nums, note in c["paths"]:
        steps = '<span class="parr">→</span>'.join(f'<a class="pstep" href="courses/{c["sessions"][n-1][0]}">{n}</a>' for n in nums)
        paths.append(f'      <div class="path"><b>{label}</b>\n        {steps}\n        <span style="font-size:.82rem;color:var(--muted)">{note}</span>\n      </div>')
    stats = "\n".join(f'      <div class="stat"><b data-count="{n}">{n}</b><span>{l}</span></div>' for n, l in c["stats"])
    honest = "\n".join(f"      <tr><td>{a}</td><td>{b}</td></tr>" for a, b in c["honest"])
    nt = "\n".join(f'        <tr><td>{q}</td><td><a href="{u}">{n}</a></td></tr>' for q, n, u in c["not_this"])
    legend = sorted({(dc, kind) for _, _, _, dc, kind, _ in c["sessions"]}, key=lambda x: ["foundational", "core", "advanced", "bench night", "capstone"].index(x[1]))
    leg = "\n".join(f'      <span><i style="background:{dc}"></i>{kind}</span>' for dc, kind in legend)
    mm = {"title": "Business\nChinese " + c["tail"], "centerColor": c["deep"], "sessions": []}
    for i, (f, t, _, dc, _, _) in enumerate(c["sessions"]):
        w = t.split(" ")
        cut = max(1, len(w) // 2)
        mm["sessions"].append({"label": " ".join(w[:cut]) + "\n" + " ".join(w[cut:]), "href": f"courses/{f}", "color": dc,
                               "concepts": [{"label": x, "href": f"courses/{f}"} for x in c["concepts"][i]]})
    mm_js = "window.MINDMAP_DATA = " + json.dumps(mm, ensure_ascii=False, indent=2) + ";"
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- social:start -->
<meta name="description" content="{c['desc']}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Learn with Phoebe">
<meta property="og:title" content="{c['title']}">
<meta property="og:description" content="{c['og']}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{url}assets/og-cover.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{c['title']}">
<meta name="twitter:description" content="{c['og']}">
<meta name="twitter:image" content="{url}assets/og-cover.png">
<!-- social:end -->
<title>{c['title']}</title>
<link rel="stylesheet" href="assets/style.css?v=1">
{STYLE_BLOCK}
</head>
<body>

<header class="masthead">
  <div class="wrap">
    <div class="eyebrow">Learn with Phoebe · Communications</div>
    <h1>Learn <span class="accent">{c['accent']}</span> {c['tail']} with Phoebe</h1>
    <p class="sub">{c['sub']}</p>
    <div class="stats-row">
{stats}
    </div>
  </div>
</header>

<main class="wrap">

  <section class="section">
    <div class="paths" style="margin-top:0">
      <h2>The six sessions 🎯</h2>
      <p class="plede">The running case is <strong>Lumen Logistics</strong>, an invented Singapore freight company, 鲁门物流 (Lǔmén Wùliú, Lumen Logistics), opening a partnership with a Shanghai distributor. You are the person they send.</p>
    </div>
    <div class="course-grid">
{chr(10).join(cards)}
    </div>
    <div class="diff-legend">
{leg}
    </div>
  </section>

  <section class="section">
    <div class="paths" style="margin-top:0">
      <h2>Your passport 🎫</h2>
      <p class="plede">Clear all three quiz questions in a session and it gets stamped. Stamps live in this browser only.</p>
    </div>
    <div class="pp-strip"></div>
  </section>

  <section class="section">
    <div class="not-this">
      <h3>What this is not, so you land in the right place 🧭</h3>
      <table class="clean">
        <tr><th>If your question is</th><th>Go here instead</th></tr>
{nt}
        <tr><td><strong>{c['here']}</strong></td><td><strong>you are in the right place</strong></td></tr>
      </table>
    </div>
  </section>

  <section class="section">
    <div class="paths">
      <h2>Choose your path 🗺️</h2>
      <p class="plede">Three ways through the same six sessions.</p>
{chr(10).join(paths)}
    </div>
  </section>

  <section class="section">
    <div class="paths" style="margin-top:0">
      <h2>What is honest here 🧾</h2>
      <p class="plede">Where a page rests on a standard, a paper or a guide, it says which and how it was read; where something is common practice rather than a documented rule, it says that instead.</p>
    </div>
    <table class="clean">
      <tr><th>Claim</th><th>Status</th></tr>
{honest}
    </table>
  </section>

  <section class="section mm-section">
    <h2>The knowledge map 🧠</h2>
    <p class="mm-lede">The whole course at a glance - hover a session to spotlight its concepts, click any node to jump in.</p>
    <div class="mm-wrap"><div id="mindmap"></div></div>
  </section>

  <footer class="pagefoot">
    <span>{slug} · by Phoebe Fu &nbsp;·&nbsp; 📚 <a href="https://phoebefu6.github.io/learn-with-phoebe/">Learn with Phoebe ↗</a></span>
    <span>Neighbours on the shelf: <a href="{c['sibling'][1]}">{c['sibling'][0]}</a> &nbsp;·&nbsp; <a href="https://phoebefu6.github.io/learn-communication-with-phoebe/">Communication ↗</a></span>
  </footer>

</main>

<script>
{mm_js}
</script>
<script src="assets/mindmap.js?v=1"></script>
<script src="assets/app.js?v=1"></script>
</body>
</html>
'''
    open(f"{GH}/{slug}/index.html", "w").write(html)
    rows = "\n".join(f"| {i+1} | {t} |" for i, (_, t, _, _, _, _) in enumerate(c["sessions"]))
    readme = f'''<!-- learn-with-phoebe hub banner -->
> ### 📚 Part of [**Learn with Phoebe**](https://phoebefu6.github.io/learn-with-phoebe/)
> The shelf of free, hands-on courses on AI, data, and the craft around them. **[Browse every course ↗](https://phoebefu6.github.io/learn-with-phoebe/)**
<!-- /learn-with-phoebe hub banner -->

# {c['title']}

{c['desc'].replace(' Free, by Phoebe Fu.', '')}

**Live site:** {url}

| # | Session |
|---|---|
{rows}

{c['bench_line']}

Every Chinese term on every page carries its pinyin and English. The running case, Lumen Logistics, is invented.

by Phoebe Fu
'''
    open(f"{GH}/{slug}/README.md", "w").write(readme)
    print("built", slug)
