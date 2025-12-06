from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def main():
    return {"message": "Welcome"}

@app.get("/{data}")
def main(data: str):
    return {"message": data}


if __name__ == "__main__":
    # Bind to all interfaces on port 8080
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)