import os
from flask import Flask, render_template, request, jsonify
import wikipedia

# Configura o Wikipedia para pesquisar em português
wikipedia.set_lang("pt")

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    dados = request.json
    pergunta = dados.get("pergunta", "")
    
    if not pergunta:
         return jsonify({"resposta": "Você não perguntou nada."})

    # Respostas básicas (já que ela não é uma IA de conversa)
    pergunta_min = pergunta.lower()
    if "oi" in pergunta_min or "olá" in pergunta_min:
        return jsonify({"resposta": "Olá! Eu sou a Geometry AI. O que você quer pesquisar?"})

    try:
        # A mágica acontece aqui: pesquisa no Wikipedia e pega as 2 primeiras frases
        resposta_pesquisa = wikipedia.summary(pergunta, sentences=2)
        return jsonify({"resposta": resposta_pesquisa})
        
    except wikipedia.exceptions.DisambiguationError as e:
        return jsonify({"resposta": "Pode ser mais específico? Existem várias coisas com esse nome."})
    except wikipedia.exceptions.PageError:
        return jsonify({"resposta": "Desculpe, não encontrei nada sobre isso na minha base de dados."})
    except Exception as e:
        return jsonify({"resposta": "Deu um erro na pesquisa."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
