import csv
import datetime
import json
import math
import numpy as np
import os
import re
import tensorflow_hub as hub
import time
import whisper
import shutil

from datetime import date

AUDIO_ROOT_FOLDER = "../youtube-audio/"
JSON_OUTPUT_FOLDER = "./json_files/"

def saveFile(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)

def convert_to_txt(audio_file):
    try:
        txt_file = os.path.splitext(audio_file)[0] + '.txt'
        tsv_file = os.path.splitext(audio_file)[0] + '.tsv'

        result = model.transcribe(audio_file, verbose=True)
        saveFile(txt_file, result["text"])
        update_file_created_modifled(audio_file, txt_file)

        with open(tsv_file, 'w', encoding='utf-8', newline='') as tsv_output_file:
            writer = csv.writer(tsv_output_file, delimiter='\t')
            writer.writerow(['start', 'end', 'text'])  # header row
            for row in result["segments"]:
                start = math.floor(row["start"])
                end = math.ceil(row["end"])
                text = row["text"]
                writer.writerow([start, end, text])
                print(f"[{start} ####> {end} {text}")
        update_file_created_modifled(audio_file, tsv_file)

    except Exception as e:
        # Code to handle the exception
        print("An error occurred:", str(e))

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

def save_chunk(txt_file_with_path, chunk_count, payload):
    # create some filename variables
    dir_path, txt_file_wo_path = os.path.split(txt_file_with_path)
    youtube_channel = os.path.split(dir_path)[1]
    audio_file_with_path = os.path.join(dir_path, os.path.splitext(txt_file_wo_path)[0] + '.m4a')
    txt_file_wo_path_or_ext = os.path.splitext(txt_file_wo_path)[0]
    # put these chunks in a folder with same name as audio_file without m4a extension
    chunk_path = JSON_OUTPUT_FOLDER + f"youtube/{youtube_channel}/"
    if not os.path.exists(chunk_path):
        os.makedirs(chunk_path)
    chunk_path = JSON_OUTPUT_FOLDER + f"youtube/{youtube_channel}/{txt_file_wo_path_or_ext}/"
    if not os.path.exists(chunk_path):
        os.makedirs(chunk_path)
    # create the chunk file
    filename = f"{txt_file_wo_path_or_ext}-{chunk_count}.json"
    print(".",end="")
    text_chunk_filename = chunk_path + filename
    if not os.path.isfile(text_chunk_filename):
        with open(text_chunk_filename, 'w', encoding='utf-8') as outfile:
            json.dump(payload, outfile, ensure_ascii=False, sort_keys=True, indent=1)
        # change the file attribs to match the audio file created, modified datetimes
        update_file_created_modifled(audio_file_with_path, text_chunk_filename)

def convert_to_chunks(embed, txt_file_with_path):
    with open(txt_file_with_path, 'r', encoding='utf-8') as file:
        content = file.read()
        chunk_count = 0
        for chunk in split_text_into_chunks(content):
            chunk_count = chunk_count + 1
            vectors = embed([chunk]).numpy().tolist()
            chunk_vector = vectors[0]
            save_chunk(txt_file_with_path, chunk_count, {'date': str(date.today()), 'request': chunk, 'vector': chunk_vector, 'response': chunk})

def walk_folder_for_extension(directory, extension):
    found_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
                if file.endswith(extension):
                        found_files.append(os.path.join(root, file))
    return found_files

def update_file_created_modifled(source, target):
        if os.path.isfile(source):
            if os.path.isfile(target):
                source_stat = os.stat(source)
                os.utime(target, (source_stat.st_ctime, source_stat.st_mtime))

# MAIN PROGRAM
if __name__ == '__main__':

    """
    # If you want to download all the whisper models locally

    models = [ 'base', 'small', 'medium', 'large', 'tiny.en', 'base.en', 'small.en', 'medium.en', 'tiny']

    for model in models:
        print('Downloading %s' % (model))
        model = whisper.load_model(model,"cpu","models",False)
    """

    """
    # update all existing txt and tsv files to have same modified date as m4a audio
    audio_files = walk_folder_for_extension(AUDIO_ROOT_FOLDER, ".m4a")
    print(f"Total audio files found {len(audio_files)}")
    current_file_number = 0
    for m4a_file in audio_files:
        current_file_number += 1

        dir_path, file_name = os.path.split(m4a_file)
        txt_file = os.path.join(dir_path, os.path.splitext(file_name)[0] + '.txt')
        tsv_file = os.path.join(dir_path, os.path.splitext(file_name)[0] + '.tsv')

        update_file_created_modifled(m4a_file, txt_file)      
        update_file_created_modifled(m4a_file, tsv_file)   

    quit()
    """

    print("loading whisper speech to text...")
    # Whisper speech to text 
    model = whisper.load_model("tiny.en", "cpu", "models", True)

    # for each audio file convert to txt and tsv file using whisper
    audio_files = walk_folder_for_extension(AUDIO_ROOT_FOLDER, ".m4a")
    print(f"Total audio files found {len(audio_files)}")
    current_file_number = 0
    for audio_file_with_path in audio_files:
        current_file_number += 1
        if os.path.isfile(os.path.splitext(audio_file_with_path)[0] + '.tsv'):
            print(f"skipping file {current_file_number} of {len(audio_files)} {audio_file_with_path}")
        else:
            print(f"working file  {current_file_number} of {len(audio_files)} {audio_file_with_path}")
            convert_to_txt(audio_file_with_path)

    print("loading google universal sentence encoder...")
    # Google Universal Sentence Encode v5
    embed = hub.load("https://tfhub.dev/google/universal-sentence-encoder-large/5")

    # for each txt file save to chunks with embeddings for semantic search
    text_files = walk_folder_for_extension(AUDIO_ROOT_FOLDER, ".txt")
    print(f"Total text files found {len(text_files)}")
    current_file_number = 0
    for txt_file_with_path in text_files:
        current_file_number += 1
        print(f"working text file  {current_file_number} of {len(text_files)} {txt_file_with_path}",end="") 
        convert_to_chunks(embed, txt_file_with_path)
        print("")
