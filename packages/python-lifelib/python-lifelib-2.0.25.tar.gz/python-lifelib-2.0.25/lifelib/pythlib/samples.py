import os

from collections import Sequence, defaultdict

class SampleSoupList(Sequence):

    def __init__(self, lt, rule, symmetry, samples):

        self.lt = lt
        self.rule = rule
        self.symmetry = symmetry
        self.samples = samples

    def __getitem__(self, i):
        return self.lt.hashsoup(self.rule, self.symmetry, self.samples[i])

    def __len__(self):
        return len(self.samples)

    def __repr__(self):
        return 'SampleSoupList(%r, %r, %r, %r)' % (self.lt, self.rule, self.symmetry, self.samples)

def download_samples(apgcode, rule, lt, domain='https://gol.hatsya.co.uk', tempfile='tempfile'):

    try:
        from urllib import urlretrieve
    except ImportError:
        from urllib.request import urlretrieve

    url = domain + '/textsamples/' + apgcode + '/' + rule
    urlretrieve(url, tempfile)

    samples = defaultdict(list)

    with open(tempfile, 'r') as f:
        for l in f:
            if '/' not in l:
                continue
            symmetry, seed = tuple(l.strip().split('/')[:2])
            if len(symmetry) > 50:
                continue
            samples[symmetry].append(seed)

    samples = {k : SampleSoupList(lt, rule, k, v) for (k, v) in samples.items()}
    return samples
