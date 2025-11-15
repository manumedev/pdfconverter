#!/bin/bash

# PDF Converter CLI Launcher Script
# This script provides an easy way to run the CLI version

echo "🔄 PDF Converter CLI Launcher"
echo "=============================="

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" &> /dev/null && pwd)"

# Change to the script directory
cd "$SCRIPT_DIR"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Check if a directory was provided as argument
if [ $# -eq 0 ]; then
    echo "📋 Usage: $0 <directory> [options]"
    echo ""
    echo "Examples:"
    echo "  $0 /path/to/documents"
    echo "  $0 /path/to/documents --flat --verbose"
    echo "  $0 . --output ../converted_pdfs"
    echo ""
    echo "For more options, run: python3 pdf_converter_cli.py --help"
    exit 1
fi

# Run the CLI with all provided arguments
echo "🚀 Running PDF Converter CLI..."
python3 pdf_converter_cli.py "$@"
