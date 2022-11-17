from flask import Flask, render_template, request, redirect, session, flash, url_for

#Classe de jogo para facilitar o processo de criação de objeto
class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo('Super Mario Odyssey', 'Aventura', 'Nintendo Switch')
jogo2 = Jogo('The Legend of Zelda: Breath of the Wild', 'Aventura', 'Nintendo Switch')
jogo3 = Jogo('Metroid Dread', 'Ação', 'Nintendo Switch')
lista = [jogo1, jogo2, jogo3]

app = Flask(__name__) #name faz referência ao proprio arquivo
app.secret_key='alura' #para utilizar session, secret key é obrigatório, para criptografar dados e não guardar informações confidenciais no navegador

class Usuario:
    def __init__(self, nome, nick, senha):
        self.nome = nome
        self.nick = nick
        self.senha = senha

usuario1 = Usuario('Xandones', 'Xandoman', '1234')
usuario2 = Usuario('Jorge', 'J', '4321')
usuario3 = Usuario('Julio', 'Lio', 'abc')

usuarios = { usuario1.nick : usuario1, usuario2.nick : usuario2, usuario3.nick : usuario3 } #dicionario

@app.route('/') #colocar esse / o navegador para funcionar
def index():
    return render_template('lista.html', titulo='Jogos', jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado']==None: #se não estiver logado, não acessa /novo, redirecionado para /login
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Jogo')

@app.route('/criar', methods= ['POST',]) #methods para falar quais métodos eu quero
def criar():
    nome = request.form['nome'] #para resgatar o nome do html
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index')) #colocar a função que instancia a pagina

@app.route('/login')
def login():
    proxima = request.args.get('proxima') #pega o argumento query do endereço do navegador por exemplo ?proxima=novo
    if not proxima:
        return render_template('login.html')
    else:
        return render_template('login.html', proxima=proxima) #novo variavel proxima em laranja atribuida a varivel proxima da função

@app.route('/autenticar', methods=['POST']) #mudar para post para tirar do get para não aparecer informações do usuario na barra de endereços
def autenticar():
    if request.form['usuario'] in usuarios: #request form é a info dada pelo usuario
        usuario = usuarios[request.form['usuario']] #se o usuario estiver cadastrado, usuario recebe o que foi digitado, aí falta só verificar a senha
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nick #uma sessão começada com o nick do usuário
            flash(usuario.nick + ' logado com sucesso!') #mensagem através da função flash, precisa alterar o arquivo html para funcionar
            proxima_pagina = request.form['proxima']
            if proxima_pagina:
                return redirect(proxima_pagina)
            else:
                return redirect(url_for('novo'))

    else:
        flash('Usuário não logado')
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso')
    return redirect(url_for('index'))

app.run(debug=True)

