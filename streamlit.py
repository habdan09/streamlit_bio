import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
#adss
dataset_path = r"C:\Users\habib\Desktop\corrected_csv.csv"

st.header("Genomic Data Analysis Dashboard")


st.title("Genomic Metrics Visualization")
st.subheader("Interactive Data Exploration")
st.write("""
Welcome to the Genomic Data Analysis Dashboard! This tool allows you to interactively 
explore and visualize your genomic metrics. 
""")

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

st.header("Interactive Data Visualization")

# line chart for Fragments vs Samples
if 'ID SAMPLE' in data.columns and 'Fragments' in data.columns:
    try:
        
        data['Fragments'] = data['Fragments'].str.replace(',', '').astype(float)

        
        fig = px.line(
            data,
            x='ID SAMPLE',
            y='Fragments',
            title='Line Chart of Fragments vs. Samples',
            labels={'ID SAMPLE': 'Sample', 'Fragments': 'Fragments'},
            markers=True
        )

        
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"An error occurred while generating the line chart: {e}")
else:
    st.warning("Required columns 'ID SAMPLE' and 'Fragments' are not present in the dataset.")


st.subheader("Explore Additional Metrics")

def generate_bar_chart(column_name):
    """Function to generate a bar chart for the selected column."""
    try:
        fig = px.bar(
            data,
            x='ID SAMPLE',
            y=column_name,
            title=f'Bar Chart of {column_name} vs. Samples',
            labels={'ID SAMPLE': 'Sample', column_name: column_name}
        )
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"An error occurred while generating the bar chart for {column_name}: {e}")

# Dropdown for column selection
available_columns = [col for col in data.columns if data[col].dtype in ['float64', 'int64']]
selected_column = st.selectbox("Select a numeric column for bar chart visualization:", available_columns)

if selected_column:
    generate_bar_chart(selected_column)

# Footer
st.markdown("---")
st.caption("Developed by [H@bib]. Powered by Streamlit and Plotly.")