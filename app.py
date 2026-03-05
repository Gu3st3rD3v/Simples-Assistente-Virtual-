import os
import urllib.request
import urllib.parse
import json
from flask import Flask, render_template, request, jsonify
from duckduckgo_search import DDGS

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        dados = request.json
        pergunta = dados.get("pergunta", "").strip()
        
        if not pergunta:
            return jsonify({"resposta": "Digite algo!"})

        # 1. TENTA DUCKDUCKGO (Busca Geral)
        try:
            with DDGS() as ddgs:
                resultados = [r for r in ddgs.text(pergunta, region='br-pt', max_results=1)]
                if resultados:
                    resumo = resultados[0]['body']
                    link = resultados[0]['href']
                    return jsonify({"resposta": f"{resumo}\n\nFonte: {link}"})
        except:
            pass # Se o DDG falhar/bloquear, ele vai para o Wikipedia abaixo

        # 2. TENTA WIKIPEDIA (Definições)
        try:
            termo = urllib.parse.quote(pergunta)
            url = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{termo}"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            res = urllib.request.urlopen(req).read()
            dados_wiki = json.loads(res)
            return jsonify({"resposta": dados_wiki["extract"]})
        except:
            return jsonify({"resposta": "Não encontrei nada sobre isso no momento."})

    except Exception as e:
        return jsonify({"resposta": "Erro interno no servidor."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
            melhor_titulo = resultados[0]["title"]
            titulo_seguro = urllib.parse.quote(melhor_titulo)
            
            # Passo 2: Pega o resumo desse assunto específico
            url_resumo = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{titulo_seguro}"
            req_resumo = urllib.request.Request(url_resumo, headers={'User-Agent': 'Mozilla/5.0'})
            resposta_resumo = urllib.request.urlopen(req_resumo).read()
            dados_resumo = json.loads(resposta_resumo)
            
            if "extract" in dados_resumo:
                texto_final = dados_resumo["extract"]
                # Tenta pegar o link da fonte para ficar mais profissional
                link_fonte = dados_resumo.get("content_urls", {}).get("desktop", {}).get("page", "")
                if link_fonte:
                    texto_final += f"\n\n(Fonte: {link_fonte})"
                    
                return jsonify({"resposta": texto_final})
            else:
                return jsonify({"resposta": "Achei o tema, mas o artigo está vazio."})
                
        except Exception as e:
            print(f"Erro na pesquisa: {e}") # Ajuda a ver o erro no log do Render
            return jsonify({"resposta": "Desculpe, minha conexão com a base de dados falhou."})
            
    except Exception as e:
        return jsonify({"resposta": "Ops, erro interno."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
