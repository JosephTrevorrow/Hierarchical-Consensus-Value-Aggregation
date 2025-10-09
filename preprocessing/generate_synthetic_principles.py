import pandas as pd
import numpy as np

def binary_principles(df):
    df['decision'] = np.nan  # Initialize the 'decision' column

    for index, row in df.iterrows():
        df.at[index, 'decision'] = (row['rel-nonrel'] * row['a_div_rel']) + (row['nonrel-rel'] * row['a_div_nonrel'])
        if df.at[index, 'decision'] < 0:
            df.at[index, 'egal'] = 1
            df.at[index, 'util'] = 0
        else:
            df.at[index, 'egal'] = 0
            df.at[index, 'util'] = 1
    return df

def range_principles(df, against_scheme, for_scheme):
    """
    This function calculates the decision based on the range of principles
    - factor is calculated as a random p value the agent will hold. 
        The principle will be calculated from principles that are in support to the agents real choice
    """
    for index, row in df.iterrows():
        total_interviewees = row['rel'] + row['nonrel']

        if df.at[index, 'decision'] < 0:
            factor = np.random.choice(against_scheme)
            egal = (factor / 10) * total_interviewees
            util = total_interviewees - egal
            egal = round(egal, 0)
            util = round(util, 0)
            # Factor is 1.0 then [egal, util] = [0, 1]
            # Factor is 10.0 then [egal, util] = [1, 0]
            # Factor is 1.8 then [egal, util] = [0.18, 0.82]
            df.at[index, 'egal'] = egal
            df.at[index, 'util'] = util
        else:
            factor = np.random.choice(for_scheme)
            egal = (factor / 10) * total_interviewees
            util = total_interviewees - egal
            egal = round(egal, 0)
            util = round(util, 0)
            df.at[index, 'egal'] = egal
            df.at[index, 'util'] = util
    return df


#####
# 1.0 = Utilitarian, 2.2= Transition point, 10.0 = Egalitarian
####
relevent_consensuses = [round(x * 0.1, 1) for x in range(10, 101)]
relevant_columns = ['p','Rel-Nonrel', 'Nonrel-Rel', 'Rel_div_p', 'Nonrel_div_p', 'Egal-Util', 'Util-Egal']

actions_filename = "/data/results/22-01-2025-actions.csv"
preference_filename = 'data/results/22-01-2025-preferences.csv'

final_df_savename = "/data/10-01-2025-ess-relevant-consensus.csv"

pref_df = pd.read_csv(preference_filename)
act_df = pd.read_csv(actions_filename)
cons_df = pd.merge(pref_df, act_df, on='p')
cons_df['p'] = cons_df['p'].round(1)

# for each row, find the corresponding Util-Egal and Egal-Util values
for index, row in cons_df.iterrows():
    cons_df.at[index, 'Egal-Util'] = (row['p'] - 1) / 9
    cons_df.at[index, 'Util-Egal'] = 1 - cons_df.at[index, 'Egal-Util']
final_df = pd.DataFrame()
for consensus in relevent_consensuses:
    filtered_df = cons_df[cons_df['p'] == consensus][relevant_columns]
    filtered_df['decision'] = (filtered_df['Rel_div_p'] * filtered_df['Rel-Nonrel']) + (filtered_df['Nonrel_div_p'] * filtered_df['Nonrel-Rel'])
    final_df = pd.concat([final_df, filtered_df], ignore_index=True)
final_df.to_csv(final_df_savename)
print(final_df.to_string())

# Split final_df into two dataframes based on the decision column
positive_df = final_df[final_df['decision'] > 0]
negative_df = final_df[final_df['decision'] < 0]

# Find quartile vals
postive_quartiles = positive_df['decision'].quantile([0.25, 0.5, 0.75])
negative_quartiles = negative_df['decision'].quantile([0.25, 0.5, 0.75])

positive_quartile_p_values = {
    'Q1': positive_df[positive_df['decision'] <= postive_quartiles[0.25]]['p'].tolist(),
    'Q2': positive_df[(positive_df['decision'] > postive_quartiles[0.25]) & (positive_df['decision'] <= postive_quartiles[0.5])]['p'].tolist(),
    'Q3': positive_df[(positive_df['decision'] > postive_quartiles[0.5]) & (positive_df['decision'] <= postive_quartiles[0.75])]['p'].tolist(),
    'Q4': positive_df[positive_df['decision'] > postive_quartiles[0.75]]['p'].tolist()
}

negative_quartile_p_values = {
    'Q1': negative_df[negative_df['decision'] <= negative_quartiles[0.25]]['p'].tolist(),
    'Q2': negative_df[(negative_df['decision'] > negative_quartiles[0.25]) & (negative_df['decision'] <= negative_quartiles[0.5])]['p'].tolist(),
    'Q3': negative_df[(negative_df['decision'] > negative_quartiles[0.5]) & (negative_df['decision'] <= negative_quartiles[0.75])]['p'].tolist(),
    'Q4': negative_df[negative_df['decision'] > negative_quartiles[0.75]]['p'].tolist()
}

#print("Positive Quartile p values:", positive_quartile_p_values)
#print("Negative Quartile p values:", negative_quartile_p_values)

# Read in data
agent_csv_file = "/data/results/22-01-2025-agent-data.csv"
df = pd.read_csv(agent_csv_file)
for index, row in df.iterrows():
    df.at[index, 'decision'] = (row['Rel-Nonrel'] * row['a_div_rel']) + (row['Nonrel-Rel'] * row['a_div_nonrel'])

