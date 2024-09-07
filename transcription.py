import whisper
from whisper.utils import get_writer 


def format_timestamp(seconds):
    """Format the timestamp in HH:MM:SS,SSS format."""
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"

def transcribe_audio(audio_file, save_path, model_name, language):
    """Transcribe the audio and save the subtitles to a file."""
    model = whisper.load_model(model_name)
    result = model.transcribe(audio_file, language=language, word_timestamps=True, verbose=False)
    segments = result.get('segments', [])
    print(segments)
    # Save the subtitles to a file
    with open(save_path, "w") as f:
        i = 0
        for segment in segments:
            # TODO: Add a parameter num_of_words_per_line and combine words into one line here
            words = segment.get('words', [])
            for word in words:
                start = word['start']
                end = word['end']
                text = word['word']
                start_time = format_timestamp(start)
                end_time = format_timestamp(end)
                f.write(f"{i+1}\n{start_time} --> {end_time}\n{text}\n\n")
                i += 1