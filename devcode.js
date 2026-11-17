/* Sulabham personal (one-device) unlock codes.
   Every phone gets a device number (saved once in this browser). The owner turns
   (course master code + device number) into a personal code with the private code maker.
   This page turns (personal code + this device number) back into the master code.
   A personal code typed on another phone gives a wrong master code, so unlocking fails.
   Plain master codes are accepted only until CUTOFF (for buyers who already have them). */
(function(){
  if(window.SUL_dev)return;
  var CUTOFF="2026-11-30",A="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ",DA="23456789ABCDEFGHJKMNPQRSTUVWXYZ";
  function norm(c){return String(c||"").toUpperCase().replace(/[^A-Z0-9]/g,"")}
  function id(){var d=null;try{d=localStorage.getItem("sul_dev")}catch(e){}
    if(!d||!/^[2-9A-HJKMNP-Z]{6}$/.test(d)){var r=new Uint8Array(6);crypto.getRandomValues(r);d="";for(var i=0;i<6;i++)d+=DA[r[i]%DA.length];try{localStorage.setItem("sul_dev",d)}catch(e){}}
    return d}
  function pad(n){return(n<10?"0":"")+n}
  function today(){var t=new Date();return t.getFullYear()+"-"+pad(t.getMonth()+1)+"-"+pad(t.getDate())}
  function mask(prod,dev){return crypto.subtle.digest("SHA-256",new TextEncoder().encode(prod+"|"+norm(dev).replace(/^D(?=[2-9A-Z]{6}$)/,"")+"|sulabham-v1")).then(function(h){return new Uint8Array(h)})}
  function check(s){var t=0;for(var i=0;i<s.length;i++)t+=A.indexOf(s[i])*(i+1);return A[t%36]}
  /* personal code -> master code (Promise). Returns "" when it cannot be a valid code here. */
  function resolve(typed,prod){var p=norm(typed);
    if(p.length===10&&check(p.slice(0,-1))===p.slice(-1)){var body=p.slice(0,-1);
      return mask(prod,id()).then(function(k){var m="";for(var i=0;i<body.length;i++)m+=A[(A.indexOf(body[i])-k[i]%36+36)%36];return m})}
    return Promise.resolve(today()<=CUTOFF?p:"")}
  /* master + device -> personal code (used by the owner's code maker) */
  function make(master,prod,dev){var m=norm(master);
    return mask(prod,dev).then(function(k){var b="";for(var i=0;i<m.length;i++)b+=A[(A.indexOf(m[i])+k[i]%36)%36];var c=b+check(b);return c.replace(/(.{5})(?=.)/g,"$1-")})}
  window.SUL_dev={id:id,resolve:resolve,make:make,cutoff:CUTOFF};
  /* show the device number next to every unlock box */
  function show(){var f=document.getElementById("codeForm");if(!f||document.getElementById("devNo"))return;
    var te=document.documentElement.lang==="te",p=document.createElement("p");p.id="devNo";
    p.style.cssText="margin:8px 0 0;font-size:.85rem;background:var(--pasupu-soft,#fff3cf);border:1px dashed var(--pasupu,#e3a400);border-radius:10px;padding:7px 10px";
    p.innerHTML=(te?"మీ పరికరం నంబర్: ":"Your device number: ")+'<b style="font-family:monospace;font-size:1.05rem;letter-spacing:.08em">D-'+id()+'</b> <button type="button" data-copydev style="margin-left:6px;font:inherit;font-size:.8rem;border:1px solid #c98f00;background:#fff;border-radius:8px;padding:2px 9px;cursor:pointer">'+(te?"కాపీ":"Copy")+'</button> <a href="device.html" style="font-size:.8rem;margin-left:4px">'+(te?"పూర్తి పేజీ":"open")+'</a><br><small>'+(te?"చెల్లింపు స్క్రీన్‌షాట్‌తో పాటు ఈ నంబర్ పంపండి. మీ కోడ్ ఈ ఫోన్‌లో మాత్రమే పనిచేస్తుంది.":"Send this number with your payment screenshot. Your code will work on this phone only.")+'</small>';
    f.parentNode.insertBefore(p,f)}
  function tick(){show();var p=document.getElementById("devNo"),te=document.documentElement.lang==="te";if(p&&p.getAttribute("data-l")!==String(te)){p.remove();show();var q=document.getElementById("devNo");if(q)q.setAttribute("data-l",String(te))}}
  /* make the device number easy to send: copy button, UPI note, ready Telegram message */
  function isTe(){return document.documentElement.lang==="te"}
  function toast(m){var t=document.getElementById("sulToast");if(!t){t=document.createElement("div");t.id="sulToast";
    t.style.cssText="position:fixed;left:12px;right:12px;bottom:84px;z-index:99999;max-width:520px;margin:0 auto;background:#14212b;color:#fff;border-radius:12px;padding:12px 14px;font:15px/1.4 sans-serif;box-shadow:0 8px 24px rgba(0,0,0,.3);text-align:center";
    document.body.appendChild(t)}t.innerHTML=m;t.style.display="block";clearTimeout(t._h);t._h=setTimeout(function(){t.style.display="none"},6000)}
  function copy(s){try{if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(s);return true}}catch(e){}
    try{var a=document.createElement("textarea");a.value=s;a.style.position="fixed";a.style.opacity="0";document.body.appendChild(a);a.select();var ok=document.execCommand("copy");a.remove();return ok}catch(e){return false}}
  function prodName(){var d=document.querySelector("dialog[open] h2, dialog[open] h3, [role=dialog] h2, #dlgT");return d&&d.textContent?d.textContent.replace(/\s+/g," ").trim().slice(0,60):document.title.split("·")[0].trim()}
  function msg(){var D="D-"+id();return(isTe()?"చెల్లింపు చేశాను ✅\nప్యాక్: ":"Payment done ✅\nPack: ")+prodName()+(isTe()?"\nపరికరం నంబర్: ":"\nDevice number: ")+D+(isTe()?"\n(స్క్రీన్‌షాట్ జత చేశాను)":"\n(screenshot attached)")}
  document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("a[href]");
    var c=e.target.closest&&e.target.closest("[data-copydev]");
    if(c){e.preventDefault();copy("D-"+id());c.textContent=isTe()?"కాపీ అయింది ✓":"Copied ✓";return}
    if(!a)return;var h=a.getAttribute("href")||"",D="D-"+id();
    if(/^upi:/i.test(h)){var tn=/[?&]tn=([^&]*)/.exec(h),cur=tn?decodeURIComponent(tn[1].replace(/\+/g," ")):"Sulabham";
      if(cur.indexOf(D)<0){var nt=encodeURIComponent((cur+" "+D).slice(0,50));a.setAttribute("href",tn?h.replace(/([?&]tn=)[^&]*/,"$1"+nt):h+(h.indexOf("?")<0?"?":"&")+"tn="+nt)}
      copy(D);toast((isTe()?"మీ పరికరం నంబర్ <b>":"Your device number <b>")+D+(isTe()?"</b> చెల్లింపు నోట్‌లో చేరింది, కాపీ కూడా అయింది. చెల్లించాక స్క్రీన్‌షాట్‌తో పాటు పంపండి.":"</b> is added to the payment note and copied. After paying, send it with your screenshot."));return}
    if(/^https:\/\/(t\.me|telegram\.me|wa\.me|api\.whatsapp\.com)\//i.test(h)&&(document.getElementById("devNo")||document.querySelector("dialog[open]")||/pack|unlock|ca\.html|prelims|aee|dsc/i.test(location.pathname))){
      copy(msg());toast(isTe()?"సందేశం కాపీ అయింది (పరికరం నంబర్ <b>"+D+"</b> తో). టెలిగ్రామ్‌లో పేస్ట్ చేసి, స్క్రీన్‌షాట్ జత చేసి పంపండి.":"Message copied with your device number <b>"+D+"</b>. In Telegram, paste it, attach the screenshot and send.")}
  },true);
  if(document.readyState!=="loading")tick();else document.addEventListener("DOMContentLoaded",tick);
  new MutationObserver(function(){tick()}).observe(document.documentElement,{subtree:true,childList:true,attributes:true,attributeFilter:["lang"]});
})();
