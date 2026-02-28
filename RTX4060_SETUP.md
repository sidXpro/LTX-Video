# LTX-Video Local Setup for RTX4060 8GB GPU

This guide provides step-by-step instructions for running LTX-Video on a laptop with an RTX4060 8GB GPU.

## System Requirements

- **GPU**: NVIDIA RTX4060 with 8GB VRAM (or similar)
- **RAM**: 16GB+ recommended
- **Python**: 3.10 or higher
- **CUDA**: 12.2 or compatible version
- **Storage**: ~20GB for model weights and dependencies

## Quick Start

### 1. Install Prerequisites

Ensure you have Python 3.10+ and CUDA installed:

```bash
# Check Python version
python --version  # Should be 3.10 or higher

# Check CUDA availability (after PyTorch installation)
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"
```

### 2. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/Lightricks/LTX-Video.git
cd LTX-Video

# Create virtual environment
python -m venv env

# Activate virtual environment
# On Windows:
env\Scripts\activate
# On Linux/Mac:
source env/bin/activate

# Install dependencies
pip install -e .[inference]
```

### 3. Generate Your First Video

```bash
# Text-to-video generation (simplest)
python run_local_rtx4060.py --prompt "A cat playing with a ball"

# Image-to-video with a custom image
python run_local_rtx4060.py --prompt "The scene comes to life" --image your_image.jpg

# Custom resolution and frames
python run_local_rtx4060.py --prompt "Ocean waves crashing on shore" --width 640 --height 384 --frames 65
```

## Usage Guide

### Basic Command Structure

```bash
python run_local_rtx4060.py --prompt "YOUR_PROMPT" [OPTIONS]
```

### Common Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--prompt` | Text description of video (required) | - | `"A bird flying"` |
| `--output` | Output video path | Auto-generated | `output.mp4` |
| `--width` | Video width (divisible by 32) | 704 | `640` |
| `--height` | Video height (divisible by 32) | 480 | `384` |
| `--frames` | Number of frames (8n+1) | 65 | `121` |
| `--fps` | Frames per second | 25 | `30` |
| `--quality` | Quality preset | `balanced` | `fast`, `high` |
| `--seed` | Random seed for reproducibility | Random | `42` |
| `--image` | Input image for i2v generation | None | `input.jpg` |
| `--video` | Input video for extension | None | `input.mp4` |
| `--enhance_prompt` | Enable auto prompt enhancement | False | - |

### Quality Presets

The script offers three quality presets optimized for RTX4060 8GB:

1. **fast** (ltxv-2b-0.9.8-distilled)
   - Fastest generation
   - Good quality
   - ~3-4GB VRAM usage
   - Recommended for iteration and testing

2. **balanced** (ltxv-2b-0.9.8-distilled) - **DEFAULT**
   - Good speed-quality balance
   - ~4-5GB VRAM usage
   - Best for most use cases

3. **high** (ltxv-2b-0.9.8-distilled-fp8)
   - Higher quality with FP8 quantization
   - Slightly slower
   - ~5-6GB VRAM usage
   - Best for final outputs

### Resolution and Frame Constraints

**Important constraints to remember:**

- **Width and Height**: Must be divisible by 32
  - Valid examples: 384, 416, 448, 480, 512, 640, 704, 768, 1024
  - Invalid examples: 400, 500, 720

- **Frames**: Must follow the formula `8n + 1` (where n ≥ 0)
  - Valid examples: 1, 9, 17, 25, 33, 41, 49, 65, 121, 257
  - Invalid examples: 30, 60, 100

**Recommended settings for RTX4060 8GB:**

| Use Case | Width | Height | Frames | Est. Time |
|----------|-------|--------|--------|-----------|
| Quick test | 384 | 384 | 25 | ~30 sec |
| Balanced | 704 | 480 | 65 | ~1 min |
| High quality | 704 | 480 | 121 | ~2 min |
| Maximum | 768 | 512 | 121 | ~3 min |

## Examples

### Example 1: Text-to-Video (Simple)

```bash
python run_local_rtx4060.py \
  --prompt "A golden retriever puppy playing in a sunny garden"
```

### Example 2: Image-to-Video

```bash
python run_local_rtx4060.py \
  --prompt "The landscape transforms through the seasons" \
  --image landscape.jpg \
  --frames 121
```

### Example 3: Custom Settings with Seed

```bash
python run_local_rtx4060.py \
  --prompt "A futuristic city with flying cars at night" \
  --width 768 \
  --height 512 \
  --frames 65 \
  --fps 30 \
  --quality high \
  --seed 42 \
  --output futuristic_city.mp4
```

### Example 4: Video Extension

```bash
python run_local_rtx4060.py \
  --prompt "The story continues" \
  --video input_video.mp4 \
  --start_frame 0 \
  --frames 121
```

### Example 5: Fast Iteration Mode

```bash
# Quick generations for testing prompts
python run_local_rtx4060.py \
  --prompt "A butterfly landing on a flower" \
  --quality fast \
  --width 512 \
  --height 512 \
  --frames 33
```

### Example 6: With Prompt Enhancement

```bash
python run_local_rtx4060.py \
  --prompt "sunset over mountains" \
  --enhance_prompt \
  --quality high
```

