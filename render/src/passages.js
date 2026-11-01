const ROOT = new URL('../data/paragraphs.json?v=islands-1', import.meta.url);
let corpus = null, loaded = null;
export const isCyrillic = letter => /^[А-ЯЁ]$/u.test(letter || '');
export function loadPassages() {
 corpus ||= fetch(ROOT).then(r => { if (!r.ok) throw new Error('Passages could not be loaded'); return r.json(); }).then(data => (loaded = data));
 return corpus;
}
export const hasPassage = text => !!loaded && typeof text === 'string' && text.length === 1 && !!loaded[text]?.text?.startsWith(text);
export async function passageFor(letter) {
 await loadPassages();
 if (!hasPassage(letter)) throw new Error(`No passage for ${letter}`);
 return loaded[letter];
}
