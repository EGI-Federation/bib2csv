#!/usr/bin/python3
import argparse
import os
import string
import sys

from pybtex.database.input import bibtex

# dictionary of the journal abbreviations
journals = {
    "aj": "Astronomical Journal",
    "actaa": "Acta Astronomica",
    "araa": "Annual Review of Astron and Astrophys",
    "apj": "Astrophysical Journal",
    "apjl": "Astrophysical Journal, Letters",
    "apjs": "Astrophysical Journal, Supplement",
    "ao": "Applied Optics",
    "apss": "Astrophysics and Space Science",
    "aap": "Astronomy and Astrophysics",
    "aapr": "Astronomy and Astrophysics Reviews",
    "aaps": "Astronomy and Astrophysics, Supplement",
    "azh": "Astronomicheskii Zhurnal",
    "baas": "Bulletin of the AAS",
    "caa": "Chinese Astronomy and Astrophysics",
    "cjaa": "Chinese Journal of Astronomy and Astrophysics",
    "icarus": "Icarus",
    "jcap": "Journal of Cosmology and Astroparticle Physics",
    "jrasc": "Journal of the RAS of Canada",
    "memras": "Memoirs of the RAS",
    "mnras": "Monthly Notices of the RAS",
    "na": "New Astronomy",
    "nar": "New Astronomy Review",
    "pra": "Physical Review A: General Physics",
    "prb": "Physical Review B: Solid State",
    "prc": "Physical Review C",
    "prd": "Physical Review D",
    "pre": "Physical Review E",
    "prl": "Physical Review Letters",
    "pasa": "Publications of the Astron. Soc. of Australia",
    "pasp": "Publications of the ASP",
    "pasj": "Publications of the ASJ",
    "rmxaa": "Revista Mexicana de Astronomia y Astrofisica",
    "qjras": "Quarterly Journal of the RAS",
    "skytel": "Sky and Telescope",
    "solphys": "Solar Physics",
    "sovast": "Soviet Astronomy",
    "ssr": "Space Science Reviews",
    "zap": "Zeitschrift fuer Astrophysik",
    "nat": "Nature",
    "iaucirc": "IAU Cirulars",
    "aplett": "Astrophysics Letters",
    "apspr": "Astrophysics Space Physics Research",
    "bain": "Bulletin Astronomical Institute of the Netherlands",
    "fcp": "Fundamental Cosmic Physics",
    "gca": "Geochimica Cosmochimica Acta",
    "grl": "Geophysics Research Letters",
    "jcp": "Journal of Chemical Physics",
    "jgr": "Journal of Geophysics Research",
    "jqsrt": "Journal of Quantitiative Spectroscopy and Radiative Transfer",
    "memsai": "Mem. Societa Astronomica Italiana",
    "nphysa": "Nuclear Physics A",
    "physrep": "Physics Reports",
    "physscr": "Physica Scripta",
    "planss": "Planetary Space Science",
    "procspie": "Proceedings of the SPIE",
}


def bib2csv(bib_file, csv_file):
    # set the output filename
    # if csv_file == None:
    #     csv_file = os.path.splitext(bib_file)[0] + '.csv'
    f = open(csv_file, 'a')
    # check if bib input file exists
    if not os.path.isfile(bib_file):
        print('The file specified does not exist')
        sys.exit()

    if not args.headless:
        # header row: author, year, title, journal
        # comment it for easier cut & paste
        f.write("author\t year\t title\t journal\t doi\n")

    # translator for removing punctuation
    translator = str.maketrans('', '', string.punctuation)

    bib_parser = bibtex.Parser()

    # open a bibtex file, given as command line argument
    bib_data = bib_parser.parse_file(bib_file)

    # loop through the individual references
    # use a tab separator for each column
    for bib_id in bib_data.entries:
        b = bib_data.entries[bib_id].fields
        # Authors
        authors = ""
        # merge multiple authors
        if "author" in bib_data.entries[bib_id].persons:
            for author in bib_data.entries[bib_id].persons["author"]:
                new_author = str(author.first_names) + " " + str(author.last_names)
                new_author = new_author.translate(translator)
                if len(authors) == 0:
                    authors = '"' + new_author
                else:
                    authors = authors + ", " + new_author
            f.write(authors + '"')
        f.write(" \t")
        # Year
        if "year" in b:
            f.write(b["year"])
        f.write(" \t")
        # Title
        if "title" in b:
            # remove trailing brackets
            title = b["title"]
            f.write(title[1:-1])
        f.write(" \t")
        # Journal
        journal_tuple = []
        if "journal" in b:
            journal_name = b["journal"]
            # convert journal abbreviations
            if journal_name[0] == '\\':
                journal_name = journals[journal_name[1:]]
            journal_tuple.append(journal_name)
        # search for journal's related fields
        for item in ["volume", "number", "pages", "month"]:
            if item in b:
                journal_tuple.append(item[0] + ":" + b[item])
        # merge journal title and journal's related fields
        journal_cell = ", ".join(journal_tuple)
        journal_cell = '"' + journal_cell + '"'
        f.write(journal_cell)
        f.write(" \t")
        # Doi
        if "doi" in b:
            f.write(b["doi"])
        f.write("\n")
    # close output file
    f.close()


arg_parser = argparse.ArgumentParser(description="Covert '.bib' files into '.csv' files."
                                                 "Default output: same name and location of the 'bib' input file")
arg_parser.add_argument('bib_file', default="sample.bib", nargs='*',
                        help='file with .bib extension to convert')
arg_parser.add_argument('-o', '--output', nargs='?',
                        help="output file with '.bib' extension."
                             "If multiple input files are defined,"
                             "they will be merged into it.")
arg_parser.add_argument('-H', '--headless', action='store_true',
                        help='do not generate the first row with the headers')
args = arg_parser.parse_args()

first_run = True
for input_file in args.bib_file:
    # set the output filename
    if args.output:
        output = args.output
        # remove the file if already exists
        if first_run:
            if os.path.exists(output):
                os.remove(output)
            first_run = False
        elif not first_run:
            args.headless = True
    else:
        output = os.path.splitext(input_file)[0] + '.csv'
        if os.path.exists(output):
            os.remove(output)
    bib2csv(input_file, output)
