from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/")
def hello_world():
    return {"Hello": "World"}

if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8080
    print(f"Your application is running on http://{host}:{port}")
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=True
    )