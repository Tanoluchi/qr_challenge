from fastapi import APIRouter ,Depends, HTTPException, status
from uuid import UUID

from app.helpers.auth_user import get_current_user
from app.helpers.statistics_response import build_statistics_response
from app.schemas.scan_schema import QRCodeStatisticsSchema
from app.services.scan_service import ScanService

from app.configs.logger import logger

StatisticsRouter = APIRouter(prefix="/statistics", tags=["QR Code Metrics"])


@StatisticsRouter.get("/scans", response_model=QRCodeStatisticsSchema)
async def get_qr_code_scan_metrics(
        qr_uuid: UUID,
        scan_service: ScanService = Depends(),
        user: dict = Depends(get_current_user)
) -> QRCodeStatisticsSchema:
    """
    Retrieve QR code scan metrics.

    Parameters:
    - `qr_uuid` (UUID): Unique identifier of the QR code.
    - `scan_service` (ScanService): Service handling scan data operations.

    Returns:
    - QRCodeStatisticsSchema: Contains total scans and detailed scan logs.

    Raises:
    - 404: If no data is found for the given QR code.
    - 500: For internal server errors.
    """
    try:
        logger.info(f"Getting scan metrics for QR code: {qr_uuid}")
        # Get total scans
        total_scans = scan_service.get_total_scan(qr_uuid)
        if not total_scans:
            logger.warning(f"No scan data found for QR code: {qr_uuid}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No scan data found for the given QR code."
            )

        # Get scan logs
        scan_logs = scan_service.get_all(qr_uuid)
        # Return the statistics schema with total scans and scan logs
        response = build_statistics_response(total_scans, scan_logs)
        logger.info(f"Successfully fetched metrics for QR code: {qr_uuid}")
        return response
    except Exception as e:
        logger.error(f"Error retrieving scan statistics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )