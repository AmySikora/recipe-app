from recipes.models import Recipe
from io import BytesIO
import base64
import matplotlib.pyplot as plt

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png).decode('utf-8')
    buffer.close()
    return graph

def get_chart(chart_type, data, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(8, 6))
    labels = kwargs.get('labels', [])
    data['Ingredient Count'] = data['Ingredients'].apply(lambda x: len(x.split(',')))

    if chart_type == '#1':
        # Bar Chart - Cooking Time
        plt.bar(labels, data['Cooking Time (min)'], color='skyblue')
        plt.title("Cooking Time by Recipe")
        plt.ylabel("Minutes")
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.grid(axis='y', linestyle='--', alpha=0.6)

    elif chart_type == '#2':
        # Pie Chart - Recipes by Difficulty with Names
        difficulty_labels = []
        difficulty_values = []

        for difficulty in data['Difficulty'].unique():
            subset = data[data['Difficulty'] == difficulty]
            names = subset['Name'].str.replace(r'<[^>]*>', '', regex=True).tolist()
            label = f"{difficulty}: " + ", ".join(names)
            difficulty_labels.append(label)
            difficulty_values.append(len(subset))

        plt.pie(
            difficulty_values,
            labels=difficulty_labels,
            autopct='%1.1f%%',
            startangle=90,
            textprops={'fontsize': 9}
        )
        plt.title("Recipes by Difficulty")

    elif chart_type == '#3':
        # Line Chart - Ingredient Count
        sorted_data = data.copy()
        sorted_data['Name'] = sorted_data['Name'].str.replace(r'<[^>]*>', '', regex=True)
        sorted_data = sorted_data.sort_values(by='Ingredient Count')

        plt.plot(sorted_data['Name'], sorted_data['Ingredient Count'], marker='o', color='orange')
        plt.title("Ingredient Count per Recipe")
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.grid(linestyle='--', alpha=0.6)

    plt.tight_layout()
    return get_graph()
