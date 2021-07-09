## COVID-19 - HCSC Code Screen

### Problem statement
As part of HCSC’s COVID19 response, the Data Science team needs to prepare daily/weekly updates of nationwide infection counts, organized by county.

For every FIPS code and date, your end user will want to know: population, daily cases, daily deaths, cumulative
cases to date, and cumulative death counts to date.

## Code execution

### Libraries and dependencies
The python version used for development is: python __3.7.6__

Please before execution install [pandas](https://pandas.pydata.org/) and [numpy](https://numpy.org/), yo can use _requirements.txt_ file to install dependencies, if you have pip installed use following command:

> **pip install** -r requirements.txt

### Execution (Create Report)

Please execute CreateReport.py file, a _.csv_ file in actual folder level will be created with following name: 

__report-COVID-Population-[timestamp]_[daily|weekly].csv__ 
(refer to [_COVID_19-Population-2021-07-09T16-13-11_weekly.csv_](COVID_19-Population-2021-07-09T16-13-11_weekly.csv_) file as an example )

Also an __extended version__ to define a custom data sources URL and output destination folder/name __is available__:

Parameters are optional, you can override any combination of them:

* __-c__: Set the file URL that represents dataset _**C**OVID-19 NY Times_
* __-p__: Set the file URL that represents dataset _**P**opulation by County_
* __-o__: Set the folder-name file of the **O**utput report
* __-t__: Set a prefix (Useful to add as part of the daily or weekly report)

Example:
>   python CreateReport.py -c https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv -o custom_report_name.csv -t weekly

Please refer to class documentation to see details of the structure, use following command in python console to see details:

> help(CovidReportHCSC)


## Process and learns

### Sanity Checked
As I did it on input files, the sanity check was done in a manual exploratory way, some of the aspects I checked are:
* Description (min, max, median, standard deviation) of numeric columns
* Number of columns and names
* *min*, *max* length per each column to find any potential issue
* *count*s by State-County to verify not missing dates rows
* Number of rows

### Learning and thoughts

On this repo you'll find an __Exploratory__ folder with [Juypter](https://jupyter.org/) notebooks per each source file where the exploratory process, issues found and cleanups strategies were implemented before creating  _CovidReportHCSC.py_ file.

* [COVID-19 NYTimes - Exploratory.ipynb](Exploratory/COVID-19%20NYTimes%20-%20Exploratory.ipynb)
* [Population Estimate Data (2020) - Exploratory.ipynb](Exploratory/Population%20Estimate%20Data%20%20(2020)%20-%20Exploratory.ipynb)
* [JOIN Dataset - Exploratory.ipynb](Exploratory/JOIN%20Dataset%20-%20Exploratory.ipynb)
---
#### NY Times Dataset

- _FIPS_ imported as float due NULL values
- All _FIPS_ are well formatted (5 characters numeric)
- There are some _FIPS_ as NULL but state-county data present (We  tried to add correct FIPS for them)
    - New York City
    - Kansas City
    - Joplin
- There are records with empty value in _deaths_ column, all of them belong to Puerto Rico
- State and County don't have an empty value or malformed name
- 13605 records have null FIPS
---
#### Population by County Dataset
- Encoding of source file need to be set due decode issue (ISO-8859-1)
- Dataset contains records with _COUNTY FIPS_ = 0, they are STATE aggregated data
- SUMLEV help us to exclude aggregation state population (Exclude _SUMLEV_ = 40)
- _POPESTIMATE2019_ is a very clean column, but it has a big standard deviation
    - Min population: 86
    - Max population: 1,039,107

---
#### Joining Dataset

- I removed PUERTO RICO since is not part of the scope of US states and is adding noise to the dataset
- FIPS need to be on format SS for state and CCC for counties concatenated SSCCC to be able to join
- There are in total 61 counties without population data (46 with Unknown name)
- There are 15 counties name with Unknown name (Some of them repeated over different states)
- Using cumsum() function to calculate cumulative deaths/cases per day
- Documented issues related to columns being convert to object type when NaN values created
---
#### Report result

### If I had more time ...

* __Automate unit testing__: The sanity check of the output was executed manually, before and after exporting result into a CSV file. A good/better practice to avoid changes in the expected columns, formats, and result in the output file that Data Scientist will consume, it's a good to have an automated Unit Test, that before deploying or being used by another person could automatically verify the result in terms of acceptance criteria.
* __Reutilization of code__: Due the scope of the exercise, the code was developed in few files only using OOP concepts. A better practice could be to create different files to reutilize them later, for example:
	* Create an _Utils.py_ file to be reused
	* Create a different class the per each file to be preprocessed; this can help us to reutilize the cleanup process,  using clean data to join with other data. 
* __Include other metrics__: The population dataset have potential to create more metrics, it contains a  set of valuable statists in terms of time that could be useful to create better prediction (For example using Temporal Series or LSTM Neuronal Networks).