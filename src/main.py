
from yunopyutils import build_logger
from logging import getLogger
from os import getenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uvicorn import run, config

_DEVELOPMENT_ENV = 'development'
_ASGI_ENV = getenv('ASGI_ENV', _DEVELOPMENT_ENV)
_PREFIX_PATH = getenv("PREFIX_PATH", "/prefix")
_LOGGER = build_logger(__file__)


class Unless():
    def filter(self, record) -> bool:
        _, _, path, _, _ = record.args
        return path not in [
            f"{_PREFIX_PATH}/",
            f"{_PREFIX_PATH}/healthy",
            f"{_PREFIX_PATH}/liveness",
            f"{_PREFIX_PATH}/docs",
            f"{_PREFIX_PATH}/openapi.json"
        ]


def _launch_asgi_server(app: FastAPI):
    log_config = config.LOGGING_CONFIG
    log_config["formatters"]["access"]["datefmt"] = "%Y-%m-%dT%H:%M:%S.%03dZ"
    log_config["formatters"]["default"]["datefmt"] = "%Y-%m-%dT%H:%M:%S.%03dZ"
    log_config["formatters"]["access"]["fmt"] = \
        '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "addr": "%(client_addr)s", "path": "%(request_line)s", "code": "%(status_code)s"}'
    log_config["formatters"]["default"]["fmt"] = \
        '{"timestamp": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'

    _PORT = int(getenv("PORT", "3000"))
    _HOST = getenv("HOST", "0.0.0.0")

    getLogger("uvicorn.access").addFilter(Unless())
    run(app, host=_HOST, port=_PORT, log_config=log_config)


def main():
    from routes import routes

    _SVC = getenv("APP_ID", "fastapi")

    app = FastAPI(title=f"{_SVC} API",
                  docs_url=f"{_PREFIX_PATH}/docs",
                  openapi_url=f"{_PREFIX_PATH}/openapi.json")

    app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(routes)

    if (_ASGI_ENV != _DEVELOPMENT_ENV):
        _launch_asgi_server(app)
    return app


if __name__ == '__main__':
    _LOGGER.debug("Starting FastAPI")
    main()
