import json
import html

def parse_postman_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data.get('item', [])
    apis = []

    token_extracted = False  # 只提取一次 token

    for item in items:
        request = item.get('request', {})
        url = request.get('url', {}).get('raw', '')
        method = request.get('method', 'GET')
        body = request.get('body', {})
        headers = request.get('header', [])

        # 默认参数
        body_type = ""
        body_content = ""
        params = []

        # 解析 form-data
        if body.get("mode") == "formdata":
            body_type = "form"
            params = [{"key": p["key"], "value": p.get("value", "")} for p in body.get("formdata", [])]

        # 解析 raw json
        elif body.get("mode") == "raw":
            body_type = "raw"
            raw_text = body.get("raw", "")
            body_content = html.escape(raw_text)

        # 拆解 URL
        domain_path = url.split("//")[-1]
        domain = domain_path.split("/")[0]
        raw_path = "/" + "/".join(domain_path.split("/")[1:])
        safe_path = html.escape(raw_path)

        # 构建 headers，并在后续接口加 token 引用
        parsed_headers = [{"key": h["key"], "value": html.escape(h.get("value", ""))} for h in headers]

        if token_extracted:
            parsed_headers.append({"key": "Authorization", "value": "Bearer ${token}"})

        # 判断是否是登录接口，添加提取规则
        extract = None
        if not token_extracted and ("登录" in item.get('name', '') or "login" in item.get('name', '').lower()):
            extract = {
                "key": "token",
                "value": "$.data.token"
            }
            token_extracted = True  # 后面就不再提取 token

        parsed = {
            "name": item.get('name', 'Unnamed API'),
            "method": method,
            "protocol": "https" if url.startswith("https://") else "http",
            "domain": domain,
            "path": safe_path,
            "port": "443" if url.startswith("https://") else "80",
            "body_type": body_type,
            "body_content": body_content,
            "params": params,
            "headers": parsed_headers,
            "extract": extract
        }
        apis.append(parsed)

    return apis
