from uuid import UUID
import qrcode
import os
import re

from pydantic import HttpUrl

from PIL import Image

from app.configs.logger import logger

# Directory to store generated QR codes
QR_CODE_DIRECTORY = "static/qr_codes"

def generate_qr_image(
        qr_uuid: UUID,
        url: HttpUrl,
        color: str,
        size: int,
    ) -> str:
    try:
        logger.debug(f"Generating QR Image with url: {url}, color: {color} and size: {size}")
        os.makedirs(QR_CODE_DIRECTORY, exist_ok=True)

        file_name = f"qr_{qr_uuid}.png"
        file_path = os.path.join(QR_CODE_DIRECTORY, file_name)

        if os.path.exists(file_path):
            os.remove(file_path)
            logger.info(f"Deleted existing QR code: {file_path}")
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        # Generate image
        img = qr.make_image(fill_color=color, back_color="white")
        img = img.resize((size, size), Image.Resampling.LANCZOS)
        # Save image
        img.save(file_path)
        logger.info(f"QR code saved: {file_path}")
        return file_path
    except Exception as e:
        logger.error(f"Error generating QR code: {e}")
        return ""

def is_valid_hex_color(color: str) -> bool:
    """
        Validates if a color is a valid hexadecimal (#RRGGBB or #RGB).
    """
    logger.debug(f'Checking color validity for hexadecimal color: {color}')
    HEX_COLOR_REGEX = r"^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
    return bool(re.match(HEX_COLOR_REGEX, color))
