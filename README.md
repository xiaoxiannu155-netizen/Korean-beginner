# 🇰🇷 韩语启蒙助手 (Korean Beginner Helper)

面向零基础学习者的智能韩语学习 App

## 项目结构

```
monorepo/
├── app/              # Flutter 前端 (iOS + Android)
│   └── lib/
│       ├── config/       # 主题 + 常量
│       ├── models/       # 数据模型
│       ├── services/     # API/音频/同步
│       ├── providers/    # Riverpod 状态
│       ├── screens/      # 页面 (首页/学习/AI/我的)
│       └── widgets/      # Joy 小精灵 + 通用组件
├── backend/          # Python FastAPI 后端
│   ├── app/
│   │   ├── api/v1/       # 35+ REST 端点
│   │   ├── services/     # 业务逻辑
│   │   ├── models/       # 15 张数据表
│   │   └── seed.py       # 502 词种子数据
│   └── tests/            # 75 个测试
├── codemagic.yaml    # iOS 自动构建配置
└── README.md
```

## 快速开始

### 后端

```bash
cd backend
docker compose up -d
curl -X POST http://localhost:8000/api/v1/admin/seed
```

### 前端

```bash
cd app
flutter pub get
flutter run          # 需要 iPhone 模拟器或 iOS 设备
```

## iOS 构建 (Codemagic)

1. Fork 此仓库到你的 GitHub
2. 注册 [codemagic.io](https://codemagic.io) (免费)
3. 连接 GitHub 仓库 → 自动检测 `codemagic.yaml`
4. 配置 Apple 开发者账号 → 触发构建
5. 生成的 IPA 自动上传 TestFlight → 手机安装

首次构建约 15 分钟，后续增量构建 ~5 分钟。

## 技术栈

| 层 | 技术 |
|----|------|
| 前端 | Flutter 3.x + Riverpod + go_router |
| 后端 | FastAPI + SQLAlchemy 2.0 + PostgreSQL |
| AI | LLM (Claude/GPT) + Azure TTS + Azure STT |
| 部署 | Docker + Codemagic CI/CD |

## 测试

- 后端: `cd backend && python -m pytest tests/` (75 tests)
- 前端: `cd app && flutter test`
