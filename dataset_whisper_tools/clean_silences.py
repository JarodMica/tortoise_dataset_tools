# Meant to try and post process a dataset split with whisperx 
import os
from pyannote.audio import Pipeline
from pydub import AudioSegment

# Initialize the pipeline
pipeline = Pipeline.from_pretrained("pyannote/voice-activity-detection",
                                    use_auth_token="")

# Function to process a single audio file
def process_audio_file(input_file, output_folder):
    # Perform voice activity detection
    output = pipeline(input_file)

    # Load the audio file using pydub
    audio = AudioSegment.from_wav(input_file)

    # Get the filename without extension
    base_filename = os.path.splitext(os.path.basename(input_file))[0]

    # Find the longest segment
    segments = [(speech.start * 1000, speech.end * 1000) for speech in output.get_timeline().support() if (speech.end - speech.start) > 1]
    if not segments:
        return  # No segments longer than 1 second found

    longest_segment = max(segments, key=lambda s: s[1] - s[0])

    # Process each detected speech segment
    for start_time, end_time in segments:
        segment_duration = end_time - start_time
        segment = audio[start_time:end_time]

        # Determine the output filename
        if (start_time, end_time) == longest_segment:
            output_file = os.path.join(output_folder, f"{base_filename}.wav")
        else:
            output_file = os.path.join(output_folder, f"{base_filename}_scrap.wav")

        # Export the segment
        segment.export(output_file, format="wav")

# Function to process all files in the input folder
def process_folder(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Process each file in the input folder
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".wav"):
            input_file = os.path.join(input_folder, file_name)
            process_audio_file(input_file, output_folder)

# Specify input and output folders
input_folder = r"training\luba_whisper_test\audio"
output_folder = r"training\luba_whisper_test\cleaned_audio"

# Process the entire folder
process_folder(input_folder, output_folder)
