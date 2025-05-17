import yt_dlp
import subprocess
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit,
                            QPushButton, QComboBox, QProgressBar, QLabel,
                            QFileDialog, QMessageBox, QGroupBox, QCheckBox, QApplication, QTabWidget)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor

def check_gpu_availability():
    try:
        # Check if nvidia-smi is available
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

class StyledButton(QPushButton):
    def __init__(self, text, primary=False, is_dark_mode=True):
        super().__init__(text)
        self.setMinimumHeight(35)
        self.is_dark_mode = is_dark_mode
        self.primary = primary
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark_mode:
            if self.primary:
                self.setStyleSheet("""
                    QPushButton {
                        background-color: #2196F3;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 8px 16px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #1976D2;
                    }
                    QPushButton:pressed {
                        background-color: #1565C0;
                    }
                    QPushButton:disabled {
                        background-color: #424242;
                        color: #757575;
                    }
                """)
            else:
                self.setStyleSheet("""
                    QPushButton {
                        background-color: #424242;
                        color: #E0E0E0;
                        border: none;
                        border-radius: 4px;
                        padding: 8px 16px;
                    }
                    QPushButton:hover {
                        background-color: #616161;
                    }
                    QPushButton:pressed {
                        background-color: #757575;
                    }
                    QPushButton:disabled {
                        background-color: #2D2D2D;
                        color: #757575;
                    }
                """)
        else:
            if self.primary:
                self.setStyleSheet("""
                    QPushButton {
                        background-color: #2196F3;
                        color: white;
                        border: none;
                        border-radius: 4px;
                        padding: 8px 16px;
                        font-weight: bold;
                    }
                    QPushButton:hover {
                        background-color: #1976D2;
                    }
                    QPushButton:pressed {
                        background-color: #1565C0;
                    }
                    QPushButton:disabled {
                        background-color: #BDBDBD;
                        color: #757575;
                    }
                """)
            else:
                self.setStyleSheet("""
                    QPushButton {
                        background-color: #E0E0E0;
                        color: #212121;
                        border: none;
                        border-radius: 4px;
                        padding: 8px 16px;
                    }
                    QPushButton:hover {
                        background-color: #BDBDBD;
                    }
                    QPushButton:pressed {
                        background-color: #9E9E9E;
                    }
                    QPushButton:disabled {
                        background-color: #F5F5F5;
                        color: #BDBDBD;
                    }
                """)

