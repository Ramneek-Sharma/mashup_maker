
# MashUp_Creater
## Overview
The Audio Mashup Creator is a Python and Node.js-based project designed to automate the process of creating customized audio mashups from YouTube videos. 

## How it works
The project involves several key steps:

* YouTube Video Search-Searches YouTube for videos based on a user-specified query.
```bash
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
```
* Audio Extraction-Downloads the audio tracks from the search results.
```bash
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
```
* Audio Trimming-Trims each audio track to the first 10 seconds.
```bash
def trim_audios(output_folder):
    for file_name in os.listdir(output_folder):
        if file_name.endswith(".mp3") and not file_name.startswith("trimmed_"):
            file_path = os.path.join(output_folder, file_name)
            trimmed_mp3_file_path = os.path.join(output_folder, "trimmed_" + file_name)
            
           
            command = [
                'ffmpeg', '-i', file_path,
                '-ss', '00:00:00',   
                '-t', '00:00:10',   
                '-c', 'copy',
                trimmed_mp3_file_path
            ]
            subprocess.run(command, check=True)
            print(f"Trimmed audio: {file_path}")

           
            os.remove(file_path)
```
* Mashup Creation-Combines the trimmed audio clips into a single mashup file.
```bash
def create_mashup(output_folder, mashup_filename="mashup.mp3"):
    trimmed_files = [os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.startswith("trimmed_") and f.endswith(".mp3")]

    if not trimmed_files:
        print("No trimmed audio files found for mashup.")
        return

   
    with open(os.path.join(output_folder, "file_list.txt"), 'w') as file:
        for audio_file in trimmed_files:
            file.write(f"file '{audio_file}'\n")

   
    mashup_file_path = os.path.join(output_folder, mashup_filename)
    command = [
        'ffmpeg', '-f', 'concat', '-safe', '0', '-i', os.path.join(output_folder, "file_list.txt"),
        '-c', 'copy', mashup_file_path
    ]
```
* Packaging- Compresses the resulting mashup into a ZIP file.
```bash
def zip_mashup(output_folder, zip_filename="mashup.zip"):
    mashup_file_path = os.path.join(output_folder, "mashup.mp3")
    zip_file_path = os.path.join(output_folder, zip_filename)

    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        if os.path.exists(mashup_file_path):
            zipf.write(mashup_file_path, arcname="mashup.mp3")
            print(f"Created ZIP: {zip_file_path}")
        else:
            print(f"Mashup file not found: {mashup_file_path}")
```
* Email Delivery-Sends the ZIP file to the user via email.
```bash
 let transporter = nodemailer.createTransport({
                service: 'gmail',
                auth: {
                    
                    user: 'email@gmail.com',
                    pass: 'pass'     
                }
            });

            let mailOptions = {
                from: 'email@gmail.com',    
                to: email,
                subject: 'Your Audio Mashup',
                text: `Hello ${email},\n\nPlease find the audio mashup attached.\n\nBest regards,\nAudio Team`,
                attachments: [
                    {
                        filename: 'mashup.zip',
                        path: zipFilePath
                    }
                ]
            };

            transporter.sendMail(mailOptions, (error, info) => {
                if (error) {
                    console.error(`Error sending email: ${error}`);
                    return res.status(500).json({ message: 'Error sending email' });
                }
```



## Features
* Search YouTube for specific artists or tracks.
* Download and process audio from multiple videos.
* Trim audio to the desired length.
* Create and send a customized audio mashup via email.


