import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from yaml_gen import get_yaml_response

app = FastAPI()

@app.post("/getresponse/")
async def combine_strings(request_body: dict):
    input = request_body.get("query")
    try:
        response = get_yaml_response(input)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)