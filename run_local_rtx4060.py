#!/usr/bin/env python3
"""
LTX-Video Generation Script for RTX4060 8GB GPU
Optimized for laptops with 8GB VRAM

This script provides an easy-to-use interface for generating videos locally
using the LTX-Video model, specifically optimized for RTX4060 8GB GPU.
"""

import argparse
import os
import sys
from pathlib import Path

# Add the parent directory to the path to import ltx_video
sys.path.insert(0, str(Path(__file__).parent))

from ltx_video.inference import infer, InferenceConfig


def main():
    parser = argparse.ArgumentParser(
        description="Generate videos with LTX-Video on RTX4060 8GB GPU",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text-to-video generation
  python run_local_rtx4060.py --prompt "A cat playing with a ball"

  # Image-to-video generation
  python run_local_rtx4060.py --prompt "A serene landscape" --image input.jpg

  # Custom resolution and frames
  python run_local_rtx4060.py --prompt "Ocean waves" --width 640 --height 384 --frames 65

  # Extend a video
  python run_local_rtx4060.py --prompt "Continuing the scene" --video input.mp4 --start_frame 0

  # High quality mode (uses FP8 quantized model for lower VRAM)
  python run_local_rtx4060.py --prompt "A bird flying" --quality high
        """
    )

    # Basic parameters
    parser.add_argument(
        "--prompt",
        type=str,
        required=True,
        help="Text prompt describing the video to generate"
    )

    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output video path (default: auto-generated with timestamp)"
    )

    # Input media options
    input_group = parser.add_mutually_exclusive_group()
    input_group.add_argument(
        "--image",
        type=str,
        help="Path to input image for image-to-video generation"
    )

    input_group.add_argument(
        "--video",
        type=str,
        help="Path to input video for video extension"
    )

    parser.add_argument(
        "--start_frame",
        type=int,
        default=0,
        help="Starting frame for conditioning (default: 0)"
    )

    # Video parameters optimized for RTX4060
    parser.add_argument(
        "--width",
        type=int,
        default=704,
        help="Video width (must be divisible by 32, default: 704)"
    )

    parser.add_argument(
        "--height",
        type=int,
        default=480,
        help="Video height (must be divisible by 32, default: 480)"
    )

    parser.add_argument(
        "--frames",
        type=int,
        default=65,
        help="Number of frames (must be 8n+1, e.g., 9, 17, 25, 33, 65, 121, default: 65)"
    )

    parser.add_argument(
        "--fps",
        type=int,
        default=25,
        help="Frames per second (default: 25)"
    )

    # Quality settings
    parser.add_argument(
        "--quality",
        type=str,
        choices=["fast", "balanced", "high"],
        default="balanced",
        help="Quality preset: fast (2B distilled), balanced (2B distilled, default), high (2B distilled FP8)"
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility (default: random)"
    )

    parser.add_argument(
        "--enhance_prompt",
        action="store_true",
        help="Enable automatic prompt enhancement"
    )

    args = parser.parse_args()

    # Validate parameters
    if args.width % 32 != 0:
        print(f"Error: Width must be divisible by 32 (got {args.width})")
        sys.exit(1)

    if args.height % 32 != 0:
        print(f"Error: Height must be divisible by 32 (got {args.height})")
        sys.exit(1)

    if (args.frames - 1) % 8 != 0:
        print(f"Error: Number of frames must be 8n+1 (e.g., 9, 17, 25, 65, 121). Got {args.frames}")
        sys.exit(1)

    # Select model config based on quality preset
    config_map = {
        "fast": "configs/ltxv-2b-0.9.8-distilled.yaml",
        "balanced": "configs/ltxv-2b-0.9.8-distilled.yaml",
        "high": "configs/ltxv-2b-0.9.8-distilled-fp8.yaml"
    }

    pipeline_config = config_map[args.quality]

    # Setup conditioning if image or video provided
    conditioning_media_paths = None
    conditioning_start_frames = None

    if args.image:
        if not os.path.exists(args.image):
            print(f"Error: Image file not found: {args.image}")
            sys.exit(1)
        conditioning_media_paths = [args.image]
        conditioning_start_frames = [args.start_frame]
        print(f"Using image-to-video mode with: {args.image}")

    elif args.video:
        if not os.path.exists(args.video):
            print(f"Error: Video file not found: {args.video}")
            sys.exit(1)
        conditioning_media_paths = [args.video]
        conditioning_start_frames = [args.start_frame]
        print(f"Using video extension mode with: {args.video}")

    # Generate output path if not specified
    if args.output is None:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.output = f"output_{timestamp}.mp4"

    # Print configuration
    print("\n" + "="*60)
    print("LTX-Video Generation - RTX4060 8GB Optimized")
    print("="*60)
    print(f"Prompt: {args.prompt}")
    print(f"Resolution: {args.width}x{args.height}")
    print(f"Frames: {args.frames} @ {args.fps} FPS")
    print(f"Quality: {args.quality}")
    print(f"Model Config: {pipeline_config}")
    print(f"Output: {args.output}")
    if args.seed is not None:
        print(f"Seed: {args.seed}")
    print("="*60 + "\n")

    # Create inference config
    config = InferenceConfig(
        pipeline_config=pipeline_config,
        prompt=args.prompt,
        height=args.height,
        width=args.width,
        num_frames=args.frames,
        output_path=args.output,
        seed=args.seed,
        fps=args.fps,
        enhance_prompt=args.enhance_prompt,
        conditioning_media_paths=conditioning_media_paths,
        conditioning_start_frames=conditioning_start_frames,
    )

    # Run inference
    try:
        print("Starting video generation...")
        print("This may take a few minutes depending on your settings.\n")
        infer(config=config)
        print(f"\n✓ Video generated successfully: {args.output}")
    except Exception as e:
        print(f"\n✗ Error during generation: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
