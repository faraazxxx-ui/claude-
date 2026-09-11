(() => {
  const cents = (hz, c) => hz * 2 ** (c / 1200);

  const APPS = [
    { id: "isochronic", name: "Isochronic", bg: "#5e5ce6", glyph: "pulse" },
    { id: "binaural", name: "Binaural", bg: "#111", glyph: "wave" },
    { id: "maqam", name: "Maqām", bg: "#ff375f", glyph: "play" },
    { id: "quran", name: "Al-Qurʾān", bg: "#30d158", glyph: "crescent" },
    { id: "focus", name: "Focus bed", bg: "#1c1c1e", glyph: "f" },
    { id: "listen", name: "Listen", bg: "#0a84ff", glyph: "speak" },
    { id: "noise", name: "Noise", bg: "#ff9f0a", glyph: "bars" },
    { id: "recovery", name: "Recovery", bg: "#ff6b00", glyph: "orb" },
    { id: "classical", name: "Classical", bg: "#2c2c2e", glyph: "clef" },
  ];

  const DAY = [
    {
      id: "wake",
      label: "Wake / initiate",
      title: "Activation without rumination",
      body: "Anhedonia and “low dopamine” here means low initiation, not a lab dopamine level. Do not start the day in theta or Saba. Use light, movement, then a short activating bed.",
      play: { kind: "combo", noise: "pink", isoHz: 16, minutes: 15, title: "Wake initiation" },
      apps: "Isochronic 16 Hz · myNoise pink · YouTube Music Rast/Bayati 10 min",
    },
    {
      id: "work",
      label: "ADHD work",
      title: "Work block",
      body: "White/pink noise has a small but significant benefit on ADHD laboratory attention tasks (g ≈ 0.25) and can impair people without ADHD. Keep lyrics out. Stop after one block so burnout does not get more beta.",
      play: { kind: "combo", noise: "pink", isoHz: 14, minutes: 25, title: "ADHD work block" },
      apps: "myNoise pink · focus@will instrumental · Speechify 1.1–1.4×",
    },
    {
      id: "crash",
      label: "Afternoon",
      title: "Protect the crash",
      body: "If you stack more stimulation here you will look productive and feel worse. Ten minutes of Bayati or a 100 Hz drone plus a walk is closer to the bimaristan model than another beta track.",
      play: { kind: "maqam", maqam: "bayati", minutes: 10, title: "Afternoon Bayati" },
      apps: "YouTube Music Bayati taqsīm · Classical slow · no Headspace yet",
    },
    {
      id: "burnout",
      label: "Burnout hour",
      title: "Restore, do not stimulate",
      body: "This is the Golden Age piece: courtyard, water, live tone. Brown noise approximates the fountain. Alpha or no beat. Familiar recitation if it settles you. Rast for collectedness.",
      play: { kind: "combo", noise: "brown", binauralHz: 10, minutes: 25, title: "Bimaristan recovery" },
      apps: "myNoise waterfall · Al-Qurʾān · Headspace breath · Classical adagio",
    },
    {
      id: "night",
      label: "Night",
      title: "Shutdown",
      body: "Theta can deepen inwardness. In treatment-resistant depression that sometimes helps sleep and sometimes feeds rumination. Prefer familiar recitation or Rast. Use Saba only if you intentionally want grief, not as a default.",
      play: { kind: "combo", noise: "brown", binauralHz: 4, minutes: 25, title: "Night shutdown" },
      apps: "Al-Qurʾān 1 / 36 / 67 / 94 · BinauralBeatGen 2–4 Hz · Headspace wind-down",
    },
  ];

  const MAQAM = {
    rast: {
      name: "Rast",
      use: "Collected activation — the traditional “soundness of mind” mode. Default for TRD mornings.",
      freqs: [261.63, 293.66, cents(329.63, -50), 349.23],
    },
    bayati: {
      name: "Bayati",
      use: "Lift and vitality without forcing cheer. Good for afternoon crash and anhedonia.",
      freqs: [293.66, cents(329.63, -50), 349.23, 392.0],
    },
    hijaz: {
      name: "Hijaz",
      use: "Open, yearning, spacious. Use when you need distance from the workday.",
      freqs: [293.66, 311.13, 369.99, 392.0],
    },
    saba: {
      name: "Saba",
      use: "Sadness and tenderness. Not the default in treatment-resistant depression.",
      warn: "Skip if you are already looping on despair. Catharsis is optional, not a protocol.",
      freqs: [293.66, cents(329.63, -50), 349.23, 369.99],
    },
  };

  const engine = {
    ctx: null,
    nodes: [],
    timer: null,
    startedAt: 0,
    title: "",
    meta: "",
  };

  const $ = (id) => document.getElementById(id);

  function iconSvg(glyph) {
    const common = 'width="34" height="34" viewBox="0 0 34 34" fill="none"';
    const map = {
      pulse: `<svg ${common}><path d="M4 17h5l3-8 6 16 3-8h9" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
      wave: `<svg ${common}><path d="M3 17c4-10 8 10 14 0s8 10 14 0" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/></svg>`,
      play: `<svg ${common}><circle cx="17" cy="17" r="12" fill="#fff"/><path d="M14 11l10 6-10 6V11z" fill="#ff375f"/></svg>`,
      crescent: `<svg ${common}><path d="M20 7a10 10 0 1 0 7 17 11 11 0 1 1-7-17z" fill="#fff"/></svg>`,
      f: `<svg ${common}><text x="17" y="24" text-anchor="middle" font-size="22" font-family="Georgia" fill="#fff">f</text></svg>`,
      speak: `<svg ${common}><path d="M6 13h6l7-6v20l-7-6H6v-8z" fill="#fff"/><path d="M23 12c2 2 2 8 0 10M26 9c4 4 4 12 0 16" stroke="#fff" stroke-width="2" stroke-linecap="round"/></svg>`,
      bars: `<svg ${common}><rect x="6" y="16" width="4" height="12" rx="1" fill="#fff"/><rect x="15" y="8" width="4" height="20" rx="1" fill="#fff"/><rect x="24" y="12" width="4" height="16" rx="1" fill="#fff"/></svg>`,
      orb: `<svg ${common}><circle cx="17" cy="17" r="11" fill="#fff"/></svg>`,
      clef: `<svg ${common}><path d="M17 28c-4 0-6-3-6-6 0-5 7-7 7-12 0-2-1-4-3-4-3 0-4 3-2 5" stroke="#f5d78a" stroke-width="2.2" fill="none" stroke-linecap="round"/><circle cx="14" cy="23" r="2.2" fill="#f5d78a"/></svg>`,
    };
    return map[glyph];
  }

  function ensureCtx() {
    if (!engine.ctx) engine.ctx = new AudioContext();
    if (engine.ctx.state === "suspended") engine.ctx.resume();
    return engine.ctx;
  }

  function track(node) {
    engine.nodes.push(node);
    return node;
  }

  function stop() {
    engine.nodes.forEach((n) => {
      try { n.stop?.(); } catch (_) {}
      try { n.disconnect?.(); } catch (_) {}
    });
    engine.nodes = [];
    clearInterval(engine.timer);
    engine.timer = null;
    $("player").hidden = true;
    $("player-title").textContent = "Idle";
    $("player-meta").textContent = "—";
    $("player-clock").textContent = "00:00";
  }

  function masterGain(volume) {
    const ctx = ensureCtx();
    const g = track(ctx.createGain());
    g.gain.value = Math.min(0.22, Number(volume) || 0.08);
    g.connect(ctx.destination);
    return g;
  }

  function startClock(minutes, title, meta) {
    engine.title = title;
    engine.meta = meta;
    engine.startedAt = Date.now();
    $("player").hidden = false;
    $("player-title").textContent = title;
    $("player-meta").textContent = meta;
    const limit = minutes ? minutes * 60 * 1000 : 0;
    clearInterval(engine.timer);
    engine.timer = setInterval(() => {
      const elapsed = Date.now() - engine.startedAt;
      const s = Math.floor(elapsed / 1000);
      $("player-clock").textContent = `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;
      if (limit && elapsed >= limit) stop();
    }, 250);
  }

  function noiseBuffer(ctx, color) {
    const len = ctx.sampleRate * 2;
    const buffer = ctx.createBuffer(1, len, ctx.sampleRate);
    const data = buffer.getChannelData(0);
    let b0 = 0, b1 = 0, b2 = 0, last = 0;
    for (let i = 0; i < len; i++) {
      const white = Math.random() * 2 - 1;
      if (color === "white") {
        data[i] = white * 0.35;
      } else if (color === "brown") {
        last = (last + 0.02 * white) / 1.02;
        data[i] = last * 3.5;
      } else {
        b0 = 0.99765 * b0 + white * 0.099046;
        b1 = 0.963 * b1 + white * 0.2965164;
        b2 = 0.5701 * b2 + white * 1.052691;
        data[i] = (b0 + b1 + b2 + white * 0.1848) * 0.08;
      }
    }
    return buffer;
  }

  function playNoise(color, volume, dest) {
    const ctx = ensureCtx();
    const src = track(ctx.createBufferSource());
    src.buffer = noiseBuffer(ctx, color);
    src.loop = true;
    const g = track(ctx.createGain());
    g.gain.value = volume ?? 0.12;
    src.connect(g).connect(dest);
    src.start();
  }

  function playIsochronic(carrier, pulseHz, volume, dest) {
    const ctx = ensureCtx();
    const osc = track(ctx.createOscillator());
    const amp = track(ctx.createGain());
    const lfo = track(ctx.createOscillator());
    const lfoGain = track(ctx.createGain());
    osc.frequency.value = carrier;
    lfo.frequency.value = pulseHz;
    lfo.type = "square";
    amp.gain.value = 0;
    lfoGain.gain.value = volume ?? 0.09;
    lfo.connect(lfoGain).connect(amp.gain);
    osc.connect(amp).connect(dest);
    osc.start();
    lfo.start();
  }

  function playBinaural(leftHz, rightHz, volume, dest) {
    const ctx = ensureCtx();
    const merger = track(ctx.createChannelMerger(2));
    const oscL = track(ctx.createOscillator());
    const oscR = track(ctx.createOscillator());
    const gL = track(ctx.createGain());
    const gR = track(ctx.createGain());
    gL.gain.value = volume ?? 0.06;
    gR.gain.value = volume ?? 0.06;
    oscL.frequency.value = leftHz;
    oscR.frequency.value = rightHz;
    oscL.connect(gL).connect(merger, 0, 0);
    oscR.connect(gR).connect(merger, 0, 1);
    merger.connect(dest);
    oscL.start();
    oscR.start();
  }

  function playMaqam(key, volume, dest) {
    const ctx = ensureCtx();
    const spec = MAQAM[key];
    spec.freqs.forEach((hz, i) => {
      const osc = track(ctx.createOscillator());
      const g = track(ctx.createGain());
      const lfo = track(ctx.createOscillator());
      const lg = track(ctx.createGain());
      osc.type = i % 2 ? "triangle" : "sine";
      osc.frequency.value = hz;
      g.gain.value = (volume ?? 0.035) * (i === 0 ? 1 : 0.55);
      lfo.frequency.value = 0.04 + i * 0.015;
      lg.gain.value = 0.012;
      lfo.connect(lg).connect(g.gain);
      osc.connect(g).connect(dest);
      osc.start();
      lfo.start();
    });
  }

  function playSpec(spec) {
    stop();
    const dest = masterGain(0.16);
    const minutes = spec.minutes || 20;
    if (spec.kind === "noise") playNoise(spec.noise, 0.14, dest);
    if (spec.kind === "iso") playIsochronic(spec.carrier || 180, spec.isoHz, 0.09, dest);
    if (spec.kind === "binaural") {
      const carrier = spec.carrier || 200;
      playBinaural(carrier, carrier + spec.binauralHz, 0.06, dest);
    }
    if (spec.kind === "maqam") playMaqam(spec.maqam, 0.04, dest);
    if (spec.kind === "combo") {
      if (spec.noise) playNoise(spec.noise, 0.1, dest);
      if (spec.isoHz) playIsochronic(spec.carrier || 170, spec.isoHz, 0.05, dest);
      if (spec.binauralHz) playBinaural(200, 200 + spec.binauralHz, 0.04, dest);
      if (spec.maqam) playMaqam(spec.maqam, 0.03, dest);
    }
    startClock(minutes, spec.title, spec.meta || `${minutes} min · stop if mood worsens`);
    $("sheet").hidden = true;
  }

  function recipeBlock(lines) {
    return `<div class="recipe"><strong>Use in your apps</strong><br>${lines.join("<br>")}</div>`;
  }

  function screens() {
    return {
      isochronic: () => `
        <h2>Isochronic</h2>
        <p>One pulsing tone. Works on a speaker, so it is closer to a real <em>īqāʿ</em> than binaural beats. Better first-line for ADHD initiation than dichotic sine waves.</p>
        <div class="row">
          <button class="primary" data-play='{"kind":"iso","isoHz":16,"minutes":15,"title":"16 Hz initiation"}'>16 Hz initiate</button>
          <button class="secondary" data-play='{"kind":"iso","isoHz":14,"minutes":25,"title":"14 Hz work"}'>14 Hz work</button>
          <button class="secondary" data-play='{"kind":"iso","isoHz":10,"minutes":20,"title":"10 Hz calm alert"}'>10 Hz calm</button>
        </div>
        ${recipeBlock([
          "Isochronic app: carrier 160–200 Hz, pulse 14–16 Hz, 15–25 min, low volume.",
          "Do not run beta pulses all day. That is how this stack feeds burnout.",
        ])}
        <div class="note">Evidence for isochronic tones is thinner than for noise or music. Treat this as an arousal metronome, not a dopamine pump.</div>
      `,
      binaural: () => `
        <h2>Binaural</h2>
        <p>Two carriers, one per ear. Requires stereo headphones. The “beat” is an illusion in the brainstem, not the hospital practice you read about. Behavioral effects are mixed-to-modest; EEG entrainment is not established.</p>
        <div class="row">
          <button class="primary" data-play='{"kind":"binaural","binauralHz":16,"minutes":20,"title":"16 Hz beta · headphones"}'>16 Hz focus</button>
          <button class="secondary" data-play='{"kind":"binaural","binauralHz":10,"minutes":20,"title":"10 Hz alpha"}'>10 Hz alpha</button>
          <button class="secondary" data-play='{"kind":"binaural","binauralHz":6,"minutes":20,"title":"6 Hz theta"}'>6 Hz theta</button>
          <button class="warn" data-play='{"kind":"binaural","binauralHz":3,"minutes":25,"title":"3 Hz delta"}'>3 Hz sleep</button>
        </div>
        ${recipeBlock([
          "BinauralBeatGen: L 200 Hz / R 216 Hz for 16 Hz; L 200 / R 210 for 10 Hz; L 200 / R 206 for 6 Hz.",
          "20–30 min, before the task, not only during it. No driving on theta/delta.",
        ])}
        <div class="warnbox">In TRD, skip 6 Hz if it makes you ruminate. Switch to recitation, Rast, or stop.</div>
      `,
      maqam: () => `
        <h2>Maqām</h2>
        <p>This is the historical layer: tones, not binaural beats. The generators below are rough tetrachord beds — a scaffold until you put a ney or oud recording over them.</p>
        ${Object.entries(MAQAM).map(([key, m]) => `
          <div class="recipe">
            <strong>${m.name}</strong>
            <p>${m.use}</p>
            ${m.warn ? `<p class="warnbox">${m.warn}</p>` : ""}
            <button class="primary" data-play='{"kind":"maqam","maqam":"${key}","minutes":15,"title":"${m.name} bed"}'>Generate ${m.name}</button>
            <div class="links">
              <a href="https://www.youtube.com/results?search_query=maqam+${m.name}+oud+taqsim" target="_blank" rel="noreferrer">YouTube Music search</a>
            </div>
          </div>
        `).join("")}
        ${recipeBlock([
          "YouTube Music / Classical: Rast or Bayati taqsīm for initiation; avoid lyric-heavy playlists during ADHD work.",
          "Traditional emotion maps are cultural, not a formulary. Familiarity matters.",
        ])}
      `,
      quran: () => `
        <h2>Al-Qurʾān</h2>
        <p>In the Islamic medical tradition this is not <em>mūsīqā</em>. It is the auditory practice you already have that most cleanly continues hospital recitation and meaning-making. Use your Al-Qurʾān app. Do not bury it under binaural tracks.</p>
        <div class="recipe">
          <strong>Settling set</strong>
          <p>Al-Fātiḥah · Yā Sīn · Al-Mulk · Al-Inshirāḥ · Al-Muʿawwidhatān. Reciters you already know beat a “frequency” stranger.</p>
        </div>
        <div class="recipe">
          <strong>Initiation set</strong>
          <p>Short, familiar, slightly more rhythmic recitation before a work block — then switch to pink noise. Do not listen to a full khatm while trying to write notes.</p>
        </div>
        ${recipeBlock([
          "Al-Qurʾān app: one sitting, 10–20 min, then stop.",
          "If recitation becomes another performance metric, it is no longer recovery.",
        ])}
      `,
      focus: () => `
        <h2>Focus bed</h2>
        <p>This replaces focus@will with a generated bed: pink noise plus a light 14 Hz pulse. Same idea as their instrumental channel — arousal support without words.</p>
        <div class="row">
          <button class="primary" data-play='{"kind":"combo","noise":"pink","isoHz":14,"minutes":25,"title":"Focus bed 25"}'>25 min bed</button>
          <button class="secondary" data-play='{"kind":"combo","noise":"pink","isoHz":16,"minutes":50,"title":"Focus bed 50"}'>50 min bed</button>
          <button class="secondary" data-play='{"kind":"noise","noise":"pink","minutes":25,"title":"Pink only"}'>Pink only</button>
        </div>
        ${recipeBlock([
          "focus@will: instrumental, no lyrics, one channel, one block.",
          "A 100 Hz pure tone also helped ADHD-trait performance in lab work — randomness is not required.",
        ])}
      `,
      listen: () => `
        <h2>Listen</h2>
        <p>Speechify is the correct ADHD tool for papers and inboxes. Audioio does not replace TTS. It tells you how to pair it so listening does not become another open loop.</p>
        <div class="recipe">
          <strong>Protocol</strong>
          <p>1. One document only.<br>2. 1.1–1.4×, not 2× if TRD fog is present.<br>3. Pink noise underneath at very low volume, or silence.<br>4. 15–20 min, then a written action of one line.<br>5. If you are only “consuming,” stop. That is burnout cosplay.</p>
        </div>
        <div class="row">
          <button class="secondary" data-play='{"kind":"noise","noise":"pink","minutes":20,"title":"Listen underlay"}'>Pink underlay</button>
        </div>
      `,
      noise: () => `
        <h2>Noise</h2>
        <p>Best-supported cheap lever for ADHD attention in this whole folder. Nigg et al. found a small benefit of white/pink noise on ADHD task performance and a small harm in non-ADHD controls. Brown noise was not in that meta-analysis; it is here as a waterfall stand-in for recovery.</p>
        <div class="row">
          <button class="primary" data-play='{"kind":"noise","noise":"pink","minutes":25,"title":"Pink noise"}'>Pink</button>
          <button class="secondary" data-play='{"kind":"noise","noise":"white","minutes":25,"title":"White noise"}'>White</button>
          <button class="secondary" data-play='{"kind":"noise","noise":"brown","minutes":30,"title":"Brown / fountain"}'>Brown</button>
        </div>
        ${recipeBlock(["myNoise: pink for work, rain/waterfall for burnout hour, keep volume conversational or lower."])}
      `,
      recovery: () => `
        <h2>Recovery</h2>
        <p>Headspace analogue: downshift. Burnout does not improve from more 16 Hz. This is the Nuri-hospital move — water, tone, breath, time-limited sitting.</p>
        <div class="row">
          <button class="primary" data-play='{"kind":"combo","noise":"brown","binauralHz":10,"minutes":20,"title":"Recovery alpha"}'>Alpha + fountain</button>
          <button class="secondary" data-play='{"kind":"combo","noise":"brown","maqam":"rast","minutes":20,"title":"Rast recovery"}'>Rast + fountain</button>
        </div>
        <div class="note">Box breath 4–4–4–4 while it runs. If you fall asleep, that counts as success, not failure.</div>
      `,
      classical: () => `
        <h2>Classical</h2>
        <p>Use your Classical app for long-form regulation. Generated beds are a scaffold; a real adagio or a Rast improvisation is closer to what Damascene musicians actually played.</p>
        <div class="row">
          <button class="primary" data-play='{"kind":"maqam","maqam":"rast","minutes":20,"title":"Rast classical bed"}'>Rast bed</button>
          <button class="secondary" data-play='{"kind":"maqam","maqam":"hijaz","minutes":20,"title":"Hijaz bed"}'>Hijaz bed</button>
        </div>
        <div class="links">
          <a href="https://www.youtube.com/results?search_query=slow+adagio+no+lyrics" target="_blank" rel="noreferrer">Adagio, no lyrics</a>
          <a href="https://www.youtube.com/results?search_query=ney+taksim+rast" target="_blank" rel="noreferrer">Ney Rast taksim</a>
        </div>
        <div class="note">Avoid minor-key despair playlists as a nightly TRD habit. Beauty is allowed; collapse is not the goal.</div>
      `,
    };
  }

  function openSheet(id) {
    const view = screens()[id];
    $("sheet-body").innerHTML = view();
    $("sheet").hidden = false;
    $("sheet-body").querySelectorAll("[data-play]").forEach((btn) => {
      btn.addEventListener("click", () => playSpec(JSON.parse(btn.dataset.play)));
    });
  }

  function renderHome() {
    $("app-grid").innerHTML = APPS.map((app) => `
      <button class="app-btn" data-app="${app.id}" type="button">
        <div class="icon" style="background:${app.bg}">${iconSvg(app.glyph)}</div>
        <span>${app.name}</span>
      </button>
    `).join("");

    $("day-strip").innerHTML = DAY.map((d) => `<button class="chip" data-day="${d.id}" type="button">${d.label}</button>`).join("");

    document.querySelectorAll("[data-app]").forEach((btn) => {
      btn.addEventListener("click", () => openSheet(btn.dataset.app));
    });
    document.querySelectorAll("[data-day]").forEach((btn) => {
      btn.addEventListener("click", () => {
        document.querySelectorAll("[data-day]").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
        const d = DAY.find((x) => x.id === btn.dataset.day);
        $("sheet-body").innerHTML = `
          <h2>${d.title}</h2>
          <p>${d.body}</p>
          <div class="row">
            <button class="primary" id="day-play">Start this block</button>
          </div>
          ${recipeBlock([d.apps])}
        `;
        $("sheet").hidden = false;
        $("day-play").addEventListener("click", () => playSpec(d.play));
      });
    });
  }

  $("stop-btn").addEventListener("click", stop);
  $("sheet-close").addEventListener("click", () => { $("sheet").hidden = true; });
  $("sheet").addEventListener("click", (e) => {
    if (e.target.id === "sheet") $("sheet").hidden = true;
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") $("sheet").hidden = true;
    if (e.key === " " && !$("player").hidden && e.target === document.body) {
      e.preventDefault();
      stop();
    }
  });

  renderHome();
})();
