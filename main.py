from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class VersionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["X-App-Version"] = "1.0.0"
        return response


class BrowserDetectionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        user_agent = request.headers.get("user-agent", "")
        
        if "Postman" in user_agent:
            print("Diqqat: Dasturchi Postman orqali API ga kirdi!")
        
        return await call_next(request)


class MaintenanceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        
        return JSONResponse(
            status_code=503,
            content={"message": "Kechirasiz, serverda texnik ishlar olib borilmoqda. 1 soatdan so'ng urinib ko'ring."}
        )


app.add_middleware(VersionMiddleware)
app.add_middleware(BrowserDetectionMiddleware)



@app.get("/")
def read_root():
    return {"message": "Middleware mashqlari uchun test endpointе"}

@app.get("/test")
def test_endpoint():
    return {"message": "Test endpoint ishlamoqd"}

@app.get("/users")
def get_users():
    return {"users": ["user1", "user2", "user3"]}

# посстоянно проблема с портом, поэтому я его поменял

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
