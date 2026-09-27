/* Static SVG chart renderers. Real data only: every renderer draws exactly the
   values it is given and draws NOTHING when it is given none. There is no
   seeded, random or shape-generated fallback (v5 decision D3); an element
   whose data-opts carry no data is hidden.

   Usage: <div data-chart="series" data-opts='{...}'></div>, rendered on
   DOMContentLoaded.

   `series` and `bars` draw the files `gridflow-distil` writes
   (site/hifi/data/series/<vendor>/<dataset>.json), which the build inlines as
   {type, unit, x_kind, x, series:[{key, values}]}. Series colours come from the
   design tokens: a series keyed like a fuel (wind, gas, nuclear, imports,
   biomass, solar, other) uses --fuel-<key>; anything else uses --ink.
   Styling is minimal plumbing; the Phase 25b template restyles it. */

(function () {
  const PALETTE = {
    forest:    "#3b6b4b",
    forestDeep:"#2a4f37",
    forestSoft:"#a9c4b3",
    forestTint:"#dfeae3",
    sky:       "#7a96a8",
    rust:      "#c45a3a",
    sand:      "#c9a96e",
    plum:      "#86627d",
    slate:     "#5a5e5f",
    ink:       "#1a1714",
    inkSoft:   "#6b6358",
    rule:      "#d8d1c2",
    paper:     "#faf7f1",
  };

  // Fallbacks mirror tokens.css, for pages whose stylesheet does not load it.
  const TOKEN_FALLBACK = {
    "--ink": "#1C2B22",
    "--muted": "#5d6a55",
    "--horizon": "#3E8C97",
    "--clay-deep": "#7C5530",
    "--olive": "#66793B",
    "--bronze": "#A5713C",
    "--petrol": "#155A6E",
    "--fuel-wind": "#3E8C97",
    "--fuel-solar": "#AFC64E",
    "--fuel-gas": "#C77E3C",
    "--fuel-nuclear": "#155A6E",
    "--fuel-imports": "#66793B",
    "--fuel-biomass": "#A5713C",
    "--fuel-other": "#A39A6A",
  };
  const FUEL_KEYS = ["wind", "solar", "gas", "nuclear", "imports", "biomass", "other"];

  function token(name) {
    const v = getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    return v || TOKEN_FALLBACK[name] || PALETTE.ink;
  }

  function seriesColor(key, i) {
    if (FUEL_KEYS.indexOf(key) !== -1) return token("--fuel-" + key);
    const cycle = ["--ink", "--horizon", "--clay-deep", "--olive", "--bronze", "--petrol"];
    return token(cycle[i % cycle.length]);
  }

  function esc(s) {
    return String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  }

  function hasValues(arr) {
    return Array.isArray(arr) && arr.some((v) => typeof v === "number" && isFinite(v));
  }

  function fmt(v) {
    const a = Math.abs(v);
    if (a < 1e-9) return "0";
    if (a >= 1000) return Math.round(v).toLocaleString("en-GB");
    if (a >= 10) return v.toFixed(0);
    return v.toFixed(1);
  }

  function niceTicks(lo, hi) {
    if (lo === hi) { lo -= 1; hi += 1; }
    const raw = (hi - lo) / 4;
    const mag = Math.pow(10, Math.floor(Math.log10(raw)));
    const norm = raw / mag;
    const step = (norm < 1.5 ? 1 : norm < 3 ? 2 : norm < 7 ? 5 : 10) * mag;
    const ticks = [];
    for (let v = Math.ceil(lo / step) * step; v <= hi + step * 1e-9; v += step) ticks.push(v);
    return ticks;
  }

  function dayLabel(iso) {
    const d = new Date(iso);
    const m = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"][d.getUTCMonth()];
    return d.getUTCDate() + " " + m;
  }

  // ── series: distilled time series, one polyline per series ──
  // x is placed by real time, so gaps in silver stay visible as gaps.
  function series(el, opts = {}) {
    const groups = (opts.series || []).filter((s) => hasValues(s.values));
    const xs = (opts.x || []).map((t) => Date.parse(t));
    if (!groups.length || xs.length < 2 || xs.some(isNaN)) return false;
    const W = opts.width || 900, H = opts.height || 300;
    const padL = 64, padR = 96, padT = 12, padB = 30;
    const innerW = W - padL - padR, innerH = H - padT - padB;
    const all = [];
    groups.forEach((s) => s.values.forEach((v) => { if (typeof v === "number") all.push(v); }));
    let lo = Math.min(...all), hi = Math.max(...all);
    if (lo > 0 && lo / (hi || 1) < 0.5) lo = 0;
    const ticks = niceTicks(lo, hi);
    lo = Math.min(lo, ticks[0]); hi = Math.max(hi, ticks[ticks.length - 1]);
    const t0 = xs[0], t1 = xs[xs.length - 1];
    const x = (t) => padL + ((t - t0) / (t1 - t0)) * innerW;
    const y = (v) => padT + innerH - ((v - lo) / (hi - lo || 1)) * innerH;
    const ink = token("--ink"), muted = token("--muted");
    let svg = `<svg viewBox="0 0 ${W} ${H}" width="100%" font-size="12" style="font-variant-numeric:tabular-nums">`;
    svg += `<g fill="${muted}" text-anchor="end">`;
    ticks.forEach((v) => {
      svg += `<text x="${padL - 8}" y="${y(v) + 4}">${fmt(v)}</text>`;
    });
    svg += `</g>`;
    svg += `<text x="${padL - 8}" y="${padT - 2}" fill="${muted}" text-anchor="end" font-size="11">${esc(opts.unit || "")}</text>`;
    if (lo < 0 && hi > 0) svg += `<line x1="${padL}" x2="${W - padR}" y1="${y(0)}" y2="${y(0)}" stroke="${muted}" stroke-width="1" stroke-dasharray="2 4"/>`;
    svg += `<line x1="${padL}" x2="${padL}" y1="${padT}" y2="${padT + innerH}" stroke="${ink}" stroke-width="1.5"/>`;
    svg += `<line x1="${padL}" x2="${W - padR}" y1="${padT + innerH}" y2="${padT + innerH}" stroke="${ink}" stroke-width="1.5"/>`;
    svg += `<g fill="${muted}" text-anchor="middle">`;
    svg += `<text x="${x(t0)}" y="${H - 8}">${dayLabel(opts.x[0])}</text>`;
    svg += `<text x="${x(t1)}" y="${H - 8}">${dayLabel(opts.x[opts.x.length - 1])}</text>`;
    svg += `</g>`;
    const endLabels = [];
    groups.forEach((s, i) => {
      const color = seriesColor(s.key, i);
      let d = "", pen = false, lastPt = null;
      s.values.forEach((v, j) => {
        if (typeof v !== "number") { pen = false; return; }
        d += `${pen ? "L" : "M"}${x(xs[j]).toFixed(1)},${y(v).toFixed(1)}`;
        pen = true; lastPt = [x(xs[j]), y(v)];
      });
      svg += `<path d="${d}" fill="none" stroke="${color}" stroke-width="1.6" stroke-linejoin="round"/>`;
      if (lastPt) endLabels.push({ x: lastPt[0] + 6, y: lastPt[1] + 4, text: s.key });
    });
    // Direct labels at each line's end, nudged apart where lines converge.
    endLabels.sort((a, b) => a.y - b.y);
    for (let k = 1; k < endLabels.length; k++) {
      endLabels[k].y = Math.max(endLabels[k].y, endLabels[k - 1].y + 14);
    }
    endLabels.forEach((l) => {
      svg += `<text x="${l.x}" y="${l.y}" fill="${ink}" font-style="italic">${esc(l.text)}</text>`;
    });
    svg += `</svg>`;
    el.innerHTML = svg;
    return true;
  }

  // ── bars: distilled categorical values, horizontal bars ──
  function bars(el, opts = {}) {
    const s = (opts.series || [])[0];
    const labels = opts.x || [];
    if (!s || !hasValues(s.values) || !labels.length) return false;
    const W = opts.width || 900, rowH = 26, labelW = 150, valueW = 110;
    const barW = W - labelW - valueW;
    const vals = s.values.map((v) => (typeof v === "number" ? v : 0));
    const max = Math.max(...vals.map(Math.abs)) || 1;
    const H = labels.length * rowH + 8;
    const ink = token("--ink"), muted = token("--muted");
    let svg = `<svg viewBox="0 0 ${W} ${H}" width="100%" font-size="12" style="font-variant-numeric:tabular-nums">`;
    labels.forEach((label, i) => {
      const yy = i * rowH + 6;
      const w = (Math.abs(vals[i]) / max) * barW;
      svg += `<text x="${labelW - 10}" y="${yy + 13}" fill="${ink}" text-anchor="end">${esc(label)}</text>`;
      svg += `<rect x="${labelW}" y="${yy}" width="${w.toFixed(1)}" height="16" fill="${seriesColor(String(label).toLowerCase(), 0)}" stroke="${ink}" stroke-width="1"/>`;
      svg += `<text x="${labelW + w + 8}" y="${yy + 13}" fill="${muted}">${fmt(vals[i])} ${esc(opts.unit || "")}</text>`;
    });
    svg += `</svg>`;
    el.innerHTML = svg;
    return true;
  }

  // ── stacked area from explicit per-layer values ─────────────
  // Every layer must carry values; without them nothing is drawn.
  function stackedArea(el, opts = {}) {
    const layers = Array.isArray(opts.series) ? opts.series : [];
    if (!layers.length || !layers.every((s) => hasValues(s.values))) return false;
    const W = opts.width || 880;
    const H = opts.height || 320;
    const padL = 48, padR = 16, padT = 16, padB = 36;
    const innerW = W - padL - padR;
    const innerH = H - padT - padB;
    const N = Math.min(...layers.map((s) => s.values.length));
    if (N < 2) return false;
    const labels = layers.map((s) => s.name);
    const colors = layers.map((s, i) => s.color || [PALETTE.rust, PALETTE.forest, PALETTE.plum, PALETTE.sky, PALETTE.sand, "#d4a73a", "#5a8aa6", PALETTE.slate][i % 8]);
    const stacks = Array.from({ length: N }, (_, i) => {
      let acc = 0;
      const out = layers.map((s) => {
        const v = Math.max(0, s.values[i] || 0);
        const seg = [acc, acc + v];
        acc += v;
        return seg;
      });
      return { layers: out, total: acc };
    });
    const totalMax = Math.max(...stacks.map((s) => s.total));
    const yMax = Math.max(totalMax * 1.08, 1e-6);
    const niceStep = (() => {
      const raw = yMax / 4;
      const mag = Math.pow(10, Math.floor(Math.log10(raw)));
      const norm = raw / mag;
      const step = norm < 1.5 ? 1 : norm < 3 ? 2 : norm < 7 ? 5 : 10;
      return step * mag;
    })();
    const yTicks = [];
    for (let v = 0; v <= yMax; v += niceStep) yTicks.push(v);
    const xTickHours = [0, 6, 12, 18, 24];
    const yLabel = opts.yLabel || "";
    const x = (i) => padL + (i / (N - 1)) * innerW;
    const y = (v) => padT + innerH - (v / yMax) * innerH;
    const paths = labels.map((_, li) => {
      const top = stacks.map((s, i) => `${x(i)},${y(s.layers[li][1])}`);
      const bot = stacks.map((s, i) => `${x(i)},${y(s.layers[li][0])}`).reverse();
      return `M${top.join(" L")} L${bot.join(" L")} Z`;
    });
    let svg = `<svg viewBox="0 0 ${W} ${H}" width="100%" height="${H}" font-family="Inter, sans-serif" font-size="11">`;
    svg += `<g stroke="${PALETTE.rule}" stroke-width="1">`;
    yTicks.forEach((v) => {
      const yy = y(v);
      svg += `<line x1="${padL}" y1="${yy}" x2="${W - padR}" y2="${yy}" stroke-dasharray="${v === 0 ? "" : "2 4"}"/>`;
    });
    svg += `</g>`;
    svg += `<g fill="${PALETTE.inkSoft}" text-anchor="end">`;
    yTicks.forEach((v) => svg += `<text x="${padL - 8}" y="${y(v) + 3}">${niceStep < 1 ? v.toFixed(1) : Math.round(v)}${yLabel ? " " + yLabel : ""}</text>`);
    svg += `</g>`;
    svg += `<g fill="${PALETTE.inkSoft}" text-anchor="middle">`;
    xTickHours.forEach((h) => {
      const xx = padL + (h / 24) * innerW;
      svg += `<text x="${xx}" y="${H - padB + 18}">${String(h).padStart(2, "0")}:00</text>`;
    });
    svg += `</g>`;
    paths.forEach((p, i) => {
      svg += `<path d="${p}" fill="${colors[i]}" fill-opacity="0.85" stroke="${colors[i]}" stroke-width="0.5"/>`;
    });
    svg += `</svg>`;
    el.innerHTML = svg;
    if (opts.legend !== false) {
      const legendEl = document.createElement("div");
      legendEl.className = "chart-legend";
      legendEl.innerHTML = labels.map((l, i) => `<span><i style="background:${colors[i]}"></i>${esc(l)}</span>`).join("");
      el.appendChild(legendEl);
    }
    return true;
  }

  // ── single-line sparkline from explicit values ──────────────
  function sparkline(el, opts = {}) {
    if (!hasValues(opts.values)) return false;
    const W = opts.width || 200;
    const H = opts.height || 40;
    const data = opts.values.slice();
    const N = opts.n || data.length;
    if (N < 2) return false;
    const min = Math.min(...data), max = Math.max(...data);
    const x = (i) => (i / (N - 1)) * W;
    const y = (v) => H - 4 - ((v - min) / (max - min || 1)) * (H - 8);
    const pts = data.map((v, i) => `${x(i)},${y(v)}`).join(" ");
    const color = opts.color || PALETTE.forest;
    const fill = opts.fill || PALETTE.forestTint;
    const area = `M0,${H} L${pts.split(" ").join(" L")} L${W},${H} Z`;
    el.innerHTML = `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
      <path d="${area}" fill="${fill}" />
      <polyline points="${pts}" fill="none" stroke="${color}" stroke-width="1.5"/>
    </svg>`;
    return true;
  }

  // ── horizontal bars from explicit items ─────────────────────
  function barsH(el, opts = {}) {
    const items = (opts.items || []).filter((d) => typeof d.value === "number");
    if (!items.length) return false;
    const W = opts.width || 320;
    const rowH = 22;
    const labelW = 120;
    const barW = W - labelW - 60;
    const max = Math.max(...items.map((d) => d.value)) || 1;
    const H = items.length * rowH + 8;
    let svg = `<svg viewBox="0 0 ${W} ${H}" width="100%" height="${H}" font-family="Inter, sans-serif" font-size="11">`;
    items.forEach((d, i) => {
      const yy = i * rowH + 6;
      const w = (d.value / max) * barW;
      svg += `<text x="0" y="${yy + 12}" fill="${PALETTE.ink}">${d.label}</text>`;
      svg += `<rect x="${labelW}" y="${yy}" width="${w}" height="14" fill="${d.color || PALETTE.forest}" fill-opacity="0.85"/>`;
      svg += `<text x="${labelW + w + 6}" y="${yy + 12}" fill="${PALETTE.inkSoft}">${d.display || d.value}</text>`;
    });
    svg += `</svg>`;
    el.innerHTML = svg;
    return true;
  }

  // ── price ladder from explicit values ───────────────────────
  function priceLadder(el, opts = {}) {
    if (!hasValues(opts.values)) return false;
    const W = opts.width || 280, H = opts.height || 110;
    const data = opts.values.slice();
    const N = opts.n || data.length;
    if (N < 2) return false;
    const min = Math.min(...data), max = Math.max(...data);
    const x = (i) => 4 + (i / (N - 1)) * (W - 8);
    const y = (v) => 8 + (1 - (v - min) / (max - min || 1)) * (H - 16);
    const pts = data.map((v, i) => `${x(i)},${y(v)}`);
    let svg = `<svg viewBox="0 0 ${W} ${H}" width="100%" height="${H}">`;
    svg += `<polyline points="${pts.join(" ")}" fill="none" stroke="${PALETTE.ink}" stroke-width="1.4"/>`;
    svg += `<circle cx="${x(N - 1)}" cy="${y(data[N - 1])}" r="3" fill="${PALETTE.forest}"/>`;
    svg += `</svg>`;
    el.innerHTML = svg;
    return true;
  }

  // ── donut from explicit data ────────────────────────────────
  function donut(el, opts = {}) {
    const data = (opts.data || []).filter((d) => typeof d.value === "number" && d.value > 0);
    if (!data.length) return false;
    const total = data.reduce((s, d) => s + d.value, 0);
    const W = opts.width || 140, H = opts.height || 140;
    const cx = W / 2, cy = H / 2, r = Math.min(W, H) / 2 - 6, ir = r - 16;
    let svg = `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">`;
    let acc = -Math.PI / 2;
    data.forEach((d) => {
      const ang = (d.value / total) * Math.PI * 2;
      const a0 = acc, a1 = acc + ang;
      acc = a1;
      const large = ang > Math.PI ? 1 : 0;
      const x0 = cx + r * Math.cos(a0), y0 = cy + r * Math.sin(a0);
      const x1 = cx + r * Math.cos(a1), y1 = cy + r * Math.sin(a1);
      const xi0 = cx + ir * Math.cos(a0), yi0 = cy + ir * Math.sin(a0);
      const xi1 = cx + ir * Math.cos(a1), yi1 = cy + ir * Math.sin(a1);
      const path = `M${x0},${y0} A${r},${r} 0 ${large} 1 ${x1},${y1} L${xi1},${yi1} A${ir},${ir} 0 ${large} 0 ${xi0},${yi0} Z`;
      svg += `<path d="${path}" fill="${d.color}" />`;
    });
    if (opts.center) {
      svg += `<text x="${cx}" y="${cy - 2}" text-anchor="middle" font-family="Fraunces, serif" font-size="22" fill="${PALETTE.ink}">${opts.center}</text>`;
      if (opts.centerSub) svg += `<text x="${cx}" y="${cy + 14}" text-anchor="middle" font-family="Inter, sans-serif" font-size="10" fill="${PALETTE.inkSoft}" letter-spacing="0.05em">${opts.centerSub}</text>`;
    }
    svg += `</svg>`;
    el.innerHTML = svg;
    return true;
  }

  window.GFCharts = { series, bars, stackedArea, sparkline, barsH, priceLadder, donut, PALETTE };

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-chart]").forEach((el) => {
      const render = window.GFCharts[el.dataset.chart];
      const opts = {};
      try { if (el.dataset.opts) Object.assign(opts, JSON.parse(el.dataset.opts)); } catch (e) { /* malformed opts draw nothing */ }
      const drawn = render ? render(el, opts) === true : false;
      if (!drawn) {
        // No data, no chart: never a placeholder shape in its place.
        el.hidden = true;
        return;
      }
      // The drawing repeats what the surrounding caption states in words.
      el.setAttribute("aria-hidden", "true");
    });
  });
})();
