# llama_index_example

Examples using added Google Universal Sentence Encoder v5 support for llama_index for domain specific search.

## local_txt_google_use.py
Example searching local youtube transcript text file:
- Split resource text file into sentence chunks around 500 characters.
- Using Google Universal Sentence Encoder v5 to create embeddings for text file chunks and query embedding.
- With everything local for llama_index to gather the context for the query, only the last web call to OpenAI to answer the query is over the web.
- Eliminates OpenAI calls when using llama_index for document and query embeddings.
- Overall less tokens used with OpenAI at less cost.

## audio_to_text_files.py
Example using Whisper to convert youtube audio files into text chunk with Google Universal Sentence Encoder v5 embeddings
- Resource: https://github.com/openai/whisper
- Assumes you have cloned the git repo and have whisper working and accessible from python
- Resource: https://github.com/ytdl-org/youtube-dl
- Assumes you have cloned the git repo for youtube-dl and have youtube-dl working
- Assumes you have a folder with youtube m4a audio files in a structure similar to /[youtube-audio]/[channel-name]/[audio-file].m4a
- You can download single youtube video or whole channel with youtube-dl
- Command line parameter -f 140 is for m4a audio
- Example command line for downloading a Bloomberg video: 
`youtube-dl --download-archive markets_downloaded.tracker -f 140 -ciw -o "%(title)s.%(ext)s" -v https://www.youtube.com/watch?v=NAZkN7n4WYU`
- converts audio to text file using whisper tiny model
- splits text file into sentence chunks of 500 characters
- creates embedding using Google Sentence Encoder v5 for text chunk
- saves text chunks with embedding as json file into specified folder

## audio_txt_google_use.py
Example that takes the output from audio_to_text_files.py and answers a query.
- assumes you have already used audio_to_text_files.py to process m4a audio files into text chunks with embeddings using google universal sentence encoder v5
