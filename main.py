import subprocess
import os
import sys
import json

def run_command(command):
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("Command failed:", e.stderr)
        return None

def parse_filesize(size):
    if size is None:
        return 0
    return size / (1024 * 1024)

def get_video_info(url):
    print("\n📥 Fetching video information...\n")
    raw_json = run_command(["yt-dlp", "-j", url])
    if raw_json is None:
        return None
    return json.loads(raw_json)

def list_formats(info):
    formats = info.get("formats", [])
    video_formats = []
    audio_formats = []

    for f in formats:
        if f.get("vcodec") != "none" and f.get("acodec") == "none":
            video_formats.append(f)
        elif f.get("acodec") != "none" and f.get("vcodec") == "none":
            audio_formats.append(f)

    # Sort video by resolution (height), then by bitrate
    video_formats.sort(key=lambda x: (x.get("height") or 0, x.get("tbr") or 0), reverse=True)
    # Sort audio by bitrate, handling None values
    audio_formats.sort(key=lambda x: x.get("abr") or 0, reverse=True)

    if video_formats:
        print("🎥 Video Formats (downloadable):")
        for f in video_formats[:6]:
            size = parse_filesize(f.get("filesize") or f.get("filesize_approx"))
            print(f"  {f['format_id']:>5}  {f.get('ext', ''):>4}  {f.get('height', 'N/A')}p  {size:.1f} MiB  {f.get('vcodec', '')}")
    else:
        print("🎥 No downloadable video formats found.")

    if audio_formats:
        print("\n🎧 Audio Formats (downloadable):")
        for f in audio_formats[:4]:
            size = parse_filesize(f.get("filesize") or f.get("filesize_approx"))
            print(f"  {f['format_id']:>5}  {f.get('ext', ''):>4}  {size:.1f} MiB  {f.get('acodec', '')}")
    else:
        print("\n🎧 No downloadable audio formats found.")

    return video_formats, audio_formats

def auto_pick_formats(video_formats, audio_formats):
    if not video_formats or not audio_formats:
        return None, None, 0

    video = video_formats[0]
    audio = next((a for a in audio_formats if 'm4a' in a.get('ext', '')), audio_formats[0])

    video_size = parse_filesize(video.get("filesize") or video.get("filesize_approx"))
    audio_size = parse_filesize(audio.get("filesize") or audio.get("filesize_approx"))
    total_size = video_size + audio_size

    print(f"\n📌 Auto-selected formats:")
    print(f"  🎥 Video: {video['format_id']} - {video.get('height', 'N/A')}p - {video.get('ext', '')} - {video_size:.1f} MiB")
    print(f"  🎧 Audio: {audio['format_id']} - {audio.get('ext', '')} - {audio_size:.1f} MiB")
    print(f"  📦 Estimated total size: {total_size:.1f} MiB")

    confirm = input("\nProceed with this selection? (Y/n): ").strip().lower()
    if confirm and confirm != "y":
        return None, None, 0

    return video["format_id"], audio["format_id"], total_size

def download_and_merge(url, video_format=None, audio_format=None, path="."):
    if video_format and audio_format:
        combined_format = f"{video_format}+{audio_format}"
        print(f"\nDownloading and merging video ({video_format}) + audio ({audio_format})...")
        try:
            subprocess.run([
                "yt-dlp",
                "-f", combined_format,
                "--merge-output-format", "mp4",
                "-P", path,
                url
            ], check=True)
            print("Download and merge complete.")
        except subprocess.CalledProcessError as e:
            print(f"Download failed: {e.stderr}")
    elif video_format:
        print(f"\nDownloading video-only format {video_format}...")
        try:
            subprocess.run([
                "yt-dlp",
                "-f", video_format,
                "-P", path,
                url
            ], check=True)
            print("Download complete.")
        except subprocess.CalledProcessError as e:
            print(f"Download failed: {e.stderr}")
    elif audio_format:
        print(f"\nDownloading audio-only format {audio_format}...")
        try:
            subprocess.run([
                "yt-dlp",
                "-f", audio_format,
                "-P", path,
                url
            ], check=True)
            print("Download complete.")
        except subprocess.CalledProcessError as e:
            print(f"Download failed: {e.stderr}")
    else:
        print("No format selected.")

def main():
    url = input("Enter the YouTube video URL: ").strip()
    info = get_video_info(url)
    if not info:
        return

    video_formats, audio_formats = list_formats(info)

    mode = input("\nDownload options:\n1. Video only\n2. Audio only\n3. Both (auto-pick best)\n4. Manual selection\nEnter 1/2/3/4: ").strip()

    video_format = None
    audio_format = None

    if mode == "1":
        video_format = input("Enter the video format code (e.g. 137): ").strip()
    elif mode == "2":
        audio_format = input("Enter the audio format code (e.g. 140): ").strip()
    elif mode == "3":
        video_format, audio_format, _ = auto_pick_formats(video_formats, audio_formats)
        if not video_format or not audio_format:
            print("Cancelled.")
            return
    elif mode == "4":
        video_format = input("Enter the video format code: ").strip()
        audio_format = input("Enter the audio format code: ").strip()
    else:
        print("Invalid choice.")
        return

    path = os.path.expanduser(input("Enter full destination path (e.g. ~/Videos): ").strip())
    if not os.path.isdir(path):
        print("Invalid path. Directory does not exist.")
        return

    download_and_merge(url, video_format, audio_format, path)

if __name__ == "__main__":
    main()
