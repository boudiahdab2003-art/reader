# هيّا نلعب — Arabic lesson games (nal3ab.pages.dev)

Smart-board games for Abdallah's mother's Arabic classes: **2nd grade and 3rd grade**.
The home page has a class switch (الصف الثاني / الصف الثالث); each class sees only its own
lessons, stickers and wheel. Direct links: nal3ab.pages.dev/#2 and nal3ab.pages.dev/#3
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

## Games (id → name)
det مُحقّق الفقرة · count عُدّ الكلمات · isit جملة أم لا؟ · order رتّب الجملة · fill أكمل القاعدة ·
tf صواب أم خطأ · what ما هذا؟ · build ابنِ الكلمة · letter الحرف الأول · qkword أيّ كلمة صحيحة؟ ·
qkletter ق أم ك؟ · hunt صيّاد الحروف · pos أين الحرف؟ · shape شكل الحرف · qkbig تحدّي ق و ك ·
match صِل بخط · mcq اختر الجواب · big التحدّي الكبير

Class 3: nouns أين الأسماء؟ (tap the nouns, coloured by إنسان/حيوان/شيء) · sortn صنّف الاسم
(the 6-box table; the word is a small chip so it fits over one box while dragged) · mfg مذكّر أم مؤنّث؟ · hdh هذا أم هذه؟ · mfmatch صِل المؤنّث بالمذكّر ·
mfwho مذكّره ومؤنّثه · conv حوّل الجملة (pick the right conversion, changed words highlighted) ·
mfbig تحدّي المذكّر والمؤنّث · story رتّب القصة (puzzle: short sentence pieces, one round per paragraph
part – 7/6/5/3 pieces – then a 5-event round for the whole story; uses `R.order` with `parts`; rows and pieces sit side by
side on wide screens so nothing is below the fold) · txtorder رتّب جمل النص · txtfill أكمل النص (1–2 missing words per
sentence plus one extra word, 6 sentences in story order; `R.fill` with `prompt`) · txtmean صِل الكلمة بمعناها ·
txtq فهم النص (true/false + questions)

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

## Testing tips
- A quick check (open every game, answer one question, watch for page errors) is enough;
  random-clicking bots get stuck on the ordering/matching games, which is not a bug.
- The service worker serves the cached page first and refreshes in the background, so after a
  deploy the smart board shows the new version from the second load.
