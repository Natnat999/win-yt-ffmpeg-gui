import os
import subprocess
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                            QLabel, QFileDialog, QComboBox, QProgressBar,
                            QMessageBox, QCheckBox, QSpinBox, QDoubleSpinBox,
                            QGroupBox, QScrollArea, QFrame, QApplication, QTabWidget)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor

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

class OperationGroup(QGroupBox):
    def __init__(self, title, is_dark_mode=True):
        super().__init__(title)
        self.is_dark_mode = is_dark_mode
        self.apply_theme()

    def apply_theme(self):
        if self.is_dark_mode:
            self.setStyleSheet("""
                QGroupBox {
                    background-color: #2D2D2D;
                    border: 1px solid #424242;
                    border-radius: 6px;
                    margin-top: 12px;
                    padding: 12px;
                    color: #E0E0E0;
                }
                QGroupBox::title {
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px;
                    color: #2196F3;
                    font-weight: bold;
                }
                QLabel {
                    color: #E0E0E0;
                }
                QComboBox, QSpinBox, QDoubleSpinBox {
                    padding: 5px;
                    border: 1px solid #424242;
                    border-radius: 4px;
                    background-color: #2D2D2D;
                    color: #E0E0E0;
                    min-height: 25px;
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox::down-arrow {
                    image: none;
                    border: none;
                }
                QComboBox QAbstractItemView {
                    background-color: #2D2D2D;
                    color: #E0E0E0;
                    selection-background-color: #424242;
                    selection-color: #E0E0E0;
                    border: 1px solid #424242;
                }
            """)
        else:
            self.setStyleSheet("""
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
                }
                QLabel {
                    color: #424242;
                }
                QComboBox, QSpinBox, QDoubleSpinBox {
                    padding: 5px;
                    border: 1px solid #E0E0E0;
                    border-radius: 4px;
                    background-color: white;
                    color: #212121;
                    min-height: 25px;
                }
                QComboBox::drop-down {
                    border: none;
                }
                QComboBox::down-arrow {
                    image: none;
                    border: none;
                }
                QComboBox QAbstractItemView {
                    background-color: white;
                    color: #212121;
                    selection-background-color: #E0E0E0;
                    selection-color: #212121;
                    border: 1px solid #E0E0E0;
                }
            """)

class FFmpegWorker(QThread):
    progress = pyqtSignal(dict)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, input_file, output_file, operations):
        super().__init__()
        self.input_file = input_file
        self.output_file = output_file
        self.operations = operations

    def run(self):
        try:
            # Build FFmpeg command based on selected operations
            command = ['ffmpeg', '-i', self.input_file]
            command.extend(['-y'])  # Overwrite output file if exists
            for op in self.operations:
                if op['type'] == 'compress':
                    command.extend([
                        '-c:v', 'libx264',
                        '-crf', str(op['quality']),
                        '-preset', op['preset']
                    ])
                elif op['type'] == 'convert':
                    command.extend(['-c:v', op['codec']])
                elif op['type'] == 'resize':
                    command.extend([
                        '-vf', f'scale={op["width"]}:{op["height"]}'
                    ])
                elif op['type'] == 'trim':
                    command.extend([
                        '-ss', str(op['start']),
                        '-t', str(op['duration'])
                    ])
                elif op['type'] == 'audio':
                    command.extend([
                        '-c:a', op['codec'],
                        '-b:a', f'{op["bitrate"]}k'
                    ])
            command.append(self.output_file)

            # Get video duration for progress calculation
            duration_cmd = ['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                          '-of', 'default=noprint_wrappers=1:nokey=1', self.input_file]
            duration_str = subprocess.check_output(duration_cmd).decode().strip()
            try:
                duration = float(duration_str)
                if duration <= 0:
                    raise ValueError
            except Exception:
                self.error.emit("Could not determine video duration. The file may be corrupted or unsupported.")
                return

            # Start FFmpeg process
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True
            )

            # Monitor progress
            while True:
                line = process.stderr.readline()
                if not line and process.poll() is not None:
                    break
                if 'time=' in line:
                    time_str = line.split('time=')[1].split()[0]
                    try:
                        hours, minutes, seconds = map(float, time_str.split(':'))
                        current_time = hours * 3600 + minutes * 60 + seconds
                        progress = (current_time / duration) * 100
                        self.progress.emit({'progress': progress})
                    except Exception:
                        pass

            if process.returncode != 0:
                raise Exception("FFmpeg processing failed")

            self.finished.emit()
        except Exception as e:
            self.error.emit(f"Processing failed: {e}")

