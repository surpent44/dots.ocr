# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains **dots.ocr**, a multilingual document parsing system that uses a single 1.7B-parameter vision-language model for unified layout detection and content recognition. The system achieves state-of-the-art performance on document parsing tasks while maintaining good reading order.

## Core Architecture

- **Main Parser**: `dots_ocr/parser.py` - Contains the `DotsOCRParser` class which is the primary interface
- **Model Interface**: `dots_ocr/model/inference.py` - Handles vLLM inference calls
- **Utilities**: 
  - `dots_ocr/utils/prompts.py` - Defines task-specific prompts for different parsing modes
  - `dots_ocr/utils/layout_utils.py` - Layout processing and visualization
  - `dots_ocr/utils/format_transformer.py` - Converts layout JSON to markdown
  - `dots_ocr/utils/image_utils.py` - Image preprocessing and handling

## Development Commands

### Environment Setup
```bash
# Create conda environment
conda create -n dots_ocr python=3.12
conda activate dots_ocr

# Install PyTorch (adjust CUDA version as needed)
pip install torch==2.7.0 torchvision==0.22.0 torchaudio==2.7.0 --index-url https://download.pytorch.org/whl/cu128

# Install package in development mode
pip install -e .
```

### Model Setup
```bash
# Download model weights (avoid directory names with periods)
python3 tools/download_model.py

# Alternative with modelscope
python3 tools/download_model.py --type modelscope
```

### Running the Parser

#### Command Line Interface
```bash
# Parse all layout info (detection + recognition)
python3 dots_ocr/parser.py demo/demo_image1.jpg

# Parse PDF with threading
python3 dots_ocr/parser.py demo/demo_pdf1.pdf --num_thread 64

# Layout detection only
python3 dots_ocr/parser.py demo/demo_image1.jpg --prompt prompt_layout_only_en

# Text extraction only
python3 dots_ocr/parser.py demo/demo_image1.jpg --prompt prompt_ocr

# Grounding OCR (extract text from specific bbox)
python3 dots_ocr/parser.py demo/demo_image1.jpg --prompt prompt_grounding_ocr --bbox 163 241 1536 705

# Use Transformers instead of vLLM
python3 dots_ocr/parser.py demo/demo_image1.jpg --use_hf true
```

#### Demo Applications
```bash
# Gradio web interface
python demo/demo_gradio.py

# Gradio with annotation support
python demo/demo_gradio_annotion.py

# Streamlit demo
python demo/demo_streamlit.py

# HuggingFace Transformers demo
python demo/demo_hf.py
```

### Docker Deployment

#### vLLM Server (Recommended)
```bash
# Build and run with Docker Compose
cd docker/
docker-compose up

# Manual vLLM server setup
export hf_model_path=./weights/DotsOCR
export PYTHONPATH=$(dirname "$hf_model_path"):$PYTHONPATH
sed -i '/^from vllm\.entrypoints\.cli\.main import main$/a\
from DotsOCR import modeling_dots_ocr_vllm' `which vllm`

# Launch vLLM server
CUDA_VISIBLE_DEVICES=0 vllm serve ${hf_model_path} \
    --tensor-parallel-size 1 \
    --gpu-memory-utilization 0.95 \
    --chat-template-content-format string \
    --served-model-name model \
    --trust-remote-code
```

## Key Concepts

### Prompt Modes
The system supports different parsing modes via prompts:
- `prompt_layout_all_en`: Full layout detection and text recognition
- `prompt_layout_only_en`: Layout detection without text extraction
- `prompt_ocr`: Text extraction only (excludes headers/footers)
- `prompt_grounding_ocr`: Extract text from specific bounding box

### Output Formats
- **JSON**: Structured layout information with bboxes, categories, and text
- **Markdown**: Converted text content following reading order
- **HTML**: For table structures
- **LaTeX**: For mathematical formulas

### Model Backends
- **vLLM** (recommended): Faster inference, supports threading
- **HuggingFace Transformers**: Direct model inference, single-threaded

## Performance Considerations

- **Image Resolution**: Optimal performance under 11,289,600 pixels
- **PDF DPI**: Recommended setting of 200 DPI for best results
- **Threading**: Use `--num_thread 64` for large PDFs (vLLM only)
- **Memory**: vLLM uses `--gpu-memory-utilization 0.95` by default

## File Naming Conventions

- Use directory names without periods (e.g., `DotsOCR` not `dots.ocr`) for model weights
- Output files follow pattern: `{filename}.json`, `{filename}.md`, `{filename}_nohf.md`
- PDF pages: `{filename}_page_{idx}.json`

## Common Issues

- **ModuleNotFoundError**: Ensure model directory name has no periods and PYTHONPATH is set correctly
- **Infinite repetition**: Caused by continuous special characters; try alternative prompts
- **High character-to-pixel ratio**: Increase image resolution or PDF DPI