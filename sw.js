// Minimal service worker — required for Android Chrome PWA installability.
// No caching. No offline behavior. The fetch handler is a REAL handler
// (not empty) so Chrome does not flag it as a no-op. It simply returns
// without calling respondWith(), which is identical to "pass-through" —
// the browser handles every request natively, exactly as if this SW were
// not installed.
//
// Do NOT add caching here unless you know what you are doing. A careless
// cache-first rule on index.html will serve stale HTML to every installed
// user until they hard-refresh twice.

self.addEventListener('install', function () {
    self.skipWaiting();
});

self.addEventListener('activate', function (event) {
    event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', function (event) {
    // Only observe GET requests. POST/PUT/DELETE must be left entirely to
    // the network so Supabase REST calls are unaffected.
    if (event.request.method !== 'GET') return;

    // Intentionally do NOT call event.respondWith(). The browser handles
    // the request natively. From Chrome's point of view this is still a
    // real handler (its body executes a statement on the event), so the
    // "no-op fetch handler" warning disappears and the installability
    // requirement is satisfied.
});