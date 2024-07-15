import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
from transformers import Trainer, TrainingArguments
import os

# Load tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=2)  # Assuming binary classification (valid or invalid)

# Define dataset class
class ContractDataset(Dataset):
    def __init__(self, tokenizer, data_dir, max_length=512):
        self.tokenizer = tokenizer
        self.max_length = max_length
        self.texts, self.labels = self.load_data(data_dir)

    def load_data(self, data_dir):
        texts = []
        labels = []
        with open(os.path.join(data_dir, 'labels.txt'), 'r', encoding='utf-8') as file:
            for line in file:
                labels.append(int(line.strip() == 'valid'))  # Convert to binary label
        for i in range(len(labels)):
            with open(os.path.join(data_dir, f'contract_{i}.txt'), 'r', encoding='utf-8') as file:
                texts.append(file.read().replace('\n', ' '))
        return texts, labels
    
    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        text = self.texts[idx]
        label = self.labels[idx]

        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            truncation=True,
            padding='max_length',
            return_tensors='pt'
        )

        inputs = {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

        return inputs

# Create dataset and dataloader
dataset = ContractDataset(tokenizer, data_dir='data')
train_dataset, val_dataset = train_test_split(dataset, test_size=0.1, random_state=42)  # Splitting into train and validation sets
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False)

# Define training arguments
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=8,
    per_device_eval_batch_size=8,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=100,
)

# Define trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
)

# Train the model
trainer.train()

# Evaluate the model
trainer.evaluate()