class DownloadWorker(QThread):
    progress = pyqtSignal(dict)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, url, output_path, format_choice):
        super().__init__()
        self.url = url
        self.output_path = output_path
        self.format_choice = format_choice
        self.has_gpu = check_gpu_availability()

    def get_ffmpeg_args(self):
        if self.has_gpu:
            # GPU encoding settings using NVENC
            return [
                '-c:v', 'h264_nvenc',  # Use NVIDIA GPU encoder
                '-preset', 'p4',       # Balanced preset
                '-tune', 'hq',         # High quality tuning
                '-rc', 'vbr',          # Variable bitrate
                '-cq', '19',           # Quality level (lower is better, 19 is visually lossless)
                '-b:v', '0',           # Let the quality parameter control the bitrate
                '-c:a', 'aac',
                '-b:a', '192k'
            ]
        else:
            # CPU encoding settings
            return [
                '-c:v', 'libx264',
                '-preset', 'medium',   # Balanced preset
                '-crf', '18',          # Quality level (lower is better, 18 is visually lossless)
                '-c:a', 'aac',
                '-b:a', '192k'
            ]

    def run(self):
        try:
            # Base options
            ydl_opts = {
                'format': 'bestvideo[height>=2160][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height>=1440][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height>=1080][ext=mp4]+bestaudio[ext=m4a]/bestvideo[height>=720][ext=mp4]+bestaudio[ext=m4a]/bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
                'outtmpl': f'{self.output_path}/%(title)s.%(ext)s',
                'progress_hooks': [self.progress_hook],
                'nocheckcertificate': True,
                'ignoreerrors': True,
                'no_warnings': True,
                'quiet': True,
                'extract_flat': False,
                'force_generic_extractor': False,
                'socket_timeout': 30,
                'retries': 10,
                'fragment_retries': 10,
                'skip_download_archive': True,
                'extractor_args': {
                    'youtube': {
                        'player_client': ['android', 'web', 'mweb', 'tv_embedded'],
                        'player_skip': ['webpage', 'configs'],
                    }
                },
                'postprocessors': [{
                    'key': 'FFmpegVideoConvertor',
                    'preferedformat': 'mp4',
                }],
                'merge_output_format': 'mp4',
                'prefer_ffmpeg': True,
                'keepvideo': False,
                'writethumbnail': False,
                'writesubtitles': False,
                'writeautomaticsub': False,
                'postprocessor_args': self.get_ffmpeg_args(),
                'geo_bypass': True,
                'geo_verification_proxy': None,
                'geo_bypass_country': None,
                'geo_bypass_ip_block': None,
                'extractor_retries': 5,
                'http_headers': {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-us,en;q=0.5',
                    'Sec-Fetch-Mode': 'navigate',
                }
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                try:
                    # First try to extract video info
                    info = ydl.extract_info(self.url, download=False)
                    if info:
                        # Check available formats
                        formats = info.get('formats', [])
                        if formats:
                            # Log available formats for debugging
                            print("\nAvailable formats:")
                            for f in formats:
                                if f.get('height'):
                                    print(f"Format: {f.get('format_id')} - Resolution: {f.get('height')}p - Ext: {f.get('ext')} - Filesize: {f.get('filesize', 'N/A')}")
                            
                            # Find the best format based on user selection
                            format_choice = self.format_choice
                            if "Full Resolution" in format_choice:
                                # Already using best format
                                pass
                            elif "1080p" in format_choice:
                                ydl_opts['format'] = 'bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/best[height<=1080]'
                            elif "720p" in format_choice:
                                ydl_opts['format'] = 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720]'
                            elif "480p" in format_choice:
                                ydl_opts['format'] = 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480]'
                            elif "Audio Only" in format_choice:
                                ydl_opts['format'] = 'bestaudio[ext=m4a]/bestaudio'
                        
                        # If info extraction succeeds, proceed with download
                        ydl.download([self.url])
                        self.finished.emit()
                        return
                except Exception as e:
                    # If info extraction fails, try direct download with different format
                    try:
                        # Try with a more specific format string
                        ydl_opts['format'] = 'bestvideo[height>=720]+bestaudio/best[height>=720]/best'
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl2:
                            ydl2.download([self.url])
                        self.finished.emit()
                        return
                    except Exception as e2:
                        raise e2

        except Exception as e:
            self.error.emit(str(e))

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            self.progress.emit(d)

DARK_STYLE = """
QWidget {
    background-color: #181818;
    color: #E0E0E0;
    font-family: 'Segoe UI', Arial, sans-serif;
}
QLabel {
    color: #E0E0E0;
}
QLineEdit, QComboBox, QProgressBar, QGroupBox, QTabWidget, QTabBar, QCheckBox {
    font-family: 'Segoe UI', Arial, sans-serif;
}
QLineEdit {
    padding: 8px;
    border: 1px solid #333;
    border-radius: 4px;
    background-color: #232323;
    color: #E0E0E0;
    min-height: 25px;
}
QComboBox {
    padding: 8px;
    border: 1px solid #333;
    border-radius: 4px;
    background-color: #232323;
    color: #E0E0E0;
    min-height: 25px;
}
QComboBox QAbstractItemView {
    background-color: #232323;
    color: #E0E0E0;
    selection-background-color: #333;
    selection-color: #E0E0E0;
    border: 1px solid #333;
}
QProgressBar {
    border: 1px solid #333;
    border-radius: 4px;
    text-align: center;
    background-color: #232323;
    color: #E0E0E0;
}
QProgressBar::chunk {
    background-color: #2196F3;
    border-radius: 3px;
}
QGroupBox {
    background-color: #232323;
    border: 1px solid #333;
    border-radius: 6px;
    margin-top: 12px;
    padding: 12px;
    color: #E0E0E0;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
    color: #42A5F5;
    font-weight: bold;
    background: transparent;
}
QTabWidget::pane {
    border: 1px solid #333;
    background: #181818;
}
QTabBar::tab {
    background: #232323;
    color: #E0E0E0;
    border: 1px solid #333;
    border-bottom: none;
    padding: 8px 16px;
    min-width: 100px;
}
QTabBar::tab:selected {
    background: #181818;
    color: #42A5F5;
    border-bottom: 2px solid #2196F3;
}
QTabBar::tab:!selected {
    margin-top: 2px;
}
QCheckBox {
    color: #E0E0E0;
    spacing: 8px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #333;
    border-radius: 3px;
    background-color: #232323;
}
QCheckBox::indicator:checked {
    background-color: #2196F3;
    border-color: #2196F3;
}
QPushButton {
    background-color: #232323;
    color: #E0E0E0;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
}
QPushButton:hover {
    background-color: #333;
}
QPushButton:pressed {
    background-color: #444;
}
QPushButton:disabled {
    background-color: #232323;
    color: #757575;
}
QMessageBox {
    background-color: #181818;
}
QMessageBox QLabel {
    color: #E0E0E0;
}
"""

