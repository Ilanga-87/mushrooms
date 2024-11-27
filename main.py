import uvicorn
from fastapi import FastAPI

from routers import all_routers

app = FastAPI(
    title="App"
)


for router in all_routers:
    app.include_router(router)

@app.get("/")
async def root():
    return "service is working"

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True, port=8000)