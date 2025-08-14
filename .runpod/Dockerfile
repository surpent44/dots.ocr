# Use the base vLLM image
FROM vllm/vllm-openai:v0.9.1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies for flash attention and transformers
RUN pip3 install flash_attn==2.8.0.post2
RUN pip3 install transformers==4.51.3

# Install additional dependencies
RUN pip3 install \
    gradio \
    gradio_image_annotation \
    PyMuPDF \
    openai \
    qwen_vl_utils \
    huggingface_hub \
    modelscope \
    accelerate \
    runpod \
    requests \
    Pillow

# Copy the dots.ocr source code
COPY dots.ocr/ /app/dots.ocr/

# Install dots.ocr package
WORKDIR /app/dots.ocr
RUN pip3 install -e .

# Create weights directory
RUN mkdir -p /weights

# Copy handler and configuration files
COPY .runpod/handler.py /app/handler.py

# Set Python path
ENV PYTHONPATH="/app/dots.ocr:${PYTHONPATH}"

# Download model weights (this should be done at build time or via init script)
# Uncomment the following line if you want to download weights at build time
# RUN cd /app/dots.ocr && python3 tools/download_model.py --save_dir /weights

# Set the handler as the entry point
WORKDIR /app
CMD ["python", "handler.py"]