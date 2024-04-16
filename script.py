from flask import Flask, render_template, request
import random

app = Flask(__name__)

    # Lista de palavras
lista_palavras = ["Moto", "Carro", "Elefante", "Açai", "Faca", "Maça", "Bola", "Tenis", "Cadeira", "Ventilador"]

@app.route('/')
def index():
        return render_template('index.html')

@app.route('/jogar', methods=['POST'])
def jogar():
        max_erros = nivel_dificuldade(3)  # Definindo max_erros aqui
        palavra_secreta = carrega_palavra_secreta("Automovel")
        letras_acertadas = inicializa_letras_acertadas(palavra_secreta)
        
        enforcou = False
        acertou = False
        erros = 0

        while(not enforcou and not acertou):
            chute = request.form['letra'] # Obtem a letra do formulário HTML

            if chute in palavra_secreta:
                marca_chute_correto(chute, letras_acertadas, palavra_secreta)
            else:
                erros += 1

            enforcou = erros == max_erros
            acertou = "_" not in letras_acertadas

        if acertou:
            resultado = "Venceu!"
        else:
            resultado = f"Perdeu! A palavra correta era: {palavra_secreta}"

        return render_template('resultado.html', resultado=resultado)
def inicializa_letras_acertadas(palavra):
        return ["_" for letra in palavra]
def carrega_palavra_secreta(grupo):
        palavras_grupo = []
        with open("palavras.txt", "r") as arquivo:
            for linha in arquivo:
                linha = linha.strip().split(";")
                if linha[0].strip().upper() == grupo.upper():
                    palavras_grupo.append(linha[1].strip().upper())
        
        palavra_secreta = random.choice(palavras_grupo)
        return palavra_secreta
def nivel_dificuldade(dificuldade):
        if dificuldade == 1:
            return 20
        elif dificuldade == 2:
            return 10
        elif dificuldade == 3:
            return 5
def marca_chute_correto(chute, letras_acertadas, palavra_secreta):
        for index, letra in enumerate(palavra_secreta):
            if chute == letra:
                letras_acertadas[index] = letra

if __name__ == '__main__':
        app.run(debug=True)
