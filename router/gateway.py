from fastapi import APIRouter

router = APIRouter()

#test_endpoint
@router.get("/testgateway")
async def test_endpoint():
    return {"message": "Hello World"}
