from llama_index import GPTListIndex
from llama_index.embeddings.google_use import GoogleUnivSentEncoderEmbedding
from llama_index.readers import Document
import re



def split_text_into_chunks(text):
    # Split input string into sentences based on punctuation marks
    sentences = re.split('(?<=[.!?]) +', text)
    # Initialize variables
    text_chunks = []
    current_chunk = ""
    # Iterate through sentences to create text chunks
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < 500:
            # If adding the sentence won't exceed 500 characters, append it to the current chunk
            current_chunk += sentence
        else:
            # If adding the sentence would exceed 500 characters, save the current chunk and start a new one
            text_chunks.append(current_chunk.strip())
            current_chunk = sentence
    # Append the last chunk if it's not empty
    if current_chunk.strip():
        text_chunks.append(current_chunk.strip())
    return text_chunks

txt_file_with_path="../../../youtube-audio/markets/Twitter Asks Some Fired Workers to Return, Delays Change to Badges.txt"

with open(txt_file_with_path, 'r', encoding='utf-8') as file:
    content = file.read()
text_chunks = split_text_into_chunks(content)

index = GPTListIndex([])
embed_model_google_use = GoogleUnivSentEncoderEmbedding()
doc_chunks = []

for i, text in enumerate(text_chunks):
    print(f"Getting embedding for chunk {i}")
    embedding = embed_model_google_use.get_text_embedding(text)
    doc = Document(text, embedding=embedding, doc_id=f"doc_id_{i}")
    doc_chunks.append(doc)

for doc in doc_chunks:
    index.insert(doc)

# query
response = index.query("What is going on with Twitter?", embed_model=embed_model_google_use, mode="embedding")
print(f"{response}")