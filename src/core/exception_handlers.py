from fastapi.exceptions import RequestValidationError
from fastapi.responses import PlainTextResponse


def attach_exception_handlers(app):
    @app.exception_handler(RequestValidationError)
    def validation_exception_handler(request, exc):
        return PlainTextResponse(str(exc), status_code=400)
