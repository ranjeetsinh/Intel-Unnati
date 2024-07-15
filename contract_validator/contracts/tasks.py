from celery import shared_task
from .models import Contract
from .utils import extract_text_from_pdf, extract_ner_details, highlight_entities, summarize_text, text_classify

@shared_task
def process_contract(contract_id):
    contract = Contract.objects.get(id=contract_id)
    file_content = contract.file.read()
    text = extract_text_from_pdf(file_content)
    entities = extract_ner_details(text)
    highlighted_text = highlight_entities(text)
    predicted_text = text_classify(text)
    summarized_text = summarize_text(text)
    contract.text = text
    contract.entities = entities
    contract.highlighted_text = highlighted_text
    contract.predicted_text = predicted_text
    contract.summarized_text = summarized_text
    contract.save()
