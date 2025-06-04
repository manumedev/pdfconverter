#!/usr/bin/env python3
"""
Demo script showing how to use the PDF Converter programmatically
"""

import os
import sys
from pathlib import Path
import shutil

# Import our PDF converter class
try:
    from pdf_converter import PDFConverter
except ImportError:
    print("Error: pdf_converter module not found. Make sure pdf_converter.py is in the same directory.")
    sys.exit(1)

def demo_conversion(maintain_structure=True):
    """Demo function showing programmatic use of the PDF converter
    
    Args:
        maintain_structure (bool): If True, maintains directory structure. 
                                 If False, creates flat list of PDFs.
    """
    
    structure_mode = "directory structure" if maintain_structure else "flat list"
    print(f"🔄 PDF Converter Demo - {structure_mode.title()}")
    print("=" * 50)
    
    # Initialize the converter
    converter = PDFConverter()
    
    # Set up paths
    test_dir = Path("test_files")
    pdf_dir = test_dir / "pdf"
    
    # Clear and recreate PDF output directory for clean demo
    if pdf_dir.exists():
        shutil.rmtree(pdf_dir)
    pdf_dir.mkdir(exist_ok=True)
    
    print(f"📁 Processing files in: {test_dir}")
    print(f"💾 Output directory: {pdf_dir}")
    print(f"🏗️  Structure mode: {structure_mode}")
    print()
    
    # Get all supported files
    supported_files = []
    for root, dirs, files in os.walk(test_dir):
        for file in files:
            file_path = Path(root) / file
            if converter.get_file_type(file_path):
                supported_files.append(file_path)
    
    if not supported_files:
        print("❌ No supported files found in test_files directory")
        return
    
    print(f"📋 Found {len(supported_files)} files to convert:")
    for file_path in supported_files:
        print(f"   • {file_path}")
    print()
    
    # Helper function to generate unique filename for flat structure
    def generate_unique_filename(output_dir, base_name, extension=".pdf"):
        output_path = output_dir / f"{base_name}{extension}"
        counter = 1
        
        while output_path.exists():
            output_path = output_dir / f"{base_name}_{counter}{extension}"
            counter += 1
        
        return output_path
    
    # Convert each file
    successful = 0
    failed = 0
    
    for file_path in supported_files:
        try:
            # Create relative path structure
            relative_path = file_path.relative_to(test_dir)
            pdf_filename = relative_path.stem + ".pdf"
            
            if maintain_structure:
                # Maintain directory structure
                output_subdir = pdf_dir / relative_path.parent
                output_subdir.mkdir(parents=True, exist_ok=True)
                output_path = output_subdir / pdf_filename
            else:
                # Flat structure - all files in root pdf directory
                base_name = relative_path.stem
                # If file is in subdirectory, include parent directory name to make it unique
                if relative_path.parent != Path('.'):
                    parent_name = str(relative_path.parent).replace('/', '_').replace('\\', '_')
                    base_name = f"{parent_name}_{base_name}"
                
                output_path = generate_unique_filename(pdf_dir, base_name)
            
            print(f"🔄 Converting: {relative_path}")
            
            # Convert the file
            if converter.convert_file(str(file_path), str(output_path)):
                successful += 1
                if maintain_structure:
                    print(f"   ✅ Success → {output_path}")
                else:
                    print(f"   ✅ Success → {output_path.name}")
            else:
                failed += 1
                print(f"   ❌ Failed")
                
        except Exception as e:
            failed += 1
            print(f"   ❌ Error: {str(e)}")
    
    print()
    print("📊 Conversion Summary:")
    print(f"   ✅ Successful: {successful}")
    print(f"   ❌ Failed: {failed}")
    print(f"   📁 PDFs saved in: {pdf_dir}")
    print(f"   🏗️  Structure: {structure_mode}")
    
    # List generated PDFs
    pdf_files = list(pdf_dir.rglob("*.pdf"))
    if pdf_files:
        print()
        print("📄 Generated PDF files:")
        for pdf_file in pdf_files:
            if maintain_structure:
                rel_path = pdf_file.relative_to(pdf_dir)
                print(f"   • {rel_path}")
            else:
                print(f"   • {pdf_file.name}")

def show_both_modes():
    """Demonstrate both structure modes"""
    print("🚀 PDF Converter Demo - Both Modes")
    print("=" * 60)
    print()
    
    # Demo 1: Maintain directory structure
    demo_conversion(maintain_structure=True)
    
    print("\n" + "="*60 + "\n")
    
    # Demo 2: Flat structure
    demo_conversion(maintain_structure=False)
    
    print("\n" + "="*60)
    print("🎉 Demo completed! Check the test_files/pdf directory to see the results.")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="PDF Converter Demo")
    parser.add_argument("--mode", choices=["structured", "flat", "both"], 
                       default="both",
                       help="Conversion mode: 'structured' (maintain dirs), 'flat' (all in one folder), or 'both' (demo both)")
    
    args = parser.parse_args()
    
    if args.mode == "structured":
        demo_conversion(maintain_structure=True)
    elif args.mode == "flat":
        demo_conversion(maintain_structure=False)
    else:  # both
        show_both_modes() 