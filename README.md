# llama_index_example

Examples using added Google Universal Sentence Encoder v5 support for llama_index for domain specific search.

## local_txt_google_use.py
Example searching local youtube transcript text file:
- Split resource text file into sentence chunks around 500 characters.
- Using Google Universal Sentence Encoder v5 to create embeddings for text file chunks and query embedding.
- With everything local for llama_index to gather the context for the query, only the last web call to OpenAI to answer the query is over the web.
- Eliminates OpenAI calls when using llama_index for document and query embeddings.
- Overall less tokens used with OpenAI at less cost.
