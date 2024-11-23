from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def root(request: Request):
    # Đọc file với encoding UTF-8
    with open('database.json', encoding="utf-8") as f:
        data = json.load(f)
    return templates.TemplateResponse("todolist.html", {"request": request, "tododict": data})

@app.get("/delete/{id}")
async def delete_todo(request: Request, id: str):
    # Đọc file với encoding UTF-8
    with open('database.json', encoding="utf-8") as f:
        data = json.load(f)
    del data[id]
    # Ghi file với encoding UTF-8
    with open('database.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return RedirectResponse("/", 303)

@app.post("/add")
async def add_todo(request: Request):
    # Đọc file với encoding UTF-8
    with open('database.json', encoding="utf-8") as f:
        data = json.load(f)
    formdata = await request.form()
    newdata = {}
    i = 1
    for id in data:
        newdata[str(i)] = data[id]
        i += 1
    newdata[str(i)] = formdata["newtodo"]
    print(newdata)
    # Ghi file với encoding UTF-8
    with open('database.json', 'w', encoding="utf-8") as f:
        json.dump(newdata, f, ensure_ascii=False, indent=4)
    return RedirectResponse("/", 303)
