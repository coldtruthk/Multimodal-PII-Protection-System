# api/main.py
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator


def create_app() -> FastAPI:
    app = FastAPI()

    # 🔴 startup 이후가 아니라, 앱 생성 직후에 미들웨어/계측 추가
    # reload 시 중복 추가를 피하려면 아래 가드도 고려(주석 참고)
    # if not any(m.cls.__name__ == "PrometheusMiddleware" for m in app.user_middleware):
    Instrumentator().instrument(app).expose(app, endpoint="/metrics")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app


app = create_app()
