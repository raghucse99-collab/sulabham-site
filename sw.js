/* Sulabham app service worker — network first, so the newest content always shows when online;
   pages and files already opened stay readable offline. */
var C="sul-v1";
self.addEventListener("install",function(e){self.skipWaiting();e.waitUntil(caches.open(C).then(function(c){return c.addAll(["/","/index.html","/app.html"]).catch(function(){})}))});
self.addEventListener("activate",function(e){e.waitUntil(caches.keys().then(function(k){return Promise.all(k.filter(function(n){return n!==C}).map(function(n){return caches.delete(n)}))}).then(function(){return self.clients.claim()}))});
self.addEventListener("fetch",function(e){var r=e.request;if(r.method!=="GET")return;var u=new URL(r.url);if(u.origin!==location.origin)return;
  e.respondWith(fetch(r).then(function(res){if(res&&res.ok&&res.type==="basic"){var cp=res.clone();caches.open(C).then(function(c){c.put(r,cp)})}return res})
    .catch(function(){return caches.match(r,{ignoreSearch:r.mode==="navigate"}).then(function(m){return m||(r.mode==="navigate"?caches.match("/index.html"):undefined)||Response.error()})}))});
