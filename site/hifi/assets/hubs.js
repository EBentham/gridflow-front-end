/* gridflow Data sources landing and vendor hubs: the buried cables (direction A, "Sections").
   The landing (main[data-cable="feeds"]) runs one cable from each drawn asset down through the topsoil
   to its vendor's terminal. A hub (main[data-cable="trunk"]) runs one cable from the drawing into a lane
   in the left margin and down through the strata, tapping each group of datasets, then silver and gold.
   Routes are measured from the rendered page, so they follow the text wherever it wraps. The cables are
   drawing only: the page reads the same without them, and below 1100px they are not drawn. */
(function () {
  "use strict";
  var NS = "http://www.w3.org/2000/svg";
  var main = document.getElementById("main");
  if (!main || !window.matchMedia) return;
  var mode = main.getAttribute("data-cable");
  var on = window.matchMedia("(min-width: 1100px)");
  var css = getComputedStyle(document.documentElement);
  function tok(name, fallback) { return (css.getPropertyValue(name) || "").trim() || fallback; }
  var INK = tok("--ink", "#1C2B22");
  var CORE = { bronze: tok("--bronze", "#A5713C"), silver: tok("--silver", "#9FADAB"), gold: tok("--gold", "#C2A14A") };
  var svg = document.createElementNS(NS, "svg");
  svg.setAttribute("class", "hub-cables");
  svg.setAttribute("aria-hidden", "true");
  svg.setAttribute("focusable", "false");
  main.insertBefore(svg, main.firstChild);

  function box(el) {
    var r = el.getBoundingClientRect();
    var m = main.getBoundingClientRect();
    return { l: r.left - m.left, t: r.top - m.top, r: r.right - m.left, b: r.bottom - m.top, w: r.width, h: r.height };
  }
  function centre(el) { var b = box(el); return [b.l + b.w / 2, b.t + b.h / 2]; }
  // a cable anchor drawn in the landscape (<circle data-a>, drawing coordinates) to page coordinates
  function anchor(key) {
    var land = main.querySelector(".landscape .land--wide");
    var a = land && land.querySelector('[data-a="' + key + '"]');
    if (!a || !land.getScreenCTM) return null;
    var p = land.createSVGPoint();
    p.x = parseFloat(a.getAttribute("cx"));
    p.y = parseFloat(a.getAttribute("cy"));
    p = p.matrixTransform(land.getScreenCTM());
    var m = main.getBoundingClientRect();
    return [p.x - m.left, p.y - m.top];
  }
  function smoothstep(t) { t = Math.max(0, Math.min(1, t)); return t * t * (3 - 2 * t); }
  function n(v) { return Math.round(v * 10) / 10; }
  function smooth(pts) {
    var d = "M" + n(pts[0][0]) + " " + n(pts[0][1]);
    for (var i = 0; i < pts.length - 1; i++) {
      var p0 = pts[i > 0 ? i - 1 : i], p1 = pts[i], p2 = pts[i + 1], p3 = pts[i + 2 < pts.length ? i + 2 : i + 1];
      d += " C" + n(p1[0] + (p2[0] - p0[0]) / 6) + " " + n(p1[1] + (p2[1] - p0[1]) / 6) + " " +
           n(p2[0] - (p3[0] - p1[0]) / 6) + " " + n(p2[1] - (p3[1] - p1[1]) / 6) + " " + n(p2[0]) + " " + n(p2[1]);
    }
    return d;
  }
  var out = [];
  function cable(d, core) {
    var tail = ' fill="none" stroke-linecap="round" stroke-linejoin="round"></path>';
    out.push('<path d="' + d + '" stroke="' + INK + '" stroke-width="4.4"' + tail);
    out.push('<path d="' + d + '" stroke="' + core + '" stroke-width="1.5"' + tail);
  }
  function joint(x, y) { out.push('<circle cx="' + n(x) + '" cy="' + n(y) + '" r="4.6" fill="' + INK + '"></circle>'); }
  function sleeve(x, y, fill) {
    out.push('<rect x="' + n(x - 7) + '" y="' + n(y - 17) + '" width="14" height="34" rx="7" fill="' + fill +
             '" stroke="' + INK + '" stroke-width="1.6"></rect>');
  }
  // an S-bend inside the topsoil band, from (x0, y0) straight down, across to x1, then straight down to y1
  function drop(x0, y0, x1, y1, ya, yb) {
    var pts = [[x0, y0], [x0, ya]];
    for (var k = 1; k < 12; k++) {
      var t = k / 12;
      pts.push([x0 + (x1 - x0) * smoothstep(t), ya + (yb - ya) * t]);
    }
    pts.push([x1, yb]);
    return smooth(pts) + " V" + n(y1);
  }

  function feeds() {
    var soil = main.querySelector(".hub-soil");
    if (!soil) return;
    var s = box(soil);
    var ends = main.querySelectorAll(".vend[data-vendor]");
    for (var i = 0; i < ends.length; i++) {
      var term = ends[i].querySelector(".term");
      var a = anchor(ends[i].getAttribute("data-vendor"));
      if (!term || !a) continue;
      var c = centre(term);
      cable(drop(a[0], a[1], c[0], c[1] - 7, s.t + 22, s.b - 30), CORE.bronze);
    }
  }

  function trunk() {
    var soil = main.querySelector(".hub-soil");
    var wrap = main.querySelector(".stratum--bronze .wrap");
    var taps = main.querySelectorAll("[data-tap]");
    if (!soil || !wrap || !taps.length) return;
    var s = box(soil);
    var lane = Math.max(14, box(wrap).l + parseFloat(getComputedStyle(wrap).paddingLeft) - 40);
    var a = anchor(main.getAttribute("data-vendor") || "elexon") || [lane, s.t - 2];
    var points = [];
    for (var i = 0; i < taps.length; i++) {
      var term = taps[i].classList.contains("term") ? taps[i] : taps[i].querySelector(".term");
      if (term) points.push({ at: centre(term), layer: taps[i].getAttribute("data-tap") });
    }
    if (!points.length) return;
    var last = points[points.length - 1].at;
    var contacts = [];
    ["silver", "gold"].forEach(function (layer) {
      var sec = main.querySelector(".stratum--" + layer);
      if (sec) contacts.push({ layer: layer, y: box(sec).t + 14 });
    });
    // the trunk, in lengths that change core colour where it crosses a contact
    var y0 = s.b - 26;
    cable(drop(a[0], a[1], lane, y0, s.t + 12, y0), CORE.bronze);
    var from = y0, core = CORE.bronze;
    for (var c = 0; c < contacts.length; c++) {
      if (contacts[c].y >= last[1]) break;
      cable("M" + n(lane) + " " + n(from) + " V" + n(contacts[c].y), core);
      from = contacts[c].y;
      core = CORE[contacts[c].layer];
    }
    cable("M" + n(lane) + " " + n(from) + " V" + n(last[1] - 14) + " Q" + n(lane) + " " + n(last[1]) + " " +
          n(lane + 14) + " " + n(last[1]) + " H" + n(last[0] - 7), core);
    for (var p = 0; p < points.length - 1; p++) {
      var at = points[p].at;
      cable("M" + n(lane) + " " + n(at[1]) + " H" + n(at[0] - 7), CORE[points[p].layer] || CORE.bronze);
      joint(lane, at[1]);
    }
    for (var q = 0; q < contacts.length; q++) {
      if (contacts[q].y < last[1]) sleeve(lane, contacts[q].y, CORE[contacts[q].layer]);
    }
  }

  function draw() {
    out = [];
    if (on.matches) {
      if (mode === "feeds") feeds();
      else if (mode === "trunk") trunk();
    }
    svg.setAttribute("width", main.scrollWidth);
    svg.setAttribute("height", main.scrollHeight);
    svg.innerHTML = out.join("");
  }
  var queued = false;
  function later() {
    if (queued) return;
    queued = true;
    window.requestAnimationFrame(function () { queued = false; draw(); });
  }
  window.addEventListener("resize", later);
  if (window.ResizeObserver) new ResizeObserver(later).observe(main);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(later);
  draw();
})();
