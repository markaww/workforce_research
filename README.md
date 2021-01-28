# Workforce research
A tool to quickly obtain insights on a population, such as job, nationality and poll results

The population is composed of a poll study data base with 9.5k people from the EU who were interviewed about their position of the implementation of a universal basic income. 
The table contains three sources:
- Population database with poll interview results
- Job descriptions and job related skills for this population, obtained from dataatwork.org with an API 
- Country names obtained with web scraping from ec.europa.eu/eurostat

The tool is divided into three sections: 

## Section 1 - Poll population job/gender study

This section provides a comprehensive study of the ocupation in this dataset. Results are aggregated by country, occupation and gender. 

To activate the functionality, please execute the script with argument --country='country_name', where country_name can be either a EU member state or alternatively 'All'. 

## Section 2 - Poll results

While the pipeline is executed you will be prompted to indicate yes/no if you would like to see a table containing aggregated results for the poll results. 

The resulting table will be printed on the terminal and also exported. It divides the population into those who voted 'In Favour' and those who voted 'Against' in the poll (discarding those who wouldn't vote) and then it tallies, for each group, the amount of pro/con arguments given. 

## Section 3 - Job related skills 

While the pipeline is executed you will be prompted to indicate yes/no if you would like to see a table containing an analysis of the most relevant job related skills for this population. 

The resulting table will be printed on the terminal and also exported. It groups the population into education level (high/medium/low/no) and in a second column, includes the 10 most relevant job related skills the people in that group have. 

 
