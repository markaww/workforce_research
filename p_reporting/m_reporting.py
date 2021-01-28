from p_analysis.m_analysis import challenge_1_analysis
from p_analysis.m_analysis import bonus_1_analysis
from p_analysis.m_analysis import bonus_2_analysis


def export_challenge():
    final_grouped = challenge_1_analysis()

    return final_grouped


def export_bonus_1():
    bonus_1_df = bonus_1_analysis()

    return bonus_1_df


def export_bonus_2():
    bonus_2_df = bonus_2_analysis()

    return bonus_2_df
