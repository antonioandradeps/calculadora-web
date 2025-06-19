# app.py
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    # Esta rota exibe o formulário da calculadora.
    return render_template('calculadora.html')

@app.route('/calcular_operacao', methods=['POST'])
def calcular_operacao():
    # Esta rota processa os dados enviados pelo formulário da calculadora.
    if request.method == 'POST':
        try:
            num1_str = request.form['numero1']
            operacao = request.form['operacao']
            num2_str = request.form['numero2']

            num1 = float(num1_str)
            num2 = float(num2_str)
            result = 0
            mensagem_erro = None

            if operacao == '+':
                result = num1 + num2
            elif operacao == '-':
                result = num1 - num2
            elif operacao == '*':
                result = num1 * num2
            elif operacao == '/':
                if num2 == 0: # Evita divisão por zero
                    mensagem_erro = "Erro: Não é possível dividir por zero."
                else:
                    result = num1 / num2
            else:
                mensagem_erro = "Operação não reconhecida. Use +, -, * ou /."

            if mensagem_erro:
                return render_template('calculadora.html', erro=mensagem_erro,
                                       numero1_antigo=num1_str,
                                       operacao_antiga=operacao,
                                       numero2_antigo=num2_str)
            else:
                # Formata a expressão para exibir no template
                expressao_completa = f"{num1} {operacao} {num2} = {result}"
                return render_template('resultado_calculo.html', expressao=expressao_completa)

        except ValueError:
            mensagem_erro = "Por favor, digite números válidos."
            return render_template('calculadora.html', erro=mensagem_erro,
                                   numero1_antigo=request.form.get('numero1', ''),
                                   operacao_antiga=request.form.get('operacao', ''),
                                   numero2_antigo=request.form.get('numero2', ''))
        except Exception as e:
            mensagem_erro = f"Ocorreu um erro inesperado: {e}"
            return render_template('calculadora.html', erro=mensagem_erro,
                                   numero1_antigo=request.form.get('numero1', ''),
                                   operacao_antiga=request.form.get('operacao', ''),
                                   numero2_antigo=request.form.get('numero2', ''))
    else:
        # Se alguém tentar acessar /calcular_operacao diretamente sem POST, redireciona para o formulário.
        return redirect(url_for('index'))

# Não precisamos do app.run() para o PythonAnywhere/Render.
