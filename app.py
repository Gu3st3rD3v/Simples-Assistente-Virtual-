import os
import urllib.request
import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    # Carrega a interface visual
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        dados = request.json
        pergunta = dados.get("pergunta", "").strip()
        
        if not pergunta:
            return jsonify({"resposta": "Por favor, digite alguma coisa."})
            
        pergunta_min = pergunta.lower()
        if pergunta_min in ["oi", "olá", "ola", "bom dia", "boa noite"]:
            return jsonify({"resposta": "Olá! Eu sou a Geometry AI. O que você gostaria de pesquisar hoje?"})

        # --- SISTEMA DE PESQUISA SEGURO (Sem chaves de API) ---
        # Ele vai pesquisar o termo diretamente na API pública do Wikipedia
        try:
            # Formata a pergunta para o link (ex: "buraco negro" vira "buraco%20negro")
            termo = pergunta.replace(" ", "%20")
            url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{termo}"
            
            # Faz a pesquisa fingindo ser um navegador comum
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            resposta_site = urllib.request.urlopen(req).read()
            dados_wiki = json.loads(resposta_site)
            
            # Se achou o resumo, ele responde
            if "extract" in dados_wiki:
                return jsonify({"resposta": dados_wiki["extract"]})
            else:
                return jsonify({"resposta": "Não encontrei informações exatas sobre isso na minha base."})
        except:
            return jsonify({"resposta": "Desculpe, tente pesquisar usando apenas palavras-chave simples (ex: 'Brasil', 'Fotossíntese', 'Albert Einstein')."})
            
    except Exception as e:
        return jsonify({"resposta": "Ops, tive um pequeno problema técnico. Tente novamente."})

if __name__ == "__main__":
    # Garante que a porta do Render seja respeitada
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