###################
# Make Test Cases #
###################
## Extreme Util (1): All agents are utilitarian
for_scheme = [value for sublist in positive_quartile_p_values.values() for value in sublist]
against_scheme = for_scheme
df = range_principles(df, against_scheme, for_scheme)
# Save the principles a file
principles_df = df[['country', 'egal', 'util']]
principles_df.rename(columns={'egal': 'rel', 'util': 'nonrel'}, inplace=True)
principles_df.to_csv("/data/results/principle_test_cases/15-01-2025-extreme-util-principles.csv", index=False)

## Extreme 2: All agents are egalitarian
for_scheme = [value for sublist in negative_quartile_p_values.values() for value in sublist]
against_scheme = for_scheme
df = range_principles(df, against_scheme, for_scheme)
# Save the principles a file
principles_df = df[['country', 'egal', 'util']]
principles_df.rename(columns={'egal': 'rel', 'util': 'nonrel'}, inplace=True)
principles_df.to_csv("/data/results/principle_test_cases/15-01-2025-extreme-egal-principles.csv", index=False)

# Random 1: Randomly assign agents to be utilitarian or egalitarian by any extent 
for_scheme = list(np.arange(1.0, 10.0, 0.1))
for_scheme = [round(num, 1) for num in for_scheme]
against_scheme = for_scheme
df = range_principles(df, against_scheme, for_scheme)
# Save the principles a file
principles_df = df[['country', 'egal', 'util']]
principles_df.rename(columns={'egal': 'rel', 'util': 'nonrel'}, inplace=True)
principles_df.to_csv("/data/results/principle_test_cases/15-01-2025-random-principles.csv", index=False)

# Quartile 1: Assign agents to be in top quartile utilitarian or egalitarian based on their decision (high investment)
for_scheme = positive_quartile_p_values['Q4']
against_scheme = negative_quartile_p_values['Q1']
print(for_scheme)
print(against_scheme)
df = range_principles(df, against_scheme, for_scheme)
# Save the principles a file
principles_df = df[['country', 'egal', 'util']]
principles_df.rename(columns={'egal': 'rel', 'util': 'nonrel'}, inplace=True)
principles_df.to_csv("/data/results/principle_test_cases/15-01-2025-top-quartile-principles.csv", index=False)

# Quartile 2: Assign agents to be in bottom quartile utilitarian or egalitarian based on their decision (low investment)
for_scheme = positive_quartile_p_values['Q1']
against_scheme = negative_quartile_p_values['Q4']
print(for_scheme)
print(against_scheme)
df = range_principles(df, against_scheme, for_scheme)
# Save the principles a file
principles_df = df[['country', 'egal', 'util']]
principles_df.rename(columns={'egal': 'rel', 'util': 'nonrel'}, inplace=True)
principles_df.to_csv("/data/results/principle_test_cases/15-01-2025-bottom-quartile-principles.csv", index=False)

## General support and general opposition principles using quartiles
for_scheme = positive_quartile_p_values['Q4'] + positive_quartile_p_values['Q3'] + positive_quartile_p_values['Q2']
against_scheme = negative_quartile_p_values['Q1'] + negative_quartile_p_values['Q2'] + negative_quartile_p_values['Q3']
print(for_scheme)
print(against_scheme)
df = range_principles(df, against_scheme, for_scheme)
# Save the principles a file
principles_df = df[['country', 'egal', 'util']]
principles_df.rename(columns={'egal': 'rel', 'util': 'nonrel'}, inplace=True)
principles_df.to_csv("/data/results/principle_test_cases/15-01-2025-general-support-principles.csv", index=False)

## General support and general opposition principles using quartiles
against_scheme = positive_quartile_p_values['Q4'] + positive_quartile_p_values['Q3'] + positive_quartile_p_values['Q2']
for_scheme = negative_quartile_p_values['Q1'] + negative_quartile_p_values['Q2'] + negative_quartile_p_values['Q3']

print(for_scheme)
print(against_scheme)
df = range_principles(df, against_scheme, for_scheme)
# Save the principles a file
principles_df = df[['country', 'egal', 'util']]
principles_df.rename(columns={'egal': 'rel', 'util': 'nonrel'}, inplace=True)
principles_df.to_csv("/data/results/principle_test_cases/15-01-2025-general-opposition-principles.csv", index=False)

## General support and general opposition principles using quartiles
for_scheme = positive_quartile_p_values['Q4'] + positive_quartile_p_values['Q3']
against_scheme = negative_quartile_p_values['Q1'] + negative_quartile_p_values['Q2']
print(for_scheme)
print(against_scheme)
df = range_principles(df, against_scheme, for_scheme)
# Save the principles a file
principles_df = df[['country', 'egal', 'util']]
principles_df.rename(columns={'egal': 'rel', 'util': 'nonrel'}, inplace=True)
principles_df.to_csv("/data/results/principle_test_cases/15-01-2025-50-pc-support-principles.csv", index=False)

## General support and general opposition principles using quartiles
against_scheme = positive_quartile_p_values['Q4'] + positive_quartile_p_values['Q3']
for_scheme = negative_quartile_p_values['Q1'] + negative_quartile_p_values['Q2']

print(for_scheme)
print(against_scheme)
df = range_principles(df, against_scheme, for_scheme)
# Save the principles a file
principles_df = df[['country', 'egal', 'util']]
principles_df.rename(columns={'egal': 'rel', 'util': 'nonrel'}, inplace=True)
principles_df.to_csv("/data/results/principle_test_cases/15-01-2025-50-pc-opposition-principles.csv", index=False)