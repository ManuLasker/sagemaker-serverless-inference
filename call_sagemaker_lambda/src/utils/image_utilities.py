
  
from base64 import b64decode, b64encode
from io import BytesIO
from PIL import Image

def base64_to_pil(base64_image: str) -> Image.Image:
    """Convert base64 image string to PIL image
    Args:
        base64Image (str): base 64 str image decode
    Returns:
        Image.Image: Pil image
    """
    # Select just the image information if there is more information
    if len(base64_image.split(",")) > 1:
        _, base64_image = base64_image.split(",")
    pil_image = Image.open(BytesIO(b64decode(base64_image)))
    if pil_image.mode == "RGBA":
        pil_image = pil_image.convert("RGB")
    return pil_image

def pil_to_base64(pil_image: Image.Image) -> str:
    """Convert pil image to base64 encode string format
    Args:
        pil_image (Image.Image): pil Image
    Returns:
        str: string base64 image
    """
    _buffer = BytesIO()
    if pil_image.mode != "RGBA":
        pil_image.save(_buffer, format="JPEG")
    else:
        pil_image.save(_buffer, format="PNG")
    img_str = b64encode(_buffer.getvalue()).decode("utf-8")
    return img_str