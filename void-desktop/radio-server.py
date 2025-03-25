from flask import Flask, Response
import subprocess

app = Flask(__name__)

@app.route('/')
def stream():
    def generate():
        ffmpeg = subprocess.Popen(
            [
                'ffmpeg',
                '-f', 'lavfi',
                '-i', 'sine=frequency=440:duration=3600',
                '-ac', '2',
                '-ar', '44100',
                '-f', 'mp3',
                '-'
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL
        )
        try:
            while True:
                data = ffmpeg.stdout.read(1024)
                if not data:
                    break
                yield data
        finally:
            ffmpeg.kill()
    return Response(generate(), mimetype='audio/mpeg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
