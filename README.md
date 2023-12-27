Project Documentation: Legal Document Summarizer
Introduction
This document provides an overview of the Legal Document Summarizer project, detailing the steps taken to develop and deploy the application. The project leverages Flask, Docker, Helm, and Google Generative AI to extract legal concepts and generate summaries from uploaded legal documents in PDF format.

Technologies Used
Flask: A lightweight web framework used to create the backend API.
Docker: Containerization technology to package the application and its dependencies.
Helm: A Kubernetes package manager used to define, install, and manage Kubernetes applications.
Google Generative AI: A high-level API client library and tools for leveraging Google's Generative AI models.
Project Structure
Backend (Flask App)
The backend is a Flask application that exposes two endpoints:

/upload (POST): Accepts PDF files, extracts text, generates a response using Google Generative AI, and provides legal concepts and summaries.
/get_summary/<document_id> (GET): Retrieves additional details or summaries based on the document ID.
Frontend (Streamlit App)
The frontend is a Streamlit application that allows users to upload PDF files and view the generated legal concepts and summaries.

Development Steps
1. Set Up Flask Application
Developed a Flask application with routes for file upload and summary retrieval.
Integrated Google Generative AI for content generation.
2. Dockerization
Created a Dockerfile to package the Flask application into a Docker image.
Built and tagged the Docker image.
3. Helm Chart Creation
Created a Helm chart with the following components:
Chart.yaml: Metadata about the Helm chart.
values.yaml: Default values for the Flask app.
templates/deployment.yaml: Kubernetes Deployment configuration.
templates/service.yaml: Kubernetes Service configuration.
4. Helm Deployment
Packaged the Helm chart using helm package ..
Installed the Helm chart on a Kubernetes cluster using helm install.
5. Streamlit Frontend
Developed a Streamlit app for user interaction with the Flask backend.
Implemented file upload functionality and displayed legal concepts and summaries.
Usage
Upload a legal document in PDF format using the Streamlit frontend.
View the generated legal concepts and summaries.
Optionally, request more details or summaries based on the document ID.
Conclusion
The Legal Document Summarizer project successfully combines Flask, Docker, Helm, and Google Generative AI to provide a streamlined solution for extracting legal concepts and generating summaries from legal documents.
