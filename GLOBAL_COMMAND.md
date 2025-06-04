# PDF Converter - Global Command

## Installation Complete! 🎉

The PDF converter has been successfully installed as a global command called `pdf-convert`.

## Usage

You can now use `pdf-convert` from anywhere on your system:

### Basic Commands

```bash
# Convert files in any directory
pdf-convert /path/to/your/documents

# Convert current directory
pdf-convert .

# Show help
pdf-convert --help

# Check version
pdf-convert --version
```

### Examples

```bash
# Convert Documents folder (maintains structure)
pdf-convert ~/Documents/MyFiles

# Convert with flat structure
pdf-convert ~/Documents/MyFiles --flat

# Convert with custom output directory
pdf-convert ~/Documents/MyFiles --output ~/Desktop/PDFs

# Convert with detailed output
pdf-convert ~/Documents/MyFiles --verbose

# Convert Desktop files to a specific location
pdf-convert ~/Desktop --output ~/Documents/ConvertedPDFs --flat
```

## Command Location

The command is installed at: `/usr/local/bin/pdf-convert`

## Supported Formats

- **Images**: JPG, PNG, GIF, BMP, TIFF, WebP
- **Documents**: DOCX, TXT, Markdown
- **Spreadsheets**: XLSX, XLS
- **Presentations**: PPTX
- **PDFs**: Existing PDFs (will be copied)

## Options

- `--flat` - Create flat structure (all PDFs in one folder)
- `--output PATH` or `-o PATH` - Custom output directory
- `--verbose` or `-v` - Show detailed output
- `--version` - Show version information
- `--help` - Show help message

## Uninstalling

To remove the global command:
```bash
sudo rm /usr/local/bin/pdf-convert
```

## Updating

To update the command with a newer version:
```bash
# Navigate to your project directory
cd "/Users/manbhawan/Library/CloudStorage/OneDrive-Personal/My projects/PDF converter"

# Copy the updated script
sudo cp pdf_converter_cli.py /usr/local/bin/pdf-convert
sudo chmod +x /usr/local/bin/pdf-convert
```

## Notes

- The command works from any directory on your system
- All original files remain unchanged
- PDFs are created in a separate directory structure
- Use `Ctrl+C` to interrupt conversion if needed 