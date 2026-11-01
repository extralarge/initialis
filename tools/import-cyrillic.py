"""Extract capitals without shipping complete fonts.

uv run --with fonttools --with brotli python tools/import-cyrillic.py SOURCE_DIRECTORY
The directory contains the original font files named in FACES below.
Existing Latin outlines are preserved when extending a bundled face.
"""
import json
import sys
from pathlib import Path

from fontTools.pens.basePen import BasePen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from fontTools.varLib.instancer import instantiateVariableFont

ROOT = Path(__file__).resolve().parents[1]
LATIN = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
CYRILLIC = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'
# slug, family, file, renderer group, (manifest weight, source weight), source
FACES = [
    ('cormorant-garamond', 'Cormorant Garamond', 'cormorantgaramond.ttf', 'roman', [(500, 500), (700, 700)], 'https://github.com/google/fonts/tree/main/ofl/cormorantgaramond'),
    ('eb-garamond', 'EB Garamond', 'ebgaramond.ttf', 'roman', [(400, 400), (700, 700)], 'https://github.com/google/fonts/tree/main/ofl/ebgaramond'),
    ('forum', 'Forum', 'forum.ttf', 'roman', [(400, 400)], 'https://github.com/google/fonts/tree/main/ofl/forum'),
    ('playfair-display', 'Playfair Display', 'playfairdisplay.ttf', 'didone', [(400, 400), (900, 900)], 'https://github.com/google/fonts/tree/main/ofl/playfairdisplay'),
    ('great-vibes', 'Great Vibes', 'greatvibes.ttf', 'script', [(400, 400)], 'https://github.com/google/fonts/tree/main/ofl/greatvibes'),
    ('poiret-one', 'Poiret One', 'poiretone.ttf', 'deco', [(400, 400)], 'https://github.com/google/fonts/tree/main/ofl/poiretone'),
    ('lighthaus', 'Lighthaus', 'Lighthaus-Regular.otf', 'roman', [(400, 400)], 'https://www.typedump.com/font/lighthaus'),
    ('foglihten-no06', 'Foglihten No.06', 'FoglihtenNo06_076.otf', 'swash', [(400, 400)], 'https://www.glukfonts.pl/font.php?font=FoglihtenNo06'),
    ('dispater', 'Dispater', 'Dispater-VF.woff2', 'swash', [(400, 400), (500, 500), (600, 600), (700, 700)], 'https://www.typedump.com/font/dispater'),
    ('sinistre', 'Sinistre', 'SinistreVF.woff2', 'uncial', [(400, 72), (700, 142), (900, 200)], 'https://www.typedump.com/font/sinistre'),
    ('saint', 'Saint', 'Saint Regular.woff2', 'blackletter', [(400, 400)], 'https://www.typedump.com/font/saint'),
    ('lack-line', 'Lack Line', 'LackLine-Regular.woff2', 'deco', [(400, 400)], 'https://www.typedump.com/font/lack-line'),
    ('oi', 'Oi', 'Oi-Regular.woff2', 'didone', [(400, 400)], 'https://www.typedump.com/font/oi'),
]


FACES += [('spectral', 'Spectral', f'Spectral-{style}.ttf', 'roman', [(weight, weight)], 'https://github.com/google/fonts/tree/main/ofl/spectral') for weight, style in [(200, 'ExtraLight'), (300, 'Light'), (400, 'Regular'), (500, 'Medium'), (600, 'SemiBold'), (700, 'Bold'), (800, 'ExtraBold')]]

class CapsPen(BasePen):
    """Only M/L/Q/C/Z: exactly the subset read by render/src/fonts.js."""
    def __init__(self, glyph_set):
        super().__init__(glyph_set)
        self.parts = []

    def emit(self, command, *points):
        self.parts.append(command + ' '.join(format(round(n, 3), 'g') for p in points for n in p))

    def _moveTo(self, p): self.emit('M', p)
    def _lineTo(self, p): self.emit('L', p)
    def _qCurveToOne(self, a, b): self.emit('Q', a, b)
    def _curveToOne(self, a, b, c): self.emit('C', a, b, c)
    def _closePath(self): self.parts.append('Z')
    def _endPath(self): self.parts.append('Z')


def main(source_dir):
    manifest_path = ROOT / 'render/fonts/base/manifest.json'
    manifest = json.loads(manifest_path.read_text())
    report = []
    for slug, name, filename, group, weights, source in FACES:
        original = TTFont(source_dir / filename)
        entry = next((f for f in manifest if f['slug'] == slug), None)
        if entry is None:
            license_name = {'lighthaus': 'Free (TypeDump)', 'saint': 'Free for commercial use (attribution)'}.get(slug, 'OFL')
            entry = dict(slug=slug, name=name, group=group, note='Cyrillic addition; selected through TypeDump', license=license_name, files={}, caps=True, source=source)
            manifest.append(entry)
        entry['characters'] = LATIN + CYRILLIC
        for weight, axis_weight in weights:
            font = instantiateVariableFont(original, {'wght': axis_weight}, inplace=False) if 'fvar' in original else original
            glyph_set, cmap = font.getGlyphSet(), font.getBestCmap()
            missing = ''.join(c for c in LATIN + CYRILLIC if ord(c) not in cmap)
            if missing:
                raise ValueError(f'{name} {weight} lacks {missing}')
            path = ROOT / f'render/fonts/caps/{slug}-{weight}.json'
            caps = json.loads(path.read_text()) if path.exists() else {'upm': font['head'].unitsPerEm}
            for char in LATIN + CYRILLIC:
                if char in caps: continue
                glyph = glyph_set[cmap[ord(char)]]
                pen = CapsPen(glyph_set)
                glyph.draw(TransformPen(pen, (1, 0, 0, -1, 0, 0)))
                if not pen.parts: raise ValueError(f'{name}: empty {char}')
                caps[char] = [glyph.width, ''.join(pen.parts)]
            path.write_text(json.dumps(caps, ensure_ascii=False, separators=(',', ':')) + '\n')
            entry['files'][str(weight)] = f'{slug}-{weight}.ttf'
            report.append(dict(font=f'{slug}-{weight}', characters=LATIN + CYRILLIC, source=source, sourceWeight=axis_weight))
        print(name, len(weights), 'weights; all 33 Russian capitals')
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    (ROOT / 'render/fonts/cyrillic-sources.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(f'{len(report)} faces ready')


if __name__ == '__main__':
    main(Path(sys.argv[1]))
