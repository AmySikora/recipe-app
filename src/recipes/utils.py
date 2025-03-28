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
    fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(8, 12))  # vertical layout

    labels = kwargs.get('labels', [])
    data['Ingredient Count'] = data['Ingredients'].apply(lambda x: len(x.split(',')))

    # Bar Chart
    axs[0].bar(labels, data['Cooking Time (min)'], color='skyblue')
    axs[0].set_title("Cooking Time")
    axs[0].set_ylabel("Minutes")
    axs[0].tick_params(axis='x', rotation=45)

    # Pie Chart
    difficulty_counts = data['Difficulty'].value_counts()
    axs[1].pie(difficulty_counts, labels=difficulty_counts.index, autopct='%1.1f%%')
    axs[1].set_title("Difficulty")

    # Line Chart
    sorted_data = data.copy()
    sorted_data['Name'] = sorted_data['Name'].str.replace(r'<[^>]*>', '', regex=True)  # Remove HTML
    sorted_data = sorted_data.sort_values(by='Ingredient Count')
    axs[2].plot(sorted_data['Name'], sorted_data['Ingredient Count'], marker='o', color='orange')
    axs[2].set_title("Ingredient Count")
    axs[2].set_ylabel("Count")
    axs[2].tick_params(axis='x', rotation=45)

    plt.tight_layout()
    return get_graph()
