import os
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

# --- CONFIGURAÇÃO DIRETA ---
client = Groq(api_key="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")

@app.route('/')
def home():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Erro: O ficheiro index.html nao foi encontrado na pasta templates. Detalhe: {str(e)}"

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        dados = request.json
        pergunta = dados.get("pergunta", "")
        
        chat = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Voce e a Geometry AI."},
                {"role": "user", "content": pergunta}
            ],
            model="llama3-8b-8192",
        )
        return jsonify({"resposta": chat.choices[0].message.content})
    except Exception as e:
        return jsonify({"resposta": f"Erro na IA: {str(e)}"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
    
