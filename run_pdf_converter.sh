#!/bin/bash

# PDF Converter Launcher Script for Mac
# This script ensures the app runs with the correct Python environment

echo "🔄 Starting PDF Converter..."

# Suppress Tkinter deprecation warning on Mac
export TK_SILENCE_DEPRECATION=1

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
REQUIRED_VERSION="3.7"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Python version $PYTHON_VERSION found, but $REQUIRED_VERSION or higher is required."
    exit 1
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if requirements are installed
echo "📦 Checking dependencies..."
python3 -c "
try:
    import PIL, docx, openpyxl, pptx, reportlab, PyPDF2, markdown
    print('✓ All dependencies are installed')
except ImportError as e:
    print(f'❌ Missing dependency: {e}')
    print('Installing requirements...')
    import subprocess
    subprocess.run(['pip3', 'install', '-r', 'requirements.txt'])
"

# Run the PDF Converter using the improved launcher
echo "🚀 Launching PDF Converter GUI with macOS optimizations..."

# Try GUI first, fallback to CLI if GUI fails due to macOS version
if python3 pdf_converter.py 2>/dev/null; then
    echo "GUI launched successfully"
else
    echo "⚠️  GUI not available (macOS version issue). Using CLI instead."
    echo "📋 CLI Usage Examples:"
    echo "   python3 pdf_converter_cli.py /path/to/documents"
    echo "   python3 pdf_converter_cli.py /path/to/documents --flat --verbose"
    echo "   python3 pdf_converter_cli.py --help"
    echo ""
    echo "💡 To convert files, run:"
    echo "   python3 pdf_converter_cli.py /path/to/your/files"
fi

echo "👋 PDF Converter closed." 