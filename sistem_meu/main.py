from flask import Flask, render_template, request, redirect, url_for, g, session, send_file, Response, jsonify, flash
import sqlite3 as sql
import pandas as pd
from io import BytesIO
from datetime import datetime
from weasyprint import HTML
from flask_sqlalchemy import SQLAlchemy
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.utils import ImageReader  # Adicionando esta linha

app = Flask(__name__)

# Set the secret key
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


# Function to get a database connection
def get_db_connection():
    return sql.connect('informações.db')

# Create the transactions table if it doesn't exist
with get_db_connection() as db:
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacoes(
        id INTEGER PRIMARY KEY,
            nome TEXT,
            tipo TEXT,
            valor REAL,
            data_lanc DATE,
            obs TEXT,
            referente TEXT,
            forma_pag TEXT
        )
    ''')

                   
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vendas(
            id INTEGER PRIMARY KEY,
            nome_cliente TEXT NOT NULL,
            email TEXT NOT NULL,
            cpf TEXT NOT NULL,
            num_parcelas TEXT NOT NULL,
            tipo_venda TEXT NOT NULL,
            data_lanc_venda DATE  -- Specify the data type for the date column
        )
    ''')


    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            cpf TEXT NOT NULL,
            address TEXT,
            contact1 TEXT,
            contact2 TEXT,
            contact3 TEXT,
            email TEXT,
            observation TEXT,
            classification TEXT  -- Adicionando a coluna de classificação
        )
    ''')

@app.route('/')
def index():
    # Use context manager for database connection
    with get_db_connection() as db:
        cursor = db.cursor()

       

        # Construir a query SQL base
        query = "SELECT * FROM transacoes WHERE 1=1"

       

        # Executar a query no banco de dados
        cursor.execute(query)
        transacoes = cursor.fetchall()

        # Fetch all transactions and expenses from the database
        cursor.execute("SELECT * FROM transacoes WHERE tipo = 'despesa'")
        despesas = cursor.fetchall()

        cursor.execute("SELECT * FROM transacoes WHERE tipo = 'receita'")
        receitas = cursor.fetchall()

        # Calculate the sum of despesas
        total_despesas = sum(float(transacao[3]) for transacao in transacoes if transacao[2] == 'Despesa')
        total_receitas = sum(float(transacao[3]) for transacao in transacoes if transacao[2] == 'Receita')

        # Calculate the total (sum of receitas and despesas)
        total = total_receitas - total_despesas

        # Count transactions by payment method
        cursor.execute("SELECT forma_pag, COUNT(*) FROM transacoes GROUP BY forma_pag")
        forma_pagamento_data = dict(cursor.fetchall())

    # Renderizar o template HTML com os dados dos gráficos
    return render_template('dashboard.php', total_receitas=total_receitas, total_despesas=total_despesas, total=total, forma_pagamento_data=forma_pagamento_data)

@app.route('/adicionar_transacao', methods=['POST'])
def adicionar_transacao():
    nome = request.form.get('nome_transacao')
    tipo = request.form.get('tipo_transacao')
    valor = float(request.form.get('valor_transacao'))
    obs = request.form.get('observacao_transacao')
    data_str = request.form.get('data_lancamento')
    data = datetime.strptime(data_str, '%Y-%m-%d').strftime('%d/%m/%Y')
    referente = request.form.get('referente_transacao')
    form_pag = request.form.get('form_pag')

    with get_db_connection() as db:
        cursor = db.cursor()
        cursor.execute(
            '''
            INSERT INTO transacoes (nome, tipo, valor, data_lanc, obs, referente, forma_pag)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (nome, tipo, valor, data, obs, referente, form_pag)
        )

        transacao_id = cursor.lastrowid
        db.commit()

    if tipo.lower() == 'receita':
        # Criar o gráfico do comprovante


        # Salvar o gráfico em um buffer de memória
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        
        # Criar um PDF com o comprovante
        pdf_buffer = BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        c.setFont("Helvetica", 20)
        c.drawString(50, 750, "Comprovante de Recebimento")
        c.drawString(50, 730, f"Transação ID: {transacao_id}")
        c.drawString(50, 710, f"Nome: {nome}")
        c.drawString(50, 690, f"Valor: R$ {valor:.2f}")
        c.drawString(50, 670, f"Data: {data}")
        c.drawString(50, 650, f"Observação: {obs}")
        c.drawString(50, 630, f"Referente: {referente}")
        c.drawString(50, 610, f"Forma de Pagamento: {form_pag}")

 # Adicionar a logo da empresa
        logo_path = "logo.png"  # Caminho para o arquivo de imagem da logo
        c.drawImage(logo_path, 400, 700, width=100, height=100)

        # Adicionar o gráfico ao PDF
        c.drawImage(ImageReader(buffer), 50, 350, width=400, height=250)
        c.save()

        # Salvar o PDF
        pdf_path = f"comprovante_recebimento_{transacao_id}.pdf"
        with open(pdf_path, "wb") as f:
            f.write(pdf_buffer.getvalue())

        return send_file(pdf_path, as_attachment=True)
    

    return render_template("transacoes.php")


