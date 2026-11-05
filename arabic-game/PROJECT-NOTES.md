# هيّا نلعب — Arabic lesson games (nal3ab.pages.dev)

Smart-board games for Abdallah's mother's Arabic classes: **2nd, 3rd and 4th grade**.
The home page has a class switch (الصف الثاني / الثالث / الرابع); each class sees only its own
lessons, stickers and wheel. Direct links: nal3ab.pages.dev/#2, #3 and #4
(the chosen class is also remembered per device).
Everything is in Arabic, right-to-left, big touch targets, works offline.

## Where things live
- **Live site:** https://nal3ab.pages.dev — Cloudflare Pages project `nal3ab`, connected to
  GitHub repo `boudiahdab2003-art/reader`, production branch `claude/arabic-lesson-game-191kzn`,
  build command: none, build output directory: `arabic-game`. A push to that branch deploys in ~30 s.
- **Source:** `arabic-game/game.html` (edit this one; also published as a claude.ai artifact).
- **Built page:** `arabic-game/index.html` — never edit by hand. Rebuild with
  `python3 tools/build-game.py` (inlines fonts from `tools/fonts-inline.css`, adds old-browser
  CSS fallbacks, offline service worker registration, error box, link-preview tags).
- **Offline:** `arabic-game/sw.js` (cache name `nal3ab-v2`), `manifest.webmanifest`, `icon.svg`.
  The page is fetched **network-first** (saved copy only offline or after 3 s), so a normal
  release reaches everyone on their next visit — no cache bump needed.
  Pages left open (smart boards) also update: the built page carries a build fingerprint
  (`<meta name="nal3ab-build">`, made by build-game.py); every 5 min and whenever the tab is shown
  again it fetches the live page, and if the fingerprint changed it reloads — only on the home
  screen, never mid-game, and at most once per new build (sessionStorage guard). Bump `CACHE` only when
  `sw.js` itself changes: the new worker deletes the old cache and reloads open pages once.
- `main` branch is a different project (redirect to qari.pages.dev) — do not touch it.

## Rules for changes
- Content must come from the lesson pages the teacher sent (scanned textbook PDFs). New phrases
  are fine when asked, built from the lesson's words; in ق/ك pairs the wrong spelling must not be
  a real Arabic word.
- Keep the JavaScript plain ES5 (the smart board browser may be old): check with
  `npx acorn --ecma5` on the script. No external scripts or fonts on the built page.
- Test before pushing (headless Chromium via Playwright is available in the cloud container).

## Lessons in the game
Class 2 (`CLASSES[2].les = [1, 2, 4, 3]`):
1. قواعد – الدرس الأول: الفقرة والجملة والكلمة (book p. 96–98)
2. قواعد – الدرس الثاني: الكلمة والحروف الهجائية (p. 102, alphabet picture chart)
3. إملاء – الدرس الأول: الحرفان المتقاربان في النطق ق – ك (p. 100–101, plus extra phrases)
   (`les: 4`; `les: 3` is the review section)

Class 3 (`CLASSES[3].les = [5, 6]`):
5. قواعد: المذكَّر والمؤنَّث – worksheet (بطاقة عمل) by أستاذة نادين فرحات, December 2025,
   exercises 1–7. Masculine "things" are scarce on the sheet, so كتاب، قلم، بيت، درس were added.
   الفرس is used only in the pair game (the sheet uses it as feminine in ex. 2 but writes
   "فرسًا أبيضَ" in ex. 1). Small typos on the sheet were fixed in the game: لِيَقْطِفَ → لِتَقْطِفَ,
   استيقظُ → اِسْتَيْقَظَ.
6. نصّ: الدّيك الشُّجاع (Kamal Al-Shartouni), three paragraphs, from a photo of the book page.
   The word meanings come from the teacher's handwriting above the words
   (خمّ = بيت الدجاج، نقيق = صوت الدجاج، يجري = يحدث، يقفز = ينطّ، يعود = يرجع، تحوم = تلتفّ).
   The full text is also readable in a fold-out box under the section.

Class 4 (`CLASSES[4].les = [7, 8]`), book unit 3 «مَنِ السّارِقُ؟», scanned pages 113–117 (p. 116 = poem):
7. قواعد: الجمع وأنواعه – والمثنّى. Plurals from ex. 1–2 (p. 113: جمع مؤنث سالم / جمع تكسير lists),
   ex. 4 (p. 114: رُدّ إلى المفرد + نوع الجمع), ex. 5 (p. 115: sentences → مثنى and جمع), the table
   and ex. 7 on p. 117 (أنا تلميذ مجتهد → نحن/هي/أنتنّ). Left out as ambiguous: the half-cut word
   "…قعة" on p. 113, كشّاف and النشاط (in the تكسير list but not clearly تكسير), الرطبة/البسيطة.
   Accepted alternatives are named in the explanations (العمّال/العاملين, السيّاح/السائحون).
8. قصيدة: الطّائرة (p. 116), two stanzas, each ending with a refrain; the book's questions a/b
   (صوت الطائرة = الرعد, صدرها = داخل الطائرة) are always asked. Readable in a fold-out box.

## Games (id → name)
det مُحقّق الفقرة · count عُدّ الكلمات · isit جملة أم لا؟ · order رتّب الجملة · fill أكمل القاعدة ·
tf صواب أم خطأ · what ما هذا؟ · build ابنِ الكلمة · letter الحرف الأول · qkword أيّ كلمة صحيحة؟ ·
qkletter ق أم ك؟ · hunt صيّاد الحروف · pos أين الحرف؟ · shape شكل الحرف · qkbig تحدّي ق و ك ·
match صِل بخط · mcq اختر الجواب · big التحدّي الكبير

