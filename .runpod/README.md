# DotsOCR - Multilingual Document Parser

[![Deploy on RunPod](https://img.shields.io/badge/Deploy-RunPod-6366f1)](https://runpod.io/gsc?template=YOUR_TEMPLATE_ID&ref=badge)

DotsOCR is a state-of-the-art multilingual document parsing system that uses a single 1.7B-parameter vision-language model for unified layout detection and content recognition. It achieves excellent performance on document parsing tasks while maintaining proper reading order.

## Features

- **Unified Architecture**: Single model handles both layout detection and text recognition
- **Multilingual Support**: Works with documents in multiple languages
- **Multiple Output Formats**: JSON, Markdown, HTML, LaTeX
- **Flexible Parsing Modes**: Full analysis, layout-only, text-only, grounding OCR
- **High Performance**: Optimized for speed with vLLM backend
- **Reading Order**: Maintains proper document reading flow

## Parsing Modes

### Full Layout Analysis (`prompt_layout_all_en`)
Performs complete document analysis including layout detection and text recognition. Returns structured JSON with bounding boxes, categories, and extracted text.

### Layout Detection Only (`prompt_layout_only_en`)
Detects document layout elements without text extraction. Useful for understanding document structure.

### Text Extraction Only (`prompt_ocr`)
Extracts text content without layout information. Excludes headers and footers.

### Grounding OCR (`prompt_grounding_ocr`)
Extracts text from a specific bounding box region. Requires bbox coordinates [x1, y1, x2, y2].

## Input Format

```json
{
  "input": {
    "image": "base64_encoded_image_or_url",
    "prompt_mode": "prompt_layout_all_en",
    "temperature": 0.1,
    "max_tokens": 16384,
    "dpi": 200,
    "bbox": [100, 100, 500, 300]  // Optional, for grounding OCR
  }
}
```

## Output Format

```json
{
  "status": "success",
  "result": {
    "layout": [...],
    "markdown": "...",
    "json": {...}
  },
  "prompt_mode": "prompt_layout_all_en",
  "config": {
    "temperature": 0.1,
    "max_tokens": 16384,
    "dpi": 200
  }
}
```

## Supported Input Types

- **Images**: JPEG, PNG, TIFF, BMP
- **PDFs**: Multi-page documents (processed page by page)
- **Base64**: Encoded image data
- **URLs**: Direct image links

## Performance Tips

- **Image Resolution**: Optimal performance under 11,289,600 pixels
- **PDF DPI**: Use 200 DPI for best quality/speed balance
- **Threading**: Increase num_threads for large PDFs (vLLM only)
- **Memory**: Ensure sufficient GPU memory for model inference

## Configuration Options

- **Temperature**: Controls output randomness (0.0-2.0, default: 0.1)
- **Max Tokens**: Maximum response length (1024-32768, default: 16384)
- **DPI**: PDF rendering quality (72-600, default: 200)
- **Threads**: Parallel processing threads (1-128, default: 64)
- **Backend**: Choose between vLLM (fast) or HuggingFace (compatible)

## Use Cases

- **Document Digitization**: Convert scanned documents to structured data
- **Information Extraction**: Extract specific content from forms and reports
- **Layout Analysis**: Understand document structure and organization
- **Multilingual Processing**: Handle documents in various languages
- **Table Extraction**: Extract and format tabular data
- **Formula Recognition**: Process mathematical expressions

## Error Handling

The service returns detailed error messages for common issues:
- Invalid input format
- Unsupported file types
- Processing timeouts
- Memory limitations

## Support

For issues and questions:
- GitHub: [ucaslcl/dots.ocr](https://github.com/ucaslcl/dots.ocr)
- Documentation: See project README for detailed usage examples

## License

Licensed under the dots.ocr License Agreement. See the project repository for full terms.