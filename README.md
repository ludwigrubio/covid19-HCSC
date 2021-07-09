## About this Repo

### Problem statement
As part of HCSC’s COVID19 response, the Data Science team needs to prepare daily/weekly updates of nationwide infection counts, organized by county.


## Code execution

### Libraries and dependencies
The python version used for development is: python __3.7.6__

Please before execution install [pandas](https://pandas.pydata.org/) and [numpy](https://numpy.org/), yo can use _requirements.txt_ file to install dependencies, if you have pip installed use following command:

> **pip install** -r requirements.txt

### Execution (Create Report)

Please execute CovidReportHCSC.py file, a .csv file in actual folder level will be created with following name: 

__report-COVID-Population-[ISO-Timestamp].csv__ 
(refer to _report-COVID-Population-2021-07-08T22:31:19.098636.csv_ file as an example )

Also an __extended version__ to define a custom data sources URL and output destination folder/name __is available__:

Set following parameters:

* __-c__: Set the file URL that represents dataset _**C**OVID-19 NY Times_
* __-p__: Set the file URL that represents dataset _**P**opulation by County_
* __-o__: Set the folder-name file of the **O**utput report.

Example:
>   _CovidReportHCSC.py_ __-c__ 'shorturl.at/pruPV' __-p__ 'shorturl.at/hsFSW' __-o__ './weekly_custom_output_report_name.csv'

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
* etc.

### Learning and thoughts

On repo you'll find an __Exploratory__ folder, there you can find [Juypter](https://jupyter.org/) notebooks per each source file where the exploratory process, issues found and cleanups strategies were implemented before creating  _CovidReportHCSC.py_ file.

* [COVID-19 NYTimes - Exploratory.ipynb](Exploratory/COVID-19%20NYTimes%20-%20Exploratory.ipynb)
* [Population Estimate Data (2020) - Exploratory.ipynb](Exploratory/Population%20Estimate%20Data%20%20(2020)%20-%20Exploratory.ipynb)

### If I had more time
* __Automate unit testing__: The sanity check of the output was executed manually, before and after exporting result into a CSV file. A good/better practice to avoid changes in the expected columns, formats, and result in the output file that Data Scientist will consume, it's a good to have an automated Unit Test, that before deploying or being used by another person could automatically verify the result in terms of acceptance criteria.
* __Reutilization of code__: Due the scope of the exercise, the code was developed in few files, only using OOP concepts. A better practice could be to create different files to reutilize them later, for example:
	* Create an _Utils.py_ file to be reused
	* Create a different class the per each file to be preprocessed; this can help us to reutilize the cleanup process,  using clean data to join with other data. 
* __Include other metrics__: The population dataset have potential to create more metrics, it contains a  set of valuable statists in terms of time that could be useful to create better prediction (For example using Temporal Series or LSTM Neuronal Networks).

