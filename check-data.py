from lingpy import *
from lingpy.compare.sanity import *
from collections import defaultdict
from itertools import combinations

def coverage_check(wordlist):
    # check mutual coverage
    for i in range(wl.height, 1, -1):
        if mutual_coverage_check(wl, i):
            print('mutual coverage is {0}'.format(i))
            break

def average_coverage(wordlist):
    sums, mins, maxs = [], ['?', 1], ['?', 0]
    for t in wordlist.cols:
        concepts = set(wl.get_list(col=t, entry='concept', flat=True))
        score = len(concepts) / wl.height
        sums += [score]
        if score < mins[1]:
            mins = t, score
        if score > maxs[1]:
            maxs = t, score
    print(sum(sums) / len(sums), mins[0], mins[1], maxs[0], maxs[1])


def average_mutual_coverage(wordlist):
    mc = mutual_coverage(wordlist)
    combs = [(a, b) for a, b in combinations(wordlist.taxa, r=2)]
    return sum([mc[a][b] for a, b in combs]) / len(combs)


def load_wordlist(what):
    wl = Wordlist('data/'+{
            'an': 'ABVD_full.tsv.uniform',
            'aa': 'Austro-Asiatic-122.tsv.uniform',
            'ie': 'ielex.tsv.uniform',
            'st': 'sinotibetan-data.tsv',
            'pn': 'pny-red.tsv'
            }[what])
    return wl


def cutout(wordlist, when):
    """Remove languages from word list if their coverage is below a certain percentage
    
    Note
    ----
    Coverage hereby refers to the number of concepts for which a word in a
    given wordlist exist, thus the number of concepts for which there is
    minimally one translation.
    """
    D = {0: [c for c in wordlist.columns]}
    for t in wordlist.cols:
        concepts = len(set(wl.get_list(col=t, entry='concept', flat=True)))
        if concepts >= when:
            for idx in wl.get_list(col=t, flat=True):
                D[idx] = wl[idx]
    return Wordlist(D)


def clean_entry(tokens):

    cleaner = {
            "55": "",
            "ùː": "uː",
            "ù": "u",
            "û": "u",
            "ṉ": "n",
            "ûː": "u",
            "ûə": "u ə",
            "ûɛ": "u ɛ",
            "ùə": "u ə",
            "ŕ": "r",
            "ḿ": "m",
            "ùa": "u a",
            "ǹ": "n",
            "ĺ": "l",
            "⁶": "",
            "⁷": "",
            "⁸": "",
            "ɩ": "ɿ",
            "ư": "u",
            "ợ": "o",
            "ố": "o",
            "ế": "e",
            "ậ": "a",
            "ấ": "a",
            "ụ": "u",
            "ắ": "a",
            "ơ": "o",
            "ứ": "u",
            "ỡ": "õ",
            "ạ": "a",
            "ả": "a",
            "ộ": "o",
            "ử": "u",
            "ị": "j",
            "ỏ": "o",
            "ặ": "a",
            "ừ": "u",
            "ẹ": "e",
            "ề": "e",
            "ồ": "o",
            "ệ": "e",
            "ầ": "a",
            "ổ": "o",
            "ớ": "o",
            "ẻ": "e",
            "ờ": "o",
            "ễ": "e",
            "ọ": "o",
            "ở": "o",
            "ủ": "u",
            "ә": "ə",
            "L": "l",
            "/": "",
            '=': '',
            "ý": "y",
            "ýo": "yo",
            "ýːe": "yː e",
            "ù̯": "u",
            "ýɔː": "y ɔ",
            "ýː": "yː",
            "ȃː": "aː",
            "ỳː": "yː",
            "ỳ": "y",
            "ýːœ": "yː œ",
            "ỳ:": "yː",
            "?": "",
            "ˈǔ": "ˈu",
            "ˈû": "ˈu",
            "ǔː": "uː",
            "ǔ": "u",
            "ˈǔː": "ˈuː",
            "ù:": "uː",
            "ˈùː": "ˈuː", 
            "?/ʔ": "ʔ",
            "Ḏ/ð": "ð",
            "&/e": "e"
            }
    return [cleaner.get(x, x) for x in tokens]


