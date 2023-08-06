# Polt

Live data visualisation via Matplotlib

[![pipeline status](https://gitlab.com/nobodyinperson/python3-polt/badges/master/pipeline.svg)](https://gitlab.com/nobodyinperson/python3-polt/commits/master)
[![coverage report](https://gitlab.com/nobodyinperson/python3-polt/badges/master/coverage.svg)](https://nobodyinperson.gitlab.io/python3-polt/coverage-report/)
[![documentation](https://img.shields.io/badge/docs-sphinx-brightgreen.svg)](https://nobodyinperson.gitlab.io/python3-polt/)
[![PyPI](https://badge.fury.io/py/polt.svg)](https://badge.fury.io/py/polt)

`polt` is a Python package for live data visualisation via
[Matplotlib](https://matplotlib.org/).

## What can `polt` do?

### Reading Numbers from STDIN

```bash
for i in `seq 1 100`;do echo $i;sleep $i;done | python3 -m polt
```

![polt-seq-stdin](/uploads/350329ce9a9045bcc0486e73405f4d64/polt-seq-stdin.png)

### Reading Numbers from Arbitrary Processes

```bash
python3 -m polt --source "cat /dev/urandom"
```

![Bildschirmfoto_2018-12-20_17-55-03](/uploads/047cf1c045ea5a5475e92a4b8b50ab4d/Bildschirmfoto_2018-12-20_17-55-03.png)


## Why on Earth is it called `polt` and not `plot`!?

I am a big fan of swapping syllables or characters around resulting in 
ridiculously-sounding words. `polt` is one of those words which I am generating 
quite frequently when typing quickly.

## Installation

The `polt` package is best installed via `pip`. Run from anywhere:

```bash
python3 -m pip install --user polt
```

This downloads and installs the package from the [Python Package
Index](https://pypi.org).

You may also install `polt` from the repository root:

```bash
python3 -m pip install --user .
```

## Documentation

Documentation of the `polt` package can be found [here on
GitLab](https://nobodyinperson.gitlab.io/python3-polt/).

Also, the command-line help page `python3 -m polt -h` is your friend.
