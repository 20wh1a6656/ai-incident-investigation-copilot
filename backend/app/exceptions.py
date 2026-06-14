from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.logging_config import logger

class CopilotException(Exception):
    """Base exception class for Copilot App"""
    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class IncidentNotFoundException(CopilotException):
    def __init__(self, incident_id: str):
        super().__init__(
            message=f"Incident with ID {incident_id} was not found in the persistent store.",
            status_code=status.HTTP_404_NOT_FOUND
        )

class AgentExecutionException(CopilotException):
    def __init__(self, agent_name: str, detail: str):
        super().__init__(
            message=f"Agent '{agent_name}' failed during execution phase. Details: {detail}",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
        )

class DatabaseException(CopilotException):
    def __init__(self, operation: str, details: str):
        super().__init__(
            message=f"Database failure encountered during: {operation}. Logs: {details}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

async def copilot_exception_handler(request: Request, exc: CopilotException) -> JSONResponse:
    logger.error(f"Application error caught: {exc.message} (Status: {exc.status_code})")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": {
                "type": exc.__class__.__name__,
                "message": exc.message
            }
        }
    )

async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.critical(f"Unhandled system error on path {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error": {
                "type": "UnhandledSystemError",
                "message": "An unexpected error occurred in the backend runtime engine."
            }
        }
    )
