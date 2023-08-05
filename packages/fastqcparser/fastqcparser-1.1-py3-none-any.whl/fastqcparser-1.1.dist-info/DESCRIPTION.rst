# Welcome to fastqcparser

python API for parsing the output of `FastQC <https://www.bioinformatics.babraham.ac.uk/projects/fastqc/>`.

# Installation

1. Recomended way to install is using ``pip``

```
pip install fastqcparser
```

2. Alternatively you can install with ``easy_install``
::

```
easy_install fastqcparser
```

3. You can also install from Github source code.
::

```
cd
git clone http://bitbucket.org/bubioinformaticshub/fastqcparser.git
cd fastqcparser
python setup.py install
```

# Usage/lazy documentation

```python

# import fastqcparser
from pprint import pprint
from fastqcparser import FastQCParser

# load file
f = FastQCParser('/path/to/fastqc_output_file.txt')

# or
f = FastQCParser('/path/to/fastqc.zip')

# or
with open('/path/to/fastqc_data.txt') as fp :
    f = FastQCParser(fp)

# or
with FastQCParser('/path/to/fastqc_output_file.txt') as f :
    print(f)

# some convenience fields are available from the Basic Statistics module
print('\n'.join([
    f.filename,
    f.file_type,
    f.encoding,
    f.total_sequences,
    f.filtered_sequences,
    f.sequence_length,
    f.percent_gc
]))

# the available modules are in f.modules
pprint(list(f.modules.keys()))

#['Basic Statistics',
# 'Per base sequence quality',
# 'Per sequence quality scores',
# 'Per base sequence content',
# 'Per base GC content',
# 'Per sequence GC content',
# 'Per base N content',
# 'Sequence Length Distribution',
# 'Sequence Duplication Levels',
# 'Overrepresented sequences',
# 'Kmer Content']

# you can access an individual module either as a key of f.modules or using
# f itself:
pprint(f.modules['Basic Statistics'])
pprint(f['Basic Statistics'])

# each module contains a dictionary
pprint(f['Basic Statistics'])

#{'addnl': {},
# 'data': [['Filename', 'sample1.fastq'],
#          ['File type', 'Conventional base calls'],
#          ['Encoding', 'Sanger / Illumina 1.9'],
#          ['Total Sequences', 1571332],
#          ['Filtered Sequences', 0],
#          ['Sequence length', 29],
#          ['%GC', 53]],
# 'fieldnames': ['Measure', 'Value'],
# 'name': 'Basic Statistics',
# 'status': 'pass'}

# 'data' contains the tabular data from the module as a list of lists, with
# numerical values cast to ints and floats as appropriate

# 'fieldnames' contains the names of each column in 'data'

# 'name' is the name of the module, same as the key

# 'status' is pass/warn/fail as reported by fastqc

# 'addnl' contains extra fields for some modules
```


