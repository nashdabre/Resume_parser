from flask import Flask, request, jsonify, render_template
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
import re
import PyPDF2
import docx2txt
import io

# Load spaCy model for text processing
nlp = spacy.load("en_core_web_sm")

# Custom stopword list to avoid removing key terms
custom_stopwords = nlp.Defaults.stop_words.difference(
    {"python", "java", "aws", "docker", "kubernetes", "ci", "cd", "machine", "learning", "data", "algorithms",
     "structures", "cloud"})

# Initialize Flask app
app = Flask(__name__)


# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text() or ''
        return text
    except Exception as e:
        print(f"Error reading PDF file: {e}")
        return ""


# Function to extract text from DOCX
def extract_text_from_docx(docx_file):
    try:
        return docx2txt.process(docx_file)
    except Exception as e:
        print(f"Error reading DOCX file: {e}")
        return ""


# Function to clean and preprocess text
def preprocess_text(text):
    # Convert to lowercase and remove special characters, keep only letters and spaces
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)

    # Lemmatize using spaCy, remove custom stopwords, and keep only meaningful words
    doc = nlp(text)
    return " ".join([token.lemma_ for token in doc if
                     not token.is_stop and token.text not in custom_stopwords and len(token.text) > 2])


# Function to compute ATS score based on cosine similarity
def compute_ats_score(resume_text, job_desc_text):
    # Preprocess resume and job description
    resume_text = preprocess_text(resume_text)
    job_desc_text = preprocess_text(job_desc_text)

    # Vectorize using TF-IDF
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume_text, job_desc_text])

    # Compute cosine similarity between resume and job description
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])

    # Return ATS score as percentage
    return round(similarity[0][0] * 100, 2)


# Route to serve the front-end page
@app.route('/')
def index():
    return render_template('index.html')


# API endpoint for calculating the ATS score
@app.route('/ats_score', methods=['POST'])
def ats_score():
    try:
        # Get resume and job description from the request
        resume_file = request.files['resume']
        job_desc_file = request.files['job_description']

        # Read and process the resume
        resume_ext = resume_file.filename.split('.')[-1].lower()
        if resume_ext == 'pdf':
            resume_text = extract_text_from_pdf(io.BytesIO(resume_file.read()))
        elif resume_ext == 'docx':
            resume_text = extract_text_from_docx(io.BytesIO(resume_file.read()))
        else:
            resume_text = resume_file.read().decode('utf-8')  # Assume plain text if not PDF or DOCX

        # Read and process the job description
        job_desc_ext = job_desc_file.filename.split('.')[-1].lower()
        if job_desc_ext == 'pdf':
            job_desc_text = extract_text_from_pdf(io.BytesIO(job_desc_file.read()))
        elif job_desc_ext == 'docx':
            job_desc_text = extract_text_from_docx(io.BytesIO(job_desc_file.read()))
        else:
            job_desc_text = job_desc_file.read().decode('utf-8')  # Assume plain text

        # Check for empty resume or job description
        if not resume_text.strip() or not job_desc_text.strip():
            return jsonify({'error': 'Empty resume or job description. Please check the files and try again.'}), 400

        # Calculate ATS score
        ats_score = compute_ats_score(resume_text, job_desc_text)

        # Return ATS score as JSON
        return jsonify({'ats_score': ats_score})

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'error': 'An error occurred while processing the files. Please try again.'}), 500


# Run the Flask app
if __name__ == "__main__":
    app.run()
