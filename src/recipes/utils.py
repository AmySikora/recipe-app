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
    fig = plt.figure(figsize=(8, 4))
    labels = kwargs.get('labels', [])

    data['Ingredient Count'] = data['Ingredients'].apply(lambda x: len(x.split(',')))

    if chart_type == '#1':  # Bar chart
        plt.bar(labels, data['Cooking Time (min)'])
        plt.xticks(rotation=45)
        plt.ylabel("Cooking Time (min)")
        plt.title("Cooking Time by Recipe")

    elif chart_type == '#2':  # Pie chart: difficulty distribution
        difficulty_counts = data['Difficulty'].value_counts()
        plt.pie(difficulty_counts, labels=difficulty_counts.index, autopct='%1.1f%%')
        plt.title("Recipe Difficulty Distribution")

    elif chart_type == '#3':  # Line chart
        sorted_data = data.sort_values(by='Ingredient Count')
        plt.plot(sorted_data['Name'], sorted_data['Ingredient Count'], marker='o')
        plt.xticks(rotation=45)
        plt.ylabel("Ingredient Count")
        plt.title("Ingredient Count per Recipe")

    else:
        plt.text(0.5, 0.5, 'No chart type selected', ha='center')

    plt.tight_layout()
    return get_graph()
