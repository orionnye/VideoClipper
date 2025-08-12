#!/usr/bin/env python3
"""
VideoClipper - A simple tool to split large videos into manageable segments
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path
from typing import List, Tuple


class VideoClipper:
	def __init__(self, input_file: str):
		self.input_file = Path(input_file)
		if not self.input_file.exists():
			raise FileNotFoundError(f"Input file not found: {input_file}")
		
		self.output_dir = self.input_file.parent / f"{self.input_file.stem}_segments"
		self.output_dir.mkdir(exist_ok=True)
	
	def get_video_duration(self) -> float:
		"""Get video duration in seconds using ffprobe"""
		cmd = [
			'ffprobe', '-v', 'quiet', '-show_entries', 'format=duration',
			'-of', 'csv=p=0', str(self.input_file)
		]
		
		try:
			result = subprocess.run(cmd, capture_output=True, text=True, check=True)
			return float(result.stdout.strip())
		except subprocess.CalledProcessError as e:
			raise RuntimeError(f"Failed to get video duration: {e}")
		except ValueError:
			raise RuntimeError("Invalid duration returned from ffprobe")
	
	def format_time(self, seconds: float) -> str:
		"""Convert seconds to HH:MM:SS format"""
		hours = int(seconds // 3600)
		minutes = int((seconds % 3600) // 60)
		secs = int(seconds % 60)
		return f"{hours:02d}:{minutes:02d}:{secs:02d}"
	
	def create_segments(self, segment_duration: int) -> List[Tuple[str, str, str]]:
		"""
		Create segments based on duration
		Returns list of (start_time, end_time, output_filename) tuples
		"""
		total_duration = self.get_video_duration()
		segments = []
		
		start_time = 0
		segment_number = 1
		
		while start_time < total_duration:
			end_time = min(start_time + segment_duration, total_duration)
			
			start_str = self.format_time(start_time)
			end_str = self.format_time(end_time)
			
			output_filename = f"{self.input_file.stem}_segment_{segment_number:03d}.mp4"
			output_path = self.output_dir / output_filename
			
			segments.append((start_str, end_str, str(output_path)))
			
			start_time = end_time
			segment_number += 1
		
		return segments
	
	def split_video(self, segment_duration: int, dry_run: bool = False) -> None:
		"""
		Split video into segments
		segment_duration: duration in seconds for each segment
		dry_run: if True, only show what would be done without actually processing
		"""
		print(f"Input file: {self.input_file}")
		print(f"Output directory: {self.output_dir}")
		
		total_duration = self.get_video_duration()
		print(f"Total video duration: {self.format_time(total_duration)}")
		
		segments = self.create_segments(segment_duration)
		print(f"Will create {len(segments)} segments")
		
		if dry_run:
			print("\n=== DRY RUN - No files will be created ===")
			for i, (start, end, output_path) in enumerate(segments, 1):
				print(f"Segment {i}: {start} - {end} -> {Path(output_path).name}")
			return
		
		print(f"\nStarting video processing...")
		
		for i, (start, end, output_path) in enumerate(segments, 1):
			print(f"Processing segment {i}/{len(segments)}: {start} - {end}")
			
			cmd = [
				'ffmpeg', '-i', str(self.input_file),
				'-ss', start, '-to', end,
				'-c', 'copy',  # Use stream copy for faster processing
				'-avoid_negative_ts', 'make_zero',
				'-y',  # Overwrite output files
				output_path
			]
			
			try:
				result = subprocess.run(cmd, capture_output=True, text=True, check=True)
				print(f"✓ Segment {i} completed: {Path(output_path).name}")
			except subprocess.CalledProcessError as e:
				print(f"✗ Error processing segment {i}: {e}")
				print(f"ffmpeg stderr: {e.stderr}")
				return
		
		print(f"\n✓ All segments created successfully in: {self.output_dir}")


def main():
	parser = argparse.ArgumentParser(
		description="Split large video files into manageable segments",
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog="""
Examples:
  # Split into 30-minute segments
  python video_clipper.py video.mp4 --duration 1800
  
  # Split into 1-hour segments  
  python video_clipper.py video.mp4 --duration 3600
  
  # Dry run to see what would be created
  python video_clipper.py video.mp4 --duration 1800 --dry-run
		"""
	)
	
	parser.add_argument('input_file', help='Input video file path')
	parser.add_argument(
		'--duration', '-d', type=int, required=True,
		help='Duration of each segment in seconds (e.g., 1800 for 30 minutes)'
	)
	parser.add_argument(
		'--dry-run', action='store_true',
		help='Show what would be done without actually processing the video'
	)
	
	args = parser.parse_args()
	
	# Validate duration
	if args.duration <= 0:
		print("Error: Duration must be positive")
		sys.exit(1)
	
	try:
		clipper = VideoClipper(args.input_file)
		clipper.split_video(args.duration, args.dry_run)
	except Exception as e:
		print(f"Error: {e}")
		sys.exit(1)


if __name__ == "__main__":
	main()
