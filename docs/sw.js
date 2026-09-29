// VERSION は build.py がファイルの中身から作る。中身が変わると古いキャッシュを捨てて入れ直す
const VERSION = "eigo-c0fd3d9b58ce";
const CORE = [
  "./",
  "index.html",
  "words.html",
  "phrases.html",
  "korean.html",
  "manifest.webmanifest",
  "icon-180.png",
  "icon-192.png",
  "icon-512.png",
];

// cache: "reload" でブラウザの HTTP キャッシュを飛ばして取る。
// これが無いと GitHub Pages の max-age=600 の間は古い HTML が新しい版にしまわれてしまう
self.addEventListener("install", (event) => {
  const fresh = CORE.map((u) => new Request(u, { cache: "reload" }));
  event.waitUntil(caches.open(VERSION).then((c) => c.addAll(fresh)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches.keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== VERSION).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

// 先にキャッシュを見る。無いもの（Google Fonts など）はネットから取って、次回のためにしまう
self.addEventListener("fetch", (event) => {
  if (event.request.method !== "GET") return;
  event.respondWith(
    caches.match(event.request, { ignoreSearch: true }).then((hit) => {
      if (hit) return hit;
      return fetch(event.request).then((res) => {
        if (res.ok || res.type === "opaque") {
          const copy = res.clone();
          caches.open(VERSION).then((c) => c.put(event.request, copy));
        }
        return res;
      });
    })
  );
});
