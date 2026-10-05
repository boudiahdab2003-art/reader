"""Builds arabic-game/index.html (the site at nal3ab.pages.dev) from arabic-game/game.html.

game.html is the source (also published as the claude.ai artifact). The built page
embeds its fonts, so it needs no internet, and registers sw.js for offline use.
Run from the repo root:  python3 tools/build-game.py
"""
import re

src = open("arabic-game/game.html", encoding="utf-8").read()
fonts = open("tools/fonts-inline.css", encoding="utf-8").read()

src = re.sub(r'<link rel="preconnect"[^>]*>\n', "", src)
src = re.sub(r'<link rel="stylesheet" href="https://fonts\.googleapis\.com[^>]*>\n', "<style>\n" + fonts + "\n</style>\n", src)
assert "googleapis" not in src and "gstatic" not in src

def split_args(t):
    out, depth, cur = [], 0, ""
    for ch in t:
        if ch == "(": depth += 1
        if ch == ")": depth -= 1
        if ch == "," and depth == 0:
            out.append(cur.strip()); cur = ""
        else:
            cur += ch
    out.append(cur.strip())
    return out

def old_value(v):
    # clamp(a,b,c) -> c and min(a,b) -> b: smart boards are big screens, so the large value fits
    while True:
        m = re.search(r"\b(clamp|min)\(", v)
        if not m: return v
        i, depth = m.end(), 1
        while depth:
            depth += {"(": 1, ")": -1}.get(v[i], 0); i += 1
        v = v[:m.start()] + split_args(v[m.end():i - 1])[-1] + v[i:]

def with_fallbacks(css):
    # older smart-board browsers drop declarations they do not understand; give each a plain twin first
    def decl(m):
        prop, val = m.group(1), m.group(2)
        extra = ""
        if re.search(r"\b(clamp|min)\(", val): extra += prop + ":" + old_value(val) + ";"
        if prop == "inset" and val.strip() == "0": extra += "top:0;right:0;bottom:0;left:0;"
        if prop == "padding-inline":
            a = val.split(); extra += "padding-right:" + a[0] + ";padding-left:" + a[-1] + ";"
        return extra + m.group(0)
    return re.sub(r"(?<=[{;])\s*([a-z-]+):([^;{}]+)", decl, css)

a = src.index("/* Layout:"); b = src.index("</style>", a)
src = src[:a] + with_fallbacks(src[a:b]) + src[b:]

compat = """
<style>
/* old browsers: flex gap and aspect-ratio */
.nogap .row>*,.nogap .opts>*,.nogap .bank>*,.nogap .lbank>*,.nogap .nums>*,.nogap .tools>*,.nogap .teams>*,.nogap .kinds>*,.nogap .tf>*,.nogap .sentence>*,.nogap .slots>*,.nogap .lslots>*,.nogap .para>*{margin:6px}
.nogap .wrap>*,.nogap .stage>*,.nogap .body>*,.nogap .sec>*,.nogap .grid>*{margin-bottom:16px}
@supports not (aspect-ratio:1){.stk{height:74px;width:74px}.wwrap{width:420px;height:420px}}
</style>
"""
head = """<!DOCTYPE html>
<html lang="ar" dir="rtl" translate="no">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<meta name="google" content="notranslate">
<meta name="description" content="ألعاب للصف الثاني على السبورة الذكية: الفقرة والجملة والكلمة، والحروف الهجائية.">
<meta property="og:title" content="هيّا نلعب! الفقرة والجملة والكلمة">
<meta property="og:description" content="ألعاب ممتعة لدرس الفقرة والجملة والكلمة والحروف الهجائية – للصف الثاني.">
<meta property="og:type" content="website">
<meta name="theme-color" content="#178a9c">
<link rel="icon" href="icon.svg" type="image/svg+xml">
<link rel="manifest" href="manifest.webmanifest">
<script>
window.onerror = function (msg, src, line) {
  var b = document.getElementById("errBox");
  if (!b && document.body) { b = document.createElement("div"); b.id = "errBox"; b.dir = "rtl"; b.style.cssText = "position:fixed;left:16px;right:16px;top:16px;z-index:99;background:#fde4df;color:#ad3826;border:3px solid #e2533f;border-radius:20px;padding:12px 18px;font:700 1.1rem Tahoma,sans-serif"; document.body.appendChild(b); }
  if (b) b.textContent = "حَدَثَتْ مُشْكِلَةٌ في الْمُتَصَفِّحِ. صَوِّروا هٰذِهِ الرِّسالَةَ: " + msg + " (" + line + ")";
};
</script>
"""
offline = """
<noscript><p style="font:700 1.5rem Tahoma,sans-serif;text-align:center;padding:40px">يَحْتاجُ هٰذا الْمَوْقِعُ إِلى تَشْغيلِ JavaScript في الْمُتَصَفِّحِ.</p></noscript>
<script>
(function () { var d = document.createElement("div"); d.style.cssText = "display:flex;flex-direction:column;row-gap:1px;position:absolute"; d.appendChild(document.createElement("div")); d.appendChild(document.createElement("div")); document.body.appendChild(d); if (d.scrollHeight !== 1) document.documentElement.className += " nogap"; d.parentNode.removeChild(d); })();
</script>
<div id="offlineNote" hidden style="position:fixed;left:16px;bottom:calc(16px + env(safe-area-inset-bottom,0px));z-index:30;background:#ffffff;color:#177548;border:3px solid #25a064;border-radius:999px;padding:6px 18px;font:800 1.05rem 'Baloo Bhaijaan 2',Tahoma,sans-serif;box-shadow:0 5px 0 #bcd6d9" dir="rtl">✓ اللُّعْبَةُ تَعْمَلُ بِدونِ إِنْتَرْنِت</div>
<script>
if ("serviceWorker" in navigator && (location.protocol === "https:" || location.hostname === "localhost")) {
  navigator.serviceWorker.register("sw.js").then(function () { return navigator.serviceWorker.ready; }).then(function () {
    var n = document.getElementById("offlineNote"); n.hidden = false;
    setTimeout(function () { n.hidden = true; }, 5000);
  }).catch(function () {});
}
</script>
"""
cut = src.index("</style>", src.index("/* Layout:")) + len("</style>")
out = head + src[:cut] + compat + "\n</head>\n<body>\n" + src[cut:].lstrip("\n") + offline + "</body>\n</html>\n"
open("arabic-game/index.html", "w", encoding="utf-8").write(out)
print("arabic-game/index.html", len(out.encode()) // 1024, "KB")
