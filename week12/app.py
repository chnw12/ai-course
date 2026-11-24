import base64, json, re
from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")

def ask(prompt, image_bytes=None, mime="image/jpeg"):
    content = [{"type": "text", "text": prompt}]
    if image_bytes:
        url = f"data:{mime};base64," + base64.b64encode(image_bytes).decode()
        content.append({"type": "image_url", "image_url": {"url": url}})
    r = client.chat.completions.create(model="gemma4", messages=[{"role": "user", "content": content}])
    return r.choices[0].message.content

def parse_json(text):
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    try:
        return json.loads(m.group(1) if m else text)
    except (json.JSONDecodeError, TypeError):
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    items = None
    error = None
    
    if request.method == 'POST':
        try:
            people = int(request.form.get('people', 1))
            if people <= 0: people = 1
        except:
            people = 1

        image_file = request.files.get('receipt')
        if image_file and image_file.filename != '':
            image_bytes = image_file.read()
            prompt = "영수증 이미지에서 항목과 금액을 추출해서 JSON으로만 답해줘. JSON 구조는 [{'item': '항목명', 'price': 금액}, ...] 형태여야 해. 다른 말은 하지 마."
            try:
                response_text = ask(prompt, image_bytes)
                items = parse_json(response_text)
                if items:
                    total_amount = sum(item.get('price', 0) for item in items)
                    result = total_amount / people
                else:
                    error = "읽지 못했습니다"
            except Exception:
                error = "읽지 못했습니다"
        else:
            amount_str = request.form.get('amount')
            if amount_str:
                try:
                    amount = float(amount_str)
                    result = amount / people
                except ValueError:
                    error = "금액을 입력해주세요."

    return render_template('index.html', result=result, items=items, error=error)

if __name__ == '__main__':
    app.run(debug=True)

import base64, json, re
from flask import Flask, render_template, request
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(base_url="https://krchoi.com/gemma4/v1", api_key="none")

def ask(prompt, image_bytes=None, mime="image/jpeg"):
    content = [{"type": "text", "text": prompt}]
    if image_bytes:
        url = f"data:{mime};base64," + base64.b64encode(image_bytes).decode()
        content.append({"type": "image_url", "image_url": {"url": url}})
    r = client.chat.completions.create(model="gemma4", messages=[{"role": "user", "content": content}])
    return r.choices[0].message.content

def parse_json(text):
    m = re.search(r"```(?:json)?\s*(.*?)```", text, re.S)
    try:
        return json.loads(m.group(1) if m else text)
    except (json.JSONDecodeError, TypeError):
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    items = None
    error = None
    
    if request.method == 'POST':
        people = int(request.form.get('people', 1))
        
        # 영수증 이미지 처리
        image_file = request.files.get('receipt')
        if image_file and image_file.filename != '':
            image_bytes = image_file.read()
            prompt = "영수증 이미지에서 항목 이름과 금액을 추출해서 JSON 형식으로 응답해줘. JSON 구조는 [{'item': '항목명', 'price': 금액}, ...] 형태여야 해. 오직 JSON만 출력해."
            
            try:
                response_text = ask(prompt, image_bytes)
                items = parse_json(response_text)
                
                if items:
                    total_amount = sum(item['price'] for item in items)
                    result = total_amount / people if people > 0 else 0
                else:
                    error = "읽지 못했습니다"
            except Exception:
                error = "읽지 못했습니다"
        
        # 직접 입력 처리
        else:
            amount_str = request.form.get('amount')
            if amount_str:
                try:
                    amount = float(amount_str)
                    result = amount / people if people > 0 else 0
                except ValueError:
                    error = "금액을 정확히 입력해주세요."

    return render_template('index.html', result=result, items=items, error=error)

if __name__ == '__main__':
    app.run(debug=True)
