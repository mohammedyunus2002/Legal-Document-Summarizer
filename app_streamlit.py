import requests
import streamlit as st

def upload_file(file):
    files = {'file': file}
    response = requests.post('http://127.0.0.1:5000/upload', files=files)
    return response.json()

def get_summary(document_id):
    response = requests.get(f'http://127.0.0.1:5000/get_summary/{document_id}')
    return response.json()

st.title('Legal Document Summarizer')

uploaded_file = st.file_uploader('Choose a PDF file', type=['pdf'])

if uploaded_file is not None:
    st.write('File Uploaded!')
    st.write('Processing...')

    # Upload file to Flask server
    flask_response = upload_file(uploaded_file)

    # Display results
    if 'error' in flask_response:
        st.error(flask_response['error'])
    else:
        document_id = flask_response['document_id']
        legal_concepts = flask_response['legal_concepts']
        summary = flask_response['summary']

        st.success('Processing complete!')
        st.write(f'Legal Concepts: {legal_concepts}')
        st.write(f'Summary: {summary}')

        # Optionally, you can request more details or summaries based on the document_id
        more_details_button = st.button('Get More Details')
        if more_details_button:
            more_details = get_summary(document_id)
            st.write('More Details:', more_details)
