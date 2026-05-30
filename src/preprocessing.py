import re
import string
import PyPDF2
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Ensure required NLTK resources are available
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

def extract_text_from_pdf(pdf_file_path_or_bytes):
    """Extracts text from a PDF file."""
    text = ""
    try:
        reader = PyPDF2.PdfReader(pdf_file_path_or_bytes)
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text

def extract_text_from_txt(txt_file_path_or_bytes):
    """Extracts text from a TXT file."""
    try:
        if isinstance(txt_file_path_or_bytes, str):
            with open(txt_file_path_or_bytes, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            return txt_file_path_or_bytes.read().decode('utf-8')
    except Exception as e:
        print(f"Error reading TXT: {e}")
        return ""

def clean_text(text):
    """
    Cleans text by removing URLs, special characters, and extra spaces.
    Converts to lowercase.
    """
    if not isinstance(text, str):
        text = str(text)
        
    text = text.lower() # Convert to lowercase
    text = re.sub(r'http\S+', '', text) # Remove URLs
    text = re.sub(r'www\.\S+', '', text) # Remove URLs
    text = re.sub(r'<.*?>', '', text) # Remove HTML tags
    text = re.sub(r'[%s]' % re.escape(string.punctuation), ' ', text) # Remove punctuation
    text = re.sub(r'\n', ' ', text) # Remove newlines
    text = re.sub(r'\s+', ' ', text).strip() # Remove extra spaces
    
    return text

def preprocess_text(text):
    """
    Applies tokenization, stopword removal, and lemmatization.
    """
    if not text:
        return ""
        
    cleaned_text = clean_text(text)
    
    # Tokenization
    tokens = word_tokenize(cleaned_text)
    
    # Stopword removal and lemmatization
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    
    processed_tokens = [
        lemmatizer.lemmatize(word) 
        for word in tokens 
        if word not in stop_words and len(word) > 2
    ]
    
    return ' '.join(processed_tokens)
