from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import os

app = Flask(__name__)
CORS(app)

# Get the default Downloads folder dynamically
DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads")

def download_mp3(video_url):
    """Downloads YouTube video as MP3 into the default Downloads folder."""
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': f'{DOWNLOAD_FOLDER}/%(title)s.%(ext)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info_dict).replace('.webm', '.mp3').replace('.m4a', '.mp3')

        return filename

    except Exception as e:
        print("Download Error:", e)
        return f"Error: {str(e)}"

@app.route('/convert', methods=['POST'])
def convert():
    data = request.json
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({"error": "No URL provided"}), 400
    
    filename = download_mp3(video_url)
    if "Error" in filename:
        return jsonify({"error": filename}), 500

    return jsonify({"message": "Download complete!", "file": filename})

if __name__ == '__main__':
    app.run(debug=True)
