# Initialis: Cyrillic extension

An extension of [Azlen's Initialis](https://github.com/azlen/initialis), retaining the original engine, interface and styles with their credits. This fork adds Russian capitals and reading passages; the original engine and styles remain credited to Azlen Elza. Deployment is managed separately by the owner.

## Run

On macOS, run `start.command` (requires Python 3). It starts a local static server and opens the page in your browser. Close its Terminal window to stop it. Alternatively, run `python3 -m http.server 8000` from this directory and open http://localhost:8000. WebGL2 in workers is required.

The default field uses Cyrillic. Separate paper controls select the alphabet, a particular face or all faces, and a fixed letter; these controls hide in reading mode. Clear Letter to return to random letters. Typing a Latin or Russian letter outside a form control also fixes the field to it. Changing the alphabet or typeface starts a new field; bookmarks remain in the browser. Original Latin faces remain available under A–Z.

## Added coverage

All 28 faces below contain all 33 Russian capitals, including Ё, plus A–Z. Original Latin outlines in the nine extended faces are preserved exactly.

| Family | Weights | Origin |
|---|---|---|
| Cormorant Garamond | 500, 700 | Google Fonts, OFL |
| EB Garamond | 400, 700 | Google Fonts, OFL |
| Forum | 400 | Google Fonts, OFL |
| Playfair Display | 400, 900 | Google Fonts, OFL |
| Great Vibes | 400 | Google Fonts, OFL |
| Poiret One | 400 | Google Fonts, OFL |
| Spectral — Production Type | 200, 300, 400, 500, 600, 700, 800 | Google Fonts, OFL |
| Lighthaus — Jerak Durzan | 400 | TypeDump, listed as Free |
| Foglihten No.06 — gluk | 400 | Author download, OFL |
| Dispater — Liubov Volkova; art direction Dmitry Goloub | 400, 500, 600, 700 | TypeDump, OFL |
| Sinistre — Collletttivo | Regular, Bold, Dark | TypeDump package, OFL |
| Saint — Liza Dushnota, Saint Agency | 400 | TypeDump package, free use with attribution |
| Lack Line — Adrien Midzic / Velvetyne | 400 | TypeDump package, OFL |
| Oi — Kostas Bartsokas | 400 | TypeDump package, OFL |

Sinistre's native variable-axis positions 72 / 142 / 200 are represented by IDs 400 / 700 / 900 to match the renderer's label convention. Dispater's four instances use its native weight values. Only capital outlines are needed at runtime, not complete font files. `render/fonts/cyrillic-sources.json` records the sources and axis positions; `render/fonts/licenses/` preserves available notices and licensing references.

Saint and Lighthaus retain their own terms and author credits. Saint's free release is documented by its authors on Behance; Lighthaus is listed as free by TypeDump. Complete outline-redistribution terms were not found in the available downloads. See `render/fonts/licenses/FREE-FONTS.md` for exact sources and limitations; neither is represented as OFL or MIT.

Stylistic substitutions are explicit in `src/alphabets.js`: e.g. Cinzel → Lighthaus, Uncial Antiqua → Sinistre, blackletter → Saint, decorative initials → Dispater. These are alternatives, not Cyrillic versions of those original designs. Random generation also samples the whole active catalogue. Bookmarked/shared originals retain their own font settings; typing an unsupported letter chooses a compatible face.

## Scope

The engine, paper, ornaments, PNG/animation downloads, bookmarks and sharing remain Initialis features. Links encode Unicode settings. The book-page context now includes 30 selected Russian passages, Cyrillic EB Garamond body text and Russian hyphenation. The original page-setting geometry and typography are retained. Both the WebGPU aged sheet and the WebGL flat-page fallback choose the passage by the actual initial ; author, title and source links are retained in the passage data. Random Cyrillic initials exclude Ъ, Ы and Ь. Latin pages retain their original texts and ET Book. Collection and individual exports include the actual selected Cyrillic font and letter.

## Rebuild outlines

`uv run --with fonttools --with brotli python tools/import-cyrillic.py SOURCE_DIRECTORY`

Supply the source font files named in the script. It checks coverage, freezes variable fonts, decomposes glyph components, flips font coordinates to the renderer's downward Y axis and emits only M/L/Q/C/Z paths. All runtime assets are already included; no build or npm install is needed to use this copy.


## Reading-page corrections

Original PAGE type settings, measure, margins, drop-cap placement and line-setting rules are retained; only Unicode word recognition and nonbreaking-space handling extend the line setter. One-letter Russian words are followed by NBSP. Excerpts now generally contain about 5,000 characters (complete shorter texts retain their natural length). Long source paragraphs may be divided at existing sentence boundaries for the fixed page engine; no words are changed. The added fixed source-credit panel and forced flat-preview mode have been removed.

The extra 40% random face override was removed. With the original Latin font pool, 1,000 wild initials and 1,000 children were verified identical to upstream for the same seeds. The intended additions are alphabet/font coverage, the Russian passage corpus, linked alphabet/Letter controls, and disabled context actions for unavailable passages.
