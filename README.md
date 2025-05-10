
```markdown
# api-jmx-generator

🎯 **一个自动化工具：上传 Postman 接口文档，一键生成 JMeter .jmx 脚本，支持参数注入、Header、提取器、变量关联等功能。**

---

## 📁 项目结构

```

api-jmx-generator/
├── app/
│   ├── main.py                  # FastAPI 主入口
│   ├── parser\_postman.py        # 解析 Postman JSON 接口
│   ├── jmx\_generator.py         # JMX 渲染逻辑
│   └── templates/
│       └── http\_sampler.xml     # JMeter HTTPSampler 模板
├── uploads/                     # 接口文档上传目录
├── output/                      # 自动生成的 .jmx 文件

````

---

## 🚀 快速启动

### 1. 安装依赖

```bash
pip install fastapi uvicorn jinja2
````

### 2. 启动服务（端口可选）

```bash
cd D:\HDHpython\api-jmx-generator
uvicorn app.main:app --reload --port 8004
```

服务地址：[http://127.0.0.1:8004](http://127.0.0.1:8004)

---

## 📝 使用方法

### Step 1: 上传接口文档（Postman JSON）

使用 Swagger / Postman 导出的 `.json` 文件，上传至 API：

```http
POST /upload
Content-Type: multipart/form-data
```

### Step 2: 自动生成 JMX 脚本

上传成功后，脚本将保存在：

```
output/output_test.jmx
```

可在 JMeter GUI 中直接打开运行。

---

## ✅ 已支持的功能

* ✔️ 自动识别接口名称、请求方式、路径、端口
* ✔️ 支持 form-data / raw JSON body
* ✔️ 自动注入 Header 参数
* ✔️ 自动提取 Token（第一个登录接口）
* ✔️ 变量关联：自动传递 `${token}` 给后续请求
* ✔️ 完整 JMeter HashTree 结构，避免结构错误

---

## 🔄 后续可扩展方向

| 功能          | 描述                                       |
| ----------- | ---------------------------------------- |
| JSON字段断言    | 自动添加状态码断言 / 响应字段断言                       |
| 多字段提取       | 支持一次提取多个字段传递到下个请求                        |
| 一键运行 + 报告生成 | 自动执行 jmeter -n -t test.jmx -l result.jtl |
| Web UI 配置界面 | 可视化添加提取字段、断言、线程组设置                       |

---

## 📎 示例 Postman JSON

确保你的接口文件结构包含字段：

```json
{
  "info": { "name": "示例" },
  "item": [
    {
      "name": "登录",
      "request": {
        "method": "POST",
        "url": { "raw": "https://domain.com/login" },
        "body": {
          "mode": "raw",
          "raw": "{\"username\":\"xxx\",\"password\":\"xxx\"}"
        },
        "header": [{ "key": "Content-Type", "value": "application/json" }]
      }
    }
  ]
}
```

---

## 👨‍💻 作者
* 开发测试：黄总
* 构建引擎：Python + FastAPI + Jinja2 + JMeter



