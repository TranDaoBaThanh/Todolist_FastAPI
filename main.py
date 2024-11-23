from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    # Đọc dữ liệu từ file JSON và trả lại dưới dạng JSON
    with open('database.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    return templates.TemplateResponse("todolist.html", {"request": request, "tododict": data})

@app.get("/delete/{id}")
async def delete_todo(request: Request, id: str):
    # Đọc dữ liệu từ file JSON
    with open('database.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Xóa công việc theo id
    if id in data:
        del data[id]
    
    # Lưu lại file JSON
    with open('database.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    # Trả về kết quả
    return JSONResponse(content={"status": "success", "id": id})

@app.post("/add")
async def add_todo(request: Request):
    # Đọc dữ liệu từ file JSON
    with open('database.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Lấy dữ liệu công việc mới
    formdata = await request.form()
    newdata = {}
    i = 1
    for id in data:
        newdata[str(i)] = data[id]
        i += 1
    newdata[str(i)] = formdata["newtodo"]
    
    # Lưu lại dữ liệu mới vào file JSON
    with open('database.json', 'w', encoding='utf-8') as f:
        json.dump(newdata, f, ensure_ascii=False, indent=4)
    
    # Trả về ID của công việc mới để có thể thêm vào DOM
    return JSONResponse(content={"status": "success", "id": str(i)})
