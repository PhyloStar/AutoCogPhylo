# Datasets in our Sample

The datasets are produced with the following commands:

```shell
$ python check-data.py aa cutout 180 write coverage
$ python check-data.py an cutout 175 write coverage
$ python check-data.py ie cutout 180 write coverage
$ python check-data.py pn cutout 160 write coverage
$ python check-data.py st cutout 100 write coverage
```

The code cleans the datasets by replacing certain bad characters (unicode lookalikes, etc.) and selecting only those languages with the required coverage. The initial requirement for the coverage is the "cutout" parameter, namely all languages which have counterparts for less than the given number of concepts will be disregarded.

The following table shows the current statistics for the selected data:

Dataset | Family | Taxa | Concepts | Concept Coverage | Minimal Mutual Coverage | Average Mutual Coverage
---     | ---    | ---  | ---      | ---              | ---                     | ---
aa-58-200 | Austro-Asiatic | 58 | 200 | 0.95 | 163 | 180
an-45-210 | Austronesian | 45 | 210 | 0.88 | 144 | 165 
ie-42-208 | Indo-European | 42 | 208 | 0.97 | 161 | 197 
pn-67-183 | Pama-Nyungan | 67 | 183 | 0.94 | 141 | 163 
st-64-110 | Sino-Tibetan | 64 | 110 | 0.96 | 90 | 101

