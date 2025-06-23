from fastapi import FastAPI,Request
import GetHeadersList
import uvicorn
app = FastAPI()

@app.get("/rpc/headers")
async def rpc_endpoint(request: Request):
    return GetHeadersList.get_headers()

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)