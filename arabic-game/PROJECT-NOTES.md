# هيّا نلعب — Arabic lesson games (nal3ab.pages.dev)

Smart-board games for a 2nd-grade Arabic class (Abdallah's mother is the teacher).
Everything is in Arabic, right-to-left, big touch targets, works offline.

## Where things live
- **Live site:** https://nal3ab.pages.dev — Cloudflare Pages project `nal3ab`, connected to
  GitHub repo `boudiahdab2003-art/reader`, production branch `claude/arabic-lesson-game-191kzn`,
  build command: none, build output directory: `arabic-game`. A push to that branch deploys in ~30 s.
- **Source:** `arabic-game/game.html` (edit this one; also published as a claude.ai artifact).
- **Built page:** `arabic-game/index.html` — never edit by hand. Rebuild with
  `python3 tools/build-game.py` (inlines fonts from `tools/fonts-inline.css`, adds old-browser
  CSS fallbacks, offline service worker registration, error box, link-preview tags).
- **Offline:** `arabic-game/sw.js` (cache name `nal3ab-v1`), `manifest.webmanifest`, `icon.svg`.
- `main` branch is a different project (redirect to qari.pages.dev) — do not touch it.

## Rules for changes
- Content must come from the lesson pages the teacher sent (scanned textbook PDFs). New phrases
  are fine when asked, built from the lesson's words; in ق/ك pairs the wrong spelling must not be
  a real Arabic word.
- Keep the JavaScript plain ES5 (the smart board browser may be old): check with
  `npx acorn --ecma5` on the script. No external scripts or fonts on the built page.
- Test before pushing (headless Chromium via Playwright is available in the cloud container).

## Lessons in the game
1. قواعد – الدرس الأول: الفقرة والجملة والكلمة (book p. 96–98)
2. قواعد – الدرس الثاني: الكلمة والحروف الهجائية (p. 102, alphabet picture chart)
3. إملاء – الدرس الأول: الحرفان المتقاربان في النطق ق – ك (p. 100–101, plus extra phrases)

## Games (id → name)
det مُحقّق الفقرة · count عُدّ الكلمات · isit جملة أم لا؟ · order رتّب الجملة · fill أكمل القاعدة ·
tf صواب أم خطأ · what ما هذا؟ · build ابنِ الكلمة · letter الحرف الأول · qkword أيّ كلمة صحيحة؟ ·
qkletter ق أم ك؟ · hunt صيّاد الحروف · pos أين الحرف؟ · shape شكل الحرف · qkbig تحدّي ق و ك ·
match صِل بخط · mcq اختر الجواب · big التحدّي الكبير

Features: tree mascot that grows apples, two teams (النجوم / الأقمار), game wheel, one sticker
per game (saved per device), hint button, drag-and-drop or tap, read-aloud if an Arabic voice exists,
review of weak rules at the end of each game.

## Adding a lesson
Add the data arrays and a renderer `R.<type>` in `game.html`, add the games to `GAMES` with a
new `les` number, add the section to `LES` and to the section order in `home()`, give each game a
`st` sticker and `wh` wheel emoji, rebuild, test, push.
