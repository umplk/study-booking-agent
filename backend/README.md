# 自习室预约系统

基于 **FastAPI + SQLAlchemy + JWT** 的自习室座位预约系统后端。

## 技术栈

| 组件 | 说明 |
|------|------|
| FastAPI | Web 框架，自动生成 OpenAPI 文档 |
| SQLAlchemy 2.x | ORM，支持多种数据库 |
| Pydantic v2 | 数据校验与序列化 |
| python-jose | JWT Token 生成与验证 |
| passlib + bcrypt | 密码哈希 |
| SQLite | 默认本地开发数据库（零配置） |
| MySQL（可选） | 生产环境数据库，切换只需改一行配置 |

## 项目结构

```
study-room-reservation/
├── app/
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置读取（.env）
│   ├── database.py          # 数据库引擎与 Session
│   ├── models/              # SQLAlchemy ORM 模型
│   ├── schemas/             # Pydantic 请求/响应模型
│   ├── routers/             # API 路由
│   └── utils/               # 工具（JWT、密码、依赖注入、统一响应）
├── requirements.txt
├── .env.example
└── README.md
```

## 快速开始

### 1. 安装依赖

```bash
pip3 install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 按需修改 .env 中的配置
```

### 3. 启动服务

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

启动后：
- API 文档（Swagger UI）：http://localhost:8000/docs
- ReDoc 文档：http://localhost:8000/redoc
- 健康检查：http://localhost:8000/health

### 4. 默认管理员

系统启动时自动创建默认管理员账号：

| 用户名 | 密码 | 角色 |
|--------|------|------|
| admin  | admin123 | admin |

## 切换到 MySQL

本项目使用 SQLAlchemy ORM，切换到 MySQL **只需改一行配置**：

1. 安装 MySQL 驱动（已在 requirements.txt 中包含 `pymysql`）
2. 在 MySQL 中创建数据库：
   ```sql
   CREATE DATABASE study_room_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
3. 修改 `.env` 文件中的 `DATABASE_URL`：
   ```env
   # 注释掉 SQLite
   # DATABASE_URL=sqlite:///./study_room.db

   # 启用 MySQL（替换用户名、密码、主机、端口）
   DATABASE_URL=mysql+pymysql://root:password@localhost:3306/study_room_db
   ```
4. 重启服务，表会自动创建。

> 无需修改任何业务代码，SQLAlchemy ORM 会自动适配不同数据库方言。

## API 列表

所有接口统一响应格式：`{ "code": 200, "message": "success", "data": ... }`

### 认证（/api/auth）

| 方法 | 路径 | 说明 | 鉴权 |
|------|------|------|------|
| POST | /api/auth/register | 用户注册 | 否 |
| POST | /api/auth/login | 用户登录，返回 JWT | 否 |

### 用户（/api/users）

| 方法 | 路径 | 说明 | 鉴权 |
|------|------|------|------|
| GET | /api/users/me | 获取当前用户信息 | 是 |
| PUT | /api/users/me | 更新个人信息 | 是 |

### 自习室（/api/rooms）

| 方法 | 路径 | 说明 | 鉴权 |
|------|------|------|------|
| GET | /api/rooms | 列出自习室（分页、搜索） | 否 |
| GET | /api/rooms/{id} | 自习室详情（含座位） | 否 |
| POST | /api/rooms | 创建自习室 | 管理员 |
| PUT | /api/rooms/{id} | 更新自习室 | 管理员 |
| DELETE | /api/rooms/{id} | 删除自习室 | 管理员 |
| GET | /api/rooms/{id}/availability | 查询某天可用座位 | 否 |

### 座位（/api/rooms/{room_id}/seats）

| 方法 | 路径 | 说明 | 鉴权 |
|------|------|------|------|
| GET | /api/rooms/{id}/seats | 列出座位 | 否 |
| POST | /api/rooms/{id}/seats | 批量创建座位 | 管理员 |
| PUT | /api/rooms/{id}/seats/{seat_id} | 更新座位状态 | 管理员 |

### 预约（/api/reservations）

| 方法 | 路径 | 说明 | 鉴权 |
|------|------|------|------|
| POST | /api/reservations | 创建预约 | 是 |
| GET | /api/reservations | 我的预约（支持状态筛选） | 是 |
| GET | /api/reservations/{id} | 预约详情 | 是 |
| PUT | /api/reservations/{id}/cancel | 取消预约 | 是（本人） |

## 使用示例

### 注册

```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"student1","email":"s1@example.com","password":"123456","student_id":"2024001","name":"张三"}'
```

### 登录

```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"student1","password":"123456"}'
```

### 创建自习室（管理员）

```bash
curl -X POST http://localhost:8000/api/rooms \
  -H "Authorization: Bearer <admin_token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"图书馆一楼自习室","location":"图书馆1F","open_time":"08:00:00","close_time":"22:00:00","capacity":100}'
```

### 创建预约

```bash
curl -X POST http://localhost:8000/api/reservations \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"seat_id":1,"room_id":1,"reservation_date":"2026-10-09","start_time":"09:00:00","end_time":"11:00:00"}'
```

## 预约规则

- 同一座位同一时间段不可重复预约（冲突检测）
- 预约时间必须在自习室开放时间内
- 不能预约过去的时间
- 只能取消自己的预约

## 数据库表结构

| 表 | 主要字段 |
|----|---------|
| users | id, username, email, password_hash, student_id, name, role, created_at, updated_at |
| rooms | id, name, location, open_time, close_time, capacity, is_active, created_at, updated_at |
| seats | id, room_id, seat_number, is_available, created_at |
| reservations | id, user_id, seat_id, room_id, reservation_date, start_time, end_time, status, created_at, updated_at |
