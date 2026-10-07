/* gridflow site chrome: the masthead, the primary nav and the footer, injected on every page.

   Page contract (set on <body>):
     data-page          which nav entry is current: home | sources | vendor | dataset | architecture | model |
                        explorer | about
     data-root          the relative path back to the site root: "" at the root, "../" one level down, "../../" two
     data-screen-label  a human label for the page, kept as page metadata; the chrome does not read it

   Every page carries its own <main id="main">. The masthead goes in before it, the footer after it.
   The small behaviours at the end (tabs, copy buttons, the sidebar scroll-spy) are shared by the
   generated dataset and vendor pages. */

(function () {
  "use strict";

  var body = document.body;
  var page = body.getAttribute("data-page") || "";
  var root = body.getAttribute("data-root") || "";

  var NAV = [
    { key: "home", label: "Home", href: "index.html" },
    { key: "sources", label: "Data sources", href: "data-sources.html" },
    { key: "architecture", label: "Architecture", href: "architecture.html" },
    { key: "model", label: "Models", href: "models.html" },
    { key: "explorer", label: "Explorer", href: "explorer.html" },
    { key: "about", label: "About", href: "index.html#about" }
  ];
  // vendor hubs and dataset pages live under Data sources
  var CURRENT = { home: "home", sources: "sources", vendor: "sources", dataset: "sources",
                  architecture: "architecture", model: "model", models: "model", explorer: "explorer",
                  about: "about" }[page];

  function links(current) {
    return NAV.map(function (item) {
      var here = current && item.key === current ? ' aria-current="page"' : "";
      return '<li><a href="' + root + item.href + '"' + here + ">" + item.label + "</a></li>";
    }).join("");
  }

  var masthead =
    '<a class="skip" href="#main">Skip to content</a>' +
    '<header class="masthead">' +
      '<div class="wrap masthead__in">' +
        '<a class="brand" href="' + root + 'index.html">gridflow</a>' +
        '<nav class="nav" aria-label="Primary"><ul>' + links(CURRENT) + "</ul></nav>" +
      "</div>" +
    "</header>";

  var footer =
    '<footer class="site-foot stratum stratum--deep">' +
      '<div class="wrap site-foot__in">' +
        '<a class="brand" href="' + root + 'index.html">gridflow</a>' +
        '<nav aria-label="Footer"><ul>' + links(null) + "</ul></nav>" +
        '<ul aria-label="Source code on GitHub">' +
          '<li><a href="https://github.com/EBentham/gridflow">gridflow</a></li>' +
          '<li><a href="https://github.com/EBentham/gridflow-models">gridflow-models</a></li>' +
          '<li><a href="https://github.com/EBentham/gridflow-front-end">gridflow-front-end</a></li>' +
        "</ul>" +
        '<p class="site-foot__line">Elliot Bentham, 2026.</p>' +
      "</div>" +
    "</footer>";

  body.insertAdjacentHTML("afterbegin", masthead);
  var main = document.querySelector("main");
  // A dataset page ends in its own deep band, which holds only related datasets (DESIGN.md, the
  // dataset page anatomy): no site footer there.
  if (main) {
    if (!main.classList.contains("ds")) main.insertAdjacentHTML("afterend", footer);
  } else {
    body.insertAdjacentHTML("beforeend", footer);
  }

  // ---------------------------------------------------------------- the dataset page's demo notebook
  // The button opens the notebook in place (and hides the two-cell call it replaces); "Copy notebook"
  // copies the code only, ready to paste into Jupyter.
  var SHUT = "Open the demo notebook", OPEN = "Close the demo notebook";
  document.querySelectorAll("button.ds-open[aria-controls]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var on = btn.getAttribute("aria-expanded") !== "true";
      btn.setAttribute("aria-expanded", on ? "true" : "false");
      btn.textContent = on ? OPEN : SHUT;
      btn.getAttribute("aria-controls").split(" ").forEach(function (id) {
        var el = document.getElementById(id);
        if (el) el.hidden = !on;
      });
      var call = document.getElementById(btn.getAttribute("data-call"));
      if (call) call.hidden = on;
    });
  });
  document.querySelectorAll("button[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var src = document.getElementById(btn.getAttribute("data-copy"));
      var status = btn.parentNode.querySelector(".ds-status");
      if (!src) return;
      function say(text) { if (status) status.textContent = text; }
      function selectIt() {
        src.hidden = false;
        src.focus();
        src.select();
        var ok = false;
        try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
        if (ok) { src.hidden = true; btn.focus(); }
        say(ok ? "Copied." : "Selected. Copy it with your keyboard.");
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(src.value).then(function () { src.hidden = true; say("Copied."); }, selectIt);
      } else {
        selectIt();
      }
    });
  });

  // ---------------------------------------------------------------- the weather-site map
  // Each marker is a link to its table row, so the map works without this. Here, hover or focus on a
  // marker opens a card with the row's facts beside it; a click or tap pins the card until another tap,
  // a tap elsewhere or Escape. A marker and its row light together. The card is clamped inside the map's
  // box, so at any width it stays on screen.
  document.querySelectorAll(".wm").forEach(function (fig) {
    var plot = fig.querySelector(".wm-plot");
    var card = fig.querySelector(".wm-card");
    var table = fig.querySelector(".wm-t");
    if (!plot || !card || !table) return;
    var heads = Array.prototype.map.call(table.querySelectorAll("thead th"), function (th) {
      return th.textContent;
    });
    var pinned = null, shown = null;

    function parts(name) {
      return {
        mark: fig.querySelector('.wm-s[data-site="' + name + '"]'),
        label: fig.querySelector('.wm-labs text[data-site="' + name + '"]'),
        row: table.querySelector('tr[data-site="' + name + '"]')
      };
    }
    function light(name, on) {
      var p = parts(name);
      [p.mark, p.label, p.row].forEach(function (el) { if (el) el.classList.toggle("is-on", on); });
    }
    function fill(row) {
      card.textContent = "";
      var cells = row.children;
      var group = row.parentNode.querySelector(".wm-gh th");
      var h = document.createElement("p");
      h.className = "wm-card__h";
      var nameCell = row.querySelector(".wm-n");
      var name = document.createElement("span");
      name.className = "wm-card__n";
      name.textContent = nameCell ? nameCell.textContent : row.getAttribute("data-site");
      var code = document.createElement("code");
      code.textContent = row.getAttribute("data-site");
      h.appendChild(name);
      h.appendChild(code);
      if (group) h.appendChild(document.createTextNode(group.textContent));
      var dl = document.createElement("dl");
      for (var i = 1; i < cells.length; i++) {
        var dt = document.createElement("dt"), dd = document.createElement("dd");
        dt.textContent = heads[i] || "";
        dd.textContent = cells[i].textContent;
        if (cells[i].classList.contains("wm-c")) dd.className = "wm-c";
        dl.appendChild(dt);
        dl.appendChild(dd);
      }
      card.appendChild(h);
      card.appendChild(dl);
    }
    function place(mark) {
      var box = plot.getBoundingClientRect();
      var dot = (mark.querySelector(".wm-dot") || mark).getBoundingClientRect();
      var x = dot.left + dot.width / 2 - box.left, y = dot.top + dot.height / 2 - box.top;
      var w = card.offsetWidth, h = card.offsetHeight, gap = 16;
      var left = x + gap, top = y - 24;
      if (left + w > box.width) left = x - gap - w;
      if (left < 0) {
        // no room either side: centre it on the marker, below it (or above when it would run off the box)
        left = Math.min(Math.max(0, x - w / 2), Math.max(0, box.width - w));
        top = y + gap + h <= box.height ? y + gap : y - gap - h;
      }
      top = Math.min(Math.max(0, top), Math.max(0, box.height - h));
      card.style.left = left + "px";
      card.style.top = top + "px";
    }
    function show(name) {
      var p = parts(name);
      if (!p.mark || !p.row) return;
      if (shown && shown !== name) light(shown, false);
      shown = name;
      light(name, true);
      fill(p.row);
      card.hidden = false;
      place(p.mark);
    }
    function hide(name) {
      if (pinned && pinned !== name) { show(pinned); return; }
      if (pinned) return;
      if (shown) light(shown, false);
      shown = null;
      card.hidden = true;
    }
    function unpin() {
      var was = pinned;
      pinned = null;
      if (was) hide(was);
    }

    fig.querySelectorAll(".wm-s").forEach(function (mark) {
      var name = mark.getAttribute("data-site");
      mark.addEventListener("mouseenter", function () { show(name); });
      mark.addEventListener("mouseleave", function () { hide(name); });
      mark.addEventListener("focus", function () { show(name); });
      mark.addEventListener("blur", function () { hide(name); });
      mark.addEventListener("click", function (e) {
        e.preventDefault();
        if (pinned === name) { unpin(); return; }
        pinned = name;
        show(name);
      });
    });
    table.querySelectorAll("tr[data-site]").forEach(function (row) {
      var name = row.getAttribute("data-site");
      row.addEventListener("mouseenter", function () { light(name, true); });
      row.addEventListener("mouseleave", function () { if (shown !== name) light(name, false); });
    });
    document.addEventListener("click", function (e) {
      if (pinned && !e.target.closest(".wm-s") && !card.contains(e.target)) unpin();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && (pinned || shown)) { pinned = null; hide(shown); }
    });
    // where the table is wider than its box, say so: the statistics start off-screen on a phone
    var box = fig.querySelector(".wm-tw"), hint = fig.querySelector(".wm-hint");
    function overflow() {
      if (box && hint) hint.hidden = box.scrollWidth <= box.clientWidth + 1;
    }
    overflow();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(overflow);
    window.addEventListener("resize", function () {
      if (shown) place(parts(shown).mark);
      overflow();
    });
  });

  // ---------------------------------------------------------------- shared page behaviours

  // copy buttons on code blocks
  document.querySelectorAll(".code-wrap").forEach(function (wrap) {
    if (wrap.querySelector(".copy")) return;
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "copy";
    btn.textContent = "Copy";
    btn.addEventListener("click", function () {
      var code = wrap.querySelector("pre, code");
      if (!code || !navigator.clipboard) return;
      navigator.clipboard.writeText(code.textContent || "").then(function () {
        btn.textContent = "Copied";
        setTimeout(function () { btn.textContent = "Copy"; }, 1200);
      });
    });
    wrap.appendChild(btn);
  });

  // tab groups: [data-tabs] holding buttons and .tab-panel siblings, matched by order
  document.querySelectorAll("[data-tabs]").forEach(function (group) {
    var buttons = group.querySelectorAll(".tabs button, .tab-buttons button");
    var panels = group.querySelectorAll(".tab-panel");
    buttons.forEach(function (b, i) {
      b.addEventListener("click", function () {
        buttons.forEach(function (x) { x.classList.remove("active"); x.setAttribute("aria-selected", "false"); });
        panels.forEach(function (x) { x.classList.remove("active"); });
        b.classList.add("active");
        b.setAttribute("aria-selected", "true");
        if (panels[i]) panels[i].classList.add("active");
      });
    });
  });

  // sidebar scroll-spy: marks the in-page anchor for the section in view
  var anchors = document.querySelectorAll('.sidebar a[href^="#"]');
  if (anchors.length && "IntersectionObserver" in window) {
    var observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (!e.isIntersecting) return;
        anchors.forEach(function (l) { l.classList.remove("active"); l.removeAttribute("aria-current"); });
        var match = document.querySelector('.sidebar a[href="#' + e.target.id + '"]');
        if (match) { match.classList.add("active"); match.setAttribute("aria-current", "location"); }
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    document.querySelectorAll("section[id]").forEach(function (s) { observer.observe(s); });
  }
})();
