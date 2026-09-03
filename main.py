from fastapi import FastAPI

app = FastAPI(
    title="",
    description="",
    version="1.0.0",
)
@app.get("/")
def root():
    return{"mensaje": "Api de productos funcionando"}
