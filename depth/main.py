from fastapi import FastAPI
import json

app = FastAPI()


@app.get("/")
async def root():
    try:
        file = open("data.json", "r")
        data = json.load(file)
        print(data)
        return data
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return {"detection": [2, 0, 0]}

# from fastapi import FastAPI
# import json

# # uvicorn main:app --reload

# # Now you can import the module from that folder

# detection = []
# app = FastAPI()

# @app.get("/")
# async def root():
#     print("hi")
#     return "hello"
#     # try:
#     #     file = open("data.json", "r")
#     #     data = json.load(file)
#     #     print(data)
#     #     return data
#     # except Exception as e:
#     #     print(f"An error occurred: {str(e)}")
#     #     return {"error": str(e)}