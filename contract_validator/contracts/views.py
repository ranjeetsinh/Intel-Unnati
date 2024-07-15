from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Contract
from .serializers import ContractSerializer
from .utils import extract_text_from_pdf, extract_ner_details, highlight_entities, summarize_text, text_classify
import logging

from django.shortcuts import render

def index(request):
    return render(request, 'contracts/index.html')


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    def create(self, request, *args, **kwargs):
        file = request.FILES['file']
        file_content = file.read()
        text = extract_text_from_pdf(file_content)
        entities = extract_ner_details(text)
        highlighted_text = highlight_entities(text)
        predicted_text = text_classify(text)
        summarized_text = summarize_text(text)
        contract = Contract.objects.create(
            file=file,
            text=text,
            entities=entities,
            highlighted_text=highlighted_text,
            predicted_text=predicted_text,
            summarized_text=summarized_text
        )
        serializer = self.get_serializer(contract)
        return Response(serializer.data, status=status.HTTP_201_CREATED)