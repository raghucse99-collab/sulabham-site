/* Sulabham — move a visitor's saved data from the old address (raghucse99-collab.github.io/sulabham)
   to sulabham.in. The old address now serves a tiny bridge page that sends everything saved in that
   browser here as  #sulmig=<data>[&h=<original hash>].  This script runs first on every page:
   - copies each saved key that is not already here (never overwrites newer data on sulabham.in);
   - keeps the old device number (so personal unlock codes keep working) unless this browser has
     already unlocked something here with a new device number;
   - restores the page's original #hash and removes the data from the address bar. */
(function(){
  var h=location.hash;if(h.indexOf("#sulmig=")!==0)return;
  var parts=h.slice(1).split("&"),data=null,orig="";
  parts.forEach(function(p){if(p.indexOf("sulmig=")===0){try{data=JSON.parse(decodeURIComponent(escape(atob(decodeURIComponent(p.slice(7))))))}catch(e){}}
    else if(p.indexOf("h=")===0){orig=decodeURIComponent(p.slice(2))}});
  try{
    if(data&&typeof data==="object"){
      var unlockedHere=false;for(var i=0;i<localStorage.length;i++){var k0=localStorage.key(i);if(/^sul_(pack|aso|code_)/.test(k0))unlockedHere=true}
      Object.keys(data).forEach(function(k){var v=data[k];if(typeof v!=="string")return;
        if(k==="sul_dev"){if(!unlockedHere||localStorage.getItem(k)===null)localStorage.setItem(k,v);return}
        if(localStorage.getItem(k)===null)localStorage.setItem(k,v)});
      localStorage.setItem("sul_moved",new Date().toISOString().slice(0,10));
    }
  }catch(e){}
  try{history.replaceState(null,"",location.pathname+location.search+(orig?"#"+orig:""))}catch(e){location.hash=orig}
})();

/* Sulabham app: link the app manifest on every page and register the offline service worker. */
(function(){
  try{var d=document,h=d.head||d.getElementsByTagName("head")[0];
    if(h&&!d.querySelector('link[rel="manifest"]')){var l=d.createElement("link");l.rel="manifest";l.href="/manifest.webmanifest";h.appendChild(l);
      var t=d.createElement("meta");t.name="theme-color";t.content="#1d4f91";h.appendChild(t);
      var a=d.createElement("link");a.rel="apple-touch-icon";a.href="/icons/icon-192.png";h.appendChild(a)}
    window.addEventListener("beforeinstallprompt",function(ev){ev.preventDefault();window.SUL_install=ev;d.dispatchEvent(new Event("sul-install"))});
    if("serviceWorker" in navigator&&location.protocol==="https:")window.addEventListener("load",function(){navigator.serviceWorker.register("/sw.js").catch(function(){})});
  }catch(e){}
})();
