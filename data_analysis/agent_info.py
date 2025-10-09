import pandas as pd
import numpy as np

# import agents file
agents_df = pd.read_csv("data/results/22-01-2025-agent-data.csv")
# Make decision and add as new column
agents_df['decision'] = np.nan  # Initialize the 'decision' column
for index, row in agents_df.iterrows():
    agents_df.at[index, 'decision'] = (row['Rel-Nonrel'] * row['a_div_rel']) + (row['Nonrel-Rel'] * row['a_div_nonrel'])
# import the agents principles and concat
principles_df = pd.read_csv("data/results/principle_test_cases/12-01-2025-principles.csv")
principles_df.rename(columns={'rel': 'egal', 'nonrel': 'util'}, inplace=True)
agents_df = pd.merge(agents_df, principles_df, on='country')

### Are hedonistic people more likely to support the action, or not?
more_nonrel_than_rel = agents_df[agents_df['nonrel'] > agents_df['rel']]
average_decision_value = more_nonrel_than_rel['decision'].mean()
more_nonrel_than_rel_count = more_nonrel_than_rel.shape[0]
print(f"Total Hedonists: {more_nonrel_than_rel_count}, Average Decision Value: {average_decision_value}")

### Are traditionalists more likely to support the action, or not?
more_rel = agents_df[agents_df['rel'] > agents_df['nonrel']]
average_decision_value = more_rel['decision'].mean()
more_rel_count = more_rel.shape[0]
print(f"Total Traditionalists: {more_rel_count}, Average Decision Value: {average_decision_value}")

## What does a FPTP vote look like?
total_decision_value = agents_df['decision'].sum()
print(f"Total Decision Value: {total_decision_value}")
mean_decision_value = agents_df['decision'].mean()
print(f"Mean Decision Value: {mean_decision_value}")

## Are egalitarians more likely to support the action, or not?
more_egal = agents_df[agents_df['egal'] > agents_df['util']]
average_decision_value = more_egal['decision'].mean()
more_egal_count = more_egal.shape[0]
print(f"Total Egalitarians: {more_egal_count}, Average Decision Value: {average_decision_value}")

## Are utilitarians more likely to support the action, or not?
more_util = agents_df[agents_df['util'] > agents_df['egal']]
average_decision_value = more_util['decision'].mean()
more_util_count = more_util.shape[0]
print(f"Total Utilitarians: {more_util_count}, Average Decision Value: {average_decision_value}")

more_nonrel_than_rel_sorted = more_nonrel_than_rel.sort_values(by='decision')
negative_decisions = more_nonrel_than_rel_sorted[more_nonrel_than_rel_sorted['decision'] < 0].shape[0]
positive_decisions = more_nonrel_than_rel_sorted[more_nonrel_than_rel_sorted['decision'] >= 0].shape[0]
print(f"Number of negative decisions: {negative_decisions}")
print(f"Number of positive decisions: {positive_decisions}")

negative_a_div_rel_count = (agents_df['a_div_rel'] < 0).sum()
positive_a_div_rel_count = (agents_df['a_div_rel'] >= 0).sum()

print(f"Number of negative a_div_rel: {negative_a_div_rel_count}")
print(f"Number of positive a_div_rel: {positive_a_div_rel_count}")

# Create a new column to indicate if an agent is more rel than nonrel
agents_df['more_rel_than_nonrel'] = agents_df['rel'] > agents_df['nonrel']

# Calculate the correlation between 'more_rel_than_nonrel' and 'decision'
correlation = agents_df['more_rel_than_nonrel'].astype(int).corr(agents_df['decision'])
print(f"Correlation between being more rel than nonrel and decision: {correlation}")

agents_df['more_nonrel_than_rel'] = agents_df['nonrel'] > agents_df['rel']
#calculate correlation between 'more_nonrel_than_rel' and 'decision'
correlation = agents_df['more_nonrel_than_rel'].astype(int).corr(agents_df['decision'])
print(f"Correlation between being more nonrel than rel and decision: {correlation}")