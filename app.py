from flask import Flask, render_template, request, jsonify, send_from_directory
from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel

aiplatform.init(project="byte-club-bot")

# Cria uma única instância do modelo
modelo = GenerativeModel("gemini-1.5-pro-002")

def generate_with_gemini(prompt):  
    response = modelo.generate_content(prompt)  
    return response.text

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            data = request.get_json() # Correção: obter dados JSON
            prompt = data.get("prompt", "").lower()
        except Exception as e:
            print(f"Erro ao analisar JSON: {e}")  # Imprima o erro específico!
            return jsonify({"error": f"Erro ao analisar JSON: {str(e)}"}), 400 # Retorne o erro para o front-end
        if any(keyword in prompt for keyword in ["html", "css", "scratch"]):
            try:
                resposta_texto = generate_with_gemini(prompt)
                return jsonify({"pergunta": prompt, "resposta": resposta_texto})
            except Exception as e:
                print(f"Erro na API do Gemini: {e}")
                return jsonify({"error": "Erro ao processar. Tente novamente."}), 500
        else:
            return jsonify({"error": "Mencione HTML, CSS ou Scratch."}), 400

    return render_template("index.html") # renderiza o template HTML para requisições GET e POST

if __name__ == "__main__":
    app.run(debug=True)
