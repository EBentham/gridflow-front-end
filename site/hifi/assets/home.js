/* gridflow homepage: the buried cables.

   On wide screens four feeds run from the drawn assets that gridflow has data for (the substation, the
   met mast, the interconnector's converter station and the gas terminal) down through the topsoil to
   the vendors that publish that data, and the silver tables splice into the gold views. The route is
   measured from the rendered page, so it follows the text wherever it wraps. The cables are drawing
   only: the page reads the same without them, and on narrow screens they are not drawn. */

(function () {
  "use strict";

  var NS = "http://www.w3.org/2000/svg";
  var main = document.getElementById("main");
  var land = document.querySelector(".landscape svg");
  if (!main || !land || !land.getScreenCTM || !window.matchMedia) return;

  var feedsOn = window.matchMedia("(min-width: 1100px)");
  var joinOn = window.matchMedia("(min-width: 1380px)");
  var css = getComputedStyle(document.documentElement);
  function tok(name, fallback) { return (css.getPropertyValue(name) || "").trim() || fallback; }
  var INK = tok("--ink", "#1C2B22");
  var BRONZE = tok("--bronze", "#A5713C");
  var SILVER = tok("--silver", "#9FADAB");
  var GOLD = tok("--gold", "#C2A14A");
  var T_SILVER = tok("--silver-tint", "#DCE2DF");
  var T_GOLD = tok("--gold-tint", "#E9DDAF");

  var svg = document.createElementNS(NS, "svg");
  svg.setAttribute("class", "cables");
  svg.setAttribute("aria-hidden", "true");
  svg.setAttribute("focusable", "false");
  main.insertBefore(svg, main.firstChild);

  function q(sel) { return document.querySelector(sel); }
  function box(el) {
    var r = el.getBoundingClientRect();
    var m = main.getBoundingClientRect();
    return { l: r.left - m.left, t: r.top - m.top, r: r.right - m.left, b: r.bottom - m.top, w: r.width, h: r.height };
  }
  // drawing coordinates of the landscape to page coordinates inside <main>
  function fromLand(x, y) {
    var p = land.createSVGPoint();
    p.x = x; p.y = y;
    p = p.matrixTransform(land.getScreenCTM());
    var m = main.getBoundingClientRect();
    return [p.x - m.left, p.y - m.top];
  }
  // the ground surface of the drawing (gen.prof on the reference board)
  function prof(x) { return 940 + 4 * Math.sin(x / 190 + 0.6) - 2.5 * Math.sin(x / 83 + 1.3); }
  function smoothstep(t) { t = Math.max(0, Math.min(1, t)); return t * t * (3 - 2 * t); }
  function n(v) { return Math.round(v * 10) / 10; }
  // Catmull-Rom through the points, as cubic Beziers (the reference generator's smooth())
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
  function cable(d, core, sheath, corew) {
    var common = ' fill="none" stroke-linecap="round" stroke-linejoin="round"></path>';
    out.push('<path d="' + d + '" stroke="' + INK + '" stroke-width="' + sheath + '"' + common);
    out.push('<path d="' + d + '" stroke="' + core + '" stroke-width="' + corew + '"' + common);
  }
  function dot(x, y, r, fill, sw) {
    out.push('<circle cx="' + n(x) + '" cy="' + n(y) + '" r="' + r + '" fill="' + fill + '"' +
             (sw ? ' stroke="' + INK + '" stroke-width="' + sw + '"' : "") + "></circle>");
  }

  // ---------------------------------------------------------------- the four feeds
  function feeds() {
    var keys = ["elexon", "nesodp", "entsoe", "gie", "neso", "openmeteo", "entsog"];
    var v = {};
    for (var k = 0; k < keys.length; k++) {
      var el = q(".vend--" + keys[k]);
      if (!el) return;
      v[keys[k]] = box(el);
    }
    function mark(key) { return [v[key].l + 16, v[key].t]; }

    var wrap = q(".purpose");
    var bed = q(".stratum--topsoil > .bedding");
    var core = q(".core__fig .core-d");
    var head = q(".cat__head");
    var body = q(".purpose__body");
    if (!wrap || !bed || !core || !head || !body) return;
    var wb = box(wrap);
    var right = wb.r - parseFloat(getComputedStyle(wrap).paddingRight);
    var RISER = [right - 20, right - 5, right + 10, right + 25];
    var bedY = box(bed).t;
    var cb = box(core);
    var bb = core.getBBox();
    var vbw = core.viewBox.baseVal.width || cb.w;
    var coreRight = cb.l + (bb.x + bb.width) * cb.w / vbw;
    var coreTop = box(q(".core")).t;
    var tray = box(body).b + 44;
    var R = 16;

    var srcs = [890, 1018, 1124, 1314];   // substation, met mast, converter station, gas terminal
    var ends = [mark("openmeteo")[0] - 36, mark("openmeteo")[0], mark("entsoe")[0], mark("entsog")[0]];
    var runs = [];
    for (var i = 0; i < 4; i++) {
      var s = fromLand(srcs[i], prof(srcs[i]) - 3);
      var xs = s[0], S = s[1], xr = RISER[i];
      // a feed that starts above the core sample swings clear of it before it goes down
      var xa = Math.max(xs, coreRight + 30 + 15 * i);
      var pts = [[xs, S]];
      var g1 = bedY + 10, rEnd = tray - 30;
      var y;
      if (xa > xs) {
        for (y = S + 10; y < coreTop; y += 11) {
          pts.push([xs + (xa - xs) * smoothstep((y - S) / (coreTop - 6 - S)), y]);
        }
      }
      var gStart = xa > xs ? coreTop : S + 50;
      for (y = (xa > xs ? coreTop + 22 : S + 30); y <= rEnd; y += 22) {
        if (y <= g1) {
          var t = smoothstep((y - gStart) / (g1 - gStart));
          var env = Math.sin(Math.PI * Math.min(1, Math.max(0, (y - gStart) / (g1 - gStart))));
          pts.push([xa + (xr - xa) * t + 16 * Math.sin((y - S) / 70) * env, y]);
        } else {
          var env2 = Math.sin(Math.PI * Math.min(1, (y - g1) / (rEnd - g1)));
          pts.push([xr + 9 * Math.sin((y - g1) / 95 + 0.4) * env2, y]);
        }
      }
      pts.push([xr, rEnd]);
      var ty = tray + 15 * i;
      var rr = 18 + (xr - RISER[0]);
      var xe = ends[i];
      runs.push(smooth(pts) + " V" + n(ty - rr) + " Q" + n(xr) + " " + n(ty) + " " + n(xr - rr) + " " + n(ty) +
                " H" + n(xe + R) + " Q" + n(xe) + " " + n(ty) + " " + n(xe) + " " + n(ty + R));
    }
    var joints = [];
    // the substation feeds Elexon, the NESO Data Portal and NESO along a lane under the heading
    var lane = box(head).b + 18;
    var ex = mark("elexon");
    cable(runs[0] + " V" + n(lane - R) + " Q" + n(ends[0]) + " " + n(lane) + " " + n(ends[0] - R) + " " + n(lane) +
          " H" + n(ex[0] + R) + " Q" + n(ex[0]) + " " + n(lane) + " " + n(ex[0]) + " " + n(lane + R) + " V" + n(ex[1]),
          BRONZE, 4.4, 1.5);
    [mark("nesodp"), mark("neso")].forEach(function (b) {
      cable("M" + n(b[0] + R) + " " + n(lane) + " Q" + n(b[0]) + " " + n(lane) + " " + n(b[0]) + " " + n(lane + R) +
            " V" + n(b[1]), BRONZE, 4.4, 1.5);
      joints.push([b[0] + R, lane]);
    });
    // the met mast feeds Open-Meteo; the converter station feeds ENTSO-E
    cable(runs[1] + " V" + n(mark("openmeteo")[1]), BRONZE, 4.4, 1.5);
    cable(runs[2] + " V" + n(mark("entsoe")[1]), BRONZE, 4.4, 1.5);
    // the gas terminal feeds ENTSO-G, with a branch to GIE
    cable(runs[3] + " V" + n(mark("entsog")[1]), BRONZE, 4.4, 1.5);
    var g = mark("gie"), x3 = ends[3], jy = g[1] - 44;
    cable("M" + n(x3) + " " + n(jy) + " Q" + n(x3) + " " + n(jy + 14) + " " + n(x3 + 14) + " " + n(jy + 16) +
          " Q" + n(g[0]) + " " + n(jy + 19) + " " + n(g[0]) + " " + n(jy + 34) + " V" + n(g[1]), BRONZE, 4.4, 1.5);
    joints.push([x3, jy]);
    joints.forEach(function (j) { dot(j[0], j[1], 4.6, INK, 0); });
  }

  // ---------------------------------------------------------------- silver tables into the gold views
  function join() {
    var rows = document.querySelectorAll(".tables li");
    var views = document.querySelectorAll(".views li");
    var goldEl = q(".stratum--gold");
    var text = q(".gold__text");
    if (rows.length !== 4 || views.length !== 4 || !goldEl || !text) return;
    var list = box(q(".tables"));
    var vb = box(q(".views"));
    var sx = Math.min(vb.l + 610, box(text).l - 110);
    var vt = box(views[0]).t;
    var sy = vt - 98;
    var c1y = box(goldEl).t + 12 - 40;
    var i, stx = list.l;
    for (i = 0; i < 4; i++) {
      var ry = box(rows[i]).t + 20;
      var xt = stx - 34 - (3 - i) * 12;
      var yin = sy - 9 + i * 6;
      cable("M" + n(stx - 12) + " " + n(ry) + " H" + n(xt + 14) + " Q" + n(xt) + " " + n(ry) + " " + n(xt) + " " +
            n(ry + 14) + " V" + n(ry + 60 + (3 - i) * 4) + " C" + n(xt) + " " + n(c1y) + " " + n(sx + 70 + i * 6) +
            " " + n(yin) + " " + n(sx + 34) + " " + n(yin), SILVER, 4, 1.4);
      dot(stx - 12, ry, 4.2, T_SILVER, 1.6);
    }
    for (i = 0; i < 4; i++) {
      var yout = sy - 9 + i * 6;
      var tx = box(views[i]).l + 10, tyv = vt - 8;
      cable("M" + n(sx - 34) + " " + n(yout) + " C" + n(sx - 90 - i * 4) + " " + n(yout) + " " + n(tx) + " " +
            n(tyv - 70 + i * 10) + " " + n(tx) + " " + n(tyv), GOLD, 4, 1.4);
      dot(tx, tyv, 4.2, T_GOLD, 1.6);
    }
    out.push('<rect x="' + n(sx - 36) + '" y="' + n(sy - 16) + '" width="72" height="32" rx="16" fill="' + GOLD +
             '" stroke="' + INK + '" stroke-width="1.6"></rect>');
    out.push('<path d="M' + n(sx - 20) + " " + n(sy - 16) + " V" + n(sy + 16) + " M" + n(sx + 20) + " " + n(sy - 16) +
             " V" + n(sy + 16) + '" stroke="' + INK + '" stroke-width="1" opacity=".5"></path>');
  }

  function draw() {
    out = [];
    if (feedsOn.matches) feeds();
    if (joinOn.matches) join();
    // main's own box, not its scrollHeight: the overlay would otherwise hold the page at its tallest
    var m = main.getBoundingClientRect();
    svg.setAttribute("width", Math.round(m.width));
    svg.setAttribute("height", Math.round(m.height));
    svg.innerHTML = out.join("");
    document.documentElement.classList.toggle("has-cables", feedsOn.matches);
  }

  // a short debounce rather than requestAnimationFrame, which never fires in a tab that is not visible
  var pending = 0;
  function schedule() {
    window.clearTimeout(pending);
    pending = window.setTimeout(draw, 60);
  }
  draw();
  window.addEventListener("resize", schedule);
  window.addEventListener("load", schedule);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(schedule);
  if ("ResizeObserver" in window) new ResizeObserver(schedule).observe(main);
})();
