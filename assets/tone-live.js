/* tone-live.js - the tone trainer for learn-business-chinese-basic-with-phoebe
 *
 * A real pitch tracker (YIN: de Cheveigne and Kawahara, JASA 2002) runs on audio in the browser,
 * turns each syllable into a pitch contour, and scores the contour's SHAPE against the four
 * Mandarin tone shapes (Chao's tone letters: T1 55, T2 35, T3 214, T4 51).
 *
 * What is REAL: the tracker, the contour, the scoring, the tone-change (sandhi) rules, every
 *   number on the bench. The same code scores the learner's microphone.
 * What is SYNTHETIC, and labelled so on the widget: the four bench "speakers". They are not
 *   recordings of people. Each is a hum built from a pitch path that follows a tone shape, at a
 *   voice height and range chosen to be typical, so the bench can show what each scoring method
 *   does to a high voice, a low voice and a narrow-range voice without needing a microphone.
 *   The claim the bench makes is the ORDERING of the methods, not an accuracy for real speech.
 *
 * Methods (the ladder):
 *   absolute   compares raw pitch in Hz to one fixed template voice (ANTI: punishes low voices)
 *   relative   compares semitones relative to the speaker's own middle pitch
 *   ranged     relative, and scaled to the speaker's own pitch range (what the trainer uses)
 * Targets:
 *   citation   the tones as the dictionary lists them (ANTI for phrases with tone changes)
 *   surface    the tones after the three tone-change rules (what native speakers say)
 */