LIGHT_STYLE = """
QWidget {
    background-color: #F5F5F5;
    color: #212121;
    font-family: 'Segoe UI', Arial, sans-serif;
}
QLabel {
    color: #212121;
}
QLineEdit, QComboBox, QProgressBar, QGroupBox, QTabWidget, QTabBar, QCheckBox {
    font-family: 'Segoe UI', Arial, sans-serif;
}
QLineEdit {
    padding: 8px;
    border: 1px solid #E0E0E0;
    border-radius: 4px;
    background-color: white;
    color: #212121;
    min-height: 25px;
}
QComboBox {
    padding: 8px;
    border: 1px solid #E0E0E0;
    border-radius: 4px;
    background-color: white;
    color: #212121;
    min-height: 25px;
}
QComboBox QAbstractItemView {
    background-color: white;
    color: #212121;
    selection-background-color: #E0E0E0;
    selection-color: #212121;
    border: 1px solid #E0E0E0;
}
QProgressBar {
    border: 1px solid #E0E0E0;
    border-radius: 4px;
    text-align: center;
    background-color: #F5F5F5;
    color: #212121;
}
QProgressBar::chunk {
    background-color: #2196F3;
    border-radius: 3px;
}
QGroupBox {
    background-color: #FFFFFF;
    border: 1px solid #E0E0E0;
    border-radius: 6px;
    margin-top: 12px;
    padding: 12px;
    color: #212121;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 10px;
    padding: 0 5px;
    color: #2196F3;
    font-weight: bold;
    background: transparent;
}
QTabWidget::pane {
    border: 1px solid #E0E0E0;
    background: #F5F5F5;
}
QTabBar::tab {
    background: #FFFFFF;
    color: #212121;
    border: 1px solid #E0E0E0;
    border-bottom: none;
    padding: 8px 16px;
    min-width: 100px;
}
QTabBar::tab:selected {
    background: #F5F5F5;
    color: #2196F3;
    border-bottom: 2px solid #2196F3;
}
QTabBar::tab:!selected {
    margin-top: 2px;
}
QCheckBox {
    color: #212121;
    spacing: 8px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border: 2px solid #E0E0E0;
    border-radius: 3px;
    background-color: white;
}
QCheckBox::indicator:checked {
    background-color: #2196F3;
    border-color: #2196F3;
}
QPushButton {
    background-color: #E0E0E0;
    color: #212121;
    border: none;
    border-radius: 4px;
    padding: 8px 16px;
}
QPushButton:hover {
    background-color: #BDBDBD;
}
QPushButton:pressed {
    background-color: #9E9E9E;
}
QPushButton:disabled {
    background-color: #F5F5F5;
    color: #BDBDBD;
}
QMessageBox {
    background-color: #F5F5F5;
}
QMessageBox QLabel {
    color: #212121;
}
"""

