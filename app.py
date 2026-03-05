import os
from flask import Flask, render_template, request, jsonify
from duckduckgo_search import DDGS
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        dados = request.json
        pergunta = dados.get("pergunta", "").strip().lower()
        
        if not pergunta:
            return jsonify({"resposta": "Por favor, digite algo."})

        # --- FUNÇÃO 1: DATA E HORA ---
        if "que dia é hoje" in pergunta or "data de hoje" in pergunta:
            meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
            agora = datetime.now()
            dia = agora.day
            mes = meses[agora.month - 1]
            ano = agora.year
            return jsonify({"resposta": f"Hoje é dia {dia} de {mes} de {ano}."})

        # --- FUNÇÃO 2: CLIMA (REDIRECIONAMENTO) ---
        if "clima em" in pergunta or "tempo em" in pergunta:
            # Se o usuário perguntar o clima, forçamos a busca no DuckDuckGo a ser específica
            busca_clima = pergunta + " previsão do tempo hoje"
            with DDGS() as ddgs:
                res = list(ddgs.text(busca_clima, region='br-pt', max_results=1))
                if res:
                    return jsonify({"resposta": f"Aqui está a previsão: {res[0]['body']}"})

        # --- FUNÇÃO 3: AKINATOR (SIMULAÇÃO) ---
        if pergunta == "akinator":
            return jsonify({"resposta": "🔮 O gênio Akinator foi invocado! Pense em um personagem e diga 'estou pronto' para começarmos (Nota: Esta é uma função experimental da Geometry AI)." })

        # --- BUSCA PADRÃO (DUCKDUCKGO) ---
        try:
            with DDGS() as ddgs:
                resultados = list(ddgs.text(pergunta, region='br-pt', max_results=1))
                if resultados:
                    resumo = resultados[0]['body']
                    return jsonify({"resposta": resumo})
        except Exception:
            pass

        # BACKUP WIKIPEDIA
        try:
            import urllib.request, json, urllib.parse
            termo = urllib.parse.quote(pergunta)
            url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{termo}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                wiki_data = json.loads(response.read())
                return jsonify({"resposta": wiki_data.get("extract", "Não encontrei detalhes.")})
        except:
            return jsonify({"resposta": "Desculpe, não consegui processar essa informação agora."})

    except Exception as e:
        return jsonify({"resposta": "Erro interno no sistema."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
