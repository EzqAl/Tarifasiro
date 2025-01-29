from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Precios definidos para cada localidad
PRECIOS = {
    "Resistencia/Ctes Cap": {
        "Chica": 7500, "Mediana": 9700, "Grande": 19400, "XL": 27500,
        "XXL": 34000, "M3": 86500, "Donación": 8250,
        "Pallet (no frágil)": 79800, "Pallet (frágil)": 109500
    },
    "Saenz Peña": {
        "Chica": 9100, "Mediana": 12000, "Grande": 21000, "XL": 28600,
        "XXL": 36200, "M3": 102300, "Donación": 8250,
        "Pallet (no frágil)": 96500, "Pallet (frágil)": 143000
    },
    "Int del Chaco/Formosa": {
        "Chica": 11500, "Mediana": 15300, "Grande": 24000, "XL": 32000,
        "XXL": 39900, "M3": 113000, "Donación": 8250
    },
    "Int Formosa": {
        "Chica": 15300, "Mediana": 18000, "Grande": 26600, "XL": 36600,
        "XXL": 47500, "M3": 137000, "Donación": 8250
    },
    "Clorinda": {
        "Chica": 12075, "Mediana": 16065, "Grande": 25200, "XL": 33600,
        "XXL": 41895, "M3": 118650, "Donación": 8250
    }
}

@app.context_processor
def inject_variables():
    return {
        'step': session.get('current_step', 'inicio'),
        'localidades': list(PRECIOS.keys()),
        'cantidad_bultos': session.get('cantidad_bultos', 0)
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    session['current_step'] = 'inicio'
    
    if request.method == 'POST':
        session['tipo_envio'] = request.form['tipo_envio']
        session['current_step'] = 'localidad'
        return redirect(url_for('handle_steps'))
    
    return render_template('index.html')

@app.route('/handle_steps', methods=['GET', 'POST'])
def handle_steps():
    current_step = session.get('current_step', 'inicio')
    
    # Lógica para cada paso
    if current_step == 'localidad':
        if request.method == 'POST':
            session['localidad'] = request.form['localidad']
            session['current_step'] = 'pallet' if session['tipo_envio'] == 'pallet' else 'cantidad_bultos'
        return redirect(url_for('handle_steps'))
    
    elif current_step == 'pallet':
        if request.method == 'POST':
            session['fragil'] = request.form.get('fragil') == 'si'
            session['pesado'] = request.form.get('pesado') == 'si'
            session['current_step'] = 'valor_declarado'
        return redirect(url_for('handle_steps'))
    
    elif current_step == 'cantidad_bultos':
        if request.method == 'POST':
            session['cantidad_bultos'] = int(request.form['cantidad'])
            session['current_step'] = 'seleccion_categorias'
        return redirect(url_for('handle_steps'))
    
    elif current_step == 'seleccion_categorias':
        if request.method == 'POST':
            session['categorias'] = request.form.getlist('categoria')
            session['pesado'] = [str(i) in request.form.getlist('pesado') for i in range(session['cantidad_bultos'])]
            session['current_step'] = 'valor_declarado'
        return redirect(url_for('handle_steps'))
    
    elif current_step == 'valor_declarado':
        if request.method == 'POST':
            session['valor_declarado'] = float(request.form['valor'])
            session['current_step'] = 'resultado'
        return redirect(url_for('handle_steps'))
    
    elif current_step == 'resultado':
        try:
            # Cálculos igual que antes...
            return render_template('index.html', **context)
        except KeyError as e:
            print(f"Error: {str(e)}")
            return redirect(url_for('index'))
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)