class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.is_dark_mode = True
        self.init_ui()
        self.apply_theme()

    def apply_theme(self):
        app = QApplication.instance()
        if self.is_dark_mode:
            if app:
                app.setStyleSheet(DARK_STYLE)
        else:
            if app:
                app.setStyleSheet(LIGHT_STYLE)

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Title and theme switcher
        title_layout = QHBoxLayout()
        title = QLabel("YouTube Video Downloader")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #2196F3;
            margin-bottom: 10px;
        """)
        title_layout.addWidget(title)
        
        # Theme switcher
        self.theme_switch = QCheckBox("Light Mode")
        self.theme_switch.setChecked(not self.is_dark_mode)
        self.theme_switch.stateChanged.connect(self.toggle_theme)
        title_layout.addWidget(self.theme_switch, alignment=Qt.AlignmentFlag.AlignRight)
        layout.addLayout(title_layout)

        # URL input group
        url_group = QGroupBox("Video URL")
        url_layout = QVBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube URL")
        url_layout.addWidget(self.url_input)
        url_group.setLayout(url_layout)
        layout.addWidget(url_group)

        # Quality selection group
        quality_group = QGroupBox("Quality Settings")
        quality_layout = QVBoxLayout()
        self.format_combo = QComboBox()
        self.format_combo.addItems([
            "Best Quality (Full Resolution)",
            "High Quality (up to 1080p)",
            "Medium Quality (up to 720p)",
            "Low Quality (up to 480p)",
            "Audio Only"
        ])
        quality_layout.addWidget(self.format_combo)
        quality_group.setLayout(quality_layout)
        layout.addWidget(quality_group)

        # Output directory group
        dir_group = QGroupBox("Output Settings")
        dir_layout = QVBoxLayout()
        self.dir_button = StyledButton("Select Output Directory", is_dark_mode=self.is_dark_mode)
        self.dir_button.clicked.connect(self.select_directory)
        self.dir_label = QLabel("No directory selected")
        self.dir_label.setStyleSheet("color: #757575;" if not self.is_dark_mode else "color: #E0E0E0;")
        dir_layout.addWidget(self.dir_button)
        dir_layout.addWidget(self.dir_label)
        dir_group.setLayout(dir_layout)
        layout.addWidget(dir_group)

        # Download button
        self.download_button = StyledButton("Download", primary=True, is_dark_mode=self.is_dark_mode)
        self.download_button.clicked.connect(self.start_download)
        layout.addWidget(self.download_button)

        # Progress group
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout()
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(25)
        progress_layout.addWidget(self.progress_bar)
        self.status_label = QLabel("Ready")
        self.status_label.setStyleSheet("color: #757575;" if not self.is_dark_mode else "color: #E0E0E0;")
        progress_layout.addWidget(self.status_label)
        progress_group.setLayout(progress_layout)
        layout.addWidget(progress_group)

        self.output_directory = None

    def toggle_theme(self, state):
        self.is_dark_mode = not state
        self.apply_theme()
        
        # Update buttons
        self.dir_button.is_dark_mode = self.is_dark_mode
        self.dir_button.apply_theme()
        self.download_button.is_dark_mode = self.is_dark_mode
        self.download_button.apply_theme()
        
        # Update status label colors
        if self.status_label.text() == "Ready":
            self.status_label.setStyleSheet("color: #757575;" if not self.is_dark_mode else "color: #E0E0E0;")
        elif "Downloading" in self.status_label.text():
            self.status_label.setStyleSheet("color: #2196F3;")
        elif "completed" in self.status_label.text().lower():
            self.status_label.setStyleSheet("color: #4CAF50;")
        elif "Error" in self.status_label.text():
            self.status_label.setStyleSheet("color: #F44336;")

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")
        if directory:
            self.output_directory = directory
            self.dir_label.setText(directory)
            self.dir_label.setStyleSheet("color: #2196F3;")

    def start_download(self):
        if not self.url_input.text():
            QMessageBox.warning(self, "Error", "Please enter a YouTube URL")
            return
        
        if not self.output_directory:
            QMessageBox.warning(self, "Error", "Please select an output directory")
            return

        self.download_button.setEnabled(False)
        self.worker = DownloadWorker(
            self.url_input.text(),
            self.output_directory,
            self.format_combo.currentText()
        )
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.download_finished)
        self.worker.error.connect(self.download_error)
        self.worker.start()

    def update_progress(self, d):
        if 'downloaded_bytes' in d and 'total_bytes' in d:
            progress = (d['downloaded_bytes'] / d['total_bytes']) * 100
            self.progress_bar.setValue(int(progress))
            self.status_label.setText(f"Downloading: {d.get('filename', '')}")
            self.status_label.setStyleSheet("color: #2196F3;")

    def download_finished(self):
        self.download_button.setEnabled(True)
        self.progress_bar.setValue(100)
        self.status_label.setText("Download completed!")
        self.status_label.setStyleSheet("color: #4CAF50;")
        QMessageBox.information(self, "Success", "Download completed successfully!")

    def download_error(self, error_msg):
        self.download_button.setEnabled(True)
        self.status_label.setText("Error occurred during download")
        self.status_label.setStyleSheet("color: #F44336;")
        QMessageBox.critical(self, "Error", f"Download failed: {error_msg}\n\nTry selecting a different quality or check if the video is available in your region.") 