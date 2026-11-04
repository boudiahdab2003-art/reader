// Keeps the game playable when the school internet drops.
// The page itself is fetched fresh whenever the internet works (so updates arrive at once);
// the saved copy is used only offline or when the network takes longer than 3 seconds.
// Other files (icon, manifest) come from the saved copy and are refreshed in the background.
// Change CACHE when this file changes: the new worker then replaces the old one and reloads open pages once.
var CACHE = "nal3ab-v2";
var FILES = ["./", "./index.html", "./manifest.webmanifest", "./icon.svg"];
self.addEventListener("install", function (e) {
  e.waitUntil(caches.open(CACHE).then(function (c) {
    return Promise.all(FILES.map(function (f) { return fetch(f, { cache: "no-cache" }).then(function (res) { if (res.ok) return c.put(f, res); }); }));
  }).then(function () { return self.skipWaiting(); }));
});
self.addEventListener("activate", function (e) {
  e.waitUntil(caches.keys().then(function (ks) {
    var old = ks.filter(function (k) { return k !== CACHE; });
    return Promise.all(old.map(function (k) { return caches.delete(k); })).then(function () { return old.length > 0; });
  }).then(function (replaced) {
    return self.clients.claim().then(function () {
      // pages still showing the old version: load them again so they get the new one
      if (!replaced) return;
      return self.clients.matchAll({ type: "window" }).then(function (cs) {
        cs.forEach(function (c) { if (c.navigate) c.navigate(c.url).catch(function () {}); });
      });
    });
  }));
});
function isPage(req) {
  if (req.mode === "navigate") return true;
  var p = new URL(req.url).pathname;
  return /\/$|\/index\.html$/.test(p);
}
function pageFirst(req, c) {
  return new Promise(function (resolve) {
    var done = false;
    function give(res) { if (!done && res) { done = true; resolve(res); } }
    function saved() { return c.match("./"); }
    var timer = setTimeout(function () { saved().then(give); }, 3000);
    fetch(req.url, { cache: "no-cache", credentials: "same-origin" }).then(function (res) {
      if (res && res.ok) c.put("./", res.clone());
      clearTimeout(timer); give(res);
    }).catch(function () {
      clearTimeout(timer);
      saved().then(function (hit) { give(hit || Response.error()); });
    });
  });
}
self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET" || new URL(req.url).origin !== location.origin) return;
  e.respondWith(caches.open(CACHE).then(function (c) {
    if (isPage(req)) return pageFirst(req, c);
    return c.match(req, { ignoreSearch: true }).then(function (hit) {
      var net = fetch(req).then(function (res) {
        if (res && res.ok) c.put(req, res.clone());
        return res;
      }).catch(function () { return hit || c.match("./"); });
      return hit || net;
    });
  }));
});
