from fastapi import FastAPI
from router import service_registry, gateway, auth

app = FastAPI()

app.include_router(service_registry.router, tags = ["service_registry"])
app.include_router(gateway.router, tags = ["gateway"])
app.include_router(auth.router, tags = ["auth"])

# test_endpoint
@app.get("/")
async def test_endpoint():
    return {"message": "Hello World"}
