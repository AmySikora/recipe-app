from recipes.models import Recipe
from io import BytesIO
import base64
import matplotlib.pyplot as plt

# Convert recipe ID to recipe object
def get_recipename_from_id(val):
    recipename = Recipe.objects.get(id=val)
    return recipename

# Convert matplotlib chart to image string
def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

# Generate chart based on selected type and data
def get_chart(chart_type, data, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(6, 3))

    if chart_type == '#1':
        # Bar chart: recipe name vs cooking time
        plt.bar(data['name'], data['cooking_time'])
        plt.ylabel("Cooking Time (min)")
        plt.xticks(rotation=45)
        plt.title("Cooking Time by Recipe")

    elif chart_type == '#2':
        # Pie chart: cooking time
        labels = kwargs.get('labels')
        plt.pie(data['cooking_time'], labels=labels, autopct='%1.1f%%')
        plt.title("Cooking Time Distribution")

    elif chart_type == '#3':
        # Line chart: recipe name vs cooking time
        plt.plot(data['name'], data['cooking_time'], marker='o')
        plt.ylabel("Cooking Time (min)")
        plt.xticks(rotation=45)
        plt.title("Cooking Time Trend")

    else:
        print('Unknown chart type')

    plt.tight_layout()
    return get_graph()