## Prompt Engineering Tips

For best results with LTX-Video:

1. **Be Specific and Detailed**: Describe actions, appearances, camera angles, lighting
2. **Use Chronological Order**: Describe events in the order they happen
3. **Keep it Focused**: 1-2 sentences work well, up to 200 words max
4. **Include Camera Work**: Mention camera movements, angles, shots
5. **Describe Motion**: Specify how things move or change

### Good Prompt Examples:

```
"A red fox walks through a snowy forest at dawn, stopping to look directly at the camera.
The camera slowly pans right as snowflakes gently fall around the fox. Soft morning light
filters through the pine trees in the background."

"Close-up shot of a steaming cup of coffee on a wooden table. Camera slowly zooms in
as steam rises and swirls in the morning sunlight. The background is softly blurred
with warm, golden tones."

"An astronaut floats weightlessly in the International Space Station, looking out the window
at Earth below. The camera rotates around them as they reach out to touch the glass.
Blue and white Earth fills the window frame, slowly rotating."
```

## Troubleshooting

### Out of Memory (OOM) Errors

If you encounter VRAM issues:

1. **Reduce resolution**: Try 640x384 or 512x512
2. **Reduce frames**: Use 33 or 25 frames instead of 65+
3. **Use fast quality**: Switch to `--quality fast`
4. **Close other applications**: Especially browsers and GPU-intensive apps

### Generation is Too Slow

1. **Use fast quality preset**: `--quality fast`
2. **Reduce frames**: Fewer frames = faster generation
3. **Use smaller resolution**: 512x512 is much faster than 768x512

### Poor Quality Output

1. **Use high quality preset**: `--quality high`
2. **Increase resolution**: Try 704x480 or 768x512
3. **Improve your prompt**: Add more detail and specificity
4. **Enable prompt enhancement**: Add `--enhance_prompt`
5. **Try different seeds**: Some seeds work better than others

### Import Errors

```bash
# Ensure all dependencies are installed
pip install -e .[inference]

# If still having issues, install explicitly:
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
pip install diffusers transformers sentencepiece imageio[ffmpeg] av
```

### Model Download Issues

Models are downloaded automatically from HuggingFace on first run. If download fails:

1. **Check internet connection**
2. **Try with HuggingFace token** (for gated models):
   ```bash
   huggingface-cli login
   ```
3. **Check disk space**: Models require ~10GB of space

## Advanced Tips

### Memory Optimization

For absolute minimum VRAM usage:

```bash
python run_local_rtx4060.py \
  --prompt "Your prompt here" \
  --quality fast \
  --width 384 \
  --height 384 \
  --frames 17
```

This should run even on GPUs with 6GB VRAM.

### Batch Processing

Create a simple batch script to generate multiple videos:

```bash
#!/bin/bash
prompts=(
  "A cat playing with a ball"
  "A sunset over the ocean"
  "A bird flying through clouds"
)

for i in "${!prompts[@]}"; do
  python run_local_rtx4060.py \
    --prompt "${prompts[$i]}" \
    --output "video_${i}.mp4" \
    --seed $((42 + i))
done
```

### Reproducible Results

Always use the same seed for reproducible outputs:

```bash
python run_local_rtx4060.py \
  --prompt "Your prompt" \
  --seed 42
```

## Performance Benchmarks

Approximate generation times on RTX4060 8GB (laptop):

| Resolution | Frames | Quality | Time | VRAM |
|------------|--------|---------|------|------|
| 384x384 | 25 | fast | ~25s | ~3GB |
| 512x512 | 33 | balanced | ~35s | ~4GB |
| 704x480 | 65 | balanced | ~55s | ~5GB |
| 704x480 | 121 | balanced | ~90s | ~5GB |
| 768x512 | 121 | high | ~120s | ~6GB |

*Times are approximate and may vary based on prompt complexity and system configuration.*

## Additional Resources

- **Main Repository**: https://github.com/Lightricks/LTX-Video
- **Model Weights**: https://huggingface.co/Lightricks/LTX-Video
- **Paper**: https://arxiv.org/abs/2501.00103
- **ComfyUI Integration**: https://github.com/Lightricks/ComfyUI-LTXVideo
- **Discord Community**: https://discord.gg/ltxplatform

## Model Information

This script uses the **ltxv-2b-0.9.8-distilled** model by default, which is:
- **Optimized for speed**: 15x faster than non-distilled models
- **VRAM efficient**: Works well with 8GB VRAM
- **High quality**: Distilled from the 13B base model
- **No CFG/STG required**: Simplified inference pipeline

The FP8 quantized version (**ltxv-2b-0.9.8-distilled-fp8**) offers:
- **Further VRAM savings**: Up to 40% less memory usage
- **Maintained quality**: Minimal quality loss vs full precision
- **Faster inference**: Additional speedup on Ada architecture GPUs

## License

This model is released under the OpenRail-M license. See the main repository for details.

## Support

For issues and questions:
- Open an issue on the [GitHub repository](https://github.com/Lightricks/LTX-Video/issues)
- Join the [Discord community](https://discord.gg/ltxplatform)
- Check the [documentation](https://docs.ltx.video)
