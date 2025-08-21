import streamlit as st, pandas as pd, numpy as np

# Generate example CSV with random grades.
def generate_example():
    students = ["Alice", "Bob", "Charlie", "David", "Eva"]
    columns = [str(i) for i in range(1, 16)]

    # Fill in the table with random grades from 0-100
    example_df = pd.DataFrame(
        np.random.randint(0, 101, size=(len(students), len(columns))),
        columns=columns
    )
    example_df.insert(0, "Name", students)

    # Convert to CSV.
    csv = example_df.to_csv(index=False)

    # Create download button for the CSV.
    st.download_button(
        label="📥 Download Example CSV",
        data=csv,
        file_name="example_grades.csv",
        mime="text/csv"
    )