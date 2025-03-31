from PySide6.QtWidgets import QPushButton, QLabel
from PySide6.QtCore import Qt, QThread, Signal
from ui.base_screen import BaseScreen
from ui.components.progress_button import ProgressButton
from data.table_loader import TableLoader
from domain.table import Table
from typing import Dict
import os
from pathlib import Path
import csv
from ui.styles.button_styles import get_sci_fi_button_style

class TableLoadingThread(QThread):
    finished = Signal(dict)
    progress = Signal(int)
    
    def __init__(self, table_loader: TableLoader, data_dir: str):
        super().__init__()
        self.table_loader = table_loader
        self.data_dir = data_dir
    
    def run(self):
        # Count the total number of files to be loaded
        data_path = Path(self.data_dir)
        print(f"Looking for table files in: {data_path.absolute()}")
        table_files = list(data_path.glob("*.csv"))
        total_files = len(table_files)
        print(f"Found {total_files} table files")
        
        if total_files == 0:
            self.progress.emit(100)  # No files to load
            self.finished.emit({})
            return
        
        # Initialize an empty tables dictionary
        tables = {}
        
        # Load each table file and update progress
        for i, file_path in enumerate(table_files):
            # Calculate progress percentage
            progress = int((i / total_files) * 100)
            self.progress.emit(progress)
            
            # Load the individual table
            table_name = file_path.stem
            
            # Read the file and create a Table object
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                dice_sides = 100  # Default to d100, could be made configurable
                
                table = Table(table_name, self.table_loader.dice_factory.create_dice(dice_sides))
                
                for row in reader:
                    min_roll = int(row['min_roll'])
                    max_roll = int(row['max_roll'])
                    text = row['text']
                    table.add_entry(min_roll, max_roll, text)
                
                tables[table_name] = table
            
            # Small sleep to allow UI updates
            self.msleep(10)
        
        # Ensure we reach 100% at the end
        self.progress.emit(100)
        self.finished.emit(tables)

class CivilisationGenerationScreen(BaseScreen):
    def __init__(self, table_loader: TableLoader):
        super().__init__("Civilisation Generation")
        self.table_loader = table_loader
        self.tables: Dict[str, Table] = {}
        
        # Create Generate button with progress
        self.generate_button = ProgressButton("Generate")
        self.generate_button.setEnabled(False)
        
        # Create result label
        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setWordWrap(True)
        self.result_label.hide()
        
        # Add widgets to layout - put result in the middle, button at the bottom
        self.layout.addStretch(1)  # Add flexible space at the top
        self.layout.addWidget(self.result_label)
        self.layout.addStretch(1)  # Add flexible space in the middle
        self.layout.addWidget(self.generate_button, alignment=Qt.AlignCenter)  # Button at the bottom
        
        # Connect signals
        self.generate_button.clicked.connect(self._on_generate)
        
        # Start loading tables
        self.start_data_loading()
    
    def start_data_loading(self):
        """Start loading the random table data"""
        self.generate_button.start_progress()
        
        # Create and start loading thread
        self.loading_thread = TableLoadingThread(self.table_loader, "data/tables")
        self.loading_thread.progress.connect(self.generate_button.set_progress)
        self.loading_thread.finished.connect(self._on_tables_loaded)
        self.loading_thread.start()
    
    def _on_tables_loaded(self, tables: Dict[str, Table]):
        """Called when tables are loaded"""
        self.tables = tables
        print(f"Tables loaded: {len(tables)} tables found")
        for table_name in tables.keys():
            print(f"  - {table_name}")
        self.generate_button.set_enabled(True)
    
    def _on_generate(self):
        """Handle generate button click"""
        if not self.tables:
            print("No tables available, cannot generate!")
            return
        
        print(f"Generate button clicked, tables available: {len(self.tables)}")
        
        # Example: Roll on the first table
        first_table = next(iter(self.tables.values()))
        result = first_table.roll()
        
        print(f"Generated result: {result.value} - {result.text}")
        
        # Show result
        self.result_label.setText(f"Roll: {result.value}\n{result.text}")
        self.result_label.show()
        
        # Replace the custom ProgressButton with a simple QPushButton
        self.layout.removeWidget(self.generate_button)
        self.generate_button.deleteLater()
        
        # Create a new standard button with the updated text
        new_button = QPushButton("Generate Again")
        new_button.setMinimumSize(300, 60)
        new_button.setMaximumWidth(300)
        new_button.setStyleSheet(get_sci_fi_button_style())
        new_button.clicked.connect(self._on_regenerate)
        
        # Add to layout at the same position
        self.layout.addWidget(new_button, alignment=Qt.AlignCenter)
        
        # Update reference to new button
        self.generate_button = new_button
        
        print("Replaced with standard QPushButton: Generate Again")
        
    def _on_regenerate(self):
        """Handle subsequent generation button clicks"""
        if not self.tables:
            return
            
        # Same functionality as _on_generate without changing the button again
        first_table = next(iter(self.tables.values()))
        result = first_table.roll()
        
        # Show result
        self.result_label.setText(f"Roll: {result.value}\n{result.text}")
        self.result_label.show() 