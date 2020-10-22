import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from jomai.api import routes

app = FastAPI()

origins = ["http://0.0.0.0:4200"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
async def read_root():
    return {"Hello": "World"}

app.include_router(routes.router)

if __name__ == "__main__":
    print("STARTING UVICORN THROUGH main.py")
    uvicorn.run("jomai.main:app", host="0.0.0.0", port=8000, reload=True)
