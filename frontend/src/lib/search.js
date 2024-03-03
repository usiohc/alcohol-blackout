import Hangul from 'hangul-js';

export function search(searchQuery, array) {
    if (searchQuery) {
        const searchChosung = Hangul.disassemble(searchQuery).map(char => Hangul.isConsonant(char) ? char : '').join('');
        return array.filter(item => {
            const itemChosung = Hangul.disassemble(item.name_ko).map(char => Hangul.isConsonant(char) ? char : '').join('');
            return itemChosung.includes(searchChosung);
        });
    } else {
        return array;
    }
}