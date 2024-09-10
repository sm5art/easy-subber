import whisper
from whisper.utils import get_writer 


def format_timestamp(seconds):
    """Format the timestamp in HH:MM:SS,SSS format."""
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"

def transcribe_audio(audio_file, save_path, model_name, language, num_of_words_per_line=5):
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
            # also include the exisitng segments method if -1 is passed.
            words = segment.get('words', [])
            # split words into lines with num_of_words_per_line variable
            lines = []
            for i in range(0, len(words), num_of_words_per_line):
                lines.append(words[i:i+num_of_words_per_line])
            for line in lines:
                start = line[0]['start']
                end = line[-1]['end']
                text = "".join([w['word'] for w in line])
                start_time = format_timestamp(start)
                end_time = format_timestamp(end)
                f.write(f"{i+1}\n{start_time} --> {end_time}\n{text}\n\n")
                i += 1