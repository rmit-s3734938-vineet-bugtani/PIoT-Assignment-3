from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import io, os, sys
import argparse, webbrowser

# MacOS
chrome_path = "open -a /Applications/Google\ Chrome.app %s"

# Windows
# chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'

# Linux
# chrome_path = '/usr/bin/google-chrome %s'

def sample_recognize(local_file_path):
    """
    Transcribe a short audio file using synchronous speech recognition

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav

    Returns:
        str: Transcript of audio file.
    """
    client = speech_v1.SpeechClient()

    # The language of the supplied audio
    language_code = "en-IN"

    config = {
        "language_code": language_code,
    }
    with io.open(local_file_path, "rb") as f:
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))
        return alternative.transcript

# [END speech_transcribe_sync]


def start_recognition(file_path="audio/1.flac"):
    # TODO Remove personal token before publishing repo.
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "creds/google-stt.json"
    os.environ["GCLOUD_PROJECT"] = "quickstart-1587792864879"
    s = sample_recognize(file_path)
    return s


def start(file_path):
    transcript = start_recognition(file_path)
    url = ''
    search_query = ''
    for t in transcript.split():
        search_query += t + '+'
    
    url = "http://localhost:5000/admin/car/?search=" + search_query
    webbrowser.get(chrome_path).open_new_tab(url)

def main():
    parser = argparse.ArgumentParser(
        description="Parse an audio file and search for cars."
    )
    parser.add_argument(
        "Name", metavar="<audio filename>", type=str, help="Name of audio file in /audio"
    )
    args = parser.parse_args()
    name = args.Name
    path = "audio/" + name
    if not os.path.isfile(path):
        print("Specified file does not exist.")
        sys.exit()

    start(path)


if __name__ == "__main__":
    main()
