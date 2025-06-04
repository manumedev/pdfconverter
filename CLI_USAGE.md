# PDF Converter - Command Line Usage Guide

## Quick Start

The PDF converter can be used as a command-line tool for batch converting files to PDF format.

### Basic Usage

```bash
# Convert all files in a directory (maintains folder structure)
python3 pdf_converter_cli.py /path/to/your/documents

# Convert current directory
python3 pdf_converter_cli.py .

# Show help
python3 pdf_converter_cli.py --help
```

## Command Line Options

### Required Arguments

- **`directory`** - Path to the directory containing files to convert

### Optional Arguments

- **`--flat`** - Create flat structure (all PDFs in one folder) instead of maintaining directory structure
- **`--output PATH`** or **`-o PATH`** - Custom output directory for PDFs
- **`--verbose`** or **`-v`** - Show detailed output including file list and conversion paths
- **`--version`** - Show version information
- **`--help`** or **`-h`** - Show help message

## Examples

### 1. Basic Conversion (Maintain Directory Structure)
```bash
python3 pdf_converter_cli.py ~/Documents/MyFiles
```
**Result:**
```
MyFiles/
├── document.docx
├── image.jpg
└── pdf/                    ← Created automatically
    ├── document.pdf
    └── image.pdf
```

### 2. Flat Structure Conversion
```bash
python3 pdf_converter_cli.py ~/Documents/MyFiles --flat
```
**Result:**
```
MyFiles/
├── document.docx
├── subfolder/
│   └── notes.txt
└── pdf/                    ← All PDFs in one folder
    ├── document.pdf
    └── subfolder_notes.pdf  ← Prefixed with parent folder
```

### 3. Custom Output Directory
```bash
python3 pdf_converter_cli.py ~/Documents/MyFiles --output ~/Desktop/ConvertedPDFs
```
**Result:** All PDFs saved to `~/Desktop/ConvertedPDFs/`

### 4. Verbose Output
```bash
python3 pdf_converter_cli.py ~/Documents/MyFiles --verbose
```
**Shows:** Detailed file list and conversion paths

### 5. Flat Structure with Custom Output
```bash
python3 pdf_converter_cli.py ~/Documents/MyFiles --flat --output ~/Desktop/PDFs --verbose
```

## Supported File Formats

| Category | Extensions |
|----------|------------|
| **Images** | JPG, JPEG, PNG, GIF, BMP, TIFF, WebP |
| **Documents** | DOCX, TXT, Markdown (.md) |
| **Spreadsheets** | XLSX, XLS |
| **Presentations** | PPTX |
| **PDFs** | PDF (will be copied) |

## Output Examples

### Structured Mode (Default)
```bash
$ python3 pdf_converter_cli.py test_files --verbose

🔄 PDF Converter - Command Line
📁 Source directory: /path/to/test_files
💾 Output directory: /path/to/test_files/pdf
🏗️  Structure mode: directory structure

📋 Found 4 files to convert:
   • README.md
   • sample_document.txt
   • sample_image.png
   • subfolder/nested_document.txt

[  1/4] Converting: README.md ✅
           → README.pdf
[  2/4] Converting: sample_document.txt ✅
           → sample_document.pdf
[  3/4] Converting: sample_image.png ✅
           → sample_image.pdf
[  4/4] Converting: subfolder/nested_document.txt ✅
           → subfolder/nested_document.pdf

📊 Conversion Summary:
   ✅ Successful: 4
   ❌ Failed: 0
   📁 PDFs saved to: /path/to/test_files/pdf
   🏗️  Structure: directory structure

🎉 Conversion completed successfully!
```

### Flat Mode
```bash
$ python3 pdf_converter_cli.py test_files --flat

🔄 PDF Converter - Command Line
📁 Source directory: /path/to/test_files
💾 Output directory: /path/to/test_files/pdf
🏗️  Structure mode: flat list

📋 Found 4 files to convert:
   Use --verbose to see file list

[  1/4] Converting: README.md ✅ → README.pdf
[  2/4] Converting: sample_document.txt ✅ → sample_document.pdf
[  3/4] Converting: sample_image.png ✅ → sample_image.pdf
[  4/4] Converting: subfolder/nested_document.txt ✅ → subfolder_nested_document.pdf

📊 Conversion Summary:
   ✅ Successful: 4
   ❌ Failed: 0
   📁 PDFs saved to: /path/to/test_files/pdf
   🏗️  Structure: flat list

🎉 Conversion completed successfully!
```

## Error Handling

### Common Errors and Solutions

1. **Directory not found**
   ```
   ❌ Error: Directory '/path/to/missing' does not exist
   ```
   *Solution:* Check the path and ensure the directory exists

2. **No supported files**
   ```
   ❌ No supported files found in the directory
   ```
   *Solution:* Check that the directory contains files with supported extensions

3. **Permission errors**
   ```
   ❌ Error: Permission denied
   ```
   *Solution:* Ensure you have read permissions for source files and write permissions for the output directory

4. **Dependency errors**
   ```
   Error importing required libraries: No module named 'PIL'
   ```
   *Solution:* Install requirements: `pip3 install -r requirements.txt`

## Tips and Best Practices

### 1. Test with a Small Directory First
```bash
# Create a test subdirectory
mkdir test_conversion
cp some_file.txt test_conversion/
python3 pdf_converter_cli.py test_conversion --verbose
```

### 2. Use Absolute Paths for Clarity
```bash
python3 pdf_converter_cli.py /Users/username/Documents/MyFiles
```

### 3. Backup Important Files
The converter doesn't modify original files, but it's always good practice to backup important documents.

### 4. Check Output Before Deleting Originals
```bash
# Convert and check results
python3 pdf_converter_cli.py ~/Documents/ToConvert
# Review PDFs in ~/Documents/ToConvert/pdf/
# Only then decide whether to keep originals
```

### 5. Use Flat Mode for Complex Directory Structures
If you have deeply nested folders and want all PDFs easily accessible:
```bash
python3 pdf_converter_cli.py ~/Documents/ComplexProject --flat
```

### 6. Custom Output for Organization
```bash
# Organize by date
python3 pdf_converter_cli.py ~/Documents/Reports --output ~/Documents/PDFs/$(date +%Y-%m-%d)
```

## Performance Notes

- **Large files**: Images and complex documents take longer to convert
- **Many files**: Use `--verbose` to monitor progress
- **Interruption**: Press `Ctrl+C` to stop conversion safely
- **Disk space**: Ensure sufficient space in the output directory

## Integration with Other Tools

### Use with find
```bash
# Find directories with specific files and convert them
find ~/Documents -name "*.docx" -execdir python3 /path/to/pdf_converter_cli.py . \;
```

### Use in Scripts
```bash
#!/bin/bash
# Convert all project directories
for dir in ~/Projects/*/; do
    echo "Converting $dir"
    python3 pdf_converter_cli.py "$dir" --flat --output ~/ConvertedProjects/$(basename "$dir")
done
```

## Exit Codes

- **0**: Success (at least one file converted)
- **1**: Error (no files converted, invalid arguments, or other errors)

Use exit codes in scripts:
```bash
if python3 pdf_converter_cli.py ~/Documents/MyFiles; then
    echo "Conversion successful!"
else
    echo "Conversion failed!"
fi
``` 