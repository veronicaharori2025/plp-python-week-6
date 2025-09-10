import requests
import os
import hashlib
from urllib.parse import urlparse
from pathlib import Path
import mimetypes
from typing import List, Optional


def validate_image_image_content_type(headers: dict) -> bool:
    """Validate if the content type in headers is an image."""
    content_type = headers.get('Content-Type', '').lower()
    valid_types = {'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/bmp'}
    return content_type in valid_types

def check_content_length(headers: dict, max_size: int = 10 * 1024 * 1024) -> bool:
    """Check if the content length is within the allowed limit. (Default is 10MB)"""
    content_length = headers.get('Content-Length')
    if content_length:
        try: 
            return int(content_length) <= max_size
        except ValueError:
            return False
    return True  # If no content length, proceed cautiously

def calculate_file_hash(file_path: str) -> str:
    """Calculate SHA256 hash of the file."""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)
    return sha256.hexdigest()

def is_duplicate_image(file_path: str, existing_hashes: set) -> bool:
    """Check if the image is a duplicate based on its hash."""
    file_hash = calculate_file_hash(file_path)
    return file_hash in existing_hashes

def fetch_and_save_image(url: str, output_dir: str, existing_hashes: set) -> Optional[str]:
    """Fetch an image from a URL and save it, with security and deduplication checks."""
    try:
        # Fetch image with timeout and user-agent for respectful access
        headers = {'User-Agent': 'UbuntuImageFetcher/1.0'}
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status() # Raise exception for HTTP errors
         
        # Validate HTTP headers
        if not validate_image_image_content_type(response.headers):
            return f'x Invalid content type for {url}: {response.headers.get("Content-Type")}'
        if not check_content_length(response.headers):
            return f'x File too large for {url}: {response.headers.get("Content-Length")} bytes'
        
        # Extract filename
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename or not mimetypes.guess_extension(response.headers.get('Content-Type', '')):
            ext = mimetypes.guess_extension(response.headers.get('Content-Type', ''))
            filename = f'downloaded_image_{hashlib.md5(url.encode()).hexdigest()[:8]}{ext}'
            
        # Ensure filename is safe (remove invalid characters)
        filename = "".join(c for c in filename if c.isalnum() or c in (".", "_", "-"))
        filepath = os.path.join(output_dir, filename)

        # Save image temporarily to check for duplicates
        temp_filepath = filepath + ".tmp"
        with open(temp_filepath, "wb") as f:
            f.write(response.content)

        # Check for duplicates
        file_hash = calculate_file_hash(temp_filepath)
        if file_hash in existing_hashes:
            os.remove(temp_filepath)  # Remove temp file
            return f"✗ Skipped {url}: Duplicate image detected"
        
        # Move temp file to final location and update hashes
        os.rename(temp_filepath, filepath)
        existing_hashes.add(file_hash)
        return f"✓ Successfully fetched: {filename}\n✓ Image saved to {filepath}"
    
    except requests.exceptions.HTTPError as e:
        return f"✗ HTTP error for {url}: {e}"
    except requests.exceptions.ConnectionError:
        return f"✗ Connection error for {url}: Unable to connect"
    except requests.exceptions.Timeout:
        return f"✗ Timeout error for {url}: Request timed out"
    except requests.exceptions.RequestException as e:
        return f"✗ Network error for {url}: {e}"
    except Exception as e:
        return f"✗ Unexpected error for {url}: {e}"
    
def main():
    """Main function to fetch images from multiple URLs with Ubuntu principles."""
    print("Welcome to the Ubuntu Image Fetcher")
    print("A tool for mindfully collecting images from the web\n")

    # Create output directory
    output_dir = "Fetched_Images"
    os.makedirs(output_dir, exist_ok=True)

    # Load existing image hashes for deduplication
    existing_hashes = set()
    for file in Path(output_dir).glob("*"):
        if file.is_file() and file.suffix in {".jpg", ".png", ".gif", ".bmp", ".webp"}:
            existing_hashes.add(calculate_file_hash(str(file)))

    # Get URLs from user (comma-separated or single)
    urls_input = input("Please enter image URL(s) (comma-separated for multiple): ")
    urls = [url.strip() for url in urls_input.split(",") if url.strip()]

    if not urls:
        print("✗ No valid URLs provided.")
        return

    # Process each URL
    for url in urls:
        print(f"\nProcessing {url}...")
        result = fetch_and_save_image(url, output_dir, existing_hashes)
        print(result)

    print("\nConnection strengthened. Community enriched.")

if __name__ == "__main__":
    main()