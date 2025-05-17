# Video Tools
[![Build Windows Executable](https://github.com/Natnat999/win-yt-ffmpeg-gui/actions/workflows/build.yml/badge.svg)](https://github.com/Natnat999/win-yt-ffmpeg-gui/actions/workflows/build.yml)

A modern, user-friendly Windows application for downloading YouTube videos and processing video files using FFmpeg. Built with Python and PyQt6, Video Tools provides a beautiful GUI for both beginners and advanced users.

---

## 🚀 Features

### YouTube Downloader
- Download videos from YouTube in various qualities (up to 4K, audio only, etc.)
- Automatic merging of best video and audio streams
- Hardware-accelerated (GPU) or CPU-based post-processing
- Smart error handling and format fallback
- Dark and light mode with instant switching

### FFmpeg Processor
- Compress, convert, resize, trim, and process audio/video files
- Queue and combine multiple operations in one go
- Real-time progress bar and status updates
- Hardware-accelerated (GPU) or CPU-based encoding
- Modern, responsive UI with dark/light mode

---

## 📦 Installation

### Prerequisites
- Python 3.9+
- [FFmpeg](https://ffmpeg.org/download.html) installed and added to your PATH
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) (installed automatically via requirements)
- Microsoft Visual C++ Redistributable (for PyQt6 on Windows)

### Setup
```bash
# Clone the repository
https://github.com/yourusername/video-tools.git
cd video-tools

# Install dependencies
pip install -r requirements.txt

# Run the application
python main.py
```

---

## 🖥️ Usage

### YouTube Downloader
1. Paste the YouTube video URL.
2. Select the desired quality (Full Resolution, 1080p, 720p, 480p, Audio Only).
3. Choose the output directory.
4. Click **Download**. Progress and status will be shown below.

### FFmpeg Processor
1. Add one or more operations (Compress, Convert, Resize, Trim, Audio).
2. Select the input and output files.
3. Click **Process**. Progress and status will be shown below.

### Dark/Light Mode
- Use the **Light Mode** checkbox in the top-right corner to switch themes instantly.

---

## 🤝 Contributing

Contributions are welcome! To contribute:
1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Commit and push (`git commit -am 'Add new feature' && git push origin feature/your-feature`)
5. Open a pull request

Please ensure your code is well-documented and tested. For major changes, open an issue first to discuss what you'd like to change.

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/)
- [PyQt6](https://riverbankcomputing.com/software/pyqt/)

---

## ⚠️ Disclaimer
This tool is for personal and educational use only. Downloading copyrighted content without permission may violate YouTube's Terms of Service and local laws. Use responsibly.
