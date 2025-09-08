Below is a concise, comprehensive summary of the README in ./youtube-dl/README.md.

Overview
- youtube-dl is a command-line tool (Python-based) to download videos from YouTube and many other sites. It is released into the public domain and supports Python 2.6, 2.7, and 3.2+.

Main functionality
- Download videos from a wide range of sites using a pluggable extractor framework.
- Handles multiple URLs, playlists, and streaming formats; can stream to stdout or write to disk.
- Automatically selects formats (with a sophisticated format selector) and can merge video+audio when needed (via ffmpeg/avconv).

Key components and concepts
- Extractors: Site-specific logic lives in extractor modules; a generic extractor handles unsupported sites. The README provides developer guidance for adding new extractors.
- Info dictionary: Extractors return an information dictionary (info dict) containing mandatory fields (id, title, url or formats) and numerous optional metadata fields.
- Utility helpers: Emphasizes safe data extraction and conversion via utility functions (e.g., int_or_none, url_or_none, traverse_obj, unified_strdate, parse_filesize, etc.) to promote robustness and future-proofing.

Output and formatting
- Output template syntax (-o, OUTPUT TEMPLATE):
  - Supported placeholders (examples): id, title, url, ext, uploader, upload_date, timestamp, width, height, duration, view_count, etc.
  - Supports nested directories, formatting (e.g., %()s, numeric formatting like % (view_count)05d), and escaping for Windows batch files.
  - Default template is %(title)s-%(id)s.%(ext)s; can output to stdout with -o -.
  - NA placeholder for missing metadata via --output-na-placeholder.
- Output examples illustrate organizing downloads into directories (e.g., by playlist, uploader, or chapter).

Format selection
- Core mechanism is --format (or -f FORMAT), a selector expression:
  - Specific format code (e.g., -f 22), or extension-based selection (e.g., -f webm) to pick best matching formats.
  - Special formats: best, worst, bestvideo, worstvideo, bestaudio, worseaudio, etc.
  - Combining and prioritizing: using slashes for priority (e.g., -f 22/17/18), comma for multiple selections (-f 22,17,18), or merging video+audio (-f 136/137/mp4/bestvideo,140/m4a/bestaudio).
  - Filters with conditions (e.g., -f "best[height=720]" or -f "[filesize>10M]").
  - Protocol filters (e.g., -f '(bestvideo+bestaudio/best)[protocol^=http]') and group expressions with parentheses.
  - Merging formats into a single file requires ffmpeg/avconv (bestvideo+bestaudio).
  - The default behavior (since 2015) is bestvideo+bestaudio/best when possible; otherwise best (single file).
- Examples demonstrate complex selection logic and considerations for Windows.

Configuration and persistence
- Configuration files:
  - Global: /etc/youtube-dl.conf
  - User: ~/.config/youtube-dl/config (and Windows equivalents)
  - Options can be placed in config files; no whitespace after - or -- in config (e.g., -o, --proxy).
  - --ignore-config to disable configuration files for a run.
  - --config-location to specify an alternate config file or directory.
- Authentication:
  - Support for .netrc to store credentials per extractor; instructions provided for secure setup.
- Download and post-processing options:
  - Download: --limit-rate, --retries, --fragment-retries, --continue, --no-part, --buffer-size, etc.
  - Post-processing: -x (extract audio via ffmpeg/avconv), --audio-format, --recode-video, --embed-subs, --embed-thumbnail, --add-metadata, etc.
  - External downloader support and related arguments.
- Filesystem and caching:
  - --output, --autonumber-start, --restrict-filenames, --no-overwrites, --rm-cache-dir, --cache-dir, etc.
- Thumbnails, verbosity, simulation, and debugging options:
  - --write-thumbnail, --list-thumbnails, --quiet, --verbose, --dump-json, --dump-pages, --write-pages, and traffic/logging controls.

Usage examples and workflows
- Embedding YoutubeDL in Python with custom logger and progress hooks.
- Streaming to a media player via stdout (-o -) and piping.
- Output template examples showing directory structure and naming conventions.

Developer instructions and standards
- How to run and test:
  - python -m youtube_dl, unittest, nosetests, or test/test_download.py.
- Adding a new extractor:
  - Example template for a new extractor in youtube_dl/extractor/yourextractor.py.
  - Steps to integrate into the codebase, add tests, and ensure compliance with coding conventions.
- Metafields and robustness:
  - Mandatory fields: id, title, and url or formats; optional fields should be accessed safely (get/try/with defaults).
  - Emphasis on fallbacks, tolerant extraction, and avoiding hard failures if non-critical fields change.
  - Use of helper parsing/conversion functions to normalize data (e.g., unified_timestamp, parse_filesize, etc.).
- Coding conventions and best practices:
  - Keep lines under 80 characters where reasonable.
  - Use non-capturing groups for regex where possible.
  - Favor flexible, resilient regex patterns and multiple data sources.

Bugs, support, and community
- Bug reporting guidance: include full verbose output (-v) and an example URL; follow issue templates.
- Site support rules and expectations for contributions; emphasis on legality of sites to be included.
- General tips for effective bug reports and feature requests, including reproducibility and context.

Other notes
- The README repeatedly references internal modules and files (e.g., youtube_dl/YoutubeDL.py, extractor/common.py) for implementation details, as guidance rather than code listing.
- The document covers broad usage, configuration, advanced features, and contributor guidelines, making it both a user manual and a developer handhold for extending youtube-dl.