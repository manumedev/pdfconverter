#!/usr/bin/env python3
"""
PDF Converter - Prominent Display Version
Makes folder selection very visible with large status displays and automatic confirmations
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
import threading
from datetime import datetime

# Suppress deprecation warning
os.environ['TK_SILENCE_DEPRECATION'] = '1'

# Import the converter class
try:
    from pdf_converter_cli import PDFConverter
except ImportError:
    print("Error: Could not import PDFConverter. Make sure pdf_converter_cli.py is in the same directory.")
    sys.exit(1)


class ProminentPDFConverterGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PDF Converter Pro")
        self.root.geometry("700x800")
        
        # Initialize converter
        self.converter = PDFConverter()
        
        # Variables
        self.selected_directory = ""
        self.conversion_progress = tk.StringVar(value="Ready to convert files")
        self.maintain_structure = tk.BooleanVar(value=True)
        self.combine_files = tk.BooleanVar(value=False)
        
        # Create GUI
        self.create_gui()
        
    def create_gui(self):
        """Create GUI with very prominent folder selection display"""
        # Main frame
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title = tk.Label(main_frame, text="PDF Converter Pro", 
                        font=("Arial", 20, "bold"), fg="blue")
        title.pack(pady=(0, 20))
        
        # HUGE PROMINENT STATUS DISPLAY
        status_mega_frame = tk.Frame(main_frame, bg="lightcyan", relief="ridge", bd=5)
        status_mega_frame.pack(fill=tk.X, pady=(0, 20), padx=5)
        
        # Status title
        tk.Label(status_mega_frame, text="📂 CURRENT FOLDER SELECTION", 
                font=("Arial", 16, "bold"), bg="lightcyan", fg="darkblue").pack(pady=(15,10))
        
        # MASSIVE status display area
        self.mega_status_frame = tk.Frame(status_mega_frame, bg="white", relief="sunken", bd=3)
        self.mega_status_frame.pack(fill=tk.X, padx=20, pady=(0,15))
        
        # Large status text
        self.mega_status_label = tk.Label(self.mega_status_frame, 
                                         text="❌ NO FOLDER SELECTED", 
                                         font=("Arial", 18, "bold"), 
                                         bg="white", fg="red",
                                         pady=20, wraplength=600)
        self.mega_status_label.pack(fill=tk.X)
        
        # Additional info label
        self.info_label = tk.Label(status_mega_frame, 
                                  text="Click the button below to select your folder", 
                                  font=("Arial", 12), bg="lightcyan", fg="darkblue")
        self.info_label.pack(pady=(0,15))
        
        # HUGE Browse button
        self.browse_btn = tk.Button(main_frame, text="📁 SELECT FOLDER TO CONVERT", 
                                   command=self.browse_directory,
                                   font=("Arial", 16, "bold"), 
                                   bg="navy", fg="white", 
                                   pady=20, padx=40,
                                   relief="raised", bd=5)
        self.browse_btn.pack(pady=15)
        
        # Selection confirmation area
        self.confirm_frame = tk.Frame(main_frame, bg="lightgreen", relief="ridge", bd=3)
        # Don't pack initially - will show after selection
        
        self.confirm_label = tk.Label(self.confirm_frame, 
                                     text="✅ FOLDER SELECTED SUCCESSFULLY!", 
                                     font=("Arial", 14, "bold"), 
                                     bg="lightgreen", fg="darkgreen")
        self.confirm_label.pack(pady=10)
        
        self.confirm_details = tk.Label(self.confirm_frame, 
                                       text="", 
                                       font=("Arial", 11), 
                                       bg="lightgreen", fg="darkgreen",
                                       wraplength=600)
        self.confirm_details.pack(pady=(0,10))
        
        # Structure options
        options_frame = tk.Frame(main_frame)
        options_frame.pack(pady=15)
        
        tk.Label(options_frame, text="Output Structure:", 
                font=("Arial", 14, "bold")).pack(anchor="w")
        
        tk.Radiobutton(options_frame, text="Maintain directory structure", 
                      variable=self.maintain_structure, value=True,
                      font=("Arial", 11)).pack(anchor="w", pady=2)
        
        tk.Radiobutton(options_frame, text="Flat list (all PDFs in one folder)", 
                      variable=self.maintain_structure, value=False,
                      font=("Arial", 11)).pack(anchor="w", pady=2)
        
        # Combine option
        combine_frame = tk.Frame(options_frame)
        combine_frame.pack(fill=tk.X, pady=(10,0))
        
        tk.Checkbutton(combine_frame, text="📄 Combine all files into single PDF", 
                      variable=self.combine_files,
                      font=("Arial", 11, "bold"), fg="blue",
                      command=self.on_combine_toggle).pack(anchor="w")
        
        self.combine_info = tk.Label(combine_frame, 
                                   text="(Each file will have its own section with title)", 
                                   font=("Arial", 9), fg="gray")
        self.combine_info.pack(anchor="w", padx=(20,0))
        
        # Progress
        progress_frame = tk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=15)
        
        tk.Label(progress_frame, text="Conversion Progress:", 
                font=("Arial", 14, "bold")).pack(anchor="w")
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        self.progress_label = tk.Label(progress_frame, textvariable=self.conversion_progress,
                                      font=("Arial", 11))
        self.progress_label.pack(anchor="w")
        
        # HUGE CONVERT BUTTON
        self.convert_button = tk.Button(main_frame, text="🔄 CONVERT TO PDF", 
                                       command=self.start_conversion,
                                       font=("Arial", 18, "bold"), 
                                       bg="green", fg="white",
                                       pady=20, padx=50,
                                       relief="raised", bd=5)
        self.convert_button.pack(pady=20)
        
        # Results
        results_frame = tk.Frame(main_frame)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(10,0))
        
        tk.Label(results_frame, text="Conversion Results:", 
                font=("Arial", 14, "bold")).pack(anchor="w")
        
        # Text area
        text_frame = tk.Frame(results_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        self.results_text = tk.Text(text_frame, height=4, font=("Courier", 10))
        scrollbar = tk.Scrollbar(text_frame, command=self.results_text.yview)
        self.results_text.config(yscrollcommand=scrollbar.set)
        
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Initial message
        self.results_text.insert(tk.END, "Welcome to PDF Converter Pro!\n")
        self.results_text.insert(tk.END, "1. Click 'SELECT FOLDER TO CONVERT'\n")
        self.results_text.insert(tk.END, "2. Choose your output structure\n") 
        self.results_text.insert(tk.END, "3. Click 'CONVERT TO PDF'\n\n")
        self.results_text.config(state=tk.DISABLED)
        
    def browse_directory(self):
        """Browse for directory with very prominent feedback"""
        print("Browse button clicked - opening directory dialog...")
        
        # Change button to show it's working
        self.browse_btn.config(text="📁 OPENING FOLDER DIALOG...", bg="orange")
        self.root.update_idletasks()
        
        # Schedule the file dialog
        self.root.after(100, self._do_browse)
        
    def _do_browse(self):
        """Actually do the browsing with prominent feedback"""
        try:
            directory = filedialog.askdirectory(title="Select Directory to Convert")
            print(f"Directory selected: {directory}")
            
            if directory:
                # Verify directory
                if not os.path.exists(directory) or not os.path.isdir(directory):
                    print(f"❌ Invalid directory: {directory}")
                    messagebox.showerror("Error", "Selected directory is not valid or accessible")
                    self._reset_display()
                    return
                
                self.selected_directory = directory
                folder_name = Path(directory).name
                parent_path = str(Path(directory).parent)
                
                print(f"Folder name: {folder_name}")
                print(f"Parent path: {parent_path}")
                
                # Schedule the prominent update
                self.root.after(10, self._update_display_prominent, directory, folder_name, parent_path)
            else:
                print("No directory selected (user cancelled)")
                self.root.after(10, self._reset_display)
                
        except Exception as e:
            print(f"❌ Error in browse dialog: {e}")
            messagebox.showerror("Error", f"Error opening directory dialog: {str(e)}")
            self._reset_display()
            
    def _reset_display(self):
        """Reset display when cancelled"""
        try:
            # Reset button
            self.browse_btn.config(text="📁 SELECT FOLDER TO CONVERT", bg="navy")
            
            # Reset mega status
            self.mega_status_label.config(text="❌ NO FOLDER SELECTED", fg="red", bg="white")
            self.mega_status_frame.config(bg="white")
            
            # Reset info
            self.info_label.config(text="Click the button below to select your folder")
            
            # Hide confirmation frame
            self.confirm_frame.pack_forget()
            
            # Update window title
            self.root.title("PDF Converter Pro - No Folder Selected")
            
            self.root.update_idletasks()
            
        except Exception as e:
            print(f"❌ Error resetting display: {e}")
            
    def _update_display_prominent(self, directory, folder_name, parent_path):
        """Update display with VERY prominent visual feedback"""
        print(f"✅ Updating display for: {folder_name}")
        
        try:
            # 1. Update button to success state
            self.browse_btn.config(text="✅ FOLDER SELECTED!", bg="green")
            
            # 2. Update MEGA status display
            status_text = f"✅ SELECTED: {folder_name}"
            self.mega_status_label.config(text=status_text, fg="darkgreen", bg="lightgreen")
            self.mega_status_frame.config(bg="lightgreen")
            
            # 3. Update info label
            truncated_path = parent_path
            if len(truncated_path) > 60:
                truncated_path = "..." + truncated_path[-57:]
            self.info_label.config(text=f"📁 Location: {truncated_path}")
            
            # 4. Show confirmation frame
            self.confirm_details.config(text=f"Ready to convert files from: {folder_name}")
            self.confirm_frame.pack(fill=tk.X, pady=10, padx=5)
            
            # 5. Update window title 
            self.root.title(f"PDF Converter Pro - {folder_name}")
            
            # 6. Force all updates
            self.root.update_idletasks()
            
            print(f"🎯 Display updated successfully: {folder_name}")
            
            # 7. Show automatic confirmation dialog
            self.root.after(200, self._show_auto_confirmation, directory, folder_name)
            
            # 8. Schedule post-selection tasks
            self.root.after(1000, self._post_selection_tasks, directory)
            
        except Exception as e:
            print(f"❌ Error updating display: {e}")
            
    def _show_auto_confirmation(self, directory, folder_name):
        """Show automatic confirmation dialog"""
        try:
            # Count files quickly for preview
            file_count = 0
            try:
                for root, dirs, files in os.walk(directory):
                    file_count += len([f for f in files if self.converter.get_file_type(Path(root) / f)])
                    if file_count > 50:  # Stop counting at 50 for speed
                        file_count = "50+"
                        break
            except:
                file_count = "unknown"
                
            # Truncate path for display
            display_path = directory
            if len(display_path) > 70:
                display_path = display_path[:35] + "..." + display_path[-32:]
                
            message = (
                f"📁 Folder Successfully Selected!\n\n"
                f"Folder Name: {folder_name}\n"
                f"Full Path: {display_path}\n"
                f"Convertible Files: {file_count}\n\n"
                f"✅ You can now choose your output structure and click 'CONVERT TO PDF'"
            )
            
            messagebox.showinfo("Selection Confirmed", message)
            
        except Exception as e:
            print(f"❌ Error showing confirmation: {e}")
            
    def _post_selection_tasks(self, directory):
        """Handle logging and preview after UI update"""
        try:
            # Log selection
            self.log_message(f"📁 Selected folder: {directory}")
            
            # Preview files
            self.preview_files(directory)
            
        except Exception as e:
            print(f"❌ Error in post-selection tasks: {e}")
            self.log_message(f"❌ Error scanning directory: {str(e)}")
    
    def preview_files(self, directory):
        """Preview files to convert"""
        try:
            files = []
            file_types = {}
            
            for root, dirs, file_list in os.walk(directory):
                for file in file_list:
                    file_path = Path(root) / file
                    file_type = self.converter.get_file_type(file_path)
                    if file_type:
                        files.append(file_path)
                        file_types[file_type] = file_types.get(file_type, 0) + 1
            
            if files:
                self.log_message(f"🔍 Found {len(files)} convertible files")
                
                # Show breakdown by type
                type_icons = {
                    'images': '🖼️',
                    'documents': '📝', 
                    'spreadsheets': '📊',
                    'presentations': '📽️',
                    'pdf': '📄'
                }
                
                breakdown_parts = []
                for file_type, count in file_types.items():
                    icon = type_icons.get(file_type, '📄')
                    breakdown_parts.append(f"{icon} {count} {file_type}")
                
                if breakdown_parts:
                    self.log_message(f"📋 File types: {' • '.join(breakdown_parts)}")
                    
                # Update the confirmation details with file count
                self.confirm_details.config(text=f"Ready to convert {len(files)} files from: {Path(directory).name}")
            else:
                self.log_message("⚠️ No convertible files found in directory")
                self.confirm_details.config(text=f"⚠️ No convertible files found in: {Path(directory).name}")
                
        except Exception as e:
            self.log_message(f"❌ Error scanning directory: {str(e)}")
    
    def log_message(self, message):
        """Add message to results"""
        try:
            self.results_text.config(state=tk.NORMAL)
            timestamp = datetime.now().strftime('%H:%M:%S')
            self.results_text.insert(tk.END, f"[{timestamp}] {message}\n")
            self.results_text.see(tk.END)
            self.results_text.config(state=tk.DISABLED)
        except Exception as e:
            print(f"❌ Error logging message: {e}")
    
    def on_combine_toggle(self):
        """Handle combine option toggle"""
        if self.combine_files.get():
            # Disable structure options when combining
            for widget in self.root.winfo_children():
                self._disable_radiobuttons(widget)
        else:
            # Re-enable structure options
            for widget in self.root.winfo_children():
                self._enable_radiobuttons(widget)
    
    def _disable_radiobuttons(self, widget):
        """Recursively disable radiobuttons"""
        if isinstance(widget, tk.Radiobutton):
            widget.config(state='disabled')
        for child in widget.winfo_children():
            self._disable_radiobuttons(child)
    
    def _enable_radiobuttons(self, widget):
        """Recursively enable radiobuttons"""
        if isinstance(widget, tk.Radiobutton):
            widget.config(state='normal')
        for child in widget.winfo_children():
            self._enable_radiobuttons(child)
    
    def start_conversion(self):
        """Start conversion"""
        directory = self.selected_directory.strip() if self.selected_directory else ""
        
        if not directory:
            messagebox.showerror("Error", "Please select a directory first by clicking 'SELECT FOLDER TO CONVERT'")
            return
        
        if not os.path.exists(directory):
            messagebox.showerror("Error", "Directory does not exist")
            return
        
        # Clear results
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.config(state=tk.DISABLED)
        
        # Update button
        self.convert_button.config(state='disabled', text="🔄 CONVERTING...", bg="orange")
        
        # Start conversion thread
        thread = threading.Thread(target=self.convert_files, args=(directory,))
        thread.daemon = True
        thread.start()
    
    def convert_files(self, directory):
        """Convert files"""
        try:
            directory_path = Path(directory)
            pdf_output_dir = directory_path / "pdf"
            pdf_output_dir.mkdir(exist_ok=True)
            
            self.log_message(f"Starting conversion...")
            self.log_message(f"Output directory: {pdf_output_dir}")
            
            # Get files
            all_files = []
            for root, dirs, files in os.walk(directory):
                for file in files:
                    file_path = Path(root) / file
                    if self.converter.get_file_type(file_path):
                        all_files.append(file_path)
            
            if not all_files:
                self.log_message("No files to convert")
                self.convert_button.config(state='normal', text="🔄 CONVERT TO PDF", bg="green")
                return
            
            # Handle combine mode
            if self.combine_files.get():
                self.log_message(f"Combining {len(all_files)} files into single PDF...")
                
                output_filename = f"{directory_path.name}_combined.pdf"
                combined_output_path = pdf_output_dir / output_filename
                
                # Import the combine function
                from pdf_converter_cli import combine_files_to_single_pdf
                
                if combine_files_to_single_pdf(all_files, combined_output_path, directory_path):
                    self.log_message("✅ Combined PDF created successfully!")
                    self.log_message(f"📁 Combined PDF saved to: {combined_output_path}")
                    self.conversion_progress.set("Complete: Combined PDF created")
                    messagebox.showinfo("Conversion Complete", 
                                      f"Combined PDF created successfully!\n\n"
                                      f"📄 Combined {len(all_files)} files into single PDF\n"
                                      f"📁 Saved to: {combined_output_path}")
                else:
                    self.log_message("❌ Failed to create combined PDF")
                    messagebox.showerror("Conversion Error", "Failed to create combined PDF")
                
                self.convert_button.config(state='normal', text="🔄 CONVERT TO PDF", bg="green")
                return
            
            self.log_message(f"Converting {len(all_files)} files...")
            
            # Setup progress
            self.progress_bar.config(maximum=len(all_files))
            
            success_count = 0
            fail_count = 0
            
            for i, file_path in enumerate(all_files):
                try:
                    relative_path = file_path.relative_to(directory_path)
                    pdf_filename = relative_path.stem + ".pdf"
                    
                    if self.maintain_structure.get():
                        output_subdir = pdf_output_dir / relative_path.parent
                        output_subdir.mkdir(parents=True, exist_ok=True)
                        output_path = output_subdir / pdf_filename
                    else:
                        base_name = relative_path.stem
                        if relative_path.parent != Path('.'):
                            parent_name = str(relative_path.parent).replace('/', '_').replace('\\', '_')
                            base_name = f"{parent_name}_{base_name}"
                        output_path = pdf_output_dir / f"{base_name}.pdf"
                    
                    self.conversion_progress.set(f"Converting: {file_path.name}")
                    
                    if self.converter.convert_file(str(file_path), str(output_path)):
                        success_count += 1
                        self.log_message(f"✓ {relative_path}")
                    else:
                        fail_count += 1
                        self.log_message(f"✗ {relative_path}")
                    
                    self.progress_bar.config(value=i + 1)
                    self.root.update_idletasks()
                    
                except Exception as e:
                    fail_count += 1
                    self.log_message(f"✗ Error: {file_path.name}")
            
            # Final summary
            self.log_message("")
            self.log_message("=== CONVERSION COMPLETE ===")
            self.log_message(f"✅ Successfully converted: {success_count}")
            self.log_message(f"❌ Failed to convert: {fail_count}")
            self.log_message(f"📁 Output location: {pdf_output_dir}")
            
            self.conversion_progress.set(f"Complete: {success_count} converted, {fail_count} failed")
            
            messagebox.showinfo("Conversion Complete", 
                              f"PDF conversion finished!\n\n"
                              f"✅ Successfully converted: {success_count} files\n"
                              f"❌ Failed to convert: {fail_count} files\n\n"
                              f"📁 All PDFs saved to:\n{pdf_output_dir}")
            
        except Exception as e:
            self.log_message(f"❌ Conversion error: {str(e)}")
            messagebox.showerror("Conversion Error", f"Conversion failed:\n{str(e)}")
        
        finally:
            self.convert_button.config(state='normal', text="🔄 CONVERT TO PDF", bg="green")
    
    def run(self):
        """Run the app"""
        self.root.mainloop()


def main():
    print("Starting PDF Converter Pro (Prominent Display Version)...")
    
    try:
        app = ProminentPDFConverterGUI()
        print("GUI created successfully!")
        app.run()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 