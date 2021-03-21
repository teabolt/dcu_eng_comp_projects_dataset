# Disclaimer

The PDF data contained in this repository belongs to Dublin City University and corresponding students. The data is extracted for informational purposes only. Please contact the owners of the repository or open an issue if you have any issues with this data.

# DCU engineering and computing projects dataset

Every year Dublin City University (DCU) holds an Expo for undergraduate computing and engineering students to show off their final year projects (https://www.dcu.ie/engineering_and_computing/Final-Year-Projects-Expo.shtml). Each Expo produces a .pdf file that talks about the Expo and gives descriptions of student projects.

In this repo it is proposed to extract all the data related to student projects (project title, programme, supervisor, descriptions, etc) from PDF files, and put that data into a structured format like JSON or CSV. The structured file should then be analysed using Data Science techniques or exposed through a simple search UI.

Currently booklets from 2020 to 2011 are supported.

## Extraction steps

These are the steps that I took to extract data (some manual, some automated).

Linux has been used.

### 1. Download all booklets (PDF's) and normalise their names

Run the `setup.sh` script, which makes use of the `booklet_urls.txt` file to download booklet PDF's.

Find the resulting PDF's in `/booklets`. Each booklet PDF is named after the year that it was made in, i.e. `2020.pdf`.

### 2. Strip PDF's

Manually clean up the original PDF's and put the results in `/booklets_stripped`.

This includes only keeping relevant pages (pages that have the projects) and removing irrelevant pages (introduction and credits).
Also attempt to remove extra information such as page numbers.

#### Remove pages

PDF's should have only those pages that have project descriptions, i.e. remove booklet cover, introduction, table of contents, list of projects.
Search online `pdf remove pages` for websites that provide this service.

Can also use the PdfTk multi-platform command line tool to remove pages. (see https://superuser.com/a/517993)

#### Remove margins

PDF's should also be stripped of margins that contain the booklet header, page numbers, etc.

Search online `pdf crop` for websites or tools. May also need `pdf merge`.

### 3. Convert PDF's to a text format

Manually convert booklets from a PDF format to a text format (.txt, .csv, .xlsx) for easy parsing. Put the results in `/booklets_text`.

Tables need to be converted accurately.

Some example tools:

- `pdftotext` linux tool
  ```
  find booklets_stripped/ -name *.pdf -exec echo {} \; -exec pdftotext {} \;
  mv booklets_stripped/*.txt booklets_text/
  ```
- Online results for `pdf to csv`
- Online results for `pdf to excel`

Alternatively just copy all the text from a stripped PDF (using CTRL+A), where it's possible to do a selection.

### 4. Parse the data from text files

Automatically convert text or excel booklet files into structured data.

See `src/` for Python and Jupyter Notebook scripts. The `projects_parser` Python module can extract fields from a text file using a mapping of field name -> regular expression. Make a copy of a Jupyter Notebook for the year being parsed, and adjust year-dependent values (i.e. data source).

Some years may need extra adjustment as the booklets do not follow the same format across the years.
E.g. in 2019 one of the projects had students all with different programmes. It was easier to just list all the programmes after the list of students (though we lose information about which student is in which programme, that is not so necessary).
**For small anomaly cases, it's best to just adjust the data, instead of writing extra logic.**

Also perform data "canonicalization" (standardisation or normalization) in this step.

https://pythex.org/ is very useful for testing out regular expressions.

### 5. Analyse or use the dataset

Uses:

- A search UI: https://prosearch.tomasb.ie/ or https://github.com/teabolt/dcu_project_search_frontend

Other ideas:

- See trends in project areas, technologies over the years.
- Check history of supervisors' projects.
- Check if a project has been done before by searching through the titles and descriptions.
- Count number of projects per year
- Count number of projects of each supervisor.

## Credits

- teabolt - https://github.com/teabolt
- KingEnoch - https://github.com/KingEnoch

## License

MIT
