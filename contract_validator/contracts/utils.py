import fitz
import logging
from io import BytesIO
from transformers import BartForConditionalGeneration, BartTokenizer
import spacy
import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Load models and tokenizers
bart_tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
bart_model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
nlp = spacy.load("en_core_web_sm")

bert_model_load_path = "bert-base-uncased"  # Use the correct public model identifier

bert_model = BertForSequenceClassification.from_pretrained(bert_model_load_path)
bert_tokenizer = BertTokenizer.from_pretrained(bert_model_load_path)

device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
bert_model.to(device)

def extract_text_from_pdf(file_path):
    try:
        text = ''
        doc = fitz.open(stream=BytesIO(file_path), filetype='pdf')
        for page in doc:
            text += page.get_text("text") + '\n'
        return text
    except Exception as e:
        logging.error(f"Error reading PDF: {e}")
        raise ValueError(f"Error reading PDF: {e}")

def split_text(text, chunk_size=1000):
    if not text:
        raise ValueError("Input text is None or empty.")
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def summarize_text(text, max_length=60, min_length=30):
    if not text:
        raise ValueError("Input text is None or empty.")
    inputs = bart_tokenizer(text, return_tensors='pt', max_length=1024, truncation=True)
    summary_ids = bart_model.generate(
        inputs['input_ids'], 
        max_length=max_length, 
        min_length=min_length, 
        length_penalty=2.0, 
        num_beams=4, 
        early_stopping=True
    )
    summary = bart_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary

def extract_ner_details(text):
    entities = []
    for line in text.splitlines():
        doc = nlp(line)
        for ent in doc.ents:
            entities.append(f"{ent.text} [{ent.label_}]\n")
    return entities

def highlight_entities(text):
    doc = nlp(text)
    highlighted_text = text
    for ent in reversed(doc.ents):
        start = ent.start_char
        end = ent.end_char
        label = ent.label_
        highlighted_text = highlighted_text[:start] + f'<mark>{ent.text}</mark>' + highlighted_text[end:]
    return highlighted_text

def predict(text):
    inputs = bert_tokenizer(text, truncation=True, max_length=128, return_tensors='pt', padding=True)
    inputs = {key: val.to(device) for key, val in inputs.items()}
    bert_model.eval()
    with torch.no_grad():
        outputs = bert_model(**inputs)
        logits = outputs.logits
        predicted_class = torch.argmax(logits, dim=1)
        return predicted_class.item()

classes = {
    1: "SERVICES", 
    2: "PAYMENT", 
    3: "TERM OF AGREEMENT", 
    4: "CONFIDENTIALITY", 
    5: "TERMINATION", 
    6: "GOVERNMENT LAW",
    7: "SIGNATURE"
}

def text_classify(pdf_text):
    arr = []
    for line in pdf_text.splitlines():
        predicted_class = predict(line)
        label = f"[{classes[predicted_class]}]" if predicted_class != 7 else ''
        arr.append([line, label])
    return arr
