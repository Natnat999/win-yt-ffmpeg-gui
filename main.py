import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTabWidget, 
                            QWidget, QVBoxLayout)
from PyQt6.QtCore import Qt
from youtube_downloader import YouTubeDownloader
from ffmpeg_processor import FFmpegProcessor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Tools")
        self.setMinimumSize(800, 600)
        
        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Create tab widget
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # Create and add tabs
        self.youtube_tab = YouTubeDownloader()
        self.ffmpeg_tab = FFmpegProcessor()
        
        tabs.addTab(self.youtube_tab, "YouTube Downloader")
        tabs.addTab(self.ffmpeg_tab, "FFmpeg Processor")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 