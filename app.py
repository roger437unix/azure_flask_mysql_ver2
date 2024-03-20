'''
docker run -d --rm --name=mysql \
-v $PWD/dados:/var/lib/mysql \
-p 3306:3306 \
-e MYSQL_ROOT_PASSWORD=mysql \
-e MYSQL_ROOT_HOST=% \
-e MYSQL_DATABASE=db_users \
-e MYSQL_USER=tux \
-e MYSQL_PASSWORD=ABC123xyz \
mysql \
--default-authentication-plugin=mysql_native_password


pip install flask mysql mysql-connector-python

# Cores de botões HTML

https://getbootstrap.com/docs/4.0/components/buttons/#outline-buttons

'''


from flask import Flask, render_template, request, redirect
import mysql.connector
from credenciais import db_config


app = Flask(__name__)

conexao = mysql.connector.connect(
    host = db_config['host'],
    user = db_config['user'],
    password = db_config['password'],
    database = db_config['database']
)


def conn():    
    cursor = conexao.cursor()
    return cursor


def tabela():
    query_create_table = '''
    CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    senha VARCHAR(50) NOT NULL
    );
    '''
    cur = conn()
    cur.execute(query_create_table)
    cur.execute('COMMIT')
    cur.close()


tabela()


@app.route('/',  methods=['GET','POST'])
def homepage():
    if request.method == 'POST':
        req = request.form        

        nome = req['nome']
        email = req['email']
        senha = req['senha']
       
        if nome != "" and email != "" and senha != "":
            query_insert = f"INSERT INTO users VALUES (NULL, '{nome}', '{email}', '{senha}')"
            cur = conn()
            cur.execute(query_insert)
            cur.execute('COMMIT')
            cur.close()            
        return redirect(request.url)		
    return render_template('homepage.html')


@app.route('/consultas')
def select():
    cur = conn()    
    cur.execute('''SELECT nome, email FROM users ORDER BY id ASC''')    
    results = cur.fetchall()    
    cur.close()     
    print(results)    
    return render_template("consultas.html", len = len(results), results = results) 


if __name__ == '__main__':    
    app.run(host='0.0.0.0', port=8080, debug=True)
