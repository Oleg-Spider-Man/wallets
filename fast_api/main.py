import uvicorn
from fastapi import FastAPI
from fast_api.routers import wallets_rout

app = FastAPI()

app.include_router(wallets_rout.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
