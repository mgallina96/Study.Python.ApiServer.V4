from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth")


@auth_router.post("/login")
async def login():
    return {"message": "Login successful"}


@auth_router.post("/logout")
async def logout():
    return {"message": "Logout successful"}


@auth_router.post("/refresh")
async def refresh():
    return {"message": "Refresh successful"}
