from fastapi import HTTPException

from app.configs.logger import logger

from app.schemas.scan_schema import (
    QRCodeStatisticsSchema,
    ScanCounterSchema,
    ScanStatisticsSchema
)


def build_statistics_response(total_scans, scan_logs) -> QRCodeStatisticsSchema:
    """
    Helper function to build the QRCodeStatisticsSchema response.

    Args:
    - `total_scans`: List of scan totals from the service.
    - `scan_logs`: List of scan logs from the service.

    Returns:
    - QRCodeStatisticsSchema: Structured data for the API response.
    """
    try:
        logger.info(f"Total scans: {total_scans}")
        logger.info(f"Scan logs: {scan_logs}")
        return QRCodeStatisticsSchema(
            total_scans=[
                ScanCounterSchema(qr_uuid=row.qr_uuid, scans=row.total_scans)
                for row in total_scans
            ],
            scan_logs=[
                ScanStatisticsSchema(
                    uuid=row.uuid,
                    qr_uuid=row.qr_uuid,
                    ip=row.ip,
                    country=row.country,
                    timezone=row.timezone,
                    created_at=row.created_at,
                )
                for row in scan_logs
            ]
        )
    except Exception as e:
        logger.error(f"Error building statistics response: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")