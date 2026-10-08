# 自习室预约系统

小组协作项目：自习室座位在线预约系统。

## 项目结构

```
study-booking-agent/
├── backend/     # 后端 (Python + FastAPI + SQLAlchemy + JWT)
└── frontend/    # 前端 (待补充)
```

## 快速开始

### 后端

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

启动后访问 http://localhost:8000/docs 查看 API 文档。

默认管理员账号：admin / admin123

### 前端

待补充。

## 技术栈

- 后端：FastAPI + SQLAlchemy + JWT + SQLite(开发) / MySQL(生产)
- 前端：待定
