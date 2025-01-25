from fastapi import Depends, APIRouter, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from app.configs.logger import logger

from uuid import UUID

from app.helpers.auth_user import get_current_user
from app.helpers.ip_info import get_country_and_timezone, get_client_ip
from app.services.qr_service import QRCodeService
from app.services.scan_service import ScanService
from app.models.scan_model import Scan

ScanerRouter = APIRouter(prefix="/scan", tags=["Scan QR Code"])

@ScanerRouter.get("/{qr_uuid}",
                  status_code=status.HTTP_200_OK,
                  summary="Simulate QR scanning"
)
async def scan_qr_code(
        qr_uuid: UUID,
        request: Request,
        qr_code_service: QRCodeService = Depends(),
        scan_service: ScanService = Depends(),
        user: dict = Depends(get_current_user)
):
    """
    Simulate QR scanning by retrieving QR Code information

    Args:
        qr_uuid (UUID): The UUID of the QR Code to be scanned
        request (Request): The FastAPI request object

    Returns:
        dict: The QR Code information
    """
    try:
        logger.info(f"Scanning QR code with UUID: {qr_uuid}")
        # Check if the QR Code exists
        qr_code = qr_code_service.get(qr_uuid)
        if not qr_code:
            logger.error("QR Code not found")
            raise HTTPException(status_code=404, detail="QR Code not found")

        # Get client IP
        client_ip = get_client_ip(request)
        # Get country and timezone from IP using ipinfo.io
        ip_info = get_country_and_timezone(client_ip)
        # Create scan data
        scan_data = Scan(
            qr_uuid=qr_uuid,
            ip=client_ip,
            country=ip_info.get('country', ''),
            timezone=ip_info.get('timezone', ''),
        )
        # Save data to scan in db
        scan_service.create(scan_data)

        # Log scan metrics
        logger.info(
            f"QR Code Scanned: "
            f"UUID={qr_uuid}, "
            f"IP={client_ip}, "
            f"Country={scan_data.country}, "
        )

        # Redirect to the URL associated with the QR code
        logger.info(f"Redirecting to URL: {qr_code.url}")
        return RedirectResponse(
            url=qr_code.url,
            status_code=status.HTTP_307_TEMPORARY_REDIRECT
        )
    except Exception as e:
        logger.error(f"Scan processing error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during QR code processing"
        )