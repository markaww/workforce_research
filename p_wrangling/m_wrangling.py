from p_acquisition.m_acquisition import acquire
aquired_result = acquire()


def challenge_1_table():


    # Remove unwanted columns

    columns = ['country_code', 'normalized_job_title', 'gender']
    final_raw = aquired_result[columns]

    # Remove unwanted columns

    columns = ['country_code', 'normalized_job_title', 'gender']
    final_raw = aquired_result[columns]

    # Rename headers

    col_dict = {'uuid_x': 'ID number',
                'country_code': 'Country',
                'gender': 'Gender',
                'normalized_job_title': 'Job Title'}
    final = final_raw.rename(columns=col_dict, inplace=False)

    # Group by country, job and gender, and add a column with respective count

    final_grouped = final.value_counts(['Country', 'Job Title', 'Gender']).reset_index(name='Quantity')

    return final_grouped


def bonus_1_table():

    # First, we create 2 tables, one with people who voted 'yes', and another with people who voted 'no'

    vote_yes = ['I would probably vote for it', 'I would vote for it']
    infavour = aquired_result[aquired_result['question_bbi_2016wave4_basicincome_vote'].isin(vote_yes)]

    vote_no = ['I would vote against it', 'I would probably vote against it']
    against = aquired_result[aquired_result['question_bbi_2016wave4_basicincome_vote'].isin(vote_no)]

    return infavour, against


def bonus_2_table():

    columns = ['dem_education_level', 'top_skill']
    final_raw = aquired_result[columns]

    return final_raw
