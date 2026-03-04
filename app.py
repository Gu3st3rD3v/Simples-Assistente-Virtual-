from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    dados = request.json
    pergunta_usuario = dados.get("pergunta", "").lower()

    # Lógica simples de resposta (Você pode trocar isso por uma API de IA real depois)
    if "oi" in pergunta_usuario:
        resposta = "Olá! Como posso te ajudar hoje?"
    elif "quem é você" in pergunta_usuario:
        resposta = "Eu sou uma IA simples hospedada no Render!"
    else:
        resposta = "Ainda estou aprendendo, mas entendi sua pergunta!"

    return jsonify({"resposta": resposta})

if __name__ == '__main__':
    app.run(debug=True)
  
