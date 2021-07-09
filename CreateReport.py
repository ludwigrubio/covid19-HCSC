# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 20:09:46 2021

@author: ludwig rubio
"""
import sys, getopt, logging
from datetime import datetime
from CovidReportHCSC import CovidReportHCSC

logging.basicConfig(level = logging.INFO, format = '%(asctime)s: %(levelname)s - %(message)s', datefmt = '%m-%d %H:%M:%S')
logger = logging.getLogger()

if __name__ == "__main__":
    
    def setArguments(argv):
        """
            Set the argument or use dafault values
            
            Parameters:
            -----------
                args (array): expected arguments
                
            Returns:
            --------
                urls (tuple): (covidURL, populationURL, reportURL)                
        """
        # Default values
        covidURL = "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
        populationURL = "https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv"  
        reportURL = f"COVID_19-Population-{datetime.strftime(datetime.utcnow(), '%Y-%m-%dT%H-%M-%S')}.csv"
        periodReport = 'daily'
        
        # Evaluate arguments
        try:
            opts, args = getopt.getopt(argv,"hc:p:o:t:",["cfile=","pfile=","ofile","tfile"])
        except getopt.GetoptError:
            print ("test.py -c <covidURL> -p <populationURL> -o <reportURL> -t ['daily'|'weekly']")
            sys.exit(2)
        
        if len(opts) > 0 :
            logger.info(f"A custom {[par for par,val in opts]} argument(s) was found, overriding default value(s)")
            for opt, arg in opts:
                if opt == '-h':
                    print ("test.py -c <covidURL> -p <populationURL> -o <reportURL> -t ['daily'|'weekly']")
                    sys.exit()
                elif opt in ("-c", "--cfile"):
                    covidURL = arg
                elif opt in ("-p", "--pfile"):
                    populationURL = arg
                elif opt in ("-o", "--ofile"):
                    reportURL = arg
                elif opt in ("-t", "--tfile"):
                    periodReport = arg
        else: 
             logger.info("No custom arguments detected, using default values:")
        
        logger.info(f"""
                       - NY Times Dataset: {covidURL}
                       - Population by County: {populationURL}
                       - File name to be exported: {reportURL.replace('.csv', f'_{periodReport}.csv')}
                     """)
        return (covidURL, populationURL, reportURL.replace('.csv', f'_{periodReport}.csv'))
        
    # Setting Argumnets values
    covidURL, populationURL, reportURL = setArguments(sys.argv[1:])

    # Pre-Process, Join and aggregation
    logger.info(f"Process started ...")
    instanceReport = CovidReportHCSC(covid_url = covidURL,
                                     population_url = populationURL,
                                     report_url = reportURL )
    
    # Export file
    logger.info(f"4) Exporting to file {reportURL} ...")
    instanceReport.exporToCSV(reportURL)
    logger.info(f"    File exported.")
    logger.info(f"Process completed successfully!.")