# llama_index_example

Examples using added Google Universal Sentence Encoder v5 support for llama_index for domain specific search.

Example searching local youtube transcript text file:
- creating embeddings for text file chunked into sentences around 500 characters
- All embeddings from Google Universal Sentence Encoder v5. Both embeddings for text file chunks and query embedding.
- Eliminates the calls when using llama_index to OpenAI for embeddings.
- Allows local embeddings using Google USE and only the last call to OpenAI using prompt with context information from llama_index goes over the web.
- Overall less tokens used with OpenAI at less cost.
