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
  if (!main || !window.matchMedia || !window.gridflowDraw) return;
  var mode = main.getAttribute("data-cable");
  var on = window.matchMedia("(min-width: 1100px)");
  var kit = window.gridflowDraw;
  var tok = kit.tok, smoothstep = kit.smoothstep, n = kit.n, smooth = kit.smooth;
  var INK = tok("--ink", "#1C2B22");
  var CORE = { bronze: tok("--bronze", "#A5713C"), silver: tok("--silver", "#9FADAB"), gold: tok("--gold", "#C2A14A") };
  var svg = document.createElementNS(NS, "svg");
  svg.setAttribute("class", "hub-cables");
  svg.setAttribute("aria-hidden", "true");
  svg.setAttribute("focusable", "false");
  main.insertBefore(svg, main.firstChild);

  function box(el) { return kit.box(el, main); }
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

/* The catalogue plot plan (templates/_partials/plan.html.j2): one plot open at a time. Without this
   script every group's list shows under its band and every plot reads as expanded. With it, all close;
   a plot opens its list in the track under its band, with a leader from the plot down to the list's
   rule, and the package under the pointer or focus lights its square in the plot. Escape or Close
   shuts the list and returns focus to its plot. ?open=<group-slug> opens one group on load. */
(function () {
  "use strict";
  var plan = document.querySelector(".plan");
  if (!plan) return;
  var plots = Array.prototype.slice.call(plan.querySelectorAll(".plot"));
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var current = null;

  function panelOf(plot) { return document.getElementById(plot.getAttribute("aria-controls")); }

  function lead(plot) {
    var panel = panelOf(plot);
    if (!panel || panel.hidden) return;
    var p = plot.getBoundingClientRect();
    var s = panel.getBoundingClientRect();
    panel.style.setProperty("--nx", (p.left + p.width / 2 - s.left).toFixed(1) + "px");
  }

  function light(plot, i) {
    var marks = plot.querySelectorAll(".plot__marks i");
    for (var k = 0; k < marks.length; k++) marks[k].classList.toggle("is-lit", k === i);
  }

  function close(plot) {
    var panel = panelOf(plot);
    plot.setAttribute("aria-expanded", "false");
    if (panel) panel.hidden = true;
    light(plot, -1);
    if (current === plot) current = null;
  }

  function open(plot, scroll) {
    if (current && current !== plot) close(current);
    var panel = panelOf(plot);
    plot.setAttribute("aria-expanded", "true");
    if (panel) panel.hidden = false;
    current = plot;
    lead(plot);
    if (scroll && panel) {
      var r = panel.getBoundingClientRect();
      var room = window.innerHeight;
      if (r.top > room - 180) {
        window.scrollBy({ top: r.top - room * 0.4, behavior: reduce ? "auto" : "smooth" });
      }
    }
  }

  plots.forEach(function (plot) {
    var panel = panelOf(plot);
    if (!panel) return;
    plot.setAttribute("aria-expanded", "false");
    panel.hidden = true;
    plot.addEventListener("click", function () {
      if (plot.getAttribute("aria-expanded") === "true") close(plot);
      else open(plot, true);
    });
    var x = panel.querySelector(".sched__x");
    if (x) {
      x.hidden = false;
      x.addEventListener("click", function () { close(plot); plot.focus(); });
    }
    panel.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { close(plot); plot.focus(); }
    });
    Array.prototype.forEach.call(panel.querySelectorAll("li[data-i]"), function (li) {
      var i = parseInt(li.getAttribute("data-i"), 10);
      li.addEventListener("mouseenter", function () { light(plot, i); });
      li.addEventListener("mouseleave", function () { light(plot, -1); });
      li.addEventListener("focusin", function () { light(plot, i); });
      li.addEventListener("focusout", function () { light(plot, -1); });
    });
  });
  plan.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && current && e.target === current) close(current);
  });
  plan.classList.add("is-live");

  var queued = false;
  window.addEventListener("resize", function () {
    if (queued || !current) return;
    queued = true;
    window.requestAnimationFrame(function () { queued = false; if (current) lead(current); });
  });
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(function () { if (current) lead(current); });

  var want = (window.location.search.match(/[?&]open=([a-z0-9-]+)/) || [])[1];
  if (want) {
    var hit = plan.querySelector('.plot[data-g="' + want + '"]');
    if (hit) open(hit, false);
  }
})();
