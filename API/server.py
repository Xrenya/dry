import uvicorn
from fastapi import FastAPI, File, UploadFile

app = FastAPI()

@app.post("/files")
async def file_upload(image1: UploadFile = File(...),
                      image2: UploadFile = File(...)
):
	print(image1)
	print(image2)
	open("image1.jpg","wb").write(image1.file.read())

	open("image2.jpg","wb").write(image2.file.read())
	return "top"

if __name__ == "__main__":
	uvicorn.run(app, host="127.0.0.1", port=8000)
