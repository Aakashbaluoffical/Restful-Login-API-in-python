from fastapi import FastAPI , Request
from fastapi.middleware.cors import CORSMiddleware
from routers import login_system
import json




app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://localhost:8000",
    "http://localhost:8001",
    "http://192.168.56.1:8000",
    "http://192.168.56.1:8001",
    "http://192.168.54.115:8001",
    ""
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login_system.router)


@app.get('/')
def about():
    return {'data':{'name': "System API for Enterprise app.","version":"1.0" }}


@app.get('/app')
def about():
    return {'data':{'name': "Login System.","version":"1.0" }}    

@app.get('/show')
def about():
    return {'data':{'name': "Docker is working","version":"1.0" }} 


if __name__ == "__main__":
    print("MAIN")
    import uvicorn
    #uvicorn.run(app,host="127.0.0.1", port=9000)
    uvicorn.run(app, host="0.0.0.0", port=9000)
