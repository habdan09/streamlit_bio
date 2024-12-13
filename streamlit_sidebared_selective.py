import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Correct file path using raw string
dataset_path = r"C:\Users\habib\Desktop\corrected_csv.csv"

# App Header
st.header("Genomic Data Analysis Dashboard")

# Title and Subtitle
st.title("Comprehensive Genomic Metrics Visualization")
st.subheader("Interactive Data Exploration")
st.write("""
Welcome to the Genomic Data Analysis Dashboard! This tool allows you to interactively 
explore and visualize your genomic metrics.
""")

# Load the dataset
try:
    data = pd.read_csv(dataset_path)
    st.write("### Preview of Uploaded Data")
    st.dataframe(data)
except FileNotFoundError:
    st.error(f"Dataset not found at path: {dataset_path}")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the dataset: {e}")
    st.stop()

# Interactive Visualization Section
st.header("Interactive Data Visualization")

# Prepare column options
column_options = list(data.columns)
column_options.append('Frequency')  # Add frequency as a special option

# Create sidebar for visualization controls
with st.sidebar:
    st.subheader("Visualization Settings")
    
    # X-axis selection
    x_column = st.selectbox(
        "Select X-axis Column", 
        column_options, 
        index=column_options.index('%GC') if '%GC' in column_options else 0
    )
    
    # Y-axis selection
    y_column = st.selectbox(
        "Select Y-axis Column", 
        column_options, 
        index=column_options.index('Frequency') if 'Frequency' in column_options else 0
    )
    
    # Chart type selection
    chart_type = st.selectbox(
        "Select Visualization Type",
        ["Line Chart", "Scatter Plot", "Bar Chart"]
    )

# Prepare data for visualization
if y_column == 'Frequency':
    # Calculate frequency of x-axis column
    plot_data = data[x_column].value_counts().reset_index()
    plot_data.columns = [x_column, 'Frequency']
    plot_data = plot_data.sort_values(by=x_column)
else:
    plot_data = data

# Create interactive plot based on user selection
if chart_type == "Line Chart":
    fig = px.line(
        plot_data, 
        x=x_column, 
        y=y_column if y_column != 'Frequency' else 'Frequency',
        title=f"{x_column} vs {y_column}",
        labels={x_column: x_column, y_column: y_column}
    )
elif chart_type == "Scatter Plot":
    fig = px.scatter(
        plot_data, 
        x=x_column, 
        y=y_column if y_column != 'Frequency' else 'Frequency',
        title=f"{x_column} vs {y_column}",
        labels={x_column: x_column, y_column: y_column}
    )
else:  # Bar Chart
    fig = px.bar(
        plot_data, 
        x=x_column, 
        y=y_column if y_column != 'Frequency' else 'Frequency',
        title=f"{x_column} vs {y_column}",
        labels={x_column: x_column, y_column: y_column}
    )

# Customize the layout
fig.update_layout(
    height=600,
    width=800,
    xaxis_title=x_column,
    yaxis_title=y_column,
    title_x=0.5,
)

# Display the interactive plot
st.plotly_chart(fig, use_container_width=True)

# Display selected data statistics
st.subheader("Selected Data Statistics")
st.write(f"**X-axis (Column):** {x_column}")
st.write(f"**Y-axis (Column):** {y_column}")

# Basic statistics of selected columns
if y_column == 'Frequency':
    st.dataframe(plot_data)
else:
    st.dataframe(plot_data[[x_column, y_column]])

# Footer/Instructions
st.write("---")
st.write("""
### Dashboard Features:
- Interactively select X and Y axes
- Choose between Line, Scatter, and Bar charts
- Explore data distributions and relationships
""")