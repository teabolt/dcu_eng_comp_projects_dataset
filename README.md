# DCU engineering and computing projects dataset

Every year Dublin City University (DCU) holds an Expo for computing and engineering students to show off their final year projects (https://www.dcu.ie/engineering_and_computing/Final-Year-Projects-Expo.shtml). Each Expo produces a .pdf file that talks about the Expo and gives descriptions of student projects.

In this repo it is proposed to extract all the data related to student projects (project title, programme, supervisor, descriptions, etc) from PDF files, and put that data into a structured format like CSV. The structured file should then be analysed using Data Science techniques.

Currently booklets from 2020 to 2011 are supported.

## Extraction steps

These are the steps that I took to extract data (some manual, some automated).

Linux has been used.

### Get all booklets

Run the `setup.sh` script.

Find the results in `/booklets`.

### Strip PDF's

Clean up the original PDF's and put the results in `/booklets_stripped`.

#### Remove pages

PDF's should have only those pages that have project descriptions, i.e. remove booklet cover, introduction, table of contents, list of projects.
Search online `pdf remove pages` for websites that provide this service.

Can also use the PdfTk multi-platform command line tool to remove pages. (see https://superuser.com/a/517993)

#### Remove margins

PDF's should also be stripped of margins that contain the booklet header, page numbers, etc.

Search online `pdf crop` for websites or tools. May also need `pdf merge`.

### Convert PDF's to a text format (TODO)

Files should be converted from PDF to a text format (.txt, .csv, or anything else) for easy parsing.

Need to accurately convert tables.

References:
* `pdftotext` linux tool
    ```
    find booklets_stripped/ -name *.pdf -exec echo {} \; -exec pdftotext {} \;
    mv booklets_stripped/*.txt text/
    ```
* Online results for `pdf to csv`
* Online results for `pdf to excel`

May need to do manual data fixing in some cases.

### Parse the data from text files (TODO)

Convert text or excel files into structured data.

Python may be good for this.

### Combine data (TODO)

Combine structured data from the last step into one spreadsheet.

### Analyse/use the dataset (TODO)

* Count of project tools / project areas each year.
* Supervisors ranked by number of projects.
* Search for all projects of a supervisor.

### Usage ideas
* See trends in project areas, technologies.
* Check history of supervisors' projects.
* Check if a project has been done before by searching through the titles and descriptions.
