# 🎬 YouTube Video Downloader CLI

## 🚀 Motivation

I often found myself needing to download YouTube videos for offline viewing or audio extraction. While numerous web-based tools and GUI applications exist, they frequently come with limitations:

* **Intrusive Advertisements**: Many web tools are cluttered with ads, making the experience cumbersome.
* **Limited Format Control**: GUIs often restrict users to predefined formats without offering detailed choices.
* **Lack of Transparency**: It's challenging to know the exact quality or size of the download beforehand.
* **Privacy Concerns**: Uploading URLs to third-party services raises privacy issues.

Desiring more control, transparency, and a streamlined experience, I decided to craft my own solution using the powerful `yt-dlp` tool.

## 🛠️ Features

* **Interactive CLI**: User-friendly prompts guide you through the download process.
* **Format Listing**: Displays available video and audio formats with details like resolution, codec, and estimated size.
* **Auto Selection**: Automatically picks the best quality video and audio combination.
* **Manual Selection**: Allows users to choose specific video and audio formats.
* **Size Estimation**: Provides estimated download sizes before proceeding.
* **Seamless Merging**: Automatically merges video and audio streams using `ffmpeg`.
* **Custom Save Path**: Specify your desired download directory.

## 📦 Prerequisites

Ensure the following are installed on your system:

* **Python 3.6+**
* **yt-dlp**: Install via pip:

  ```bash
  pip install yt-dlp
  ```
* **ffmpeg**: Required for merging video and audio. Installation methods vary:

  * **macOS**:

    ```bash
    brew install ffmpeg
    ```
  * **Ubuntu/Debian**:

    ```bash
    sudo apt install ffmpeg
    ```
  * **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to your system PATH.

## 📄 Usage

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/nagsujosh/youtube-downloader-cli.git
   cd youtube-downloader-cli
   ```

2. **Run the Script**:

   ```bash
   python main.py
   ```

3. **Follow the Prompts**:

   * Enter the YouTube video URL.
   * View available video and audio formats.
   * Choose your download option:

     * Video only
     * Audio only
     * Both (auto-pick best)
     * Manual selection
   * Specify the download directory.

4. **Download and Enjoy**:
   The script will download and, if necessary, merge the selected streams, saving the final file to your specified directory.

## 📝 Example

```
Enter the YouTube video URL: https://www.youtube.com/watch?v=example

📥 Fetching video information...

🎥 Video Formats (downloadable):
  137   mp4  1080p  847.5 MiB  avc1.640028
  248  webm  1080p  725.0 MiB  vp9

🎧 Audio Formats (downloadable):
  140   m4a  128.0 MiB  mp4a.40.2
  251  webm  160.0 MiB  opus

Download options:
1. Video only
2. Audio only
3. Both (auto-pick best)
4. Manual selection
Enter 1/2/3/4: 3

📌 Auto-selected formats:
  🎥 Video: 137 - 1080p - mp4 - 847.5 MiB
  🎧 Audio: 140 - m4a - 128.0 MiB
  📦 Estimated total size: 975.5 MiB

Proceed with this selection? (Y/n): y

Enter full destination path (e.g. ~/Videos): ~/Downloads

Downloading and merging video (137) + audio (140)...
Download and merge complete.
```

## 🤝 Contributing

Contributions are welcome! If you have suggestions for improvements or encounter issues, please open an issue or submit a pull request.

## 📄 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.