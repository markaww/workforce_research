from sqlalchemy import create_engine
import pandas as pd
import requests

def acquire():

    # 1/3 Connection to the db

    sqlitedb_rel_path = 'data/processed/raw_data_project_m1.db'
    conn_str = f'sqlite:///{sqlitedb_rel_path}'
    engine = create_engine(conn_str)

    # Use dBeaver to cleanup a few fields i.e. gender, then make a DataFrame:

    sql_query = """ 
    SELECT country_info.uuid,
           country_info.country_code,
           career_info.dem_education_level,
           career_info.normalized_job_code, 
           personal_info.age, 
           personal_info.gender,
           poll_info.question_bbi_2016wave4_basicincome_vote,
           poll_info.question_bbi_2016wave4_basicincome_argumentsagainst,
       poll_info.question_bbi_2016wave4_basicincome_argumentsfor 
    FROM country_info
    JOIN career_info ON country_info.uuid = career_info.uuid
    JOIN personal_info ON personal_info.uuid = career_info.uuid
    JOIN poll_info ON poll_info.uuid = personal_info.uuid
    """

    poll_db = pd.read_sql_query(sql_query, engine)

    poll_job_code = poll_db['normalized_job_code'].unique().tolist()

    # 2/3 Extract job skills and description table using APIs
    # Make a list with job ids from the csv, and use it to get job names from website (open skills api)

    poll_db = pd.read_sql_query(sql_query, engine)

    poll_job_code = poll_db['normalized_job_code'].unique().tolist()

    url_list = []
    for i in poll_job_code:
        url_list.append(f'http://api.dataatwork.org/v1/jobs/{i}/related_skills')

    # Make a DataFrame with the collection of results.

    lst = []
    for url in url_list:
        response = requests.get(url)
        json_data = response.json()
        lst.append(json_data)

    api_skills = pd.DataFrame(lst)

    # Remove nulls

    api_skills.drop(index=api_skills[api_skills.skills.isnull()].index, inplace=True)

    #Formula to get the first skill, which is always the one with highest 'importance' value

    def get_max(x):
        top_skill = pd.json_normalize(x).iloc[0]['skill_name']
        return top_skill

    api_skills['top_skill'] = api_skills['skills'].apply(get_max)

    # 3/3 Get country names with web scraping

    url = 'https://ec.europa.eu/eurostat/statistics-explained/index.php/Glossary:Country_codes'
    html = requests.get(url).content

    # Make the soup

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Assign the correct [0] table data to variable tablle

    table = soup.find_all('table')[0]

    # Remove anything that isn't countries or acronyms

    items = [x.text for x in table.find_all('td')]

    # Create a dict of 2 lists (countries and their acronyms), and convert to DF

    countries = []
    acronyms = []
    for i in items:
        if i.startswith('('):
            acronyms.append(i[1:-2])
        else:
            countries.append(i[:-1])

    raw_dict = {'countries': countries, 'acronyms': acronyms}

    # This dict, however is not exactly the right shape for a latter pd.replace,

    raw_dict_df = pd.DataFrame(raw_dict)
    new_dict = raw_dict_df.set_index('acronyms').to_dict()
    countries_dict = new_dict['countries']

    # Adjust a couple keys missing in the countries table

    countries_dict['GB'] = 'Great Britain'
    countries_dict['GR'] = 'Greece'
    del countries_dict['EL']

    # From wrangling, include the lines to lead to a single table output
    # Merge poll file with api job list

    poll_api_merge = poll_db.merge(api_skills, left_on='normalized_job_code', right_on='job_uuid', how='outer')

    # Map countries from countries_dict

    poll_api_merge_countries = poll_api_merge.fillna('Unemployed').replace({"country_code": countries_dict})

    # Small correction to the education level column, where nulls were populated with Unemployed

    poll_api_merge_countries['dem_education_level'] = poll_api_merge_countries['dem_education_level'].str.replace(
        'Unemployed', 'no')

    return poll_api_merge_countries
