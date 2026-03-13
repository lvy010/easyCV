# easy-cv

A CV defined in YAML using a YAMLResume-like spec, with FastAPI API + 在线预览编辑器。

## 功能

- `resume.yaml`：简历数据源（可版本管理）
- `GET /resume`：在线预览简历
- `GET /editor`：左侧 YAML 编辑、右侧实时预览
- `GET /api/resume`：获取 JSON 数据
- `PUT /api/resume`：以 JSON 覆盖更新
- `GET /api/resume/raw`：获取原始 YAML
- `PUT /api/resume/raw`：保存原始 YAML（服务端校验 YAML 合法性）

## 快速开始

```bash
cd /root/easy-cv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8010
```

打开：

- 预览页: [http://127.0.0.1:8010/resume](http://127.0.0.1:8010/resume)
- 编辑器: [http://127.0.0.1:8010/editor](http://127.0.0.1:8010/editor)
- API 文档: [http://127.0.0.1:8010/docs](http://127.0.0.1:8010/docs)

## 后续可扩展（方便接 skill）

- 增加 `POST /api/resume/optimize`：接入你的 skill 或 LLM，对 YAML 局部改写
- 多模板渲染（`/resume?theme=minimal`）
- 一键导出 PDF（Playwright/WeasyPrint）
