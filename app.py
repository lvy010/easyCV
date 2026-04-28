from pathlib import Path
from typing import Any, Dict

import yaml
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from pydantic import BaseModel


BASE_DIR = Path(__file__).resolve().parent
RESUME_FILE = BASE_DIR / "resume.yaml"

app = FastAPI(title="easy-cv", version="0.1.0")
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


class ResumeDataPayload(BaseModel):
    data: Dict[str, Any]


class ResumeRawPayload(BaseModel):
    yaml_text: str


def _read_resume() -> Dict[str, Any]:
    if not RESUME_FILE.exists():
        raise HTTPException(status_code=404, detail="resume.yaml 不存在")
    text = RESUME_FILE.read_text(encoding="utf-8")
    parsed = yaml.safe_load(text) or {}
    if not isinstance(parsed, dict):
        raise HTTPException(status_code=400, detail="resume.yaml 顶层必须是对象")
    return parsed


def _write_resume(data: Dict[str, Any]) -> None:
    RESUME_FILE.write_text(
        yaml.safe_dump(data, sort_keys=False, allow_unicode=True),
        encoding="utf-8",
    )


@app.get("/", include_in_schema=False)
def root() -> RedirectResponse:
    return RedirectResponse(url="/resume")


@app.get("/resume", response_class=HTMLResponse, include_in_schema=False)
def resume_page(request: Request) -> HTMLResponse:
    data = _read_resume()
    return templates.TemplateResponse(
        request,
        "resume.html",
        context={
            "resume": data,
            "basics": data.get("basics", {}),
            "education": data.get("education", []),
            "code": data.get("code", []),
            "personal_docs": data.get("personal_docs"),
            "team_projects": data.get("team_projects", []),
            "personal_projects": data.get("personal_projects", []),
            "lab_tutorials": data.get("lab_tutorials", []),
            "skills": data.get("skills", []),
            "open_source_experience": data.get("open_source_experience", []),
            "project_experience": data.get("project_experience", []),
        },
    )


@app.get("/editor", response_class=HTMLResponse, include_in_schema=False)
def editor_page(request: Request) -> HTMLResponse:
    yaml_text = RESUME_FILE.read_text(encoding="utf-8") if RESUME_FILE.exists() else ""
    return templates.TemplateResponse(
        request, "editor.html", context={"yaml_text": yaml_text}
    )


@app.get("/api/resume")
def get_resume_data() -> Dict[str, Any]:
    return _read_resume()


@app.put("/api/resume")
def put_resume_data(payload: ResumeDataPayload) -> Dict[str, str]:
    _write_resume(payload.data)
    return {"message": "已更新 resume.yaml"}


@app.get("/api/resume/raw")
def get_resume_raw() -> Dict[str, str]:
    if not RESUME_FILE.exists():
        raise HTTPException(status_code=404, detail="resume.yaml 不存在")
    return {"yaml_text": RESUME_FILE.read_text(encoding="utf-8")}


@app.put("/api/resume/raw")
def put_resume_raw(payload: ResumeRawPayload) -> Dict[str, str]:
    try:
        parsed = yaml.safe_load(payload.yaml_text) or {}
    except yaml.YAMLError as exc:
        raise HTTPException(status_code=400, detail=f"YAML 解析失败: {exc}") from exc
    if not isinstance(parsed, dict):
        raise HTTPException(status_code=400, detail="YAML 顶层必须是对象")
    RESUME_FILE.write_text(payload.yaml_text, encoding="utf-8")
    return {"message": "YAML 已保存"}
