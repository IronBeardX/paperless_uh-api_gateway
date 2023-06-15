from fastapi import FastAPI
from router import service_registry, gateway, auth
import uvicorn

app = FastAPI()

app.include_router(service_registry.router, tags = ["service_registry"])
app.include_router(gateway.router, tags = ["gateway"])
app.include_router(auth.router, tags = ["auth"])

# test_endpoint
@app.get("/")
async def test_endpoint():
    return {"message": "Hello World"}

if __name__ == '__main__':
    uvicorn.run(app, host = "0.0.0.0", port = 8000)