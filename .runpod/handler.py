"""
RunPod serverless handler for DotsOCR document parsing
"""
import os
import json
import base64
import tempfile
from io import BytesIO
from PIL import Image
import runpod

# Import the DotsOCR parser
from dots_ocr.parser import DotsOCRParser


def handler(job):
    """
    Main handler function for RunPod serverless execution
    
    Expected input format:
    {
        "input": {
            "image": "base64_encoded_image_or_url",
            "prompt_mode": "prompt_layout_all_en",  # optional
            "bbox": [x1, y1, x2, y2],  # optional, for grounding OCR
            "temperature": 0.1,  # optional
            "max_tokens": 16384,  # optional
            "dpi": 200  # optional, for PDFs
        }
    }
    """
    try:
        job_input = job["input"]
        
        # Get environment variables with defaults
        prompt_mode = job_input.get("prompt_mode", os.getenv("PROMPT_MODE", "prompt_layout_all_en"))
        temperature = float(job_input.get("temperature", os.getenv("TEMPERATURE", "0.1")))
        max_tokens = int(job_input.get("max_tokens", os.getenv("MAX_TOKENS", "16384")))
        top_p = float(job_input.get("top_p", os.getenv("TOP_P", "1.0")))
        num_threads = int(job_input.get("num_threads", os.getenv("NUM_THREADS", "64")))
        dpi = int(job_input.get("dpi", os.getenv("DPI", "200")))
        use_hf = job_input.get("use_hf", os.getenv("USE_HF", "false")).lower() == "true"
        min_pixels = job_input.get("min_pixels", os.getenv("MIN_PIXELS"))
        max_pixels = job_input.get("max_pixels", os.getenv("MAX_PIXELS"))
        
        # Convert string env vars to int if they exist
        if min_pixels:
            min_pixels = int(min_pixels)
        if max_pixels:
            max_pixels = int(max_pixels)
        
        # Initialize the parser
        parser = DotsOCRParser(
            temperature=temperature,
            top_p=top_p,
            max_completion_tokens=max_tokens,
            num_thread=num_threads,
            dpi=dpi,
            min_pixels=min_pixels,
            max_pixels=max_pixels,
            use_hf=use_hf
        )
        
        # Process the input image
        image_input = job_input.get("image")
        if not image_input:
            return {"error": "No image provided in input"}
        
        # Handle base64 encoded image
        if image_input.startswith("data:image"):
            # Extract base64 data
            base64_data = image_input.split(",")[1]
            image_data = base64.b64decode(base64_data)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
                temp_file.write(image_data)
                temp_file_path = temp_file.name
        
        elif image_input.startswith("http"):
            # Handle URL - download and save
            import requests
            response = requests.get(image_input)
            response.raise_for_status()
            
            with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as temp_file:
                temp_file.write(response.content)
                temp_file_path = temp_file.name
        
        else:
            # Assume it's a file path
            temp_file_path = image_input
        
        try:
            # Parse the document
            if prompt_mode == "prompt_grounding_ocr":
                bbox = job_input.get("bbox")
                if not bbox or len(bbox) != 4:
                    return {"error": "bbox required for grounding OCR mode. Format: [x1, y1, x2, y2]"}
                
                result = parser.parse_one_image_grounding(
                    image_file=temp_file_path,
                    bbox=bbox,
                    prompt_mode=prompt_mode
                )
            else:
                result = parser.parse_one_image(
                    image_file=temp_file_path,
                    prompt_mode=prompt_mode
                )
            
            # Clean up temporary file if we created one
            if image_input.startswith(("data:image", "http")):
                os.unlink(temp_file_path)
            
            return {
                "status": "success",
                "result": result,
                "prompt_mode": prompt_mode,
                "config": {
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                    "dpi": dpi,
                    "use_hf": use_hf
                }
            }
            
        except Exception as parse_error:
            # Clean up temporary file if we created one
            if image_input.startswith(("data:image", "http")):
                try:
                    os.unlink(temp_file_path)
                except:
                    pass
            raise parse_error
            
    except Exception as e:
        return {
            "error": f"Processing failed: {str(e)}",
            "status": "error"
        }


# Initialize the serverless function
runpod.serverless.start({"handler": handler})