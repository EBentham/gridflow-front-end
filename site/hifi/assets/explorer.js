/* Explorer page: the click trail. Where the three steps sit side by side (1180px and up), a cable runs out of
   each ringed control, round the page margin and into the tab bar of the next window. The layout does not
   depend on it; below 1180px the steps stack and there is no trail. */
(function () {
  "use strict";

  var NS = "http://www.w3.org/2000/svg";
  var INK = "#1C2B22", CORE = "#AFC64E", SOIL = "#ECE8DA";
  var host = document.querySelector(".tour-st");
  if (!host) return;

  function el(name, attrs) {
    var n = document.createElementNS(NS, name);
    Object.keys(attrs).forEach(function (k) { n.setAttribute(k, attrs[k]); });
    return n;
  }

  // an orthogonal polyline with rounded corners
  function rpath(pts, r) {
    var d = "M" + pts[0][0] + " " + pts[0][1];
    for (var i = 1; i < pts.length - 1; i++) {
      var a = pts[i - 1], b = pts[i], c = pts[i + 1];
      var la = Math.max(Math.abs(b[0] - a[0]), Math.abs(b[1] - a[1])) || 1;
      var lb = Math.max(Math.abs(c[0] - b[0]), Math.abs(c[1] - b[1])) || 1;
      var rr = Math.min(r, la / 2, lb / 2);
      var ux = (b[0] - a[0]) / la, uy = (b[1] - a[1]) / la, vx = (c[0] - b[0]) / lb, vy = (c[1] - b[1]) / lb;
      d += " L" + (b[0] - ux * rr) + " " + (b[1] - uy * rr) + " Q" + b[0] + " " + b[1] + " " +
           (b[0] + vx * rr) + " " + (b[1] + vy * rr);
    }
    var z = pts[pts.length - 1];
    return d + " L" + z[0] + " " + z[1];
  }

  function draw() {
    var old = host.querySelector(".trail");
    if (old) old.remove();
    if (window.innerWidth < 1180) return;
    var o = host.getBoundingClientRect();
    function box(sel) {
      var n = host.querySelector(sel);
      if (!n) return null;
      var r = n.getBoundingClientRect();
      return { l: r.left - o.left, r: r.right - o.left, t: r.top - o.top, b: r.bottom - o.top };
    }
    var r1 = box(".s1 .ring"), r2 = box(".s2 .ring"), w2 = box(".s2 .win"), w3 = box(".s3 .win");
    var wrap = box(".tour");
    if (!r1 || !r2 || !w2 || !w3 || !wrap) return;
    var side = parseFloat(getComputedStyle(host.querySelector(".tour")).paddingLeft) || 80;
    var gl = Math.max(12, wrap.l + side / 2), gr = Math.min(o.width - 12, wrap.r - side / 2);
    var y1 = (r1.t + r1.b) / 2, b2 = w2.t + 21, y2 = (r2.t + r2.b) / 2, b3 = w3.t + 21;
    var p1 = rpath([[r1.l, y1], [gl, y1], [gl, b2], [w2.l, b2]], 14);
    var p2 = rpath([[r2.r, y2], [gr, y2], [gr, b3], [w3.r, b3]], 14);

    var svg = el("svg", { "class": "trail", width: o.width, height: o.height, "aria-hidden": "true", focusable: "false" });
    [p1, p2].forEach(function (d) {
      svg.appendChild(el("path", { d: d, fill: "none", stroke: INK, "stroke-width": 5.2, "stroke-linecap": "round", "stroke-linejoin": "round" }));
      svg.appendChild(el("path", { d: d, fill: "none", stroke: CORE, "stroke-width": 2.3, "stroke-linecap": "round", "stroke-linejoin": "round" }));
    });
    [[w2.l, b2], [w3.r, b3]].forEach(function (p) {
      svg.appendChild(el("circle", { cx: p[0], cy: p[1], r: 5.5, fill: SOIL, stroke: INK, "stroke-width": 1.8 }));
      svg.appendChild(el("circle", { cx: p[0], cy: p[1], r: 1.8, fill: INK }));
    });
    [[r1.l, y1], [r2.r, y2]].forEach(function (p) {
      svg.appendChild(el("circle", { cx: p[0], cy: p[1], r: 3.2, fill: INK }));
    });
    host.appendChild(svg);
  }

  var t;
  function soon() { clearTimeout(t); t = setTimeout(draw, 80); }
  draw();
  window.addEventListener("resize", soon);
  window.addEventListener("load", draw);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(draw);
})();
