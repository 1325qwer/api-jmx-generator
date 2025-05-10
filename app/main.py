from fastapi import FastAPI, UploadFile, File
import shutil, os
from app.parser_postman import parse_postman_file
from app.jmx_generator import generate_jmx

app = FastAPI()

@app.post("/upload")
async def upload_postman_file(file: UploadFile = File(...)):
    save_path = f"./uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    apis = parse_postman_file(save_path)
    jmx_path = generate_jmx(apis)

    return {"msg": "JMX 生成成功", "file": jmx_path}
