# BaseMountRetrieve
Package for retrieving files from BaseMount in the output style of a local MiSeq run.

### Requirements
- [BaseMount](https://basemount.basespace.illumina.com/)
- Python 3.6

### Installation
`pip install basemountretrieve`

### Usage
```
Usage: basemountretrieve [OPTIONS]

Options:
  -p, --projectdir PATH  Path to the directory on BaseMount for a particular
                         project. e.g. basemount/Projects/[your project].
  -o, --outdir PATH      Directory to dump all runs for project [required]
  --version              Specify this flag to print the version and exit.
  --help                 Show this message and exit.

```