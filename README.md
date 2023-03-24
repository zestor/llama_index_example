# llama_index_example

Examples using added Google Universal Sentence Encoder v5 support for llama_index for domain specific search.

## local_txt_google_use.py
Example searching local youtube transcript text file:
- Split resource text file into sentence chunks around 500 characters.
- Using Google Universal Sentence Encoder v5 to create embeddings for text file chunks and query embedding.
- With everything local for llama_index to gather the context for the query, only the last web call to OpenAI to answer the query is over the web.
- Eliminates OpenAI calls when using llama_index for document and query embeddings.
- Overall less tokens used with OpenAI at less cost.

# audio_to_text_files.py
Example using Whisper to convert youtube audio files into text chunk with embeddings
- Assumes you have a folder with youtube m4a audio files in a structure similar to /[youtube-audio]/[channel-name]/[audio-file].m4a
- You can download single youtube video or whole channel with youtube-dl
- Command line parameter -f 140 is for m4a audio
> youtube-dl --download-archive markets_downloaded.tracker -f 140 -ciw -o "%(title)s.%(ext)s" -v https://www.youtube.com/watch?v=NAZkN7n4WYU
- converts audio to text file
- splits text file into sentence chunks of 500 characters
- creates embedding using Google Sentence Encoder v5 for text chunk
- saves text chunks with embedding as json file into specified folder
