import streamlit as st
import json
from aggregation2 import AggregationTree

# Title and instructions
st.title("Aggregation Tree Viewer")
st.write("Enter the file path of the JSON file to compute group-by statistics and visualize the tree.")

# Input for the file path
file_path = st.text_input("Enter the JSON file path:")

if file_path:
    try:
        # Load the JSON data from the provided file path
        with open(file_path, 'r') as file:
            data = json.load(file)

        # Validate the structure of the JSON file
        if not all(
            isinstance(record, dict) and 
            "fname" in record and 
            "bnum" in record and 
            "os" in record and 
            "pr" in record 
            for record in data
        ):
            st.error("Invalid JSON format. Ensure the file contains records with 'fname', 'bnum', 'os', and 'pr' fields.")
        else:
            # Display the loaded data
            st.write("Loaded Data:")
            st.json(data)

            # Create AggregationTree instance
            aggregation_tree = AggregationTree(data)

            # Select group-by column
            group_by_column = st.selectbox("Select a column to group by:", ["fname", "bnum", "os"])

            # Compute and display results
            if st.button("Compute Statistics"):
                result = aggregation_tree.compute_groupby(group_by_column)
                st.write(f"Group-by Results for '{group_by_column}':")
                st.json(result)

            # Generate and display the tree image
            if st.button("Generate Tree Visualization"):
                graph = aggregation_tree.root.generate_graphviz()
                graph_path = "tree_visualization"
                graph.render(graph_path, cleanup=True)
                st.image(f"{graph_path}.png", caption="Aggregation Tree Visualization")
    except FileNotFoundError:
        st.error("File not found. Please check the file path and try again.")
    except json.JSONDecodeError:
        st.error("Invalid JSON file. Ensure the file contains valid JSON data.")