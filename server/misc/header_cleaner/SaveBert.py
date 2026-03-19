import os
from transformers import BertTokenizer, BertModel

# Define your local storage path
MODEL_PATH = "./models/bert_local"

def download_and_save_bert():
    if not os.path.exists(MODEL_PATH):
        os.makedirs(MODEL_PATH)

    print("Downloading BERT model and tokenizer...")
    tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    model = BertModel.from_pretrained('bert-base-uncased')

    # Save to local disk
    tokenizer.save_pretrained(MODEL_PATH)
    model.save_pretrained(MODEL_PATH)
    print(f"Model saved successfully to {MODEL_PATH}")

if __name__ == "__main__":
    download_and_save_bert()