@app.route('/transacoes')
def tabela():
    # Use context manager for database connection
    with get_db_connection() as db:
        cursor = db.cursor()

        # Obter parâmetros do filtro
        tipo_transacao = request.args.get('tipo_transacao', 'all')
        referente_transacao = request.args.get('referente_transacao', '')
        nome_transacao = request.args.get('nome_transacao', '')
        valor_transacao = request.args.get('valor_transacao', '')
        dia_referente = request.args.get('data_lancamento', '')
        obs_transacao = request.args.get('observacao_transacao', '')
        forma_pagamento = request.args.get('form_pag', '')

        data_atual = datetime.now().strftime('%Y-%m-%d')

        # Construir a query SQL base
        query = "SELECT * FROM transacoes WHERE 1=1"

        # Adicionar condições ao filtro
        if tipo_transacao != 'all':
            query += f" AND tipo = '{tipo_transacao}'"

        if referente_transacao:
            query += f" AND referente LIKE '%{referente_transacao}%'"
        if nome_transacao:
            query += f" AND nome LIKE '%{nome_transacao}%'"

        if valor_transacao:
            query += f" AND valor = {float(valor_transacao)}"
        if dia_referente:
            query += f" AND data_lanc = '{dia_referente}'"
        if obs_transacao:
            query += f" AND obs LIKE '%{obs_transacao}%'"
        # Add condition for payment method
        if forma_pagamento:
            query += f" AND forma_pag = '{forma_pagamento}'"

        # Executar a query no banco de dados
        cursor.execute(query)
        transacoes = cursor.fetchall()

        # Fetch all transactions and expenses from the database
        cursor.execute("SELECT * FROM transacoes WHERE tipo = 'despesa'")
        despesas = cursor.fetchall()

        cursor.execute("SELECT * FROM transacoes WHERE tipo = 'receita'")
        receitas = cursor.fetchall()

        # Calculate the sum of despesas
        total_despesas = sum(float(transacao[3]) for transacao in transacoes if transacao[2] == 'Despesa')
        total_receitas = sum(float(transacao[3]) for transacao in transacoes if transacao[2] == 'Receita')

        # Calculate the total (sum of receitas and despesas)
        total = total_receitas - total_despesas

    return render_template('transacoes.php', transacoes=transacoes, despesas=despesas, receitas=receitas, total_despesas=total_despesas, total_receitas=total_receitas, total=total, data_atual=data_atual)

# APAGAR TRANSACAO

@app.route('/apagar_transacao/<int:id>', methods=['POST'])
def apagar_transacao(id):
    with get_db_connection() as db:
        cursor = db.cursor()
        
        # Excluir transação da tabela principal
        cursor.execute("DELETE FROM transacoes WHERE id = ?", (id,))
        db.commit()

    return redirect('/transacoes')



# Exportar informações



