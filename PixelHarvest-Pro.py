import customtkinter as ctk
from tkinter import messagebox
import requests
from urllib.parse import quote
from PIL import Image, ImageTk
import os
import io
import threading
import time
import webbrowser
from datetime import datetime
import re
import subprocess
import sys

class PixelHarvestPro(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("PixelHarvest Pro - Media Downloader")
        self.geometry("1200x800")
        self.minsize(1100, 750)
        
        # Configure theme
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Initialize variables
        self.media_items = []
        self.keyword = ""
        self.api_key = ""
        self.downloading = False
        self.media_type = "images"
        self.selected_items = []
        self.creator_name = "Bilal Rachdi"  # Define creator_name here
        self.github_url = "https://github.com/xdrshdy"
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Create main grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Header frame
        header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="#2c3e50")
        header_frame.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Logo and title
        logo_label = ctk.CTkLabel(
            header_frame, 
            text="🎬", 
            font=("Arial", 32),
            width=50,
            text_color="#3498db"
        )
        logo_label.grid(row=0, column=0, padx=(20, 10), pady=10)
        
        title_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_frame.grid(row=0, column=1, sticky="w")
        
        title_label = ctk.CTkLabel(
            title_frame, 
            text="PixelHarvest Pro",
            font=("Arial", 28, "bold"),
            text_color="#ecf0f1"
        )
        title_label.grid(row=0, column=0, padx=(0, 5), sticky="w")
        
        subtitle_label = ctk.CTkLabel(
            title_frame, 
            text="Image & Video Downloader",
            font=("Arial", 16),
            text_color="#bdc3c7"
        )
        subtitle_label.grid(row=1, column=0, sticky="w")
        
        # Control frame
        control_frame = ctk.CTkFrame(self, corner_radius=10)
        control_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))
        control_frame.grid_columnconfigure(0, weight=1)
        control_frame.grid_rowconfigure(5, weight=1)
        
        # Search section
        search_label = ctk.CTkLabel(
            control_frame, 
            text="Media Search",
            font=("Arial", 18, "bold"),
            anchor="w"
        )
        search_label.grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")
        
        # Keyword entry
        keyword_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        keyword_frame.grid(row=1, column=0, padx=20, pady=5, sticky="ew")
        keyword_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            keyword_frame, 
            text="Keyword:",
            font=("Arial", 14),
            width=100
        ).grid(row=0, column=0, padx=(0, 10), sticky="w")
        
        self.search_entry = ctk.CTkEntry(
            keyword_frame, 
            placeholder_text="Enter search term (e.g. 'mountains' or 'ocean waves')",
            font=("Arial", 14),
            height=40
        )
        self.search_entry.grid(row=0, column=1, sticky="ew")
        self.search_entry.bind("<Return>", lambda e: self.start_search())
        
        # Settings frame
        settings_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        settings_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        settings_frame.grid_columnconfigure(0, weight=1)
        settings_frame.grid_columnconfigure(1, weight=1)
        settings_frame.grid_columnconfigure(2, weight=1)
        
        # Media type selection
        ctk.CTkLabel(
            settings_frame, 
            text="Media Type:",
            font=("Arial", 14)
        ).grid(row=0, column=0, padx=(0, 10), sticky="w")
        
        self.media_type_var = ctk.StringVar(value="images")
        self.media_type_menu = ctk.CTkOptionMenu(
            settings_frame, 
            values=["images", "videos"],
            font=("Arial", 14),
            width=100,
            variable=self.media_type_var,
            command=self.media_type_changed
        )
        self.media_type_menu.grid(row=0, column=1, padx=(0, 20), sticky="w")
        
        # Item count
        ctk.CTkLabel(
            settings_frame, 
            text="Number of Items:",
            font=("Arial", 14)
        ).grid(row=0, column=2, padx=(0, 10), sticky="w")
        
        self.item_count = ctk.CTkOptionMenu(
            settings_frame, 
            values=[str(i) for i in range(1, 21)],
            font=("Arial", 14),
            width=100
        )
        self.item_count.set("5")
        self.item_count.grid(row=0, column=3, padx=(0, 20), sticky="w")
        
        # Quality selection
        ctk.CTkLabel(
            settings_frame, 
            text="Quality:",
            font=("Arial", 14)
        ).grid(row=0, column=4, padx=(0, 10), sticky="w")
        
        self.quality_var = ctk.StringVar(value="original")
        self.quality_menu = ctk.CTkOptionMenu(
            settings_frame, 
            values=["original", "large", "medium", "small"],
            font=("Arial", 14),
            width=120,
            variable=self.quality_var
        )
        self.quality_menu.grid(row=0, column=5, sticky="w")
        
        # API key frame
        api_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        api_frame.grid(row=3, column=0, padx=20, pady=5, sticky="ew")
        api_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            api_frame, 
            text="API Key:",
            font=("Arial", 14),
            width=100
        ).grid(row=0, column=0, padx=(0, 10), sticky="w")
        
        self.api_entry = ctk.CTkEntry(
            api_frame, 
            placeholder_text="Enter your Pexels API key",
            font=("Arial", 14),
            show="*",
            height=40
        )
        self.api_entry.grid(row=0, column=1, sticky="ew")
        
        # API key help
        api_help = ctk.CTkButton(
            api_frame,
            text="?",
            width=30,
            height=30,
            font=("Arial", 14, "bold"),
            fg_color="transparent",
            hover_color="#2c3e50",
            command=self.show_api_help
        )
        api_help.grid(row=0, column=2, padx=(10, 0))
        
        # Search button
        self.search_btn = ctk.CTkButton(
            control_frame,
            text="Search Media",
            font=("Arial", 16, "bold"),
            height=45,
            command=self.start_search,
            fg_color="#3498db",
            hover_color="#2980b9"
        )
        self.search_btn.grid(row=4, column=0, padx=20, pady=20, sticky="ew")
        
        # Preview section
        preview_frame = ctk.CTkFrame(self, corner_radius=10)
        preview_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=(0, 20))
        preview_frame.grid_columnconfigure(0, weight=1)
        preview_frame.grid_rowconfigure(1, weight=1)
        
        # Preview header
        preview_header = ctk.CTkFrame(preview_frame, fg_color="transparent")
        preview_header.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        preview_header.grid_columnconfigure(1, weight=1)
        
        preview_label = ctk.CTkLabel(
            preview_header, 
            text="Media Previews",
            font=("Arial", 18, "bold"),
            anchor="w"
        )
        preview_label.grid(row=0, column=0, sticky="w")
        
        # Selection controls
        selection_frame = ctk.CTkFrame(preview_header, fg_color="transparent")
        selection_frame.grid(row=0, column=1, sticky="e")
        
        ctk.CTkLabel(
            selection_frame, 
            text="Selection:",
            font=("Arial", 12)
        ).pack(side="left", padx=(0, 10))
        
        self.select_all_btn = ctk.CTkButton(
            selection_frame,
            text="Select All",
            font=("Arial", 12),
            width=80,
            height=25,
            command=self.select_all_items
        )
        self.select_all_btn.pack(side="left", padx=(0, 5))
        
        self.deselect_all_btn = ctk.CTkButton(
            selection_frame,
            text="Deselect All",
            font=("Arial", 12),
            width=80,
            height=25,
            command=self.deselect_all_items
        )
        self.deselect_all_btn.pack(side="left", padx=(0, 5))
        
        # Preview container with scrollbar
        self.preview_container = ctk.CTkScrollableFrame(
            preview_frame, 
            fg_color="transparent"
        )
        self.preview_container.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")
        self.preview_container.grid_columnconfigure(0, weight=1)
        
        # Status bar
        self.status_var = ctk.StringVar(value="Ready to search for media...")
        status_bar = ctk.CTkLabel(
            self, 
            textvariable=self.status_var,
            font=("Arial", 12),
            anchor="w",
            height=30,
            corner_radius=0,
            fg_color="#2c3e50"
        )
        status_bar.grid(row=3, column=0, sticky="ew", padx=0, pady=0)
        
        # Footer with copyright
        self.create_footer()
        
    def create_footer(self):
        # Footer frame
        footer_frame = ctk.CTkFrame(self, fg_color="transparent", height=60)
        footer_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=(0, 10))
        footer_frame.grid_columnconfigure(0, weight=1)
        
        # Copyright and links
        copyright_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        copyright_frame.pack(fill="x", pady=5)
        
        # Copyright text - FIXED: Use the instance variable
        copyright_text = f"© {datetime.now().year} PixelHarvest Pro - Created by {self.creator_name}"
        ctk.CTkLabel(
            copyright_frame,
            text=copyright_text,
            font=("Arial", 11),
            text_color="#7f8c8d"
        ).pack(side="left", padx=20)
        
        # GitHub button
        github_btn = ctk.CTkButton(
            copyright_frame,
            text="GitHub",
            font=("Arial", 11, "bold"),
            width=70,
            height=25,
            fg_color="#333333",
            hover_color="#444444",
            command=lambda: webbrowser.open(self.github_url)
        )
        github_btn.pack(side="left", padx=5)
        
        # Powered by Pexels
        pexels_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        pexels_frame.pack(fill="x", pady=5)
        
        self.pexels_label = ctk.CTkLabel(
            pexels_frame,
            text="Powered by Pexels API",
            font=("Arial", 11),
            text_color="#7f8c8d",
            cursor="hand2"
        )
        self.pexels_label.pack(side="right", padx=20)
        self.pexels_label.bind("<Button-1>", self.open_pexels_website)
        
    def media_type_changed(self, choice):
        self.media_type = choice
        self.clear_preview()
        
    def select_all_items(self):
        for item in self.media_items:
            if 'selected' in item and 'checkbox' in item:
                item['selected'] = True
                item['checkbox'].select()
        
    def deselect_all_items(self):
        for item in self.media_items:
            if 'selected' in item and 'checkbox' in item:
                item['selected'] = False
                item['checkbox'].deselect()
        
    def open_pexels_website(self, event):
        webbrowser.open("https://pexels.com/api")
        
    def show_api_help(self):
        help_text = """
        To use PixelHarvest Pro, you need a Pexels API key:
        
        1. Go to https://www.pexels.com/api/
        2. Create a free account
        3. Get your API key from the dashboard
        
        The free API key allows:
        - 200 requests per hour
        - 200,000 requests per month
        - Access to over 3 million free photos and videos
        
        Note: The API key is required for media downloads.
        """
        messagebox.showinfo("API Key Help", help_text.strip())
        
    def start_search(self):
        # Get values from UI
        self.keyword = self.search_entry.get().strip()
        try:
            count = int(self.item_count.get())
        except ValueError:
            count = 5  # Default value if conversion fails
        quality = self.quality_var.get()
        self.api_key = self.api_entry.get().strip()
        self.media_type = self.media_type_var.get()
        
        # Validate inputs
        if not self.keyword:
            messagebox.showerror("Input Error", "Please enter a search keyword")
            return
            
        if not self.api_key:
            messagebox.showerror("API Key Missing", "Please enter your Pexels API key")
            return
            
        # Disable search button during search
        self.search_btn.configure(state="disabled", text="Searching...")
        self.status_var.set(f"Searching for '{self.keyword}' {self.media_type}...")
        
        # Start search in a new thread
        threading.Thread(
            target=self.search_media, 
            args=(count, quality),
            daemon=True
        ).start()
    
    def search_media(self, count, quality):
        try:
            # Clear previous results
            self.media_items = []
            self.selected_items = []
            
            # API request based on media type
            headers = {"Authorization": self.api_key}
            
            if self.media_type == "images":
                search_url = f"https://api.pexels.com/v1/search?query={quote(self.keyword)}&per_page={min(count, 30)}"
                endpoint = "photos"
            else:  # videos
                search_url = f"https://api.pexels.com/videos/search?query={quote(self.keyword)}&per_page={min(count, 30)}"
                endpoint = "videos"
            
            response = requests.get(search_url, headers=headers)
            
            if response.status_code == 401:
                self.after(0, lambda: messagebox.showerror(
                    "API Error", 
                    "Invalid API key. Please check your Pexels API key."
                ))
                return
                
            response.raise_for_status()
            data = response.json()
            
            if endpoint not in data or not data[endpoint]:
                self.after(0, lambda: messagebox.showinfo(
                    "No Results", 
                    f"No {self.media_type} found for '{self.keyword}'"
                ))
                return
            
            # Clear preview area
            self.after(0, self.clear_preview)
            
            # Process results
            media_list = data[endpoint]
            self.after(0, lambda: self.status_var.set(
                f"Found {len(media_list)} {self.media_type}. Loading previews..."
            ))
            
            # Create media items
            for i, item in enumerate(media_list):
                # Create a dictionary to store media info
                media_item = {
                    'id': i,
                    'type': self.media_type,
                    'data': item,
                    'selected': True,  # Selected by default
                    'checkbox': None,
                    'preview_img': None
                }
                self.media_items.append(media_item)
                
                # Get thumbnail URL
                if self.media_type == "images":
                    thumb_url = item['src']['medium']
                else:  # videos
                    thumb_url = item['image']
                
                # Add to preview in UI thread
                self.after(0, lambda idx=i, url=thumb_url, total=len(media_list): 
                    self.create_preview(idx, url, total)
                )
                # Add small delay to prevent UI freezing
                time.sleep(0.1)
            
            self.after(0, lambda: self.status_var.set(
                f"Found {len(self.media_items)} {self.media_type}. Ready to download."
            ))
            
            # Add download buttons
            self.after(0, self.add_download_buttons)
            
        except requests.exceptions.RequestException as e:
            self.after(0, lambda: messagebox.showerror(
                "API Error", 
                f"Failed to fetch media: {str(e)}"
            ))
        except Exception as e:
            self.after(0, lambda: messagebox.showerror(
                "Error", 
                f"An unexpected error occurred: {str(e)}"
            ))
        finally:
            self.after(0, lambda: self.search_btn.configure(
                state="normal", 
                text="Search Media"
            ))
    
    def clear_preview(self):
        for widget in self.preview_container.winfo_children():
            widget.destroy()
    
    def create_preview(self, index, url, total):
        try:
            # Create frame for each preview
            frame = ctk.CTkFrame(self.preview_container, corner_radius=8)
            frame.pack(fill="x", pady=5, padx=5)
            frame.grid_columnconfigure(1, weight=1)
            
            # Add checkbox for selection
            chk_var = ctk.BooleanVar(value=True)
            checkbox = ctk.CTkCheckBox(
                frame, 
                text="", 
                variable=chk_var,
                width=20,
                command=lambda idx=index: self.toggle_selection(idx)
            )
            checkbox.grid(row=0, column=0, rowspan=2, padx=(10, 5), pady=10, sticky="n")
            
            # Store checkbox in media item
            if index < len(self.media_items):
                self.media_items[index]['checkbox'] = checkbox
            
            # Download thumbnail
            img_data = requests.get(url).content
            img = Image.open(io.BytesIO(img_data))
            
            # Create thumbnail
            img.thumbnail((180, 180))
            photo_img = ImageTk.PhotoImage(img)
            
            # Create image label
            img_label = ctk.CTkLabel(frame, text="", image=photo_img)
            img_label.image = photo_img  # Keep reference
            
            # Store image reference in media item
            if index < len(self.media_items):
                self.media_items[index]['preview_img'] = photo_img  # Prevent garbage collection
                
            img_label.grid(row=0, column=1, rowspan=2, padx=10, pady=10)
            
            # Create info label
            if index < len(self.media_items):
                if self.media_type == "images":
                    info_text = f"Image {index+1} of {total}\nSize: {self.media_items[index]['data']['width']}x{self.media_items[index]['data']['height']}"
                    media_type = "🖼️ Image"
                else:
                    duration = self.format_duration(self.media_items[index]['data']['duration'])
                    info_text = f"Video {index+1} of {total}\nDuration: {duration}"
                    media_type = "🎬 Video"
                    
                info_label = ctk.CTkLabel(
                    frame, 
                    text=info_text, 
                    font=("Arial", 14),
                    anchor="w",
                    justify="left"
                )
                info_label.grid(row=0, column=2, sticky="w", padx=(0, 10), pady=(10, 0))
                
                # Photographer info
                photographer = self.media_items[index]['data']['user']['name']
                photographer_label = ctk.CTkLabel(
                    frame, 
                    text=f"Photographer: {photographer} | {media_type}",
                    font=("Arial", 12),
                    text_color="#3498db",
                    anchor="w"
                )
                photographer_label.grid(row=1, column=2, sticky="w", padx=(0, 10), pady=(0, 10))
            
            # Update status
            self.status_var.set(f"Loaded preview {index+1} of {total}")
            
        except Exception as e:
            print(f"Error creating preview: {e}")
    
    def format_duration(self, seconds):
        """Convert seconds to MM:SS format"""
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def toggle_selection(self, index):
        if index < len(self.media_items):
            self.media_items[index]['selected'] = not self.media_items[index]['selected']
        
    def add_download_buttons(self):
        # Create download buttons frame
        button_frame = ctk.CTkFrame(self.preview_container, fg_color="transparent")
        button_frame.pack(fill="x", pady=10, padx=10)
        
        # Download selected button
        self.download_selected_btn = ctk.CTkButton(
            button_frame, 
            text="Download Selected",
            font=("Arial", 16, "bold"),
            height=45,
            command=self.download_selected,
            fg_color="#27ae60",
            hover_color="#219653"
        )
        self.download_selected_btn.pack(side="left", padx=(0, 10), pady=5, fill="x", expand=True)
        
        # Download all button
        self.download_all_btn = ctk.CTkButton(
            button_frame, 
            text="Download All",
            font=("Arial", 16, "bold"),
            height=45,
            command=self.download_all,
            fg_color="#9b59b6",
            hover_color="#8e44ad"
        )
        self.download_all_btn.pack(side="right", pady=5, fill="x", expand=True)
    
    def download_selected(self):
        self.download_items(selected_only=True)
    
    def download_all(self):
        self.download_items(selected_only=False)
    
    def download_items(self, selected_only=False):
        if self.downloading:
            return
            
        self.downloading = True
        
        # Get items to download
        items_to_download = []
        for item in self.media_items:
            if 'selected' in item and (not selected_only or item['selected']):
                items_to_download.append(item)
        
        if not items_to_download:
            messagebox.showinfo("No Selection", "No items selected for download")
            self.downloading = False
            return
            
        # Disable buttons during download
        self.download_selected_btn.configure(state="disabled", text="Downloading...")
        self.download_all_btn.configure(state="disabled")
        self.status_var.set(f"Preparing to download {len(items_to_download)} items...")
        
        # Start download in a new thread
        threading.Thread(
            target=self.perform_download, 
            args=(items_to_download,),
            daemon=True
        ).start()
    
    def perform_download(self, items_to_download):
        try:
            # Create folder with keyword name
            folder_name = re.sub(r'[^\w\s-]', '', self.keyword).strip()[:20]
            save_path = os.path.join(os.path.expanduser("~"), "Downloads", "PixelHarvest", folder_name)
            os.makedirs(save_path, exist_ok=True)
            
            # Create subfolders for images and videos
            images_path = os.path.join(save_path, "Images")
            videos_path = os.path.join(save_path, "Videos")
            os.makedirs(images_path, exist_ok=True)
            os.makedirs(videos_path, exist_ok=True)
            
            # Download each item
            for i, item in enumerate(items_to_download):
                # Update status
                self.after(0, lambda i=i: self.status_var.set(
                    f"Downloading item {i+1} of {len(items_to_download)}..."
                ))
                
                if item['type'] == "images":
                    # Download image
                    quality = self.quality_var.get()
                    img_url = item['data']['src'].get(quality, "")
                    if not img_url:
                        # Fallback to next best quality
                        for q in ['original', 'large', 'medium', 'small']:
                            if item['data']['src'].get(q):
                                img_url = item['data']['src'][q]
                                break
                    
                    if img_url:
                        img_data = requests.get(img_url).content
                        img_path = os.path.join(images_path, f"{folder_name}_{i+1}.jpg")
                        
                        with open(img_path, 'wb') as f:
                            f.write(img_data)
                else:
                    # Download video
                    video_url = self.get_best_video_url(item['data'])
                    if video_url:
                        video_data = requests.get(video_url, stream=True)
                        video_path = os.path.join(videos_path, f"{folder_name}_{i+1}.mp4")
                        
                        with open(video_path, 'wb') as f:
                            for chunk in video_data.iter_content(chunk_size=1024*1024):  # 1MB chunks
                                if chunk:
                                    f.write(chunk)
                
                # Small delay to show progress
                time.sleep(0.1)
            
            # Show completion message
            self.after(0, lambda: messagebox.showinfo(
                "Download Complete", 
                f"✅ {len(items_to_download)} items saved to:\n{save_path}"
            ))
            
            self.after(0, lambda: self.status_var.set(
                f"Downloaded {len(items_to_download)} items to {save_path}"
            ))
            
            # Open download folder
            self.after(0, lambda: self.open_download_folder(save_path))
            
        except Exception as e:
            self.after(0, lambda: messagebox.showerror(
                "Download Error", 
                f"Failed to download items: {str(e)}"
            ))
        finally:
            self.downloading = False
            self.after(0, lambda: self.download_selected_btn.configure(
                state="normal", 
                text="Download Selected"
            ))
            self.after(0, lambda: self.download_all_btn.configure(
                state="normal", 
                text="Download All"
            ))
    
    def get_best_video_url(self, video_data):
        """Select the best quality video URL"""
        # Sort by quality (highest first)
        if 'video_files' in video_data:
            sorted_files = sorted(video_data['video_files'], 
                                 key=lambda x: x.get('width', 0) * x.get('height', 0), 
                                 reverse=True)
            
            # Get the highest quality video
            if sorted_files:
                best_video = sorted_files[0]
                return best_video.get('link', "")
        return ""
    
    def open_download_folder(self, path):
        """Open the download folder in the file explorer"""
        try:
            if os.path.exists(path):
                if os.name == 'nt':  # Windows
                    os.startfile(path)
                elif os.name == 'posix':  # macOS, Linux
                    if sys.platform == 'darwin':
                        subprocess.Popen(['open', path])
                    else:
                        subprocess.Popen(['xdg-open', path])
        except Exception as e:
            print(f"Error opening folder: {e}")

if __name__ == "__main__":
    app = PixelHarvestPro()
    app.mainloop()