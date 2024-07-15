import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync, sync_to_async
from .models import Contract

class ContractConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.contract_id = self.scope['url_route']['kwargs']['contract_id']
        self.contract_group_name = f'contract_{self.contract_id}'

        await self.channel_layer.group_add(
            self.contract_group_name,
            self.channel_name
        )

        await self.accept()

        # Send initial data
        contract = await self.get_contract(self.contract_id)
        await self.send(text_data=json.dumps({
            'text': contract.text,
            'entities': contract.entities,
            'highlighted_text': contract.highlighted_text,
            'predicted_text': contract.predicted_text,
            'summarized_text': contract.summarized_text,
        }))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.contract_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        pass

    @staticmethod
    async def get_contract(contract_id):
        contract = await sync_to_async(Contract.objects.get)(id=contract_id)
        return contract

    @staticmethod
    def contract_to_json(contract):
        return {
            'text': contract.text,
            'entities': contract.entities,
            'highlighted_text': contract.highlighted_text,
            'predicted_text': contract.predicted_text,
            'summarized_text': contract.summarized_text,
        }