@app.route('/exportar_pdf', methods=['GET'])
def exportar_pdf():
    with get_db_connection() as db:
        cursor = db.cursor()

        # Obtain filter parameters
        tipo_transacao = request.args.get('tipo_transacao', 'all')
        referente_transacao = request.args.get('referente_transacao', '')
        nome_transacao = request.args.get('nome_transacao', '')
        valor_transacao = request.args.get('valor_transacao', '')
        dia_referente = request.args.get('data_lancamento', '')
        obs_transacao = request.args.get('observacao_transacao', '')
        forma_pagamento = request.args.get('form_pag', '')

       # Construir a query SQL base
        query = "SELECT * FROM transacoes WHERE 1=1"

        # Adicionar condições ao filtro
        if tipo_transacao != 'all':
            query += f" AND tipo = '{tipo_transacao}'"

        if referente_transacao:
            query += f" AND referente LIKE '%{referente_transacao}%'"
        if nome_transacao:
            query += f" AND nome LIKE '%{nome_transacao}%'"

        if valor_transacao:
            query += f" AND valor = {float(valor_transacao)}"
        if dia_referente:
            query += f" AND data_lanc = '{dia_referente}'"
        if obs_transacao:
            query += f" AND obs LIKE '%{obs_transacao}%'"
        # Adicionar condição para o método de pagamento
        if forma_pagamento:
            query += f" AND forma_pag = '{forma_pagamento}'"

        # Executar a query no banco de dados
        cursor.execute(query)
        transacoes = cursor.fetchall()

        # Converta as transações para um DataFrame do Pandas
        df = pd.DataFrame(transacoes, columns=['id', 'nome', 'tipo', 'valor', 'data_lanc', 'obs', 'referente', 'forma_pag'])

        # Create an HTML string from the DataFrame
        html_string = df.to_html(index=False)

        # Create an HTML string from the DataFrame with styles
        html_string = """
<html>
    <head>
        <link href='https://unpkg.com/boxicons@2.1.4/css/boxicons.min.css' rel='stylesheet'>
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"
            integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL"
            crossorigin="anonymous"></script>
    
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Lilita+One&display=swap" rel="stylesheet">
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Black+Ops+One&display=swap" rel="stylesheet">
        <style>
                      @page {
                    size: landscape;
                }
                @font-face {
    font-family: 'Varino Regular';
    src: url('/static/varino/Varino - Normal.otf') format('opentype');
}
            body {
                font-family: 'Varino Regular';
                color: #ffffff;
                background-color: #110070;
                text-align: center;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
            }
            th, td {
                border-bottom: 1px solid #00d79e;
                padding: 10px;
                text-align: left;
            }
            th {
                background-color: #8000ff;
                color: #fff;
            }
            td {
                background-color: #050022;
            }
        </style>
    </head>
    <body>
        <h1 style="                 font-family: 'Varino Regular';

        font-size: 50px;
    
        color: #00ff91;border-bottom:1px solid #00ff91   ">Transaction Report JGByte</h1>
        """ + df.to_html(index=False) + """
    </body>
    </html>
        
        """

        # Generate PDF from HTML using WeasyPrint
        pdf_bytes = HTML(string=html_string).write_pdf()

    # Create a BytesIO buffer and write PDF bytes to it
    pdf_buffer = BytesIO(pdf_bytes)

    return send_file(pdf_buffer, download_name='JGByte_transactions.pdf', as_attachment=True, mimetype='application/pdf')


# ==================================================================
#                          PESSOAS OU EMPRESAS
# ==================================================================

# pessoas ou emrpesas:
@app.route('/pessoas_empresas', methods=['GET', 'POST'])
def pessoas_empresas():
    if request.method == 'POST':
        name = request.form['name']
        cpf = request.form['cpf']
        address = request.form['address']
        contact1 = request.form['contact1']
        contact2 = request.form['contact2']
        contact3 = request.form['contact3']
        email = request.form['email']
        observation = request.form['observation']
        classification = request.form['classification']  # Add this line to get the classification from the form

        # Connect to the database
        conn = sql.connect('informações.db')
        cur = conn.cursor()

        # Insert data into the people table
        cur.execute("INSERT INTO people (name, cpf, address, contact1, contact2, contact3, email, observation, classification) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (name, cpf, address, contact1, contact2, contact3, email, observation, classification))
        conn.commit()
        conn.close()

        # Flash message for successful addition
        flash('Pessoa adicionada com sucesso!', 'success')

        # Render the template
        return render_template('pessoas.html')
    else:
        # Connect to the database
        conn = sql.connect('informações.db')
        cur = conn.cursor()

        # Retrieve data from the people table
        cur.execute("SELECT * FROM people")
        people = cur.fetchall()
        conn.close()

        # Render the template with people data
        return render_template('pessoas.html', people=people)



@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_pessoa(id):
    if request.method == 'POST':
        # Obter os novos dados do formulário de edição
        new_name = request.form['name']
        new_cpf = request.form['cpf']
        new_address = request.form['address']
        new_contact1 = request.form['contact1']
        new_contact2 = request.form['contact2']
        new_contact3 = request.form['contact3']
        new_email = request.form['email']
        new_observation = request.form['observation']
        new_classification = request.form['classification']  # Adicione esta linha para obter a nova classificação

        # Conectar ao banco de dados
        conn = sql.connect('informações.db')  # Changed here

        cur = conn.cursor()

        # Executar a operação de UPDATE no banco de dados
        cur.execute("UPDATE people SET name=?, cpf=?, address=?, contact1=?, contact2=?, contact3=?, email=?, observation=?, classification=? WHERE id=?", 
                    (new_name, new_cpf, new_address, new_contact1, new_contact2, new_contact3, new_email, new_observation, new_classification, id))

        # Commit da transação e fechamento da conexão
        conn.commit()
        conn.close()

        # Redirecionar de volta para a página de pessoas após a edição
        flash('Pessoa editada com sucesso!', 'success')
        return redirect('/pessoas_empresas')
    else:
        # Lógica para carregar os dados da pessoa com o ID fornecido e exibi-los no modal de edição
        return redirect('/pessoas_empresas')



# template
@app.route("/templates")
def templates():
    return render_template("templates.html")


if __name__ == '__main__':
    app.run(debug=True)