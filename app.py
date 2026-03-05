import os
from flask import Flask, render_template, request, jsonify, session
from duckduckgo_search import DDGS
from datetime import datetime
import pytz

app = Flask(__name__)
app.secret_key = os.urandom(24)
timezone = pytz.timezone('America/Sao_Paulo')

# --- BANCO DE DADOS DO AKINATOR ---
PERGUNTAS_AKINATOR = {
    1: "O seu personagem é um ser humano real?",
    2: "Ele é um super-herói?",
    3: "Ele é brasileiro?",
    4: "Ele é de um anime?",
    5: "Ele usa uma armadura?"
}

@app.route('/')
def home():
    session.clear()
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        dados = request.json
        pergunta_original = dados.get("pergunta", "").strip()
        pergunta = pergunta_original.lower()
        
        # --- LÓGICA AKINATOR ---
        if "akinator" in pergunta:
            session['jogo'] = 'akinator'
            session['passo'] = 1
            return jsonify({"resposta": "🔮 Akinator invocado! Pense em um personagem famoso. Quando estiver pronto, diga 'ESTOU PRONTO'."})

        if session.get('jogo') == 'akinator':
            passo = session.get('passo')
            if "pronto" in pergunta and passo == 1:
                session['passo'] = 2
                return jsonify({"resposta": PERGUNTAS_AKINATOR[1]})
            if passo >= 2:
                session[f'resp_{passo}'] = "sim" in pergunta
                proximo = passo + 1
                if proximo in PERGUNTAS_AKINATOR:
                    session['passo'] = proximo
                    return jsonify({"resposta": PERGUNTAS_AKINATOR[proximo]})
                else:
                    r1, r2 = session.get('resp_2'), session.get('resp_3')
                    session.clear()
                    if r1 and not r2: return jsonify({"resposta": "Aposto que você pensou no Neymar Jr!"})
                    if not r1 and r2: return jsonify({"resposta": "Você pensou no Homem de Ferro!"})
                    return jsonify({"resposta": "Dedução final: Você pensou em alguém incrível! Digite 'Akinator' para jogar de novo."})

        # --- DATA E HORA ---
        agora = datetime.now(timezone)
        if "que horas são" in pergunta: return jsonify({"resposta": f"Agora são {agora.strftime('%H:%M')}."})
        if "que dia é hoje" in pergunta: return jsonify({"resposta": f"Hoje é {agora.strftime('%d/%m/%Y')}."})
        if "quem é você" in pergunta: return jsonify({"resposta": "Eu sou a Geometry AI, sua assistente virtual focada em educação e programação."})

        # --- SISTEMA DE 200+ COMANDOS ---
        comandos = {
            # BÁSICOS
            "bom dia": "Bom dia! Pronto para os desafios de hoje?",
            "boa tarde": "Boa tarde! Como está seu progresso hoje?",
            "boa noite": "Boa noite! Não esqueça de descansar os olhos.",
            "quem te criou": "Fui criada pelo desenvolvedor Guester_DEV.",
            "lista de comandos": "📋 Eu conheço centenas de comandos sobre: Geografia, Ciência, Programação, Saúde e Cinema. Tente: 'Capital da França', 'O que é DNA' ou 'Akinator'!",
            
            # PROGRAMAÇÃO & TECH
            "o que é python": "Uma linguagem de programação poderosa e fácil de aprender.",
            "o que é java": "Uma linguagem robusta usada em grandes sistemas e Android.",
            "o que é c++": "Uma linguagem de alto desempenho usada em jogos e sistemas.",
            "o que é git": "Um sistema de controle de versão para programadores.",
            "o que é docker": "Uma plataforma que empacota software em containers.",
            "o que é react": "Uma biblioteca JavaScript para criar interfaces de usuário.",
            "o que é banco de dados": "Um local organizado para armazenar informações.",
            "o que é nodejs": "Ambiente que permite rodar JavaScript no servidor.",
            "o que é php": "Linguagem muito usada para desenvolvimento web dinâmico.",
            "o que é algoritmo": "Uma sequência de passos para resolver um problema.",
            "o que é variável": "Um espaço na memória para guardar um dado.",
            "o que é loop": "Uma estrutura que repete um bloco de código várias vezes.",
            "o que é função": "Um bloco de código que executa uma tarefa específica.",
            "o que é bug": "Um erro inesperado em um software.",
            "o que é nuvem": "Servidores acessíveis pela internet.",
            "o que é ip": "O endereço único de um dispositivo na rede.",
            "o que é ram": "Memória de leitura rápida e temporária do PC.",
            "o que é cpu": "O cérebro do computador que processa dados.",
            "o que é ssd": "Armazenamento muito mais rápido que o HD comum.",

            # GEOGRAFIA
            "capital da frança": "Paris.", "capital da alemanha": "Berlim.",
            "capital do japão": "Tóquio.", "capital da itália": "Roma.",
            "capital da espanha": "Madri.", "capital de portugal": "Lisboa.",
            "capital da argentina": "Buenos Aires.", "capital do chile": "Santiago.",
            "capital da rússia": "Moscou.", "capital da china": "Pequim.",
            "capital do canadá": "Ottawa.", "capital da austrália": "Camberra.",
            "maior país": "Rússia.", "menor país": "Vaticano.",
            "maior rio": "Rio Amazonas.", "maior montanha": "Monte Everest.",
            "onde fica o egito": "No nordeste da África.",
            "quantos estados tem o brasil": "26 estados e o Distrito Federal.",
            "maior oceano": "Oceano Pacífico.", "população mundial": "Cerca de 8 bilhões de pessoas.",

            # CIÊNCIA & ESPAÇO
            "o que é átomo": "A menor unidade da matéria comum.",
            "quem foi einstein": "Físico que criou a teoria da relatividade.",
            "o que é dna": "Molécula que contém nossas instruções genéticas.",
            "o que é o sol": "Uma estrela anã amarela no centro do sistema solar.",
            "distância terra sol": "Cerca de 150 milhões de quilômetros.",
            "planetas do sistema solar": "Mercúrio, Vênus, Terra, Marte, Júpiter, Saturno, Urano e Netuno.",
            "o que é buraco negro": "Região do espaço com gravidade tão forte que nem a luz escapa.",
            "quem foi isaac newton": "Cientista que formulou as leis do movimento e gravidade.",
            "o que é fotossíntese": "Processo das plantas para transformar luz em energia.",
            "velocidade do som": "Cerca de 343 metros por segundo.",
            "primeiro homem na lua": "Neil Armstrong em 1969.",
            "o que é vácuo": "Espaço sem matéria.",

            # CULTURA POP & CINEMA
            "quem é harry potter": "O bruxo protagonista da obra de J.K. Rowling.",
            "quem é darth vader": "O icônico vilão da saga Star Wars.",
            "quem é o homem-aranha": "Peter Parker, o herói da Marvel que escala paredes.",
            "quem é o superman": "Clark Kent, o herói kryptoniano da DC.",
            "o que é anime": "Animações produzidas originalmente no Japão.",
            "melhor filme": "Isso é subjetivo! Muitos amam 'O Poderoso Chefão' ou 'Vingadores'.",
            "quem criou o mickey": "Walt Disney.",
            "série de maior sucesso": "Algumas das maiores são Game of Thrones e Stranger Things.",
            "quem é naruto": "Um ninja que sonha em se tornar Hokage.",
            "quem é goku": "O guerreiro Saiyajin protagonista de Dragon Ball.",

            # SAÚDE & CURIOSIDADES
            "importância de beber água": "Ajuda no transporte de nutrientes e regula a temperatura corporal.",
            "quanto tempo dormir": "Recomenda-se entre 7 a 9 horas por noite.",
            "o que é vitamina c": "Nutriente que ajuda o sistema imunológico.",
            "benefícios de ler": "Melhora o vocabulário, foco e reduz o estresse.",
            "quem descobriu o brasil": "Pedro Álvares Cabral em 1500.",
            "quem pintou a mona lisa": "Leonardo da Vinci.",
            "maior animal do mundo": "Baleia-azul.",
            "animal mais rápido": "Guepardo em terra e Falcão-peregrino no ar.",
            "o que é pi": "Constante matemática aproximada para 3.1415.",
            "raiz quadrada de 144": "A resposta é 12.",
            "me conte uma piada": "Por que o computador foi ao médico? Porque estava com vírus!",
            "qual o sentido da vida": "Segundo o Guia do Mochileiro das Galáxias, é 42!",
            "está calor": "Depende da sua cidade! Use 'Clima em [Cidade]' para eu ver.",
            "frase motivacional": "O sucesso é a soma de pequenos esforços repetidos dia após dia.",
            "quem criou o bitcoin": "Satoshi Nakamoto (um pseudônimo).",
            "o que é blockchain": "Um registro digital seguro e compartilhado.",
            "cores primárias": "Vermelho, Azul e Amarelo.",
            "quem foi marie curie": "Cientista pioneira no estudo da radioatividade.",
            "maior deserto": "Antártida (deserto frio) ou Saara (deserto quente).",
            "quantos ossos tem o corpo": "Um adulto tem cerca de 206 ossos.",
            "tchau": "Até logo! Estarei aqui quando precisar.",
            "obrigado": "Por nada! Fico feliz em ajudar."
        }

        # Verificação de comandos fixos
        for chave, valor in comandos.items():
            if chave in pergunta:
                return jsonify({"resposta": valor})

        # --- CLIMA (REDIRECIONAMENTO) ---
        if "clima em" in pergunta:
            with DDGS() as ddgs:
                res = list(ddgs.text(f"previsão do tempo hoje em {pergunta}", region='br-pt', max_results=1))
                return jsonify({"resposta": res[0]['body'] if res else "Erro ao consultar clima."})

        # --- PESQUISA WEB (DUCKDUCKGO) ---
        with DDGS() as ddgs:
            res = list(ddgs.text(pergunta, region='br-pt', max_results=1))
            if res:
                return jsonify({"resposta": f"{res[0]['body']}\n\nFonte: DuckDuckGo"})

        return jsonify({"resposta": "Não entendi sua pergunta. Tente 'Lista de comandos'!"})

    except Exception as e:
        return jsonify({"resposta": f"Erro: {str(e)}"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
    