(function (root) {
  "use strict";

  var SR = 16000, FRAME = 640, HOP = 160; // 40 ms window, 10 ms hop

  /* ---------- tones as Chao levels (1 = low, 5 = high), sampled at 10 points ---------- */
  function shape(levels) {
    var out = [], n = 10;
    for (var i = 0; i < n; i++) {
      var t = i / (n - 1) * (levels.length - 1), k = Math.min(levels.length - 2, Math.floor(t)), f = t - k;
      out.push(levels[k] * (1 - f) + levels[k + 1] * f);
    }
    return out;
  }
  var TONES = {
    1: shape([5, 5]),
    2: shape([3, 4, 5]),
    3: shape([2, 1, 1, 4]),      // full third tone, said alone or phrase-finally
    "3h": shape([2, 1, 1, 1]),   // half third: before tones 1, 2, 4 the rise is dropped
    4: shape([5, 3, 1])
  };
  var NAMES = { 1: "first (high, level)", 2: "second (rising)", 3: "third (dipping)", "3h": "half third (low)", 4: "fourth (falling)" };

  /* ---------- tone-change (sandhi) rules ---------- */
  /* syllables: [{ hz: "你", py: "ni", t: 3 }, ...]; t 0 = neutral. Returns surface tones. */
  function applySandhi(syl) {
    var s = syl.map(function (x) { return x.t; });
    // 3 + 3: the first third tone becomes a second tone (right to left for runs of two)
    for (var i = s.length - 2; i >= 0; i--) if (s[i] === 3 && s[i + 1] === 3) s[i] = 2;
    for (i = 0; i < syl.length - 1; i++) {
      var next = s[i + 1];
      if (syl[i].hz === "不" && next === 4) s[i] = 2;
      if (syl[i].hz === "一" && !syl[i].ordinal) s[i] = (next === 4 ? 2 : (next >= 1 && next <= 3 ? 4 : s[i]));
    }
    // a third tone that is not last and not before a third tone is a half third
    for (i = 0; i < s.length - 1; i++) if (s[i] === 3) s[i] = "3h";
    return s;
  }

  /* ---------- synthetic speaker: a hum that follows a pitch path ---------- */
  function synth(syls, voice, opts) {
    opts = opts || {};
    var dur = 0.32, gap = 0.08, n = Math.round((dur + gap) * syls.length * SR), out = new Float32Array(n), ph = 0, pos = 0;
    syls.forEach(function (tone) {
      var path = tone === 0 ? shape([3, 2]) : TONES[tone];
      var len = Math.round(dur * SR);
      for (var i = 0; i < len; i++) {
        var u = i / len, k = u * (path.length - 1), a = Math.floor(k), f = k - a;
        var lev = path[Math.min(a, path.length - 1)] * (1 - f) + path[Math.min(a + 1, path.length - 1)] * f;
        var semis = (lev - 3) / 4 * voice.range;               // level 3 = the voice's middle
        var hz = voice.mid * Math.pow(2, semis / 12);
        ph += 2 * Math.PI * hz / SR;
        var env = Math.sin(Math.PI * Math.min(1, u * 1.15));   // soft on and off
        out[pos + i] = env * (0.6 * Math.sin(ph) + 0.25 * Math.sin(2 * ph) + 0.12 * Math.sin(3 * ph));
      }
      pos += len + Math.round(gap * SR);
    });
    if (opts.noise) for (var j = 0; j < n; j++) out[j] += (Math.random() - 0.5) * opts.noise;
    return out;
  }

  /* ---------- YIN pitch tracker ---------- */
  function yin(buf, sr, lo, hi) {
    var W = buf.length >> 1, tauMin = Math.floor(sr / hi), tauMax = Math.min(W - 1, Math.ceil(sr / lo));
    var d = new Float32Array(tauMax + 1), cm = new Float32Array(tauMax + 1), run = 0, e = 0;
    for (var i = 0; i < W; i++) e += buf[i] * buf[i];
    if (e / W < 1e-4) return 0;                                   // silence
    for (var tau = 1; tau <= tauMax; tau++) {
      var s = 0;
      for (i = 0; i < W; i++) { var x = buf[i] - buf[i + tau]; s += x * x; }
      d[tau] = s; run += s; cm[tau] = run ? s * tau / run : 1;
    }
    for (tau = tauMin; tau <= tauMax; tau++) {
      if (cm[tau] < 0.15) {
        while (tau + 1 <= tauMax && cm[tau + 1] < cm[tau]) tau++;
        var a = cm[tau - 1], b = cm[tau], c = cm[Math.min(tau + 1, tauMax)];
        var p = tau + (a - c) / (2 * (a - 2 * b + c) || 1);       // parabolic refinement
        return sr / p;
      }
    }
    return 0;                                                     // unvoiced
  }
  function track(samples, sr) {
    sr = sr || SR;
    var f0 = [];
    for (var s = 0; s + FRAME <= samples.length; s += HOP) f0.push(yin(samples.subarray(s, s + FRAME), sr, 60, 500));
    return f0;
  }

  /* split the frame track into syllables at runs of unvoiced frames */
  function syllables(f0) {
    var out = [], cur = [];
    f0.forEach(function (v) {
      if (v > 0) cur.push(v);
      else if (cur.length) { if (cur.length >= 8) out.push(cur); cur = []; }
    });
    if (cur.length >= 8) out.push(cur);
    return out;
  }
  function resample(arr, n) {
    var out = [];
    for (var i = 0; i < n; i++) {
      var t = i / (n - 1) * (arr.length - 1), k = Math.min(arr.length - 2, Math.floor(t)), f = t - k;
      out.push(arr.length < 2 ? arr[0] : arr[k] * (1 - f) + arr[k + 1] * f);
    }
    return out;
  }
  function median(a) { var b = a.slice().sort(function (x, y) { return x - y; }); return b[b.length >> 1]; }
  function st(hz, ref) { return 12 * Math.log(hz / ref) / Math.LN2; }

  /* trim the first and last 15 percent of each syllable: onsets and offsets are unstable */
  function core(hzs) { var a = Math.floor(hzs.length * 0.15), b = Math.ceil(hzs.length * 0.85); return hzs.slice(a, b); }

  /* ---------- the three scoring methods ---------- */
  var TEMPLATE_VOICE = { mid: 210, range: 10 };   // the fixed voice the absolute method assumes

  function levelsFromHz(hzs, method, speaker) {
    // returns the contour expressed in Chao levels (1..5) under each method's assumptions
    if (method === "absolute") return hzs.map(function (h) { return 3 + st(h, TEMPLATE_VOICE.mid) / TEMPLATE_VOICE.range * 4; });
    if (method === "relative") return hzs.map(function (h) { return 3 + st(h, speaker.mid) / TEMPLATE_VOICE.range * 4; });
    return hzs.map(function (h) { return 3 + st(h, speaker.mid) / speaker.range * 4; });   // ranged
  }
  /* estimate a speaker's middle pitch and range from everything they said */
  function speakerOf(sylHz) {
    var all = [].concat.apply([], sylHz.map(core));
    var sorted = all.slice().sort(function (a, b) { return a - b; });
    var lo = sorted[Math.floor(sorted.length * 0.05)], hi = sorted[Math.floor(sorted.length * 0.95)];
    var rng = Math.max(4, st(hi, lo));                                    // never divide by a tiny range
    return { mid: Math.sqrt(lo * hi), range: rng };
  }
  function dist(a, b) { var s = 0; for (var i = 0; i < a.length; i++) s += (a[i] - b[i]) * (a[i] - b[i]); return Math.sqrt(s / a.length); }
  function classify(levels) {
    var best = null;
    [1, 2, 3, "3h", 4].forEach(function (t) {
      var d = dist(levels, TONES[t]);
      if (!best || d < best.d) best = { t: t, d: d };
    });
    return best;
  }
  /* a tone matches its target if it classifies as the target; 3 and 3h count as each other */
  function same(a, b) { return a === b || (a === 3 && b === "3h") || (a === "3h" && b === 3); }

  /* calibration: the speaker says ma ma ma ma on the four tones once; their middle pitch and
     range come from that, not from the phrase being scored. A phrase on one level (gongsi,
     two first tones) has no range of its own, so judged alone it cannot be told from the middle. */
  var CALIB = [1, 2, 3, 4];
  function calibrate(samples, sr) { return speakerOf(syllables(track(samples, sr))); }

  function scoreUtterance(samples, targets, method, sr, speaker) {
    var f0 = track(samples, sr), sy = syllables(f0);
    var n = Math.min(sy.length, targets.length), sp = speaker || speakerOf(sy.slice(0, n)), res = [];
    for (var i = 0; i < n; i++) {
      if (targets[i] === 0) { res.push({ target: 0, heard: 0, ok: null }); continue; }   // neutral: not scored
      var lv = resample(levelsFromHz(core(sy[i]), method, sp), 10), c = classify(lv);
      res.push({ target: targets[i], heard: c.t, ok: same(c.t, targets[i]), d: c.d, levels: lv });
    }
    var scored = res.filter(function (r) { return r.ok !== null; });
    return { syllables: res, found: sy.length, expected: targets.length, speaker: sp,
             correct: scored.filter(function (r) { return r.ok; }).length, scored: scored.length };
  }

  /* ---------- the bench: four synthetic speakers, three methods, two targets ---------- */
  var SPEAKERS = [
    { id: "high", label: "Higher voice", mid: 220, range: 10 },
    { id: "low", label: "Lower voice", mid: 115, range: 10 },
    { id: "narrow", label: "Narrow-range voice", mid: 170, range: 5 },
    { id: "wide", label: "Wide-range voice", mid: 190, range: 14 }
  ];
  /* the phrase list: business words, with dictionary (citation) tones; surface tones are computed */
  var PHRASES = [
    { hz: "你好", py: "nǐ hǎo", en: "hello", syl: [{ hz: "你", py: "nǐ", t: 3 }, { hz: "好", py: "hǎo", t: 3 }] },
    { hz: "您好", py: "nín hǎo", en: "hello (polite)", syl: [{ hz: "您", py: "nín", t: 2 }, { hz: "好", py: "hǎo", t: 3 }] },
    { hz: "开会", py: "kāihuì", en: "have a meeting", syl: [{ hz: "开", py: "kāi", t: 1 }, { hz: "会", py: "huì", t: 4 }] },
    { hz: "经理", py: "jīnglǐ", en: "manager", syl: [{ hz: "经", py: "jīng", t: 1 }, { hz: "理", py: "lǐ", t: 3 }] },
    { hz: "老板", py: "lǎobǎn", en: "boss, owner", syl: [{ hz: "老", py: "lǎo", t: 3 }, { hz: "板", py: "bǎn", t: 3 }] },
    { hz: "不是", py: "bú shì", en: "is not", syl: [{ hz: "不", py: "bù", t: 4 }, { hz: "是", py: "shì", t: 4 }] },
    { hz: "一定", py: "yídìng", en: "certainly", syl: [{ hz: "一", py: "yī", t: 1 }, { hz: "定", py: "dìng", t: 4 }] },
    { hz: "一起", py: "yìqǐ", en: "together", syl: [{ hz: "一", py: "yī", t: 1 }, { hz: "起", py: "qǐ", t: 3 }] },
    { hz: "买卖", py: "mǎimài", en: "buying and selling, business", syl: [{ hz: "买", py: "mǎi", t: 3 }, { hz: "卖", py: "mài", t: 4 }] },
    { hz: "合同", py: "hétong", en: "contract", syl: [{ hz: "合", py: "hé", t: 2 }, { hz: "同", py: "tong", t: 0 }] },
    { hz: "价格", py: "jiàgé", en: "price", syl: [{ hz: "价", py: "jià", t: 4 }, { hz: "格", py: "gé", t: 2 }] },
    { hz: "公司", py: "gōngsī", en: "company", syl: [{ hz: "公", py: "gōng", t: 1 }, { hz: "司", py: "sī", t: 1 }] }
  ];
  function surface(p) { return applySandhi(p.syl); }
  function citation(p) { return p.syl.map(function (x) { return x.t; }); }

  /* run every phrase through one speaker, saying the SURFACE tones correctly (and, for the
     mistake test, with one deliberately wrong tone), and score with a method against a target */
  function benchCell(speaker, method, target, calibrated) {
    var ok = 0, n = 0, caught = 0, wrongs = 0;
    var prof = calibrated === false ? null : calibrate(synth(CALIB, speaker));
    PHRASES.forEach(function (p) {
      var said = surface(p);
      var r = scoreUtterance(synth(said, speaker), target === "citation" ? citation(p) : said, method, SR, prof);
      r.syllables.forEach(function (s) { if (s.ok !== null) { n++; if (s.ok) ok++; } });
      // the mistake test: swap the last scored tone for a clearly different one
      var bad = said.slice(), idx = bad.length - 1;
      while (idx >= 0 && bad[idx] === 0) idx--;
      if (idx >= 0) {
        bad[idx] = { 1: 4, 2: 4, 3: 1, "3h": 1, 4: 1 }[bad[idx]];
        var r2 = scoreUtterance(synth(bad, speaker), said, method, SR, prof);
        var s2 = r2.syllables[idx];
        if (s2 && s2.ok !== null) { wrongs++; if (!s2.ok) caught++; }
      }
    });
    return { correctRight: ok, scored: n, mistakesCaught: caught, mistakes: wrongs };
  }
  function runBench() {
    var out = {};
    ["absolute", "relative", "ranged"].forEach(function (m) {
      out[m] = {};
      SPEAKERS.forEach(function (s) { out[m][s.id] = benchCell(s, m, "surface"); });
    });
    out.citation = {}; out.uncalibrated = {};
    SPEAKERS.forEach(function (s) {
      out.citation[s.id] = benchCell(s, "ranged", "citation");
      out.uncalibrated[s.id] = benchCell(s, "ranged", "surface", false);
    });
    return out;
  }

  /* ---------- UI ---------- */
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function pct(a, b) { return b ? Math.round(100 * a / b) + "%" : "-"; }
  var TN = { 1: "1", 2: "2", 3: "3", "3h": "3 (half)", 4: "4", 0: "neutral" };

  function buildBench(el, res) {
    var rows = [
      ["absolute", "Raw pitch in Hz, one template voice", "anti"],
      ["relative", "Semitones from your own middle pitch", ""],
      ["ranged", "Semitones from your middle, scaled to your range, calibrated", "good"],
      ["uncalibrated", "As above, but judging each phrase on its own", ""],
      ["citation", "Calibrated, but scored against dictionary tones", "anti"]
    ];
    var head = SPEAKERS.map(function (s) { return "<th>" + esc(s.label) + "<em>" + s.mid + " Hz, " + s.range + " semitones</em></th>"; }).join("");
    var body = rows.map(function (r) {
      var cells = SPEAKERS.map(function (s) {
        var c = res[r[0]][s.id];
        return "<td><b>" + pct(c.correctRight, c.scored) + "</b><em>right tones heard right</em>" +
          "<b class='tl-catch'>" + c.mistakesCaught + " of " + c.mistakes + "</b><em>mistakes caught</em></td>";
      }).join("");
      return "<tr class='tl-" + r[2] + "'><th>" + esc(r[1]) + (r[2] === "anti" ? " <span class='mb-anti'>trap</span>" : "") + "</th>" + cells + "</tr>";
    }).join("");
    el.innerHTML = "<table class='dt-table tl-table'><thead><tr><th>Scoring method</th>" + head + "</tr></thead><tbody>" + body + "</tbody></table>" +
      "<p class='mb-hint'>The four speakers are synthetic hums that follow each tone's shape at a typical voice height and range, not recordings of people. Each says all " +
      PHRASES.length + " phrases with the tones a native speaker uses, then again with one tone deliberately wrong. The tracker, the contour and the scoring are real and run in your browser; the same code scores your microphone below.</p>";
  }

  function buildPractice(el) {
    var opts = PHRASES.map(function (p, i) { return "<option value='" + i + "'>" + esc(p.hz + " (" + p.py + ", " + p.en + ")") + "</option>"; }).join("");
    el.innerHTML =
      "<div class='tl-row tl-cal'><span class='tl-calstate'>Step 1: say <b>mā má mǎ mà</b> once so the trainer learns your voice.</span>" +
      "<button type='button' class='btn tl-calrec'>Calibrate (2 seconds)</button></div>" +
      "<div class='tl-row'><label>Phrase <select class='tl-phrase'>" + opts + "</select></label>" +
      "<button type='button' class='btn tl-hear'>Hear the tone shape</button>" +
      "<button type='button' class='btn primary tl-rec'>Record 2 seconds</button>" +
      "<button type='button' class='btn tl-say'>Try the synthetic voice</button></div>" +
      "<div class='tl-target'></div><div class='tl-out'></div>" +
      "<p class='mb-hint'>Your recording stays in this page; nothing is uploaded. Say the phrase once, at a normal speed. The shape is what is scored, so a high or a low voice is fine.</p>";
    var sel = el.querySelector(".tl-phrase"), tgt = el.querySelector(".tl-target"), out = el.querySelector(".tl-out");
    var profile = null, calState = el.querySelector(".tl-calstate");
    function showTarget() {
      var p = PHRASES[+sel.value], c = citation(p), s = surface(p);
      tgt.innerHTML = "<span class='tl-big'>" + esc(p.hz) + "</span> <span>(" + esc(p.py) + ", " + esc(p.en) + ")</span>" +
        "<span class='tl-tones'>dictionary tones " + c.map(function (t) { return TN[t]; }).join(" + ") +
        " · said as " + s.map(function (t) { return TN[t]; }).join(" + ") + (c.join() !== s.join() ? " <b>(a tone change applies)</b>" : "") + "</span>";
    }
    function show(r) {
      var p = PHRASES[+sel.value];
      if (r.found < r.expected) { out.innerHTML = "<div class='mb-verdict is-bad'>Heard " + r.found + " syllable(s), expected " + r.expected + ". Try again a little louder, with a short gap between syllables.</div>"; return; }
      out.innerHTML = "<div class='mb-verdict " + (r.correct === r.scored ? "is-good" : "is-ok") + "'>" + r.correct + " of " + r.scored + " tones heard as intended</div>" +
        "<ul class='tl-list'>" + r.syllables.map(function (s, i) {
          return "<li><b>syllable " + (i + 1) + ", " + esc(p.syl[i].py) + "</b>: " + (s.ok === null ? "neutral tone, not scored" : "aimed for tone " + TN[s.target] + ", heard tone " + TN[s.heard] + (s.ok ? " · right" : " · try again")) + "</li>";
        }).join("") + "</ul>";
    }
    sel.addEventListener("change", function () { showTarget(); out.innerHTML = ""; });
    el.querySelector(".tl-say").addEventListener("click", function () {
      var p = PHRASES[+sel.value];
      show(scoreUtterance(synth(surface(p), SPEAKERS[1]), surface(p), "ranged", SR, calibrate(synth(CALIB, SPEAKERS[1]))));
    });
    el.querySelector(".tl-hear").addEventListener("click", function () {
      var p = PHRASES[+sel.value], s = synth(surface(p), { mid: 180, range: 10 });
      try {
        var ctx = new (root.AudioContext || root.webkitAudioContext)(), b = ctx.createBuffer(1, s.length, SR);
        b.getChannelData(0).set(s); var src = ctx.createBufferSource(); src.buffer = b; src.connect(ctx.destination); src.start();
      } catch (e) { out.innerHTML = "<div class='mb-verdict is-bad'>This browser cannot play audio here.</div>"; }
    });
    function record(done) {
      if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) { out.innerHTML = "<div class='mb-verdict is-bad'>No microphone access in this browser. The synthetic voice button shows the same scoring.</div>"; return; }
      out.innerHTML = "<div class='mb-verdict is-ok'>Recording for 2 seconds...</div>";
      navigator.mediaDevices.getUserMedia({ audio: true }).then(function (stream) {
        var ctx = new (root.AudioContext || root.webkitAudioContext)(), srcN = ctx.createMediaStreamSource(stream);
        var proc = ctx.createScriptProcessor(4096, 1, 1), chunks = [];
        proc.onaudioprocess = function (e) { chunks.push(new Float32Array(e.inputBuffer.getChannelData(0))); };
        srcN.connect(proc); proc.connect(ctx.destination);
        setTimeout(function () {
          proc.disconnect(); srcN.disconnect(); stream.getTracks().forEach(function (t) { t.stop(); });
          var len = chunks.reduce(function (a, c) { return a + c.length; }, 0), all = new Float32Array(len), o = 0;
          chunks.forEach(function (c) { all.set(c, o); o += c.length; });
          var ratio = ctx.sampleRate / SR, down = new Float32Array(Math.floor(len / ratio));
          for (var i = 0; i < down.length; i++) down[i] = all[Math.floor(i * ratio)];
          done(down);
        }, 2000);
      }).catch(function () { out.innerHTML = "<div class='mb-verdict is-bad'>Microphone permission was not given. The synthetic voice button shows the same scoring.</div>"; });
    }
    el.querySelector(".tl-calrec").addEventListener("click", function () {
      record(function (down) {
        var sy = syllables(track(down, SR));
        if (sy.length < 4) { out.innerHTML = "<div class='mb-verdict is-bad'>Heard " + sy.length + " of 4 syllables. Say ma ma ma ma with a short gap between each.</div>"; return; }
        profile = speakerOf(sy);
        calState.innerHTML = "Calibrated: your middle pitch is about " + Math.round(profile.mid) + " Hz and your range about " + Math.round(profile.range) + " semitones.";
        out.innerHTML = "";
      });
    });
    el.querySelector(".tl-rec").addEventListener("click", function () {
      record(function (down) {
        var p = PHRASES[+sel.value];
        if (!profile) out.innerHTML = "";
        show(scoreUtterance(down, surface(p), "ranged", SR, profile || undefined));
        if (!profile) out.innerHTML += "<p class='mb-hint'>Not calibrated yet, so this phrase was judged on its own. Phrases on one level, like 公司 (gōngsī, company), score better after step 1.</p>";
      });
    });
    showTarget();
  }

  function init() {
    var benchEl = document.getElementById("tone-bench"), pracEl = document.getElementById("tone-practice");
    if (benchEl) {
      /* about two seconds of real audio analysis: let the page paint first */
      benchEl.innerHTML = "<p class='mb-hint'>Computing: four voices, twelve phrases, five methods...</p>";
      setTimeout(function () { var res = runBench(); buildBench(benchEl, res); root.TONE_LIVE = { results: res, ready: true }; }, 60);
    }
    if (pracEl) buildPractice(pracEl);
  }

  var api = { synth: synth, track: track, syllables: syllables, applySandhi: applySandhi, scoreUtterance: scoreUtterance,
              runBench: runBench, benchCell: benchCell, calibrate: calibrate, CALIB: CALIB, PHRASES: PHRASES, SPEAKERS: SPEAKERS, TONES: TONES, surface: surface, citation: citation };
  if (typeof module !== "undefined" && module.exports) module.exports = api;
  if (typeof document !== "undefined") {
    if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
  }
})(typeof window !== "undefined" ? window : this);
