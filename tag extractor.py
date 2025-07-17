import streamlit as st
import fitz  # PyMuPDF
import re
import pandas as pd
from io import BytesIO

# Streamlit app title
st.title("Tagnummers Extractor uit PDF")

# Upload PDF file
uploaded_file = st.file_uploader("Upload een PDF-bestand", type="pdf")

# Regex pattern for tag numbers like T.001.5001 or EM.003.9101
tag_pattern = re.compile(r'\b[A-Z]{1,3}\.\d{3}\.\d{4}\b')

if uploaded_file:
    # Read PDF with PyMuPDF
    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
    tag_numbers = set()

    # Extract text and find tag numbers
    for page in doc:
        text = page.get_text()
        matches = tag_pattern.findall(text)
        tag_numbers.update(matches)

    # Convert to DataFrame
    df = pd.DataFrame(sorted(tag_numbers), columns=["Tag Number"])

    # Show results
    st.subheader("Gevonden Tagnummers")
    st.dataframe(df)

    # Download as Excel
    output = BytesIO()
    df.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)
    st.download_button(
        label="📥 Download als Excel",
        data=output,
        file_name="tag_numbers.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
