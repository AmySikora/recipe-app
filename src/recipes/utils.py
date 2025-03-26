from recipes.models import Recipe
from io import BytesIO
import base64
import matplotlib.pyplot as plt

# Optional helper (you can delete if not used)
def get_recipename_from_id(val):
    return Recipe.objects.get(id=val)

# Convert matplotlib chart to base64 image
def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png).decode('utf-8')
    buffer.close()
    return graph

# Create chart based on type
def get_chart(chart_type, data, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(8, 4))
    labels = kwargs.get('labels', [])

    if chart_type == '#1':  # Bar chart
        # Count ingredients for each recipe
        data['Ingredient Count'] = data['Ingredients'].apply(lambda x: len(x.split(',')))

        x = range(len(labels))
        width = 0.35

        # Bar chart with side-by-side bars
        plt.bar([i - width/2 for i in x], data['Cooking Time (min)'], width=width, label='Cooking Time')
        plt.bar([i + width/2 for i in x], data['Ingredient Count'], width=width, label='Ingredient Count')

        plt.xticks(ticks=x, labels=labels, rotation=45)
        plt.ylabel("Minutes / Count")
        plt.title("Recipe Cooking Time vs Ingredient Count")
        plt.legend()

    elif chart_type == '#2':  # Pie chart
        plt.pie(data['Cooking Time (min)'], labels=labels, autopct='%1.1f%%')
        plt.title("Cooking Time Distribution")

    elif chart_type == '#3':  # Line chart
        plt.plot(labels, data['Cooking Time (min)'], marker='o')
        plt.xticks(rotation=45)
        plt.ylabel("Cooking Time (min)")
        plt.title("Cooking Time Trend")

    else:
        print('Unknown chart type')

    plt.tight_layout()
    return get_graph()
