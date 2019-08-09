# DCU engineering and computing projects dataset

Every year Dublin City University (DCU) holds an Expo for computing and engineering students to show off their final year projects (https://www.dcu.ie/engineering_and_computing/Final-Year-Projects-Expo.shtml). Each Expo produces a .pdf file that talks about the Expo and gives descriptions of student projects.

In this repo it is proposed to extract all the data related to student projects (project title, programme, supervisor, descriptions, etc) from PDF files, and put that data into a structured format like CSV. The structured file should then be analysed using Data Science techniques.

Update: Booklets from 2011 to 2019 are supported.


## Extraction steps

These are the steps that I took to extract data (some manual, some automated).

Linux has been used.

### Get all booklets

See the `setup.sh` script.

Results in `/booklets`.

### Strip PDF's

Clean up the underlying PDF's.

PDF's should have only those pages that have project descriptions, i.e. remove cover, introduction, etc. pages.
Search online `pdf remove pages` for websites that provide this service.

PDF's should also be stripped of margins that contain the booklet header, page numbers, etc.
Search online `pdf crop` for websites that can do this.

Results in `/booklets_stripped`.

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

### Parse data from text files (TODO)

Python may be good for this.

### Combine data (TODO)

### Analyse/use the dataset (TODO)

Ideas:
* Trends in project areas, technologies.
* History of supervisors' projects.
* Check if a project has been done before by searching through the titles and descriptions.