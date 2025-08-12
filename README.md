# VideoClipper

A simple, efficient tool to split large video files into manageable segments. Perfect for handling massive videos that are too large for traditional video editing software.

## Features

- **Fast processing**: Uses ffmpeg's stream copy for minimal processing time
- **Flexible segmentation**: Split videos into any duration you specify
- **Dry-run mode**: Preview what will be created before processing
- **Progress tracking**: See real-time progress as segments are created
- **Open source**: Uses ffmpeg under the hood

## Prerequisites

### Install ffmpeg

**macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use Chocolatey:
```bash
choco install ffmpeg
```

## Usage

### Basic Usage

Split a video into 30-minute segments:
```bash
python video_clipper.py your_video.mp4 --duration 1800
```

Split a video into 1-hour segments:
```bash
python video_clipper.py your_video.mp4 --duration 3600
```

### Dry Run (Preview)

See what segments would be created without actually processing:
```bash
python video_clipper.py your_video.mp4 --duration 1800 --dry-run
```

### Common Duration Values

- **30 minutes**: `1800` seconds
- **1 hour**: `3600` seconds  
- **2 hours**: `7200` seconds
- **3 hours**: `10800` seconds

## Output

The program creates a new directory next to your input file named `{filename}_segments/` containing all the split video files:

```
your_video.mp4
your_video_segments/
├── your_video_segment_001.mp4
├── your_video_segment_002.mp4
├── your_video_segment_003.mp4
└── ...
```

## Example: 13-Hour Video

For your 13-hour video, you might want to split it into 2-hour segments:

```bash
python video_clipper.py your_13hour_video.mp4 --duration 7200
```

This will create approximately 7 segments of 2 hours each (the last segment will be shorter).

## Performance Notes

- Uses stream copy (`-c copy`) for maximum speed - no re-encoding
- Processing time depends on your storage speed, not CPU
- Each segment maintains the original video quality
- Works with most video formats that ffmpeg supports

## Troubleshooting

**"ffmpeg command not found"**
- Make sure ffmpeg is installed and in your PATH
- Try running `ffmpeg -version` to verify installation

**"Input file not found"**
- Check the file path is correct
- Use absolute paths if needed

**Permission errors**
- Ensure you have write permissions in the output directory
- On macOS/Linux, you might need to make the script executable:
  ```bash
  chmod +x video_clipper.py
  ```

## License

This tool is open source and uses ffmpeg, which is licensed under the LGPL.