Class 3, lesson 5 (المذكّر والمؤنّث):
- nouns أين الأسماء؟ – tap the nouns in a sentence; each lights up as إنسان/حيوان/شيء
- sortn صنّف الاسم – the worksheet's 6-box table; the word is a small chip so it fits over one box
- mfg مذكّر أم مؤنّث؟ – always includes one feminine word without ة (الشمس، الريح، السماء، الأم)
- hdh هذا أم هذه؟ – exercise 3
- mfmatch صِل المؤنّث بالمذكّر – exercise 2 animal pairs
- mfwho مذكّره ومؤنّثه – "ما مؤنث الجمل؟" and the reverse
- conv حوّل الجملة – exercises 4–5; pick the right conversion, changed words highlighted
- mfbig تحدّي المذكّر والمؤنّث – 10 mixed questions

Class 3, lesson 6 (الدّيك الشُّجاع):
- story رتّب القصة – the puzzle: short sentence pieces, one round per paragraph part
  (7/6/5/3 pieces), then a 5-event round for the whole story; `R.order` with `parts`; rows and
  pieces sit side by side on wide screens so nothing is below the fold
- txtorder رتّب جمل النص – word-order sentences from the text
- txtfill أكمل النص – 1–2 missing words per sentence plus one extra word that does not belong,
  6 of 12 sentences in story order; `R.fill` with `prompt`
- txtmean صِل الكلمة بمعناها – the teacher's handwritten meanings
- txtq فهم النص – true/false then multiple choice, ending with "why is the rooster brave?"

Class 4, lesson 7 (الجمع والمثنّى):
- jtype ما نوع الجمع؟ – drag the plural onto one of 3 boxes; always one trick word
  (أوقات/أصوات = تكسير, منتجات/حيوانات/اختراعات = مؤنث سالم of a masculine singular); `R.jtype`
- jplural اجمع الكلمة – MCQ: right plural, its dual, and a wrong ending
- jsing رُدّ إلى المفرد – match plural ↔ singular
- jconv حوّل إلى المثنى والجمع – `R.conv` with a custom `dir` label
- jbig تحدّي الجمع
Class 4, lesson 8 (الطائرة): porder رتّب القصيدة (stanza puzzles, then whole poem), pfill أكمل
القصيدة, pq فهم القصيدة (passage shows the stanza: `PTXT.a1/a2` are arrays of lines), pjam جموع القصيدة.

Features: tree mascot that grows apples, two teams (النجوم / الأقمار), game wheel, one sticker
per game (saved per device), hint button, drag-and-drop or tap, read-aloud if an Arabic voice exists,
review of weak rules at the end of each game.

## Adding a lesson
Add the data arrays and a renderer `R.<type>` in `game.html` (or reuse one: `R.order` with
`parts` makes a story/sequence puzzle, `R.match`, `R.mcq`, `R.tf` with `ctx` for a passage), add the
games to `GAMES` with a new `les` number, add the section to `LES` and its number to the right
class in `CLASSES` (that sets the section order), give each game a title (in `TNAME` or `title:`),
a unique `st` sticker and a `wh` wheel emoji (old-board-safe emoji only, nothing newer than ~2016),
rebuild, test, push. Ask which class a new lesson is for if it is not on the sheet.

## Dragging
`dragify()` shrinks any big card around the finger while it is dragged (at most 300 px wide and
45% of the screen width), so a card always covers just one target. Keep that when adding drag games.

## Working with Abdallah
- He writes short requests ("release", "update memory", "split it more"). "Release" means push
  to `claude/arabic-lesson-game-191kzn` (that deploys the site). "Memory" means this file.
- He forwards his mother's material: scanned PDFs, worksheets, or phone photos of book pages
  (sometimes with her handwritten notes, e.g. word meanings — use them).
- Say which class a new lesson goes to; a 3rd-grade sheet says "الصف: الثالث الأساسي".
- Point out anything changed from the source (typos fixed, ambiguous words left out, words added).
- He likes visible, tested results: screenshots of the real page, a drag test, then release.

## Cloud session limits
- The session cannot open nal3ab.pages.dev (network policy), so a deploy cannot be checked from
  here; ask Abdallah to open it once to check.
- Bash heredocs that contain `$$` or `${...}` (Playwright scripts) can be refused by a safety check;
  write test scripts with the Write tool into the scratchpad and run them with `node`.

## Testing tips
- A quick check (open every game, answer one question, watch for page errors) is enough;
  random-clicking bots get stuck on the ordering/matching games, which is not a bug.
  Solve those properly instead: match by `data-i` (col a ↔ col b), and for story/order rounds
  read the right order from `game.html` and tap the bank tiles in that order.
- For drag problems, drag with `page.mouse` (down → move in steps → up) and check that the ghost
  is small, exactly one `.dz.over` lights up, and the drop lands on the aimed target — on a
  1280×860 "board" and a 390×844 phone. Reload with `about:blank` first: changing only `#2/#3`
  does not reload the page.
- Service-worker changes cannot be tested from `file://`: serve the folder on `localhost` with a
  small Node server and test with Playwright (old files → visit → swap in new files → reload).

## Change log
- Oct 2026: class 2 – lessons 1–3 (paragraph/sentence/word, alphabet, ق/ك) and the review.
- 5 Nov 2026: class 4 – plurals/dual (unit 3, p. 113–117) and the poem الطّائرة; open pages
  now check for a new version and reload on the home screen.
- Nov 2026: class switch; class 3 lesson 5 (المذكّر والمؤنّث worksheet) and lesson 6
  (الدّيك الشُّجاع: story puzzle, sentence order, fill the text, word meanings, comprehension);
  story puzzle split into short pieces; small word chip in صنّف الاسم; every drag game shrinks
  big cards while dragged; site switched to network-first (v2) because laptops that had used
  the site kept showing the old saved version.
