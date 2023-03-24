# llama_index_example

Examples using added Google Universal Sentence Encoder v5 support for llama_index for domain specific search.

Example chunking local youtube transcript text file
- creating embeddings for text file chunked into sentences around 500 characters
- All embeddings from Google Universal Sentence Encoder v5. Embeddings for text file chunks and query embedding
- Reduces the calls to OpenAI when using llama_index for embeddings
- Allows local embeddings using Google USE and only the last call to OpenAI using prompt with context information from llama_index goes over the web.
