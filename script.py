import random
import metodos as mtd
from flask import Flask, render_template, request, session

app = Flask(__name__)
app.secret_key = "serve"

mtd.criar_arquivo_palavras()


@app.route("/")
def index():
    grupo_ranking = mtd.ler_criar_ranking()    
    return render_template("index.html", titulo="Jogo",  grupo_ranking=grupo_ranking)


@app.route("/iniciar", methods=["POST"])
def escolher_grupo():
    chute = request.form.get("letra")
    grupo_escolhido = request.form.get("grupo")
    dificuldade_escolhida = request.form.get("dificuldade")
    jogador = request.form.get("nome").strip()

    while "  " in jogador:
        jogador = jogador.replace("  ", " ")

    palavra_secreta = mtd.carrega_palavra_secreta(grupo_escolhido)
    letras_acertadas = mtd.inicializa_letras_acertadas(palavra_secreta)
    session["palavra_secreta"] = palavra_secreta
    session["letras_acertadas"] = letras_acertadas
    session["grupo_escolhido"] = grupo_escolhido
    session["dificuldade_escolhida"] = dificuldade_escolhida
    session["jogador"] = jogador
    erros = 0
    session["erros"] = erros
  
    return render_template("Start.html", grupo_escolhido=grupo_escolhido
                                        , dificuldade_escolhida=dificuldade_escolhida
                                        , palavra_secreta=palavra_secreta
                                        , letras_palavra=letras_acertadas
                                        , letras_acertadas=letras_acertadas
                                        , titulo="Jogo Forca"
                                        , erros=erros
                                        , jogador=jogador
                                        , letra = chute
                            )


@app.route("/jogar", methods=["POST"])
def jogar():
    chute = request.form.get("letra")
    enforcou = False
    acertou = False
    erros = session.get("erros", 0)
    palavra_secreta = session.get("palavra_secreta", None)
    letras_acertadas = session.get("letras_acertadas", None)
    grupo_escolhido = session.get("grupo_escolhido", None)
    dificuldade_escolhida = session.get("dificuldade_escolhida", None)
    jogador = session.get("jogador", None)
    max_erros = mtd.nivel_dificuldade(dificuldade_escolhida)
    
    if(chute in palavra_secreta):
        mtd.marca_chute_correto(chute, letras_acertadas, palavra_secreta)
    else:
        erros += 1
        session["erros"] = erros

    if session["erros"] >= max_erros:
        enforcou = True
        pontos = mtd.calcular_pontos(len(palavra_secreta), "DERROTA", erros, max_erros)
        mtd.popular_ranking(jogador,dificuldade_escolhida,"DERROTA", palavra_secreta, pontos)
        return render_template("Fim.html", resultado="DERROTA", jogador=jogador,confete_derrota=True) 
    
    if "_" not in letras_acertadas:
        acertou = True
        pontos = mtd.calcular_pontos(len(palavra_secreta), "VITORIA", erros, max_erros)
        mtd.popular_ranking(jogador,dificuldade_escolhida,"VITORIA", palavra_secreta, pontos)
        return render_template("Fim.html", resultado="VITORIA", jogador=jogador, disparar_confetes=True)
    
    return render_template("Start.html", titulo="Jogo Forca"
                                        , grupo_escolhido=grupo_escolhido
                                        , dificuldade_escolhida=dificuldade_escolhida
                                        , palavra_secreta=palavra_secreta
                                        , letras_palavra=letras_acertadas
                                        , letras_acertadas=letras_acertadas
                                        , letra=chute
                                        , erros=erros
                                        , enforcou=enforcou
                                        , acertou=acertou
                                        , max_erros = max_erros
                                        , jogador=jogador
                                        )


if __name__ == "__main__":
    app.run(debug=True)