def check_tokens(wordlist):
    """
    Check the segmented sounds in the wordlist and see whether they are accepted by LingPy
    """
    errors = defaultdict(int)
    langs = []
    for idx, tokens in wordlist.iter_rows('tokens'):
        for a, b in zip(tokens, tokens2class(tokens, 'cv', cldf=True)):
            if b == '0':
                errors[a] += 1
    for k, v in errors.items():
        print(k, '\t', v)


def write_wordlist(wordlist, where):

    filename = 'data-{0}-{1}-{2}'.format(
            where, 
            str(wordlist.width).rjust(2, '0'), 
            str(wordlist.height).rjust(3, '0')
            )
    # add regular cognate identifiers for lingpy
    if 'cognate_class' in wordlist.header:
        wordlist.add_entries('cog', 'concept,cognate_class', lambda x, y:
                x[y[0]]+'-'+x[y[1]])
        wordlist.renumber('cog')
    else:
        wordlist.add_entries('cognate_class', 'concept,cogid', lambda x, y: 
                '{0}:{1}'.format(x[y[0]], x[y[1]]))

    # check for iso code or glotto code
    if not 'iso_code' in wordlist.header:
        isoc = 'glottocode'
    else:
        isoc = 'iso_code'
    cols = ['doculect', isoc, 'concept', 'concepticon_id', 'form', 'tokens', 'asjp', 'dolgo',
            'sca', 'cognate_class', 'cogid']

    if 'form' in wordlist.header:
        ipa = lambda x, y: x[y, 'form'] 
    elif 'ipa' in wordlist.header:
        ipa = lambda x, y: x[y, 'ipa']
    else:
        ipa = lambda x, y: ''.join(x[y, 'tokens'])

    D = {0: cols}
    errors = defaultdict(int)
    for idx in wordlist:
        form = ipa(wordlist, idx)
        cid = wordlist[idx, 'concepticon_id'] or ''
        d, iso, c, t, cc, cogid = (wordlist[idx, k] for k in [
            'doculect', isoc, 'concept', 'tokens', 'cognate_class',
            'cogid'])
        # we modify tokens by excluding all word boundary markers to allow for
        # a more consistent analysis, we also exclude the tones
        tks = []
        for t, cls in zip(clean_entry(t), tokens2class(clean_entry(t), 'cv')):
            if t:
                if cls == '0':
                    errors[t] += 1
                if cls in 'T_+0':
                    pass
                else:
                    tks += [t]
        tks = ' '.join(tks).split(' ')

        sca, dolgo, asjp = [' '.join(tokens2class(tks, x)) for x in ['sca', 'asjp', 'dolgo']]
        D[idx] = [d, iso, c, cid, form, tks, asjp, dolgo, sca,
                cc, cogid]
    Wordlist(D).output('tsv', filename='data/'+filename, ignore='all',
            prettify=False)
    if errors:
        for error, count in errors.items():
            print('!', error, count)
        print(sum(errors.values()))
    else:
        print('no errors found')

if __name__ == '__main__':

    from sys import argv
    wl = False
    for name in ['an', 'aa', 'ie', 'st', 'pn']:
        if name in argv:
            wl = load_wordlist(name)
            break

    if wl:
        if 'cutout' in argv:
            print(wl.width, wl.height)
            wl = cutout(wl, int(argv[argv.index('cutout')+1]))
            print(wl.width, wl.height)
        if 'coverage' in argv:
            coverage_check(wl)
            average_coverage(wl)
            check_tokens(wl)
            print('{0:.2f}'.format(average_mutual_coverage(wl)))
        if 'write' in argv:
            write_wordlist(wl, name)


