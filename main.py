import argparse
from p_reporting.m_reporting import export_challenge
from p_reporting.m_reporting import export_bonus_1
from p_reporting.m_reporting import export_bonus_2

COUNTRIES = ['Belgium',
             'Lithuania',
             'Portugal',
             'Bulgaria',
             'Spain',
             'Luxembourg',
             'Romania',
             'Czechia',
             'France',
             'Hungary',
             'Slovenia',
             'Denmark',
             'Croatia',
             'Malta',
             'Slovakia',
             'Germany',
             'Italy',
             'Netherlands',
             'Finland',
             'Estonia',
             'Cyprus',
             'Austria',
             'Sweden',
             'Ireland',
             'Latvia',
             'Poland',
             'Great Britain',
             'Greece']


def argument_parser():
    parser = argparse.ArgumentParser(description='Obtain a full or country focused scope')

    # arguments here!
    parser.add_argument("-c", "--country", help="Create output for country X", type=str)
    parser.add_argument("-v", "--votes", help="Print table with In Favour/Against counts", type=str)

    args = parser.parse_args()

    return args


def main():
    print('Running pipeline...')

    # 1/3 - Export the Challenge 1 result to csv using parsed arguments

    if argument_parser().country in COUNTRIES:
        for c in COUNTRIES:
            table = export_challenge()
            table.loc[table['Country'] == argument_parser().country].to_csv(f'data/results/{argument_parser()}.csv',
                                                                            index=False)
            break
    elif argument_parser().country == 'All':
        table = export_challenge()
        table.to_csv('data/results/all.csv')

    else:
        raise ValueError("Please chose a valid country from the list, or alternatively, type 'All'")

    print('Table exported! Check your output folder ')

    # 2/3 - Print and export bonus 1 table to csv

    b1 = input('Would you also like an excel table with bonus 1? (yes/no)')
    if b1 == 'yes':
        bonus_1_table = export_bonus_1()
        print(bonus_1_table)
        bonus_1_table.to_csv('data/results/votes.csv')
        print('table has been exported, Check your folder!')
    elif b1 == 'no':
        print('Whatever... Your loss!')

    # 3/3 - Print and export bonus 2 table to csv

    b1 = input('How about top skills table for bonus 2? (yes/no)')
    if b1 == 'yes':
        bonus_2_table = export_bonus_2()
        bonus_2_table.to_csv('data/results/top_skills.csv')
        print(bonus_2_table)
        print('table has been exported, Check your folder!')
    elif b1 == 'no':
        print('Oh... what a waste of my time then')

    print('Script complete, thanks for using this awesome tool')


if __name__ == '__main__':
    arguments = argument_parser()
    main()
