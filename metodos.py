import random
from flask import session

def popular_ranking(nome, nivel, status, palavra, pontuacao):
    with open("ranking.txt", "a") as arquivo:
        arquivo.write(f"{nome};{nivel};{status};{palavra};{pontuacao}\n")

def calcular_pontos(tamanho_palavra, resultado_jogo, letras_erradas, nivel_dificuldade):
    fator_tamanho_palavra = 5
    fator_letras_erradas = -5
    fator_nivel_dificuldade = 5

    pontos_tamanho_palavra = tamanho_palavra * fator_tamanho_palavra
    pontos_resultado = 100 if resultado_jogo == "VITORIA" else 0 
    pontos_letras_erradas = letras_erradas * fator_letras_erradas
    pontos_nivel_dificuldade = (10 - nivel_dificuldade) * fator_nivel_dificuldade  

    pontos_totais = pontos_tamanho_palavra + pontos_resultado + pontos_letras_erradas + pontos_nivel_dificuldade
    return pontos_totais


def carrega_palavra_secreta(grupo_escolhido): 
    arquivo = open("palavras.txt","r")
    palavras_grupo = []

    for linha in arquivo:
        linha = linha.strip()
        coluna = linha.split(";")
        if coluna[0].strip().upper() == grupo_escolhido.upper():
            palavras_grupo.append(coluna[1].strip().upper())
    arquivo.close()

    numero = random.randrange(0, len(palavras_grupo))
    palavra_secreta = palavras_grupo[numero].upper()
    return palavra_secreta


def marca_chute_correto(chute, letras_acertadas, palavra_secreta):
    index = 0
    for letra in palavra_secreta:
        if (chute == letra):
            letras_acertadas[index] = letra
        index += 1
    session["letras_acertadas"] = letras_acertadas


def inicializa_letras_acertadas(palavra): 
    return ["_" for letra in palavra]


def nivel_dificuldade(dificuldade):
    if dificuldade == "FACIL":
        max_erros = 10
    elif dificuldade == "MEDIO":
        max_erros = 5
    elif dificuldade == "DIFICIL":
        max_erros = 2
    return max_erros



def ler_criar_ranking():
    try:
        with open("ranking.txt", "r") as arquivo:
            grupo_ranking = []
            for linha in arquivo:
                palavra = linha.strip()
                grupo_ranking.append(palavra)
        grupo_ranking.sort(key=lambda x: int(x.split(';')[4]), reverse=True)
    except FileNotFoundError:
        with open("ranking.txt","a+") as arquivo:
            grupo_ranking = []
            for linha in arquivo:
                palavra = linha.strip()
                grupo_ranking.append(palavra)
        grupo_ranking.sort(key=lambda x: int(x.split(';')[4]), reverse=True)

    for i, palavra in enumerate(grupo_ranking, 1):
        palavra_split = palavra.split(';')
        palavra_split.insert(0, str(i))
        grupo_ranking[i - 1] = ';'.join(palavra_split)
    return grupo_ranking



def criar_arquivo_palavras():
    try:
        with open("palavras.txt", "r") as arquivo:
            return
    except FileNotFoundError:
        with open("palavras.txt", "w") as arquivo:
            palavras = [
                "Automovel;carro",
                "Automovel;Rodas",
                "Automovel;Motor",
                "Automovel;Velocidade",
                "Automovel;Direcao",
                "Automovel;Combustivel",
                "Automovel;Pneus",
                "Automovel;Carroceria",
                "Automovel;Marcha",
                "Automovel;Suspensao",
                "Paises;Argentina",
                "Paises;Espanha",
                "Paises;Italia",
                "Paises;Mexico",
                "Paises;Australia",
                "Paises;Coreia do Sul",
                "Paises;Egito",
                "Paises;Suecia",
                "Paises;Nigeria",
                "Paises;Tailandia",
                "Frutas;Banana",
                "Frutas;Maca",
                "Frutas;Morango",
                "Frutas;Abacaxi",
                "Frutas;Laranja",
                "Frutas;Melancia",
                "Frutas;Uva",
                "Frutas;Pera",
                "Frutas;Manga",
                "Frutas;Kiwi",
                "Animais;Leao",
                "Animais;Elefante",
                "Animais;Tigre",
                "Animais;Girafa",
                "Animais;Cachorro",
                "Animais;Gato",
                "Animais;Urso",
                "Animais;Zebra",
                "Animais;Coelho",
                "Animais;Macaco",
                "Profissoes;Medico",
                "Profissoes;Professor",
                "Profissoes;Engenheiro",
                "Profissoes;Advogado",
                "Profissoes;Arquiteto",
                "Profissoes;Cozinheiro",
                "Profissoes;Policial",
                "Profissoes;Bombeiro",
                "Profissoes;Jornalista",
                "Profissoes;Ator",
                "Filmes;Titanic",
                "Filmes;Matrix",
                "Filmes;O Senhor dos Aneis",
                "Filmes;Pulp Fiction",
                "Filmes;Star Wars",
                "Filmes;Forrest Gump",
                "Filmes;O Poderoso Chefao",
                "Filmes;Harry Potter",
                "Filmes;Jurassic Park",
                "Filmes;Avatar"
            ]
            for palavra in palavras:
                arquivo.write(palavra + "\n")


