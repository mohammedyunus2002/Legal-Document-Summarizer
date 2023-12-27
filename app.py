from flask import Flask, request, jsonify
import os
import google.generativeai as genai
import PyPDF2
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
import nltk
from dotenv import load_dotenv  

nltk.download('punkt')

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)

for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)

model = genai.GenerativeModel('gemini-pro')

def get_gemini_response(question):
    response = None
    try:
        response = model.generate_content(question)
        return response
    except Exception as e:
        print(f"Error: {e}")
        return None

def extract_text_from_pdf(pdf_filepath):
    with open(pdf_filepath, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text

def extract_legal_concepts(response):
    legal_concepts = []

    if response and hasattr(response, 'candidates') and response.candidates:
        try:
            generated_text = response.candidates[0].content.parts[0].text
            terms_to_identify = ["Terms of Use", "Privacy Policy", "Limitation of Liability", "Indemnification", "Disclaimer", "Intellectual Property"]
            sentences = generated_text.split('.')
            for sentence in sentences:
                for term in terms_to_identify:
                    if term in sentence:
                        legal_concepts.append(sentence.strip())
                        break
        except (AttributeError, IndexError):
            print("Error: Unable to extract text from the response or index out of range")

    return legal_concepts


def generate_summary(text, num_sentences=3):
    parser = PlaintextParser.from_string(text, Tokenizer('english'))
    summarizer = LsaSummarizer()
    summary = summarizer(parser.document, num_sentences)
    return ' '.join(str(sentence) for sentence in summary)

app = Flask(__name__)

UPLOADER_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOADER_FOLDER   

if not os.path.exists(UPLOADER_FOLDER):
    os.makedirs(UPLOADER_FOLDER)

document_summaries = {}

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    uploaded_filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(uploaded_filepath)
    
    document_content = extract_text_from_pdf(uploaded_filepath)
    response = get_gemini_response(document_content)

    app.logger.info(f"Generated response: {response}")
    print(response.candidates[0].content.parts)

    legal_concepts = extract_legal_concepts(response)
    print(legal_concepts)

    summary = generate_summary(document_content)
    print(summary)

    document_id = len(document_summaries) + 1
    document_summaries[document_id] = {'filename': file.filename, 'summary': summary}

    return jsonify({'document_id': document_id, 'message': 'File uploaded and processed successfully', 'legal_concepts': legal_concepts, 'summary': summary})

@app.route('/get_summary/<int:document_id>', methods=['GET'])
def get_summary(document_id):
    if document_id in document_summaries:
        return jsonify(document_summaries[document_id])
    else:
        return jsonify({'error': 'Document ID not found'})

if __name__ == '__main__':
    app.run(debug=True)
