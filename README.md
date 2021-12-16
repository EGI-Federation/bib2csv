# bibe2csv (Convert `.bib` file to `.csv`)

This is a command-line application written in Python to convert a list of
publications in `.bib` to `.csv`.

EGI needs to provide the list of publications of several institutes as a
spreadsheet with few defined columns:

## __Output required__

|Author|Year|Title|Source|DOI|
|---|---|---|---|---|
|   |   |   |   |   |
|   |   |   |   |   |

This information can be downloaded as a `${filename}.bib` from websites like
[https://inspirehep.net/](https://inspirehep.net)
and
[https://ui.adsabs.harvard.edu/](https://ui.adsabs.harvard.edu/)
but they need to be converted and the list can be composed of a few thousand entries.
The script is built around the specific requirements converting and reordering just
the required fields and merging several others in the `Source` column.
It accepts incomplete tuples to avoid losing information.

## Install requirements

``` sh
pip install -r requirements.txt
```

Tested with `python3`

## Usage

For the helpline:

``` sh
./bib2csv -h
```

Use the following command to convert `${filename}.bib` to `${filename}.csv` :

``` sh
./bib2csv ${flename}.md
```

A file named `${filename}.csv` will be generated in the folder of the orignal file.

It is also possible to merge multiple input `${files}.bib` in the same output file,
with `-o`:

``` sh
./bib2csv ${flename1}.md ${flename2}.md -o $%{outputfile.csv}
```

To remove the first line containing the header specify the option `-H`,
will make the copy and paste quicker.