class FFmpegProcessor(QWidget):
    def __init__(self):
        super().__init__()
        self.is_dark_mode = True
        self.init_ui()
        self.apply_theme()
        self.operations = []

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
        title = QLabel("FFmpeg Video Processor")
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

        # Create scroll area for operations
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.operations_layout = QVBoxLayout(scroll_content)
        self.operations_layout.setSpacing(10)
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # Add operation buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        
        add_compress = StyledButton("Add Compression", is_dark_mode=self.is_dark_mode)
        add_compress.clicked.connect(lambda: self.add_operation('compress'))
        buttons_layout.addWidget(add_compress)
        
        add_convert = StyledButton("Add Conversion", is_dark_mode=self.is_dark_mode)
        add_convert.clicked.connect(lambda: self.add_operation('convert'))
        buttons_layout.addWidget(add_convert)
        
        add_resize = StyledButton("Add Resize", is_dark_mode=self.is_dark_mode)
        add_resize.clicked.connect(lambda: self.add_operation('resize'))
        buttons_layout.addWidget(add_resize)
        
        add_trim = StyledButton("Add Trim", is_dark_mode=self.is_dark_mode)
        add_trim.clicked.connect(lambda: self.add_operation('trim'))
        buttons_layout.addWidget(add_trim)
        
        add_audio = StyledButton("Add Audio", is_dark_mode=self.is_dark_mode)
        add_audio.clicked.connect(lambda: self.add_operation('audio'))
        buttons_layout.addWidget(add_audio)
        
        layout.addLayout(buttons_layout)

        # File selection
        file_group = QGroupBox("File Selection")
        file_layout = QVBoxLayout()
        
        input_layout = QHBoxLayout()
        self.input_button = StyledButton("Select Input File", is_dark_mode=self.is_dark_mode)
        self.input_button.clicked.connect(self.select_input_file)
        self.input_label = QLabel("No file selected")
        self.input_label.setStyleSheet("color: #757575;" if not self.is_dark_mode else "color: #E0E0E0;")
        input_layout.addWidget(self.input_button)
        input_layout.addWidget(self.input_label)
        file_layout.addLayout(input_layout)

        output_layout = QHBoxLayout()
        self.output_button = StyledButton("Select Output File", is_dark_mode=self.is_dark_mode)
        self.output_button.clicked.connect(self.select_output_file)
        self.output_label = QLabel("No file selected")
        self.output_label.setStyleSheet("color: #757575;" if not self.is_dark_mode else "color: #E0E0E0;")
        output_layout.addWidget(self.output_button)
        output_layout.addWidget(self.output_label)
        file_layout.addLayout(output_layout)
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)

        # Process button
        self.process_button = StyledButton("Process", primary=True, is_dark_mode=self.is_dark_mode)
        self.process_button.clicked.connect(self.start_processing)
        layout.addWidget(self.process_button)

        # Progress section
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

        self.input_file = None
        self.output_file = None

    def toggle_theme(self, state):
        self.is_dark_mode = not state
        self.apply_theme()
        
        # Update buttons
        self.input_button.is_dark_mode = self.is_dark_mode
        self.input_button.apply_theme()
        self.output_button.is_dark_mode = self.is_dark_mode
        self.output_button.apply_theme()
        self.process_button.is_dark_mode = self.is_dark_mode
        self.process_button.apply_theme()
        
        # Update all operation groups
        for i in range(self.operations_layout.count()):
            widget = self.operations_layout.itemAt(i).widget()
            if isinstance(widget, OperationGroup):
                widget.is_dark_mode = self.is_dark_mode
                widget.apply_theme()
        
        # Update status label colors
        if self.status_label.text() == "Ready":
            self.status_label.setStyleSheet("color: #757575;" if not self.is_dark_mode else "color: #E0E0E0;")
        elif "Processing" in self.status_label.text():
            self.status_label.setStyleSheet("color: #2196F3;")
        elif "completed" in self.status_label.text().lower():
            self.status_label.setStyleSheet("color: #4CAF50;")
        elif "Error" in self.status_label.text():
            self.status_label.setStyleSheet("color: #F44336;")

    def add_operation(self, op_type):
        group = OperationGroup("", self.is_dark_mode)
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        if op_type == 'compress':
            group.setTitle("Compression")
            quality_layout = QHBoxLayout()
            quality_layout.addWidget(QLabel("Quality:"))
            quality_spin = QSpinBox()
            quality_spin.setRange(0, 51)
            quality_spin.setValue(23)
            quality_layout.addWidget(quality_spin)
            layout.addLayout(quality_layout)
            
            preset_layout = QHBoxLayout()
            preset_layout.addWidget(QLabel("Preset:"))
            preset_combo = QComboBox()
            preset_combo.addItems(['ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 'medium', 'slow', 'slower', 'veryslow'])
            preset_combo.setCurrentText('medium')
            preset_layout.addWidget(preset_combo)
            layout.addLayout(preset_layout)
            
            operation = {
                'type': 'compress',
                'quality': quality_spin.value(),
                'preset': preset_combo.currentText()
            }
            
            quality_spin.valueChanged.connect(lambda v: operation.update({'quality': v}))
            preset_combo.currentTextChanged.connect(lambda v: operation.update({'preset': v}))
            
        elif op_type == 'convert':
            group.setTitle("Conversion")
            codec_layout = QHBoxLayout()
            codec_layout.addWidget(QLabel("Codec:"))
            codec_combo = QComboBox()
            codec_combo.addItems(['libx264', 'libx265', 'mpeg4', 'vp9'])
            codec_layout.addWidget(codec_combo)
            layout.addLayout(codec_layout)
            
            operation = {
                'type': 'convert',
                'codec': codec_combo.currentText()
            }
            
            codec_combo.currentTextChanged.connect(lambda v: operation.update({'codec': v}))
            
        elif op_type == 'resize':
            group.setTitle("Resize")
            size_layout = QHBoxLayout()
            size_layout.addWidget(QLabel("Width:"))
            width_spin = QSpinBox()
            width_spin.setRange(1, 7680)
            width_spin.setValue(1920)
            size_layout.addWidget(width_spin)
            
            size_layout.addWidget(QLabel("Height:"))
            height_spin = QSpinBox()
            height_spin.setRange(1, 4320)
            height_spin.setValue(1080)
            size_layout.addWidget(height_spin)
            layout.addLayout(size_layout)
            
            operation = {
                'type': 'resize',
                'width': width_spin.value(),
                'height': height_spin.value()
            }
            
            width_spin.valueChanged.connect(lambda v: operation.update({'width': v}))
            height_spin.valueChanged.connect(lambda v: operation.update({'height': v}))
            
        elif op_type == 'trim':
            group.setTitle("Trim")
            trim_layout = QHBoxLayout()
            trim_layout.addWidget(QLabel("Start (seconds):"))
            start_spin = QDoubleSpinBox()
            start_spin.setRange(0, 999999)
            trim_layout.addWidget(start_spin)
            
            trim_layout.addWidget(QLabel("Duration (seconds):"))
            duration_spin = QDoubleSpinBox()
            duration_spin.setRange(0, 999999)
            trim_layout.addWidget(duration_spin)
            layout.addLayout(trim_layout)
            
            operation = {
                'type': 'trim',
                'start': start_spin.value(),
                'duration': duration_spin.value()
            }
            
            start_spin.valueChanged.connect(lambda v: operation.update({'start': v}))
            duration_spin.valueChanged.connect(lambda v: operation.update({'duration': v}))
            
        elif op_type == 'audio':
            group.setTitle("Audio")
            audio_layout = QHBoxLayout()
            audio_layout.addWidget(QLabel("Codec:"))
            codec_combo = QComboBox()
            codec_combo.addItems(['aac', 'mp3', 'opus', 'vorbis'])
            audio_layout.addWidget(codec_combo)
            
            audio_layout.addWidget(QLabel("Bitrate (kbps):"))
            bitrate_spin = QSpinBox()
            bitrate_spin.setRange(32, 320)
            bitrate_spin.setValue(192)
            audio_layout.addWidget(bitrate_spin)
            layout.addLayout(audio_layout)
            
            operation = {
                'type': 'audio',
                'codec': codec_combo.currentText(),
                'bitrate': bitrate_spin.value()
            }
            
            codec_combo.currentTextChanged.connect(lambda v: operation.update({'codec': v}))
            bitrate_spin.valueChanged.connect(lambda v: operation.update({'bitrate': v}))
        
        # Add remove button
        remove_button = StyledButton("Remove")
        remove_button.clicked.connect(lambda: self.remove_operation(group, operation))
        layout.addWidget(remove_button)
        
        group.setLayout(layout)
        self.operations_layout.addWidget(group)
        self.operations.append(operation)

    def remove_operation(self, group, operation):
        self.operations.remove(operation)
        group.deleteLater()

    def select_input_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Select Input File", "",
            "Video Files (*.mp4 *.avi *.mkv *.mov *.wmv);;All Files (*.*)"
        )
        if file_name:
            self.input_file = file_name
            self.input_label.setText(file_name)
            self.input_label.setStyleSheet("color: #2196F3;")

    def select_output_file(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Select Output File", "",
            "MP4 Files (*.mp4);;All Files (*.*)"
        )
        if file_name:
            self.output_file = file_name
            self.output_label.setText(file_name)
            self.output_label.setStyleSheet("color: #2196F3;")

    def start_processing(self):
        if not self.input_file:
            QMessageBox.warning(self, "Error", "Please select an input file")
            return
        
        if not self.output_file:
            QMessageBox.warning(self, "Error", "Please select an output file")
            return
        
        if not self.operations:
            QMessageBox.warning(self, "Error", "Please add at least one operation")
            return

        self.process_button.setEnabled(False)
        self.worker = FFmpegWorker(
            self.input_file,
            self.output_file,
            self.operations
        )
        self.worker.progress.connect(self.update_progress)
        self.worker.finished.connect(self.processing_finished)
        self.worker.error.connect(self.processing_error)
        self.worker.start()

    def update_progress(self, d):
        self.progress_bar.setValue(int(d['progress']))
        self.status_label.setText(f"Processing: {int(d['progress'])}%")
        self.status_label.setStyleSheet("color: #2196F3;")

    def processing_finished(self):
        self.process_button.setEnabled(True)
        self.progress_bar.setValue(100)
        self.status_label.setText("Processing completed!")
        self.status_label.setStyleSheet("color: #4CAF50;")
        QMessageBox.information(self, "Success", "Processing completed successfully!")

    def processing_error(self, error_msg):
        self.process_button.setEnabled(True)
        self.status_label.setText("Error occurred during processing")
        self.status_label.setStyleSheet("color: #F44336;")
        QMessageBox.critical(self, "Error", f"Processing failed: {error_msg}") 