# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 16:37:51 CST 2021

@author: ludwig rubio
"""
import sys, getopt
import pandas as pd
import numpy as np
from datetime import datetime

class CovidReportHCSC():
    """
    Class to create an isntance of new report in Daily/Monthly basis
    
    Attributes:
        
        covidCounties (pandas.DataFrame):
            Dataframe simplified an clena to be joined with population dataset
        populationCounties (pandas.DataFrame):
            DataFrame simplified with 5 digits format FIPS to join with COVID dataset
        report (pandas.DataFrame):
            Datafrmae with final report to be exported
    """
    
    def __init__(self, covid_url, population_url, report_url):

        self.covidCounties = self.__preprocessCOVIDFile(covid_url)
        self.populationCounties = self.__preprocessPopulationFile(population_url)
        self.report = self.joinCOVIDPopulation()

    def __preprocessCOVIDFile(self, covid_url):
        return 0
    
    def __preprocessPopulationFile(self, population_url):
        return 0  
    
    def joinCOVIDPopulation(self):
        return 0  
    
    def exporToCSV(self, file_name):
        return 0
        #self.report.to_csv(file_name)

if __name__ == "__main__":
    
    def setArguments(argv):
        """
            Set the argument or use dafult values
            
            Parameters:
                args (array): expected arguments
                
            Returns:
                urls (tuple): (covidURL, populationURL, reportURL)
                
        """
        # Default values
        covidURL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
        populationURL = "https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv"  
        reportURL = f"report-COVID-Population-{datetime.utcnow().isoformat()}.csv"        
        
        try:
            opts, args = getopt.getopt(argv,"hc:p:o:",["cfile=","pfile=","ofile"])
        except getopt.GetoptError:
            print ('test.py -c <covidURL> -p <popultionURL> -o <reportURl>')
            sys.exit(2)
        
        for opt, arg in opts:
            if opt == '-h':
                print ('test.py -c <covidURL> -p <popultionURL> -o <reportURl>')
                sys.exit()
            elif opt in ("-c", "--cfile"):
                covidURL = arg
            elif opt in ("-p", "--pfile"):
                populationURL = arg
            elif opt in ("-o", "--ofile"):
                reportURL = arg
        return (covidURL, populationURL, reportURL)
        
    covidURL, populationURL, reportURL = setArguments(sys.argv[1:])

    instanceReport = CovidReportHCSC(covid_url = covidURL,
                                     population_url = populationURL,
                                     report_url = reportURL )
    
    instanceReport.exporToCSV(reportURL)
