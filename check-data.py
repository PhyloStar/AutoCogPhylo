from lingpy import *
from lingpy.compare.sanity import *
from collections import defaultdict

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

def load_wordlist(what):
    wl = Wordlist('data/'+{
            'an': 'abvd_96.tsv.uniform',
            'aa': 'Austro-Asiatic-122.tsv.uniform',
            'ie': 'ielex.tsv.uniform',
            'st': 'sinotibetan-data.tsv',
            'pn': 'pny-red.tsv'
            }[what])
    return wl


def cutout(wordlist, when):
    """Remove languages from word list if their coverage is below a certain
    percentage"""
    D = {0: [c for c in wordlist.columns]}
    for t in wordlist.cols:
        concepts = len(set(wl.get_list(col=t, entry='concept', flat=True)))
        if concepts >= when:
            for idx in wl.get_list(col=t, flat=True):
                D[idx] = wl[idx]
    return Wordlist(D)

def check_tokens(wordlist):
    errors = defaultdict(int)

    for idx, tokens in wordlist.iter_rows('tokens'):
        for a, b in zip(tokens, tokens2class(tokens, 'cv', cldf=True)):
            if b == '0':
                errors[a] += 1
    print(len(errors), sum(errors.values()))
    for k, v in errors.items():
        print(k, '\t', v)


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


