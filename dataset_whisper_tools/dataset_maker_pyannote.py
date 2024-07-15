import os
import random
from pyannote.audio import Pipeline
from pydub import AudioSegment
import whisper
import whisperx

model_name = "large-v3"
# model = whisperx.load_model(model_name, "cuda")#, compute_type="float16")
model = whisper.load_model(model_name, "cuda")#, compute_type="float16")

def split_audio(input_file_path, output_folder_path, token, suffix):
    # Initialize the pipeline
    pipeline = Pipeline.from_pretrained("pyannote/voice-activity-detection", use_auth_token=token)
    output = pipeline(input_file_path)

    # Load the audio file with pydub
    audio = AudioSegment.from_wav(input_file_path)
    
    # Ensure the output directory exists
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    
    train_list = []

    for speech in output.get_timeline().support():
        start_time = int(speech.start * 1000)  # Convert to milliseconds
        end_time = int(speech.end * 1000)      # Convert to milliseconds
        
        # Extract the audio segment
        audio_segment = audio[start_time:end_time]
        
        # Set frame rate to 24kHz
        audio_segment = audio_segment.set_frame_rate(24000)
        
        # Define the output file path
        output_file_path = os.path.join(output_folder_path, f"split_{suffix}.wav")
        
        # Export the audio segment
        audio_segment.export(output_file_path, format="wav")
        
        print(f"Segment {suffix} saved: {output_file_path}")

        # Transcribe the audio segment
        transcription = transcribe_whisper(output_file_path)
        
        # Add entry to train list
        train_list.append(f"{os.path.basename(output_file_path)}|{transcription}|0")
        
        suffix += 1
    
    return train_list, suffix

def transcribe_whisperx(input_path):
    # There's some weird issue with whisperx where the sr at other values was not catching the entire audio file...
    # using whisper instead to transcribe.
    audio = whisperx.load_audio(input_path, sr=22500)
    result = model.transcribe(audio, language="en")
    
    model_a, metadata = whisperx.load_align_model(language_code=result["language"], device="cuda")
    result = whisperx.align(result["segments"], model_a, metadata, audio, device="cuda", return_char_alignments=False)
    
    text = " ".join([segment['text'] for segment in result['segments']])

    return text.strip()

def transcribe_whisper(input_path):
    audio = whisper.load_audio(input_path)
    result = model.transcribe(audio, language="en")
    text = "".join([segment['text'] for segment in result['segments']])

    return text.strip()

def process_audio_folder(input_folder_path, output_folder_path, token):
    suffix = 1
    all_train_list = []
    
    for file_name in os.listdir(input_folder_path):
        if file_name.endswith('.wav'):
            input_file_path = os.path.join(input_folder_path, file_name)
            print(f"Processing file: {input_file_path}")
            train_list, suffix = split_audio(input_file_path, output_folder_path, token, suffix)
            all_train_list.extend(train_list)

    # Split all_train_list into train and validation sets
    val_count = max(1, int(0.05 * len(all_train_list)))  # Ensure at least one item in validation set
    val_list = random.sample(all_train_list, val_count)
    train_list = [item for item in all_train_list if item not in val_list]
    
    # Save the train list to a file
    train_list_path = os.path.join(output_folder_path, "train_list.txt")
    with open(train_list_path, "w", encoding='utf-8') as f:
        for entry in train_list:
            f.write(f"{entry}\n")
    
    # Save the validation list to a file
    val_list_path = os.path.join(output_folder_path, "val_list.txt")
    with open(val_list_path, "w", encoding='utf-8') as f:
        for entry in val_list:
            f.write(f"{entry}\n")

input_folder_path = r"F:\wnr\ray"
output_folder_path = r"training\ray"
token = ""
process_audio_folder(input_folder_path, output_folder_path, token)
