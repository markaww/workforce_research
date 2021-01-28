import pandas as pd

from p_wrangling.m_wrangling import challenge_1_table
from p_wrangling.m_wrangling import bonus_1_table
from p_wrangling.m_wrangling import bonus_2_table


def challenge_1_analysis():

    ch1_table = challenge_1_table()

    # Add a column percentage as ( quantity / total quantity )

    total_quantity = ch1_table ['Quantity'].sum()
    ch1_table ['Percentage'] = (((ch1_table ['Quantity'] / total_quantity) * 100).round(2)).astype(str) + '%'

    return ch1_table


def bonus_1_analysis():
    bonus_1 = bonus_1_table()

    # 1/4 - from those who voted 'yes', we count how many 'pro' arguments were given

    infavour_pro = bonus_1[0]['question_bbi_2016wave4_basicincome_argumentsfor'].unique()
    infavour_pro_a = [item for item in infavour_pro]
    infavour_pro_b = [i.split(' | ') for i in infavour_pro_a]
    infavour_pro_c = [i for sublist in infavour_pro_b for i in sublist]

    # 2/4 - from those who voted 'yes', we count how many 'con' arguments were given

    infavour_con = bonus_1[0]['question_bbi_2016wave4_basicincome_argumentsagainst'].unique()
    infavour_con_a = [item for item in infavour_con]
    infavour_con_b = [i.split(' | ') for i in infavour_con_a]
    infavour_con_c = [i for sublist in infavour_con_b for i in sublist]

    # 3/4 - from those who voted 'no', we count how many 'pro' arguments were given

    against_pro = bonus_1[1]['question_bbi_2016wave4_basicincome_argumentsfor'].unique()
    against_pro_a = [item for item in against_pro]
    against_pro_b = [i.split(' | ') for i in against_pro_a]
    against_pro_c = [i for sublist in against_pro_b for i in sublist]

    # 4/4 - from those who voted 'no', we count how many 'con' arguments were given

    against_con = bonus_1[1]['question_bbi_2016wave4_basicincome_argumentsagainst'].unique()
    against_con_a = [item for item in against_con]
    against_con_b = [i.split(' | ') for i in against_con_a]
    against_con_c = [i for sublist in against_con_b for i in sublist]

    # Now we feed the 4 counts obtained into a dataframe as per the bonus 1 instructions

    bonus_1 = {'Number of Pro Arguments': [len(infavour_pro_c), len(against_pro_c)],
               'Number of Con Arguments': [len(infavour_con_c), len(against_con_c)]}

    bonus_1_df = pd.DataFrame(bonus_1,
                              index=['In Favour', 'Against'],
                              columns=['Number of Pro Arguments', 'Number of Con Arguments'])

    return bonus_1_df


def bonus_2_analysis():
    bonus_2 = bonus_2_table()

    # Group the population into education-level buckets, and aggregate the skills for each into a list

    bonus_2_grouped = bonus_2.groupby('dem_education_level').agg(list).reset_index()

    # Count in each skill list the number of each skill, replace the list with a dictionary

    from collections import Counter

    def counter(x):
        return dict(Counter(x))

    bonus_2_grouped['top_skill'] = bonus_2_grouped['top_skill'].apply(counter)

    # Finally, replace each dict with the key (skill) that has the highest value (frequency)

    def get_tops(x):
        tops = sorted(x, key=x.get, reverse=True)[:10]
        return tops

    bonus_2_grouped['top_10_skills'] = bonus_2_grouped['top_skill'].apply(get_tops)

    columns = ['dem_education_level', 'top_10_skills']
    final = bonus_2_grouped[columns]

    return final

