# Quick Start Guide - RTX4060 8GB

Get started with LTX-Video on your RTX4060 8GB GPU in 5 minutes!

## Step 1: Setup (One-time)

### Windows Users:
```cmd
# Run the setup script
setup_rtx4060.bat
```

### Linux/Mac Users:
```bash
# Run the setup script
chmod +x setup_rtx4060.sh
./setup_rtx4060.sh
```

### Manual Setup (if scripts don't work):
```bash
# Create and activate virtual environment
python -m venv env

# Windows:
env\Scripts\activate

# Linux/Mac:
source env/bin/activate

# Install dependencies
pip install -e .[inference]
```

## Step 2: Generate Your First Video

```bash
python run_local_rtx4060.py --prompt "A cat playing with a ball"
```

That's it! Your video will be saved as `output_YYYYMMDD_HHMMSS.mp4`

## Common Usage Examples

### Text-to-Video (Fast - ~30 seconds)
```bash
python run_local_rtx4060.py \
  --prompt "A serene sunset over the ocean" \
  --quality fast
```

### Image-to-Video
```bash
python run_local_rtx4060.py \
  --prompt "The scene comes to life" \
  --image input.jpg \
  --frames 65
```

### Higher Quality (Slower - ~2 minutes)
```bash
python run_local_rtx4060.py \
  --prompt "A bird flying through clouds" \
  --quality high \
  --width 768 \
  --height 512 \
  --frames 121
```

### With Custom Seed (Reproducible)
```bash
python run_local_rtx4060.py \
  --prompt "A futuristic cityscape at night" \
  --seed 42 \
  --output my_video.mp4
```

## Parameter Quick Reference

| What you want | Command |
|---------------|---------|
| Faster generation | Add `--quality fast` |
| Better quality | Add `--quality high` |
| Longer video | Increase `--frames 121` (must be 8n+1) |
| Bigger resolution | Increase `--width 768 --height 512` |
| Save specific name | Add `--output myfile.mp4` |
| Same result again | Add `--seed 42` (any number) |

## Recommended Settings for RTX4060 8GB

### Quick Test (30 seconds)
```bash
python run_local_rtx4060.py \
  --prompt "YOUR_PROMPT" \
  --quality fast \
  --width 512 \
  --height 512 \
  --frames 33
```

### Balanced (1 minute) - **RECOMMENDED**
```bash
python run_local_rtx4060.py \
  --prompt "YOUR_PROMPT" \
  --width 704 \
  --height 480 \
  --frames 65
```

### High Quality (2-3 minutes)
```bash
python run_local_rtx4060.py \
  --prompt "YOUR_PROMPT" \
  --quality high \
  --width 768 \
  --height 512 \
  --frames 121
```

## Troubleshooting

### "Out of memory" error
- Use `--quality fast`
- Reduce frames: `--frames 33` or `--frames 25`
- Reduce resolution: `--width 512 --height 512`

### "Model not found" error
- Models download automatically on first run
- Ensure you have internet connection
- Need ~10GB free disk space

### Slow generation
- Use `--quality fast`
- Reduce frames and resolution
- Close other GPU applications

## Next Steps

- Read the full documentation: [RTX4060_SETUP.md](RTX4060_SETUP.md)
- Learn prompt engineering tips
- Experiment with different seeds and settings
- Try image-to-video and video extension features

## Support

- Issues: https://github.com/Lightricks/LTX-Video/issues
- Discord: https://discord.gg/ltxplatform
- Documentation: https://docs.ltx.video
