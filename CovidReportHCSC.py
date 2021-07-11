# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 16:37:51 CST 2021

@author: ludwig rubio
"""
import logging
import pandas as pd

logger = logging.getLogger()

class CovidReportHCSC():
    """
    Class to create an isntance of new report in Daily/Monthly basis
    
    Attributes:
    -----------    
        covidCounties (pandas.DataFrame):
            Dataframe simplified an clena to be joined with population dataset
        populationCounties (pandas.DataFrame):
            DataFrame simplified with 5 digits format FIPS to join with COVID dataset
        report (pandas.DataFrame):
            Datafrmae with final report to be exported
    """
    
    def __init__(self, covid_url, population_url, report_url):
        """
        Constructor, alll data source and report ouput URLs.
        
        Parameters:
        -----------
            covid_url (string): COVID19 Data Source URL
            population_url (string): Population Data Source URL
            report_url (string): Output custom file folder/name 

        """
        logger.info("1) NY Times DataSet preprocess started ...")
        self.covidCounties = self.__preprocessCOVIDFile(covid_url)
        logger.info("    NY Times preprocess completed.")
        logger.info("2) Population by County preprocess Started ...")
        self.populationCounties = self.__preprocessPopulationFile(population_url)
        logger.info("    Population by County preporcess Times Completed.")
        logger.info("3) Join process started...")
        self.report = self.joinCOVIDPopulation()
        logger.info("    Join process completed.")

    def __preprocessCOVIDFile(self, covid_url):
        
        try:
            covidCounties = pd.read_csv(covid_url, parse_dates=True, keep_default_na=False)
        except:
            logger.error(f"There was an issue trying to read file: {covid_url}, please verify file exists")
            raise
        
        try:
            # Remove PUERTO RICO
            covidCounties = covidCounties[covidCounties['state'] !='Puerto Rico']
            # Tranform deaths to Integer type
            covidCounties['deaths'] = covidCounties['deaths'].str.strip().astype('float').astype('Int64')
            # Convert dates to Date type
            covidCounties['date'] = pd.to_datetime(covidCounties['date'])
            # Fixing missing FIP for New York
            covidCounties.loc[covidCounties['county'] == 'New York City', 'fips']  = '36061'
        except:
            logger.error(f"There was an issue preprocessing the file, please ensure file is following defined standard https://github.com/nytimes/covid-19-data")
            raise
        
        return covidCounties
    
    def __preprocessPopulationFile(self, population_url):
        
        try:
            populationCounties = pd.read_csv(population_url, parse_dates=True, keep_default_na=False, encoding='ISO-8859-1')
        except:
            logger.error(f"There was an issue trying to read file: {population_url}, please verify file exists")
       
        try:
            # Keep only needed data
            populationCounties = populationCounties.loc[populationCounties['SUMLEV'] == 50][['STATE','COUNTY','POPESTIMATE2019']]
            # Raname column
            populationCounties.rename(columns={"POPESTIMATE2019": "population_2019"},  inplace = True)
            
            # Create FIPS in format SSCCC
            populationCounties['COUNTY'] = populationCounties['COUNTY'].astype(str).str.zfill(3)
            populationCounties['STATE'] = populationCounties['STATE'].astype(str).str.zfill(2)
            populationCounties['fips'] =  populationCounties['STATE'] +  populationCounties['COUNTY']
        except:
            logger.error(f"There was an issue preprocessing the file, please ensure file is following defined standard https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.pdf")
            raise        
        return populationCounties
    
    def joinCOVIDPopulation(self):
        """
        Joining data sources an applying required aggregations.
        
        Returns:
        --------
            report (pandas.DataFrame): include columns:
                                         fips
                                         state
                                         county
                                         population_2019
                                         daily_cases
                                         daily_deaths
                                         cumulative_cases_to_date
                                         cumulative_death_to_date
        """
        joined =  self.covidCounties.merge( self.populationCounties, how='left', on='fips')
        # Fix known issue: when a Nan is created is converted to An Object type
        joined['population_2019'] = joined['population_2019'].astype('Int64')
       
        # Comulative data
        joined = joined[['date','fips','county','state','population_2019', 'cases','deaths']]
        joined.sort_values(['date']).reset_index(drop=True)
        joined["cumulative_cases_to_date"] = joined.groupby(['fips'])['cases'].cumsum(axis=0)
        joined["cumulative_death_to_date"] = joined.groupby(['fips'])['deaths'].cumsum(axis=0)
        
        # Fix know Issue
        joined["cumulative_death_to_date"] =joined["cumulative_death_to_date"].astype('Int64')
        # Raname columns
        joined.rename(columns={"cases": "daily_cases", "deaths": "daily_deaths"},  inplace = True)
        return joined 
    
    def exporToCSV(self, file_name):
        """
        Export final report into a CSV file
        
        Parameters:
        -----------
            file_name (string): name of file to be exported, by default COVID_19-Population-[timestamp]_[daily|weekly].csv
            
        Returns:
        --------
            report (csv): create a file in specified folder/name              
        """
        
        self.report.to_csv(file_name, index=False)