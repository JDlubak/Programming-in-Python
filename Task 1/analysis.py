import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools

full_data = pd.read_csv("data.csv", header=None)
category = full_data[0]
data = full_data.iloc[:, 1:]
labels = ('Length [mm]', 'Diameter [mm]', 'Height [mm]',
          'Whole weight [g]', 'Shucked weight [g]',
          'Viscera weight [g]', 'Shell weight [g]', 'Rings')

table_1 = category.value_counts().reset_index()
table_1.columns = ['', 'count']
table_1['%'] = round((table_1['count'] / len(category)) * 100, 2)
table_1[''] = table_1[''].replace({'M': 'Male',
                                   'F': 'Female',
                                   'I': 'Infant'})
print(table_1.to_string(index=False))

data.columns = labels
table_2 = data.describe().T
table_2 = table_2[['mean', 'std', 'min',
                   '25%', '50%', '75%', 'max']].round(3)
print(table_2)

plt.bar(table_1[''], table_1['count'],
        color='green', edgecolor='black')
plt.title('Counts of occurrences of each category')
plt.xlabel('Category')
plt.ylabel('Count')
plt.show()

fig, axes = plt.subplots(4, 2, figsize=(8, 12))
axes = axes.flatten()
for i, label in enumerate(labels):
    axes[i].hist(data[label], bins=30, color='skyblue',
                 edgecolor='black')
    axes[i].set_title(label)
    axes[i].set_xlabel(label)
    axes[i].set_ylabel('Frequency')
plt.tight_layout()
plt.show()

pairs = list(itertools.combinations(labels, 2))
fig, axes = plt.subplots(14, 2, figsize=(6, 42))
axes = axes.flatten()
for i, (first_label, second_label) in enumerate(pairs):
    axes[i].scatter(data[first_label], data[second_label])
    axes[i].set_ylabel(first_label)
    axes[i].set_xlabel(second_label)
plt.tight_layout()
plt.show()

correlation_matrix = data[labels].corr()
correlation_matrix = correlation_matrix.round(3)
short_names = {
    'Length [mm]': 'L',
    'Diameter [mm]': 'D',
    'Height [mm]': 'H',
    'Whole weight [g]': 'W_W',
    'Shucked weight [g]': 'Shu_W',
    'Viscera weight [g]': 'V_W',
    'Shell weight [g]': 'She_W',
    'Rings': 'R'
}
correlation_matrix = correlation_matrix.rename(columns=short_names)
print(correlation_matrix)

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, fmt=".3f",
            cmap="Reds_r", cbar=True, square=True)
plt.title("linear correlation matrix")
plt.tight_layout()
plt.show()

plt.figure(figsize=(8, 6))
x_label = 'Length [mm]'
y_label = 'Diameter [mm]'
sns.regplot(data, x=x_label, y=y_label,
            scatter_kws={'color': 'red'},
            line_kws={'color': 'blue', 'linewidth': 3})
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.show()

grouped_data = full_data
grouped_data.columns = ['Sex'] + list(data.columns)
grouped_data = grouped_data.groupby('Sex').describe().round(3)

table_3 = grouped_data.stack(future_stack=True, level=0)
table_3 = table_3[['mean', 'std', 'min', '25%', '50%', '75%', 'max']]
table_3.index.names = ['Sex', 'Feature']
table_3 = table_3.swaplevel('Sex', 'Feature')
table_3 = table_3.loc[list(labels)]
table_3 = table_3.rename(index={'M': 'Male',
                                'F': 'Female',
                                'I': 'Infant'}, level='Sex')
print(table_3)

fig, axes = plt.subplots(4, 2, figsize=(8, 12))
axes = axes.flatten()

for i, label in enumerate(labels):
    full_data.boxplot(column=label, by='Sex', ax=axes[i])
    axes[i].set_title('')
    axes[i].set_xlabel('Sex')
    axes[i].set_ylabel(label)

plt.suptitle('')
plt.tight_layout()
plt.show()
