# Ubuntu Image Fetcher

A Python script designed to download images from the web with a focus on community, respect, sharing, and practicality—core principles of the Ubuntu philosophy, "I am because we are."

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Examples](#examples)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Ubuntu Image Fetcher connects to the global internet community by fetching shared image resources, respects servers through proper error handling and timeouts, organizes images for easy sharing, and serves practical needs such as:

- **Content Curation**: Creating image galleries for websites or social media  
- **Data Engineering**: Collecting clean, validated image datasets for computer vision models

This standalone script (`fetch_images.py`) fetches images from one or more URLs, validates their content type and size, and prevents duplicates using SHA-256 hashing.

### Ubuntu Principles

- **Community**: Connects users to web content creators by fetching shared images
- **Respect**: Uses custom User-Agent and timeouts to avoid overloading servers
- **Sharing**: Saves images in an organized directory for easy access and redistribution  
- **Practicality**: Provides a simple, reliable tool for downloading images with security and deduplication

## Features

### Core Functionality
- **Multi-URL Support**: Accepts one or more URLs via comma-separated input
- **Automatic Directory Creation**: Creates the `Fetched_Images` directory if it doesn't exist
- **Smart Filename Handling**: Extracts filenames from URLs or generates unique ones
- **Binary Mode Saving**: Saves images in binary mode to prevent corruption

### Security and Validation
- **Content-Type Validation**: Ensures responses are images (JPEG, PNG, GIF, BMP, WebP)
- **Size Limiting**: Rejects files larger than 10MB to avoid resource exhaustion
- **Safe Filenames**: Sanitizes filenames to remove invalid characters
- **Temporary File Handling**: Downloads to `.tmp` files for validation before final save
- **Respectful Requests**: Includes User-Agent and 10-second timeouts

### Deduplication and Efficiency
- **Hash-Based Deduplication**: Uses SHA-256 hashes to skip duplicate images
- **Session Persistence**: Loads hashes of existing images at startup
- **Memory Efficient**: O(1) lookup via in-memory set

### Error Handling
- **Granular Exceptions**: Distinguishes between HTTP errors, connection issues, and timeouts
- **Graceful Degradation**: Continues processing remaining URLs if one fails
- **User-Friendly Output**: Uses ✓ for successes and ✗ for errors

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Quick Install

1. **Download the Script**
   ```bash
   # Option 1: Clone repository (if hosted)
   git clone https://github.com/veronicaharori2025/plp-python-week-6.git
   cd ubuntu-image-fetcher
   
   # Option 2: Download fetch_images.py directly
   ```

2. **Install Dependencies**
   ```bash
   pip install requests
   ```

3. **Run the Script**
   ```bash
   python fetch_images.py
   ```

### Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install requests
python fetch_images.py
```

### Troubleshooting

- **Module Not Found**: Ensure requests is installed (`pip install requests`)
- **Permission Errors**: Use `pip install --user requests` or activate a virtual environment
- **Network Issues**: Check connectivity or set `HTTP_PROXY`/`HTTPS_PROXY` environment variables
- **Python Version**: Verify Python is 3.8+ (`python --version`)

## Usage

### Basic Usage

Run the script and provide URLs when prompted:

```bash
python fetch_images.py
```

Enter one or more URLs, comma-separated. Images are saved to `./Fetched_Images/`.

### Input Guidelines

- **URLs**: Must be valid HTTP/HTTPS URLs pointing to images
- **Formats**: JPEG, PNG, GIF, BMP, WebP (enforced via Content-Type)
- **Input Format**: Comma-separated URLs
- **Invalid URLs**: Handled gracefully with clear error messages

### Performance Notes

- **Sequential Processing**: Suitable for small batches (<100 URLs)
- **Hash Computation**: Efficient for <10,000 files due to in-memory set
- **Network**: 10-second timeout per request ensures reliability

## Project Structure

```
ubuntu-image-fetcher/
├── fetch_images.py  # Main script with all logic
└── Fetched_Images/          # Output directory (created at runtime)
```

### Code Breakdown

**Main Functions:**
- `validate_image_content_type()`: Checks Content-Type against image MIME types
- `check_content_length()`: Ensures file size is ≤10MB  
- `calculate_file_hash()`: Computes SHA-256 hash in 4KB chunks
- `is_duplicate_image()`: Checks hash against existing set
- `fetch_and_save_image()`: Core fetching, validation, and saving logic
- `main()`: Handles user input and orchestrates the process

## Examples

### Successful Download
```
$ python fetch_images.py
Welcome to the Ubuntu Image Fetcher
A tool for mindfully collecting images from the web

Please enter image URL(s) (comma-separated for multiple): https://httpbin.org/image/jpeg

Processing https://httpbin.org/image/jpeg...
✓ Successfully fetched: image.jpeg
✓ Image saved to Fetched_Images/image.jpeg

Connection strengthened. Community enriched.
```

### Multiple URLs
```
Please enter image URL(s): https://httpbin.org/image/jpeg,https://httpbin.org/image/png

Processing https://httpbin.org/image/jpeg...
✓ Successfully fetched: image.jpeg
✓ Image saved to Fetched_Images/image.jpeg

Processing https://httpbin.org/image/png...
✓ Successfully fetched: image.png  
✓ Image saved to Fetched_Images/image.png

Connection strengthened. Community enriched.
```

### Duplicate Detection
```
Processing https://httpbin.org/image/jpeg...
✗ Skipped https://httpbin.org/image/jpeg: Duplicate image detected
```

### Error Handling
```
Processing https://invalid-url.com/image.jpg...
✗ HTTP error for https://invalid-url.com/image.jpg: 404 Client Error: Not Found
```

## Future Enhancements

### Scalability
- **Asynchronous Fetching**: Use `aiohttp` with `asyncio` for concurrent downloads
- **Database for Hashes**: Store hashes in SQLite or Redis for persistence across sessions

### Security Enhancements  
- **Image Integrity**: Use PIL (Pillow) to verify image files
- **Rate Limiting**: Add rate limiting to respect server policies

### Extensibility
- **Custom Output Directory**: Add command-line argument for output path
- **Additional File Types**: Extend support for PDFs or other formats
- **CLI Tool**: Refactor into a package with `argparse`
- **Interactive Loop**: Allow users to add more URLs after each batch

### Monitoring
- **Logging**: Add logging to write to `fetch.log`
- **Metrics**: Track success/failure rates with Prometheus

## Contributing

Contributions are welcome, embodying Ubuntu's community spirit:

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -m 'Add feature'`
4. Push: `git push origin feature/new-feature`
5. Open a Pull Request

## License

This project embodies the Ubuntu philosophy of community and sharing. Please specify your preferred license.

---

*Ubuntu Image Fetcher - Connecting communities through mindful image collection*