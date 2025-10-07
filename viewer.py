from flask import Flask, render_template_string, url_for
import os
import json

app = Flask(__name__)
app.static_folder = "clips"

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>📹 Event Clips Viewer</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f4f4; padding: 20px; }
        h1 { color: #333; }
        .clip { background: #fff; padding: 15px; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        video { width: 480px; border: 1px solid #ccc; margin-bottom: 10px; }
        p { margin: 5px 0; }
        a { text-decoration: none; color: #007BFF; }
    </style>
</head>
<body>
    <h1>🎬 Saved Event Clips</h1>
    {% for clip in clips %}
        <div class="clip">
            <video controls>
                <source src="{{ url_for('static', filename=clip.filename.split('clips/')[1]) }}" type="video/avi">
            </video>
            <p><strong>Event:</strong> {{ clip.event_type }}</p>
            <p><strong>Saved At:</strong> {{ clip.timestamp }}</p>
            <p><strong>Start Time:</strong> {{ clip.start_time or "N/A" }}</p>
            <p><strong>End Time:</strong> {{ clip.end_time or "N/A" }}</p>
            <p><strong>GPS:</strong> Lat {{ clip.gps.lat }}, Lon {{ clip.gps.lon }}</p>
            <a href="{{ url_for('static', filename=clip.filename.split('clips/')[1]) }}" download>⬇️ Download Clip</a>
        </div>
    {% endfor %}
</body>
</html>
"""

@app.route("/")
def index():
    valid_clips = []
    if os.path.exists("metadata.json"):
        with open("metadata.json", "r") as f:
            for line in f:
                try:
                    clip = json.loads(line)
                    if os.path.exists(clip["filename"]):
                        valid_clips.append(clip)
                except Exception as e:
                    print(f"⚠️ Skipping invalid metadata line: {e}")
    return render_template_string(TEMPLATE, clips=valid_clips)

if __name__ == "__main__":
    app.run(debug=True)