/* PLC LOGO!/ZEN course: progressive enhancement. No dependencies, no network, no globals.
   Every component initialises independently and only if its markup is present. */
(function () {
  'use strict';

  var PREFIX = 'plc-course:';
  var TICK_MS = 100;
  var WINDOW_S = 15;
  var SVG_W_MIN = 280;
  var LAMP_COLOURS = ['green', 'amber', 'red', 'neutral'];

  /* ---------------------------------------------------------------- helpers */

  function qs(sel, root) { return (root || document).querySelector(sel); }
  function qsa(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }

  function make(tag, cls, text) {
    var node = document.createElement(tag);
    if (cls) node.className = cls;
    if (text != null) node.textContent = text;
    return node;
  }

  function escapeXml(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c];
    });
  }

  var storage = (function () {
    try {
      var probe = PREFIX + '__probe';
      window.localStorage.setItem(probe, '1');
      window.localStorage.removeItem(probe);
      return window.localStorage;
    } catch (e) {
      return null;
    }
  })();

  function readStore(key) {
    if (!storage || !key) return null;
    try { return storage.getItem(PREFIX + key); } catch (e) { return null; }
  }
  function writeStore(key, value) {
    if (!storage || !key) return;
    try {
      if (value == null || value === '') storage.removeItem(PREFIX + key);
      else storage.setItem(PREFIX + key, value);
    } catch (e) { /* quota or privacy mode: progress simply is not remembered */ }
  }
  function readJson(key, fallback) {
    var raw = readStore(key);
    if (raw == null) return fallback;
    try { return JSON.parse(raw); } catch (e) { return fallback; }
  }

  /** Lower-case, strip Vietnamese diacritics (NFD) and map đ to d. */
  function fold(text) {
    return String(text == null ? '' : text)
      .normalize('NFD')
      .replace(/[̀-ͯ]/g, '')
      .replace(/đ/g, 'd').replace(/Đ/g, 'd')
      .toLowerCase();
  }

  function isoDate(d) {
    var m = d.getMonth() + 1;
    var day = d.getDate();
    return d.getFullYear() + '-' + (m < 10 ? '0' : '') + m + '-' + (day < 10 ? '0' : '') + day;
  }

  /* ---------------------------------------------------------------- multiple choice */

  function initQuizzes() {
    var all = qsa('.c-mcq');
    if (!all.length) return;
    var groups = [];

    function groupFor(el) {
      var host = el.closest('.c-quiz');
      if (!host) return null;
      for (var i = 0; i < groups.length; i++) if (groups[i].el === host) return groups[i];
      var g = {
        el: host,
        key: host.getAttribute('data-key') || '',
        score: qs('.c-quiz-score', host),
        results: {},
        questions: []
      };
      var saved = readJson(g.key, null);
      if (saved && typeof saved === 'object') g.results = saved;
      groups.push(g);
      return g;
    }

    function updateScore(g) {
      if (!g.score) return;
      var right = 0;
      g.questions.forEach(function (q) { if (g.results[q.id] === true) right++; });
      g.score.textContent = 'Đúng ngay lần đầu: ' + right + '/' + g.questions.length;
    }

    function setSolved(q) {
      q.solved = true;
      q.options.forEach(function (btn) {
        if (btn !== q.correctBtn) btn.disabled = true;
      });
    }

    function revealCorrect(q) {
      var li = q.correctBtn && q.correctBtn.closest('li');
      if (!li) return;
      li.classList.add('is-correct');
      q.correctBtn.setAttribute('aria-pressed', 'true');
      var fb = qs('.c-mcq-feedback', li);
      if (fb) fb.hidden = false;
      setSolved(q);
    }

    function resetQuestion(q) {
      q.solved = false;
      q.options.forEach(function (btn) {
        var li = btn.closest('li');
        btn.disabled = false;
        btn.removeAttribute('aria-disabled');
        btn.setAttribute('aria-pressed', 'false');
        if (li) {
          li.classList.remove('is-correct', 'is-wrong');
          var fb = qs('.c-mcq-feedback', li);
          if (fb) fb.hidden = true;
        }
      });
    }

    function choose(q, btn) {
      if (q.solved || btn.getAttribute('aria-disabled') === 'true') return;
      var li = btn.closest('li');
      var correct = btn.getAttribute('data-index') === q.answer;
      var g = q.group;

      if (g && g.results[q.id] === undefined) {
        g.results[q.id] = correct;
        writeStore(g.key, JSON.stringify(g.results));
        updateScore(g);
      }

      btn.setAttribute('aria-pressed', 'true');
      if (li) {
        li.classList.add(correct ? 'is-correct' : 'is-wrong');
        var fb = qs('.c-mcq-feedback', li);
        if (fb) fb.hidden = false;
      }
      if (correct) setSolved(q);
      else btn.setAttribute('aria-disabled', 'true');
    }

    all.forEach(function (el, n) {
      var g = groupFor(el);
      var q = {
        el: el,
        id: el.id || ('q' + n),
        answer: String(el.getAttribute('data-answer')),
        options: qsa('.c-mcq-option', el),
        group: g,
        solved: false,
        correctBtn: null
      };
      q.options.forEach(function (btn, i) {
        if (!btn.hasAttribute('data-index')) btn.setAttribute('data-index', String(i));
        btn.setAttribute('aria-pressed', 'false');
        if (btn.getAttribute('data-index') === q.answer) q.correctBtn = btn;
        var fb = qs('.c-mcq-feedback', btn.closest('li') || el);
        if (fb) {
          if (!fb.id) fb.id = q.id + '-fb-' + i;
          fb.setAttribute('aria-live', 'polite');
          btn.setAttribute('aria-describedby', fb.id);
        }
        btn.addEventListener('click', function () { choose(q, btn); });
      });
      if (g) {
        g.questions.push(q);
        if (g.results[q.id] !== undefined) revealCorrect(q);
      }
    });

    groups.forEach(function (g) {
      updateScore(g);
      var reset = qs('.c-quiz-reset', g.el);
      if (!reset) return;
      reset.addEventListener('click', function () {
        g.results = {};
        writeStore(g.key, null);
        g.questions.forEach(resetQuestion);
        updateScore(g);
      });
    });
  }

  /* ---------------------------------------------------------------- worked examples */

  function initWorkedExamples() {
    qsa('textarea.c-we-input[data-key]').forEach(function (ta) {
      var key = ta.getAttribute('data-key');
      var saved = readStore(key);
      if (saved != null) ta.value = saved;
      ta.addEventListener('input', function () { writeStore(key, ta.value); });
    });
  }

  /* ---------------------------------------------------------------- checklists */

  function initChecklists() {
    qsa('.c-checklist').forEach(function (box) {
      var key = box.getAttribute('data-key') || '';
      var boxes = qsa('input[type="checkbox"]', box);
      var out = qs('.c-checklist-progress', box);
      var saved = readJson(key, []);
      if (!Array.isArray(saved)) saved = [];

      function refresh() {
        var done = boxes.filter(function (b) { return b.checked; }).length;
        if (out) out.textContent = done + '/' + boxes.length + ' tiêu chí';
        box.style.setProperty('--p', boxes.length ? String(Math.round(done * 100 / boxes.length)) : '0');
      }

      boxes.forEach(function (b, i) {
        if (saved.indexOf(i) !== -1) b.checked = true;
        b.addEventListener('change', function () {
          var picked = [];
          boxes.forEach(function (x, j) { if (x.checked) picked.push(j); });
          writeStore(key, picked.length ? JSON.stringify(picked) : null);
          refresh();
        });
      });
      if (out && !out.hasAttribute('aria-live')) out.setAttribute('aria-live', 'polite');
      refresh();
    });
  }

  /* ---------------------------------------------------------------- logic simulator */

  function lampFor(out) {
    var declared = String(out.lamp || out.color || out.colour || '').toLowerCase();
    if (LAMP_COLOURS.indexOf(declared) !== -1) return declared;
    var text = fold((out.label || '') + ' ' + (out.id || ''));
    if (/\b(xanh|green|chay|run)\b/.test(text)) return 'green';
    if (/\b(vang|amber|yellow|canh bao|warning)\b/.test(text)) return 'amber';
    if (/\b(do|red|loi|fault|bao dong|alarm|dung khan|stop)\b/.test(text)) return 'red';
    return 'neutral';
  }

  function fmtSeconds(ticks) { return (ticks / 10).toFixed(1); }

  function initSim(root) {
    var specNode = qs('script.c-sim-spec', root);
    if (!specNode) return;
    var spec;
    try {
      spec = JSON.parse(specNode.textContent);
    } catch (e) {
      root.appendChild(make('p', 'c-sim-error', 'Không đọc được cấu hình mô phỏng.'));
      root.setAttribute('data-ready', '1');
      return;
    }

    /* ---- model */
    var vals = Object.create(null);
    var inputs = (spec.inputs || []).map(function (d) {
      vals[d.id] = 0;
      return { def: d, id: d.id, momentary: d.mode !== 'toggle', pressed: false, latch: false, btn: null, valEl: null };
    });
    var blocks = (spec.blocks || []).map(function (d) {
      vals[d.id] = 0;
      return { def: d, id: d.id, type: String(d.type || '').toUpperCase(), q: 0, prev: 0, n: 0, left: 0, shown: 0, row: null };
    });
    var outputs = (spec.outputs || []).map(function (d) {
      vals[d.id] = 0;
      return { def: d, id: d.id, lamp: lampFor(d), lampEl: null, stateEl: null };
    });
    var chartRefs = Array.isArray(spec.chart) ? spec.chart.filter(function (r) { return r in vals; }) : [];

    var ticks = 0;
    var history = [];
    var timer = null;
    var onScreen = true;
    var lastStatus = '';

    function get(ref) {
      if (ref === 'hi') return 1;
      return vals[ref] ? 1 : 0;
    }
    function timerTicks(d) { return Math.max(0, Math.round((Number(d.T) || 0) * 10)); }

    function evalBlock(b) {
      var d = b.def;
      var ins = (d.in || []).map(get);
      var x = ins.length ? ins[0] : 0;
      var count = ins.reduce(function (a, v) { return a + v; }, 0);
      var tt;
      switch (b.type) {
        case 'AND': b.q = ins.length && count === ins.length ? 1 : 0; break;
        case 'OR': b.q = count > 0 ? 1 : 0; break;
        case 'NAND': b.q = ins.length && count === ins.length ? 0 : 1; break;
        case 'NOR': b.q = count > 0 ? 0 : 1; break;
        case 'XOR': b.q = count % 2; break;
        case 'NOT': b.q = x ? 0 : 1; break;
        case 'RS':
          if (get(d.R)) b.q = 0;
          else if (get(d.S)) b.q = 1;
          break;
        case 'ONDELAY':
          tt = timerTicks(d);
          if (x) { b.n = Math.min(b.n + 1, tt); b.q = b.n >= tt ? 1 : 0; }
          else { b.n = 0; b.q = 0; }
          break;
        case 'OFFDELAY':
          tt = timerTicks(d);
          if (x) { b.left = 0; b.q = 1; b.shown = 0; }
          else {
            if (b.prev) b.left = tt;
            b.shown = b.left;
            b.q = b.left > 0 ? 1 : 0;
            if (b.left > 0) b.left--;
          }
          break;
        case 'PULSE':
          if (x && !b.prev) b.q = b.q ? 0 : 1;
          break;
        default: b.q = 0;
      }
      b.prev = x;
      return b.q;
    }

    function step() {
      inputs.forEach(function (i) {
        vals[i.id] = (i.pressed || i.latch) ? 1 : 0;
        i.latch = false;
      });
      blocks.forEach(function (b) { vals[b.id] = evalBlock(b); });
      outputs.forEach(function (o) { vals[o.id] = get(o.def.from); });
      ticks++;
      sample();
      render();
    }

    function sample() {
      history.push({ k: ticks, v: chartRefs.map(get) });
      if (history.length > WINDOW_S * 10 + 30) history.shift();
    }

    /* ---- DOM */
    var grid = make('div', 'c-sim-grid');

    var inSec = make('section', 'c-sim-inputs');
    inSec.setAttribute('aria-label', 'Ngõ vào');
    var inLabel = make('p', 'c-sim-label', 'Ngõ vào');
    inLabel.setAttribute('aria-hidden', 'true');
    var inList = make('div', 'c-sim-input-list');
    inSec.appendChild(inLabel);
    inSec.appendChild(inList);

    var blkSec = make('section', 'c-sim-blocks');
    blkSec.setAttribute('aria-label', 'Khối logic');
    var blkLabel = make('p', 'c-sim-label', 'Khối logic');
    blkLabel.setAttribute('aria-hidden', 'true');
    var blkList = make('ul', 'c-sim-block-list');
    blkSec.appendChild(blkLabel);
    blkSec.appendChild(blkList);

    var outSec = make('section', 'c-sim-outputs');
    outSec.setAttribute('aria-label', 'Ngõ ra');
    var outLabel = make('p', 'c-sim-label', 'Ngõ ra');
    outLabel.setAttribute('aria-hidden', 'true');
    var outList = make('div', 'c-sim-out-list');
    outSec.appendChild(outLabel);
    outSec.appendChild(outList);

    var status = make('p', 'c-sim-status');
    status.setAttribute('aria-live', 'polite');
    status.setAttribute('role', 'status');

    var actions = make('div', 'c-sim-actions');
    var resetBtn = make('button', 'c-sim-reset', 'Đặt lại');
    resetBtn.type = 'button';
    var clock = make('span', 'c-sim-clock', 't = 0.0 s');
    actions.appendChild(resetBtn);
    actions.appendChild(clock);

    var chartHost = null;
    var chartCap = null;
    if (chartRefs.length) {
      chartHost = make('div', 'c-sim-chart');
      chartCap = make('p', 'c-sim-chart-cap', 'Biểu đồ thời gian · ' + WINDOW_S + ' giây gần nhất');
    }

    inputs.forEach(function (i) {
      var btn = make('button', 'c-sim-input');
      btn.type = 'button';
      btn.setAttribute('aria-pressed', 'false');
      btn.setAttribute('data-input', i.id);
      btn.setAttribute('data-mode', i.momentary ? 'momentary' : 'toggle');
      btn.appendChild(make('span', 'c-sim-in-label', i.def.label || i.id));
      btn.appendChild(make('span', 'c-sim-in-mode', i.momentary ? 'Nhấn giữ' : 'Bật / tắt'));
      i.valEl = make('span', 'c-sim-in-val', '0');
      i.valEl.setAttribute('aria-hidden', 'true');
      btn.appendChild(i.valEl);
      i.btn = btn;
      inList.appendChild(btn);
      bindInput(i);
    });

    blocks.forEach(function (b) {
      var d = b.def;
      var refs;
      if (b.type === 'RS') refs = 'S=' + d.S + ', R=' + d.R;
      else refs = (d.in || []).join(', ');
      var li = make('li', 'c-sim-block');
      li.setAttribute('data-block', b.id);
      li.appendChild(make('span', 'c-sim-b-id', b.id));
      var desc = make('span', 'c-sim-b-desc');
      var typeText = b.type + ((b.type === 'ONDELAY' || b.type === 'OFFDELAY') ? ' T=' + (Number(d.T) || 0) + ' s' : '');
      desc.appendChild(make('span', 'c-sim-b-type', typeText));
      desc.appendChild(document.createTextNode(refs ? ' ← ' + refs : ''));
      b.noteEl = make('span', 'c-sim-b-note');
      b.noteEl.hidden = true;
      desc.appendChild(b.noteEl);
      li.appendChild(desc);
      b.valEl = make('span', 'c-sim-b-val', '0');
      b.valEl.setAttribute('data-v', '0');
      li.appendChild(b.valEl);
      b.row = li;
      blkList.appendChild(li);
    });

    outputs.forEach(function (o) {
      var row = make('div', 'c-sim-out');
      o.lampEl = make('span', 'c-lamp');
      o.lampEl.setAttribute('data-lamp', o.lamp);
      o.lampEl.setAttribute('aria-hidden', 'true');
      row.appendChild(o.lampEl);
      row.appendChild(make('span', 'c-sim-out-label', o.def.label || o.id));
      o.stateEl = make('span', 'c-sim-out-state', 'TẮT');
      row.appendChild(o.stateEl);
      outList.appendChild(row);
    });

    grid.appendChild(inSec);
    if (blocks.length) grid.appendChild(blkSec);
    grid.appendChild(outSec);
    root.appendChild(grid);
    root.appendChild(status);
    root.appendChild(actions);
    if (chartHost) { root.appendChild(chartHost); root.appendChild(chartCap); }
    root.setAttribute('data-ready', '1');

    /* ---- input handling */
    function setPressed(i, on) {
      if (i.pressed === on) return;
      i.pressed = on;
      if (on) i.latch = true;
      i.btn.setAttribute('aria-pressed', on ? 'true' : 'false');
      i.valEl.textContent = on ? '1' : '0';
    }

    function bindInput(i) {
      var btn = i.btn;
      if (!i.momentary) {
        btn.addEventListener('click', function () { setPressed(i, !i.pressed); });
        return;
      }
      btn.addEventListener('pointerdown', function (e) {
        if (e.button > 0) return;
        e.preventDefault();
        try { btn.setPointerCapture(e.pointerId); } catch (err) { /* synthetic pointer */ }
        btn.focus({ preventScroll: true });
        setPressed(i, true);
      });
      ['pointerup', 'pointercancel', 'lostpointercapture'].forEach(function (name) {
        btn.addEventListener(name, function () { setPressed(i, false); });
      });
      btn.addEventListener('contextmenu', function (e) { e.preventDefault(); });
      btn.addEventListener('click', function (e) { e.preventDefault(); });
      btn.addEventListener('keydown', function (e) {
        if (e.key !== ' ' && e.key !== 'Enter' && e.key !== 'Spacebar') return;
        e.preventDefault();
        if (!e.repeat) setPressed(i, true);
      });
      btn.addEventListener('keyup', function (e) {
        if (e.key !== ' ' && e.key !== 'Enter' && e.key !== 'Spacebar') return;
        e.preventDefault();
        setPressed(i, false);
      });
      btn.addEventListener('blur', function () { setPressed(i, false); });
    }

    /* ---- render */
    function blockNote(b) {
      var d = b.def;
      var tt = timerTicks(d);
      if (b.type === 'ONDELAY') {
        if (b.q) return 'đã đạt ' + fmtSeconds(tt) + ' s';
        if (b.n > 0) return fmtSeconds(b.n) + ' / ' + fmtSeconds(tt) + ' s';
        return '';
      }
      if (b.type === 'OFFDELAY') {
        if (!get((d.in || [])[0]) && b.q) return 'còn ' + fmtSeconds(b.shown) + ' s';
        return '';
      }
      return '';
    }

    function render() {
      blocks.forEach(function (b) {
        b.valEl.textContent = String(b.q);
        b.valEl.setAttribute('data-v', String(b.q));
        if (b.noteEl) {
          var note = blockNote(b);
          b.noteEl.textContent = note;
          b.noteEl.hidden = !note;
        }
      });
      var parts = [];
      outputs.forEach(function (o) {
        var on = !!vals[o.id];
        o.lampEl.classList.toggle('is-on', on);
        o.stateEl.textContent = on ? 'BẬT' : 'TẮT';
        parts.push((o.def.label || o.id) + ': ' + (on ? 'bật' : 'tắt'));
      });
      var text = parts.join(' · ');
      if (text !== lastStatus) { status.textContent = text; lastStatus = text; }
      clock.textContent = 't = ' + fmtSeconds(ticks) + ' s';
      drawChart();
    }

    function drawChart() {
      if (!chartHost) return;
      var w = Math.max(SVG_W_MIN, Math.floor(chartHost.clientWidth) || 640);
      var rowH = 26;
      var padTop = 6;
      var axisH = 24;
      var longest = chartRefs.reduce(function (m, r) { return Math.max(m, String(r).length); }, 2);
      var gutter = Math.min(120, Math.max(40, longest * 7.5 + 14));
      var plotL = gutter;
      var plotR = w - 22;
      var h = padTop + rowH * chartRefs.length + axisH;
      var nowS = ticks / 10;
      var t1 = Math.max(WINDOW_S, nowS);
      var t0 = t1 - WINDOW_S;
      function x(sec) { return plotL + (Math.max(t0, sec) - t0) / WINDOW_S * (plotR - plotL); }

      var start = 0;
      for (var s = 0; s < history.length; s++) { if (history[s].k / 10 <= t0) start = s; else break; }
      var parts = [];
      parts.push('<svg xmlns="http://www.w3.org/2000/svg" width="' + w + '" height="' + h + '" viewBox="0 0 ' + w + ' ' + h +
        '" role="img" aria-label="Biểu đồ thời gian ' + WINDOW_S + ' giây gần nhất: ' + escapeXml(chartRefs.join(', ')) + '">');

      chartRefs.forEach(function (ref, r) {
        var top = padTop + r * rowH;
        if (r % 2 === 0) parts.push('<rect class="c-sim-row-bg" x="0" y="' + top + '" width="' + w + '" height="' + rowH + '"/>');
      });
      var bottom = padTop + rowH * chartRefs.length;
      for (var sec = Math.ceil(t0); sec <= Math.floor(t1); sec++) {
        if (sec % 5 !== 0) continue;
        var gx = x(sec).toFixed(1);
        parts.push('<line class="c-sim-grid-line" x1="' + gx + '" x2="' + gx + '" y1="' + padTop + '" y2="' + bottom + '"/>');
      }

      chartRefs.forEach(function (ref, r) {
        var top = padTop + r * rowH;
        var yHi = top + 5;
        var yLo = top + rowH - 5;
        var kind = 'input';
        var lamp = '';
        blocks.forEach(function (b) { if (b.id === ref) kind = 'block'; });
        outputs.forEach(function (o) { if (o.id === ref) { kind = 'output'; lamp = o.lamp; } });
        parts.push('<text x="' + (gutter - 8) + '" y="' + (top + rowH / 2 + 4) + '" text-anchor="end">' + escapeXml(ref) + '</text>');
        var d = '';
        for (var s2 = start; s2 < history.length; s2++) {
          var xs = x(history[s2].k / 10).toFixed(1);
          var ys = history[s2].v[r] ? yHi : yLo;
          d += s2 === start ? 'M' + xs + ' ' + ys : 'H' + xs + 'V' + ys;
        }
        if (d) d += 'H' + plotR;
        parts.push('<path class="c-sim-trace" data-kind="' + kind + '"' + (lamp ? ' data-lamp="' + lamp + '"' : '') +
          ' d="' + d + '"/>');
      });

      parts.push('<line class="c-sim-axis" x1="' + plotL + '" x2="' + plotR + '" y1="' + bottom + '" y2="' + bottom + '"/>');
      for (var tk = Math.ceil(t0); tk <= Math.floor(t1); tk++) {
        var tx = x(tk).toFixed(1);
        var major = tk % 5 === 0;
        parts.push('<line class="c-sim-axis" x1="' + tx + '" x2="' + tx + '" y1="' + bottom + '" y2="' + (bottom + (major ? 6 : 3)) + '"/>');
        if (major) parts.push('<text x="' + tx + '" y="' + (bottom + 19) + '" text-anchor="middle">' + tk + ' s</text>');
      }
      parts.push('</svg>');
      chartHost.innerHTML = parts.join('');
    }

    /* ---- clock control */
    function reset() {
      inputs.forEach(function (i) { setPressed(i, false); i.latch = false; vals[i.id] = 0; });
      blocks.forEach(function (b) { b.q = 0; b.prev = 0; b.n = 0; b.left = 0; b.shown = 0; vals[b.id] = 0; });
      outputs.forEach(function (o) { vals[o.id] = 0; });
      ticks = 0;
      history = [];
      lastStatus = '';
      sample();
      render();
    }

    function shouldRun() { return onScreen && !document.hidden; }
    function syncTimer() {
      if (shouldRun() && timer == null) timer = window.setInterval(step, TICK_MS);
      else if (!shouldRun() && timer != null) { window.clearInterval(timer); timer = null; }
    }

    resetBtn.addEventListener('click', reset);
    document.addEventListener('visibilitychange', syncTimer);
    if ('IntersectionObserver' in window) {
      onScreen = false;
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { onScreen = e.isIntersecting; });
        syncTimer();
      }).observe(root);
    }
    if ('ResizeObserver' in window && chartHost) {
      var lastW = 0;
      new ResizeObserver(function () {
        var cw = chartHost.clientWidth;
        if (cw !== lastW) { lastW = cw; drawChart(); }
      }).observe(chartHost);
    }

    sample();
    render();
    syncTimer();
  }

  function initSims() {
    qsa('.c-sim').forEach(function (root) { safely(function () { initSim(root); }); });
  }

  /* ---------------------------------------------------------------- schedule */

  function initSchedule() {
    var now = new Date();
    var today = isoDate(now);
    var dateText = now.toLocaleDateString('vi-VN', { day: '2-digit', month: '2-digit', year: 'numeric' });
    var week = '';

    qsa('table.c-sched').forEach(function (table) {
      qsa('tbody tr[data-start][data-end]', table).forEach(function (tr) {
        var start = tr.getAttribute('data-start');
        var end = tr.getAttribute('data-end');
        tr.classList.remove('is-current', 'is-past');
        tr.removeAttribute('aria-current');
        if (end < today) tr.classList.add('is-past');
        else if (start <= today) {
          tr.classList.add('is-current');
          tr.setAttribute('aria-current', 'date');
          if (!week) {
            var cell = tr.cells && tr.cells[0];
            week = cell ? cell.textContent.replace(/\s+/g, ' ').trim() : '';
          }
        }
      });
    });

    qsa('[data-today]').forEach(function (el) {
      var mode = el.getAttribute('data-today');
      if (mode === 'week') { if (week) el.textContent = week; }
      else if (mode === 'date') el.textContent = dateText;
      else el.textContent = week ? dateText + ' · ' + week : dateText;
    });
  }

  /* ---------------------------------------------------------------- glossary */

  function initGlossary() {
    var controls = qsa('input.c-search[data-target], select.c-filter[data-target]');
    if (!controls.length) return;
    var targets = [];
    controls.forEach(function (c) {
      var sel = c.getAttribute('data-target');
      if (targets.indexOf(sel) === -1) targets.push(sel);
    });

    targets.forEach(function (sel) {
      var host;
      try { host = qs(sel); } catch (e) { host = null; }
      if (!host) return;
      var mine = controls.filter(function (c) { return c.getAttribute('data-target') === sel; });
      var searchBox = mine.filter(function (c) { return c.tagName === 'INPUT'; })[0] || null;
      var filterBox = mine.filter(function (c) { return c.tagName === 'SELECT'; })[0] || null;
      var terms = qsa('.c-term', host).map(function (t) {
        var platform = String(t.getAttribute('data-platform') || '').toLowerCase().split(/[\s,]+/).filter(Boolean);
        return { el: t, hay: fold(t.getAttribute('data-search') || t.textContent), platform: platform };
      });

      var counter = qs('.c-search-count[data-target="' + sel + '"]');
      if (!counter) {
        var scope = (searchBox || filterBox).parentElement;
        while (scope && !counter) {
          counter = qs('.c-search-count', scope);
          scope = scope.parentElement;
        }
      }
      if (counter && !counter.hasAttribute('aria-live')) counter.setAttribute('aria-live', 'polite');

      function apply() {
        var words = fold(searchBox ? searchBox.value : '').split(/\s+/).filter(Boolean);
        var plat = filterBox ? filterBox.value.toLowerCase() : '';
        var shown = 0;
        terms.forEach(function (t) {
          var ok = words.every(function (w) { return t.hay.indexOf(w) !== -1; }) &&
            (!plat || t.platform.indexOf(plat) !== -1);
          t.el.hidden = !ok;
          if (ok) shown++;
        });
        if (counter) counter.textContent = shown + ' thuật ngữ';
      }

      mine.forEach(function (c) {
        c.addEventListener('input', apply);
        c.addEventListener('change', apply);
      });
      apply();
    });
  }

  /* ---------------------------------------------------------------- timeline, print, toc */

  function initTimelines() {
    qsa('.c-timeline').forEach(function (tl) {
      var seen = [];
      qsa('.c-tl-seg', tl).forEach(function (seg) {
        var kind = seg.getAttribute('data-kind') || '';
        var idx = seen.indexOf(kind);
        if (idx === -1) { seen.push(kind); idx = seen.length - 1; }
        seg.setAttribute('data-tint', String(idx % 4));
      });
    });
  }

  function initPrint() {
    qsa('[data-print]').forEach(function (b) {
      b.addEventListener('click', function () { window.print(); });
    });
  }

  function initTocSpy() {
    var links = qsa('.c-toc a[href^="#"]');
    if (!links.length) return;
    var pairs = [];
    links.forEach(function (a) {
      var id = decodeURIComponent(a.getAttribute('href').slice(1));
      var target = id ? document.getElementById(id) : null;
      if (target) pairs.push({ link: a, target: target });
    });
    if (!pairs.length) return;
    var queued = false;

    function update() {
      queued = false;
      var current = null;
      pairs.forEach(function (p) { if (p.target.getBoundingClientRect().top <= 120) current = p; });
      pairs.forEach(function (p) {
        if (p === current) p.link.setAttribute('aria-current', 'location');
        else p.link.removeAttribute('aria-current');
      });
    }
    window.addEventListener('scroll', function () {
      if (!queued) { queued = true; window.requestAnimationFrame(update); }
    }, { passive: true });
    update();
  }

  /* ---------------------------------------------------------------- boot */

  function safely(fn) {
    try { fn(); } catch (e) { /* one broken widget must never take the page down */ }
  }

  function boot() {
    [initQuizzes, initWorkedExamples, initChecklists, initSims, initSchedule,
      initGlossary, initTimelines, initPrint, initTocSpy].forEach(safely);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
