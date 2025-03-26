from recipes.models import Recipe
from io import BytesIO
import base64
import matplotlib.pyplot as plt

# Optional helper function (can be removed if unused)
def get_recipename_from_id(val):
    recipename = Recipe.objects.get(id=val)
    return recipename

# Convert matplotlib chart to image string
def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png).decode('utf-8')
    buffer.close()
    return graph

# Generate chart based on selected type and data
def get_chart(chart_type, data, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(6, 3))

    # Get labels passed from the view
    labels = kwargs.get('labels', [])

    if chart_type == '#1':
        # Bar chart: recipe name vs cooking time
        plt.bar(labels, data['Cooking Time (min)'])
        plt.ylabel("Cooking Time (min)")
        plt.xticks(rotation=45)
        plt.title("Cooking Time by Recipe")

    elif chart_type == '#2':
        # Pie chart: breakdown of cooking time
        plt.pie(data['Cooking Time (min)'], labels=labels, autopct='%1.1f%%')
        plt.title("Cooking Time Distribution")

    elif chart_type == '#3':
        # Line chart: recipe name vs cooking time
        plt.plot(labels, data['Cooking Time (min)'], marker='o')
        plt.ylabel("Cooking Time (min)")
        plt.xticks(rotation=45)
        plt.title("Cooking Time Trend")

    else:
        print('Unknown chart type')

    plt.tight_layout()
    return get_graph()
