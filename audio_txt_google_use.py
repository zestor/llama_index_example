from llama_index import GPTListIndex
from llama_index.embeddings.google_use import GoogleUnivSentEncoderEmbedding
from llama_index.readers import Document
import re
import os
import json 

def walk_folder_for_extension(directory, extension):
    found_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
                if file.endswith(extension):
                        found_files.append(os.path.join(root, file))
    return found_files

# load prior knowledge from disk
# assumes answers persisted to disk are credible
def load_prior_knowledge():
    retval = list()

    return retval

JSON_OUTPUT_FOLDER = "./json_files/"
index = GPTListIndex([])
embed_model_google_use = GoogleUnivSentEncoderEmbedding()
doc_chunks = []

for file in walk_folder_for_extension(JSON_OUTPUT_FOLDER,".json"):
    print('prior knowledge %s' % file)
    with open(file, 'r', encoding='utf-8') as file:
        knowledge_content = file.read()
    knowledge_json = json.loads(knowledge_content)
    text = knowledge_json['response']
    embedding = knowledge_json['vector']
    doc = Document(text, embedding=embedding)
    index.insert(doc)

# query
response = index.query("What is going on with Twitter?", embed_model=embed_model_google_use, mode="embedding")
print(f"{response}")