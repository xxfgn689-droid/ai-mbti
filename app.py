from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app)

# 加载题库
QUESTIONS_PATH = os.path.join(os.path.dirname(__file__), "questions.json")
with open(QUESTIONS_PATH, "r", encoding="utf-8") as f:
    QUESTIONS = json.load(f)["questions"]

# 16种人格类型描述
TYPES = {
    "INTJ": {"name": "建筑师", "desc": "富有战略思维，独立且坚定。善于制定长远规划，对复杂系统有深刻洞察。"},
    "INTP": {"name": "逻辑学家", "desc": "创新型思考者，对知识和真理有强烈渴求。喜欢分析抽象概念和理论。"},
    "ENTJ": {"name": "指挥官", "desc": "天生的领导者，果断且自信。善于组织人员和资源实现目标。"},
    "ENTP": {"name": "辩论家", "desc": "聪明好奇的思想者，喜欢智力挑战。善于从多角度分析问题。"},
    "INFJ": {"name": "提倡者", "desc": "安静而神秘，富有理想主义和同理心。致力于帮助他人和让世界更美好。"},
    "INFP": {"name": "调停者", "desc": "富有诗意和理想主义，重视内在和谐与真实性。对价值观有深刻坚持。"},
    "ENFJ": {"name": "主人公", "desc": "富有魅力的领导者，善于激励他人。关注他人成长和群体和谐。"},
    "ENFP": {"name": "竞选者", "desc": "热情且有创造力，热爱探索可能性。善于与人建立深刻连接。"},
    "ISTJ": {"name": "物流师", "desc": "务实可靠，做事有条不紊。重视传统和规则，是值得信赖的执行者。"},
    "ISFJ": {"name": "守卫者", "desc": "温暖细心的保护者，忠诚且尽责。默默付出，守护所爱之人。"},
    "ESTJ": {"name": "总经理", "desc": "出色的管理者，果断且高效。善于组织流程和带领团队达成目标。"},
    "ESFJ": {"name": "执政官", "desc": "热情关怀的协调者，重视和谐与互助。善于照顾他人的实际需求。"},
    "ISTP": {"name": "鉴赏家", "desc": "冷静的观察者，善于动手解决问题。灵活务实，享受探索事物运作原理。"},
    "ISFP": {"name": "探险家", "desc": "温和的艺术灵魂，活在当下。通过感官和审美探索世界。"},
    "ESTP": {"name": "企业家", "desc": "精力充沛的行动派，善于临场发挥。喜欢冒险和直接体验。"},
    "ESFP": {"name": "表演者", "desc": "天生的娱乐家，热爱生活和社交。用热情和活力感染周围的人。"},
}

@app.route('/')
def index():
    return jsonify({
        "name": "AI MBTI Test API",
        "version": "1.0",
        "endpoints": {
            "/api/questions": "GET - 获取所有题目",
            "/api/submit": "POST - 提交答案获取结果"
        }
    })

@app.route('/api/questions', methods=['GET'])
def get_questions():
    return jsonify({
        "version": "28",
        "total": len(QUESTIONS),
        "questions": QUESTIONS
    })

@app.route('/api/submit', methods=['POST'])
def submit_answers():
    data = request.get_json()
    if not data or 'answers' not in data:
        return jsonify({"error": "Missing answers"}), 400
    
    answers = {a["q_id"]: a["choice"] for a in data.get("answers", [])}
    
    # 初始化维度计分
    dims = {
        "EI": {"E": 0, "I": 0, "pair": ("E", "I"), "tie": "I"},
        "SN": {"S": 0, "N": 0, "pair": ("S", "N"), "tie": "N"},
        "TF": {"T": 0, "F": 0, "pair": ("T", "F"), "tie": "F"},
        "JP": {"J": 0, "P": 0, "pair": ("J", "P"), "tie": "P"}
    }
    
    # 计分
    for q in QUESTIONS:
        if q["id"] in answers:
            letter = q["a_indicates"] if answers[q["id"]] == "A" else q["b_indicates"]
            dim = q["dimension"]
            dims[dim][letter] += 1
    
    # 计算每个维度的结果
    result = {}
    for dim, data in dims.items():
        a, b = data["pair"]
        result[dim] = {
            a: data[a],
            b: data[b],
            "result": a if data[a] > data[b] else (b if data[b] > data[a] else data["tie"])
        }
    
    # 组合 MBTI 类型
    mbti = "".join(result[d]["result"] for d in ["EI", "SN", "TF", "JP"])
    info = TYPES.get(mbti, {"name": "未知", "desc": ""})
    
    return jsonify({
        "type": mbti,
        "type_name": info["name"],
        "dimensions": result,
        "description": info["desc"]
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)