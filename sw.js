// «قارئ الكلمات» moved to https://qari.pages.dev/: this removes the old offline copy (its saved page) and then itself.
self.addEventListener('install',()=>self.skipWaiting());
self.addEventListener('activate',e=>{e.waitUntil((async()=>{
  await Promise.all((await caches.keys()).map(k=>caches.delete(k)));
  await self.registration.unregister();
})());});
