from recipes.models import Recipe
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import textwrap  # Required for label wrapping in pie chart

# Converts matplotlib plot to base64 PNG for embedding in HTML
def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')  # Save plot to buffer
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png).decode('utf-8')  # Encode as base64
    buffer.close()
    return graph

# Generates a chart based on chart_type and provided DataFrame
def get_chart(chart_type, data, **kwargs):
    plt.switch_backend('AGG')  # Use non-GUI backend suitable for servers
    fig = plt.figure(figsize=(8, 6))  # Set figure size

    labels = kwargs.get('labels', [])

    # Compute ingredient count per recipe
    data['Ingredient Count'] = data['Ingredients'].apply(lambda x: len(x.split(',')))

    if chart_type == '#1':
        # Bar Chart: Cooking Time by Recipe
        plt.bar(labels, data['Cooking Time (min)'], color='skyblue')
        plt.title("Cooking Time by Recipe")
        plt.ylabel("Minutes")
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.grid(axis='y', linestyle='--', alpha=0.6)

    elif chart_type == '#2':
        # Pie Chart: Recipes grouped by Difficulty
        difficulty_labels = []
        difficulty_values = []

        for difficulty in data['Difficulty'].unique():
            # Get names of recipes under each difficulty
            subset = data[data['Difficulty'] == difficulty]
            names = subset['Name'].str.replace(r'<[^>]*>', '', regex=True).tolist()  # Strip HTML
            full_label = f"{difficulty}: " + ", ".join(names)
            wrapped_label = "\n".join(textwrap.wrap(full_label, width=25))  # Wrap text for readability

            difficulty_labels.append(wrapped_label)
            difficulty_values.append(len(subset))

        plt.pie(
            difficulty_values,
            labels=difficulty_labels,
            autopct='%1.1f%%',         # Show percentage
            textprops={'fontsize': 9},
            startangle=90,             # Start angle for rotation
            pctdistance=0.8,           # Position of percent text
            labeldistance=1.2          # Position of label
        )
        plt.title("Recipes by Difficulty")

    elif chart_type == '#3':
        # Line Chart: Ingredient Count per Recipe
        sorted_data = data.copy()
        sorted_data['Name'] = sorted_data['Name'].str.replace(r'<[^>]*>', '', regex=True)
        sorted_data = sorted_data.sort_values(by='Ingredient Count')

        plt.plot(
            sorted_data['Name'],
            sorted_data['Ingredient Count'],
            marker='o',
            color='orange'
        )
        plt.title("Ingredient Count per Recipe")
        plt.ylabel("Count")
        plt.xticks(rotation=45, ha='right', fontsize=9)
        plt.grid(linestyle='--', alpha=0.6)

    plt.tight_layout()  # Adjust layout to avoid overlapping labels
    return get_graph()  # Return base64 string of the plot
