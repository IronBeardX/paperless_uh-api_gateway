from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from router import service_registry, gateway, auth, crud_endpoints
import uvicorn

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",  # Ajusta los orígenes permitidos según tus necesidades
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(service_registry.router, tags = ["service_registry"])
app.include_router(gateway.router, tags = ["gateway"])
app.include_router(auth.router, tags = ["auth"])
app.include_router(crud_endpoints.router, tags = ["crud_endpoints"])

# test_endpoint
@app.get("/")
async def test_endpoint():
    return {"message": "Hello World"}

if __name__ == '__main__':
    uvicorn.run(app, host = "0.0.0.0", port = 8000)