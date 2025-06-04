# PDF Converter for Mac

A desktop application for Mac that converts various file types to PDF format. Simply select a directory, and the app will convert all supported files in that directory and its subdirectories to PDF, with options for organizing the output.

## Features

- **Batch Conversion**: Convert entire directories and subdirectories at once
- **Multiple File Formats**: Supports images, documents, spreadsheets, and presentations
- **Flexible Output Structure**: Choose between maintaining directory structure or creating a flat list
- **Progress Tracking**: Real-time progress bar and detailed conversion logs
- **User-Friendly GUI**: Clean and intuitive interface built with tkinter
- **Conflict Resolution**: Automatic filename handling to prevent overwrites

## Supported File Formats

- **Images**: JPG, JPEG, PNG, GIF, BMP, TIFF, WebP
- **Documents**: DOCX, TXT, Markdown (.md)
- **Spreadsheets**: XLSX, XLS
- **Presentations**: PPTX
- **PDFs**: Existing PDFs will be copied to maintain file organization

## Installation

### Prerequisites

- Python 3.7 or higher
- macOS (tested on macOS 11+)

### Setup

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd pdf-converter
   ```

2. **Install Python dependencies**
   ```bash
   pip3 install -r requirements.txt
   ```

   Or install individually:
   ```bash
   pip3 install Pillow python-docx openpyxl python-pptx reportlab PyPDF2 markdown
   ```

3. **Make the script executable**
   ```bash
   chmod +x pdf_converter.py
   ```

## Usage

### Running the Application

```bash
python3 pdf_converter.py
```

### Using the GUI

1. **Launch the application** - The GUI window will open
2. **Select Directory** - Click "Browse" to choose the directory containing files to convert
3. **Choose Output Structure**:
   - **Maintain directory structure**: Preserves the original folder hierarchy
   - **Flat list**: Places all PDFs in one folder with unique names
4. **Start Conversion** - Click "Convert to PDF" to begin the process
5. **Monitor Progress** - Watch the progress bar and conversion logs in real-time
6. **View Results** - Converted PDFs will be saved in a new "pdf" folder within the selected directory

## Output Structure Options

### Maintain Directory Structure (Default)

Preserves the original folder hierarchy in the PDF output directory.

**Before conversion:**
```
/Users/username/Documents/MyFiles/
├── document.docx
├── image.jpg
├── spreadsheet.xlsx
└── subfolder/
    ├── presentation.pptx
    └── notes.txt
```

**After conversion (Structured):**
```
/Users/username/Documents/MyFiles/
├── document.docx
├── image.jpg
├── spreadsheet.xlsx
├── subfolder/
│   ├── presentation.pptx
│   └── notes.txt
└── pdf/                    ← New folder created
    ├── document.pdf
    ├── image.pdf
    ├── spreadsheet.pdf
    └── subfolder/          ← Directory structure preserved
        ├── presentation.pdf
        └── notes.pdf
```

### Flat List Structure

Places all converted PDFs in a single folder with unique names to prevent conflicts.

**After conversion (Flat):**
```
/Users/username/Documents/MyFiles/
├── document.docx
├── image.jpg
├── spreadsheet.xlsx
├── subfolder/
│   ├── presentation.pptx
│   └── notes.txt
└── pdf/                    ← New folder created
    ├── document.pdf
    ├── image.pdf
    ├── spreadsheet.pdf
    ├── subfolder_presentation.pdf  ← Prefixed with parent folder
    └── subfolder_notes.pdf         ← Automatic conflict resolution
```

## Programmatic Usage

You can also use the converter programmatically:

```python
from pdf_converter import PDFConverter

converter = PDFConverter()

# Convert a single file
success = converter.convert_file("input.docx", "output.pdf")

# Check if a file type is supported
file_type = converter.get_file_type("document.xlsx")  # Returns 'spreadsheets'
```

### Demo Script

Run the included demo script to see both output modes:

```bash
# Demo both modes
python3 demo.py

# Demo only structured mode
python3 demo.py --mode structured

# Demo only flat mode
python3 demo.py --mode flat
```

## Creating a Mac App Bundle (Optional)

To create a standalone Mac application:

1. **Install py2app**
   ```bash
   pip3 install py2app
   ```

2. **Create setup.py**
   ```python
   from setuptools import setup
   
   APP = ['pdf_converter.py']
   DATA_FILES = []
   OPTIONS = {
       'argv_emulation': True,
       'plist': {
           'CFBundleName': 'PDF Converter',
           'CFBundleDisplayName': 'PDF Converter',
           'CFBundleIdentifier': 'com.yourname.pdf-converter',
           'CFBundleVersion': '1.0.0',
           'CFBundleShortVersionString': '1.0.0',
       }
   }
   
   setup(
       app=APP,
       data_files=DATA_FILES,
       options={'py2app': OPTIONS},
       setup_requires=['py2app'],
   )
   ```

3. **Build the app**
   ```bash
   python3 setup.py py2app
   ```

4. **Find your app in the `dist/` folder**

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Make sure all dependencies are installed: `pip3 install -r requirements.txt`
   - Check Python version: `python3 --version` (should be 3.7+)

2. **Permission Errors**
   - Ensure you have read permissions for the source directory
   - Ensure you have write permissions for the parent directory (to create the "pdf" folder)

3. **Conversion Failures**
   - Check the conversion logs in the app for specific error messages
   - Some file formats might not be supported or might be corrupted
   - Very large files might take longer to convert

4. **Tkinter Deprecation Warning**
   - If you see a Tk deprecation warning, you can suppress it by setting: `export TK_SILENCE_DEPRECATION=1`

### Performance Tips

- **Large Directories**: For directories with many files, the conversion might take some time
- **File Size**: Very large files (especially images) might take longer to convert
- **Memory Usage**: Converting many large files simultaneously might use significant memory
- **Flat Structure**: Use flat structure for easier file management when dealing with complex directory hierarchies

## File Conversion Details

### Images
- Converted using Pillow library
- Maintains aspect ratio and resolution
- Automatically converts to RGB color space if needed

### Documents
- **DOCX**: Extracts text content and formatting
- **TXT**: Preserves line breaks and basic formatting
- **Markdown**: Basic markdown rendering to PDF

### Spreadsheets
- **XLSX/XLS**: Shows sheet names and cell content
- Limited to first 50 rows and 10 columns for readability
- Multiple sheets are included in the same PDF

### Presentations
- **PPTX**: Extracts text from all slides
- Each slide becomes a separate page in the PDF
- Slide numbers are included for reference

## Contributing

Feel free to contribute to this project by:
- Reporting bugs
- Suggesting new features
- Adding support for additional file formats
- Improving the user interface

## License

This project is open source. Please check the license file for details.

## Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Look at the conversion logs in the app for error details
3. Create an issue in the project repository

---

**Note**: This application is designed specifically for Mac and uses native Python libraries. For best results, ensure you're running a recent version of macOS and Python 3.7+. 