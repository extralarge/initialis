import { fontInfo } from '../render/src/fonts.js?v=islands-1';

export const LATIN = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
export const CYRILLIC = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ';
export const isInitial = text => /^[A-ZА-ЩЭЮЯЁ]$/u.test(text || '');
export const supportsText = (font, text) => !!font && [...text].every(ch => (font.characters || LATIN).includes(ch));
export const alphabetLetters = alphabet => alphabet === 'latin' ? LATIN : CYRILLIC;
export const lettersForFont = (fonts, id) => alphabetLetters(fonts.find(f => f.id === id)?.alphabet || 'cyrillic');

// Stylistic alternatives; the original Latin fonts are kept unchanged.
const ALTERNATIVES = {
    cinzel: 'lighthaus-400', marcellus: 'lighthaus-400', 'luxurious-roman': 'lighthaus-400',
    'cinzel-decorative': 'foglihten-no06-400', 'almendra-display': 'foglihten-no06-400',
    'uncial-antiqua': 'sinistre-400', medievalsharp: 'sinistre-400', metamorphous: 'sinistre-700',
    unifrakturmaguntia: 'saint-400', unifrakturcook: 'saint-400', fruktur: 'saint-400',
    'pirata-one': 'saint-400', 'grenze-gotisch': 'saint-400', 'germania-one': 'saint-400',
    'elsie-swash-caps': 'oi-400', rye: 'oi-400', monoton: 'lack-line-400',
    'pinyon-script': 'great-vibes-400', 'monsieur-la-doulaise': 'great-vibes-400',
    'mea-culpa': 'great-vibes-400', ballet: 'great-vibes-400', 'herr-von-muellerhoff': 'great-vibes-400',
    'macondo-swash-caps': 'dispater-400', 'berkshire-swash': 'dispater-500',
};

export function fontForText(id, text, fonts) {
    const pool = fonts.filter(f => supportsText(f, text));
    if (!pool.length) return id;
    if (pool.some(f => f.id === id)) return id;
    const slug = id.replace(/-\d+$/, '');
    const preferred = id.startsWith('init-') ? 'dispater-400' : ALTERNATIVES[slug];
    if (pool.some(f => f.id === preferred)) return preferred;
    const group = fontInfo(id)?.group;
    return (pool.find(f => f.group === group) || pool.find(f => f.id === 'cormorant-garamond-700') || pool[0]).id;
}
