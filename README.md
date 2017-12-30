# AutoCogPhylo
Repository for testing how good Bayesian phylogenetic algorithms fare with automated vs gold cognate judgments

# Requirements

- lingpy >= 2.6.1

# Preparing the Data

To prepare the data, we offer further instructions in the file `data.md`, where you can find more information on how we cleaned and converted the data to our formats.

# Preparing the LingPy-Analyses

LingPy analyses were created using four separate scripts:

- `turchin.py`: computes the turchin (consonant-class matching approach) analysis (see Turchin et al. 2010)
- `sca.py`: computes the cognates based on SCA distances (List 2012)
- `edit-dist.py`: computes cognates based on (normalized) edit-distance (Levenshtein 1965)
- `lexstat.py`: computes the lexstat-infomap (List et al. 2017) distances

# Generating nexus files

> python3 online_pmi.py data/IELex-2016.tsv.asjp ielex_pmi

> python3 ldn_cluster.py data/IELex-2016.tsv.asjp ielex_ldn
