import os
import subprocess
import yt_dlp
import zipfile
import argparse

def search_videos(query, max_results=5):
    search_url = f'https://www.youtube.com/results?search_query={query}'
    ydl_opts = {
        'quiet': True,
        'extract_flat': True,
        'force_generic_extractor': True,
        'no_warnings': True,
        'playlist_items': '1-' + str(max_results)
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(search_url, download=False)
        entries = info_dict.get('entries', [])
        video_urls = [entry['url'] for entry in entries if entry['url']]
        
    return video_urls

def download_audios(video_urls, output_folder=None):
    if output_folder is None:
        output_folder = os.path.join(os.path.expanduser('~'), 'Desktop')

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_folder, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for url in video_urls:
            print(f"Downloading audio: {url}")
            ydl.download([url])

def trim_audios(output_folder):
    for file_name in os.listdir(output_folder):
        if file_name.endswith(".mp3") and not file_name.startswith("trimmed_"):
            file_path = os.path.join(output_folder, file_name)
            trimmed_mp3_file_path = os.path.join(output_folder, "trimmed_" + file_name)
            
            # Trim the MP3 file to 10 seconds
            command = [
                'ffmpeg', '-i', file_path,
                '-ss', '00:00:00',   # Start time
                '-t', '00:00:10',    # Duration (10 seconds)
                '-c', 'copy',
                trimmed_mp3_file_path
            ]
            subprocess.run(command, check=True)
            print(f"Trimmed audio: {file_path}")

            # Remove the original file
            os.remove(file_path)

def create_mashup(output_folder, mashup_filename="mashup.mp3"):
    trimmed_files = [os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.startswith("trimmed_") and f.endswith(".mp3")]

    if not trimmed_files:
        print("No trimmed audio files found for mashup.")
        return

    # Create a file with the list of audio files
    with open(os.path.join(output_folder, "file_list.txt"), 'w') as file:
        for audio_file in trimmed_files:
            file.write(f"file '{audio_file}'\n")

    # Concatenate the audio files
    mashup_file_path = os.path.join(output_folder, mashup_filename)
    command = [
        'ffmpeg', '-f', 'concat', '-safe', '0', '-i', os.path.join(output_folder, "file_list.txt"),
        '-c', 'copy', mashup_file_path
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Created mashup: {mashup_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error creating mashup: {e}")

    # Cleanup
    os.remove(os.path.join(output_folder, "file_list.txt"))

    # Optionally remove the trimmed files
    for file in trimmed_files:
        os.remove(file)

def zip_mashup(output_folder, zip_filename="mashup.zip"):
    mashup_file_path = os.path.join(output_folder, "mashup.mp3")
    zip_file_path = os.path.join(output_folder, zip_filename)

    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        if os.path.exists(mashup_file_path):
            zipf.write(mashup_file_path, arcname="mashup.mp3")
            print(f"Created ZIP: {zip_file_path}")
        else:
            print(f"Mashup file not found: {mashup_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process audio files.')
    parser.add_argument('--query', type=str, required=True, help='Search query for videos.')
    parser.add_argument('--max_results', type=int, default=5, help='Number of results to fetch.')

    args = parser.parse_args()

    output_folder = os.path.join(os.path.expanduser('~'), 'Desktop')
    video_urls = search_videos(args.query, args.max_results)
    download_audios(video_urls, output_folder)
    trim_audios(output_folder)
    create_mashup(output_folder)
    zip_mashup(output_folder)
