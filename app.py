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

@app.route('/', methods=['GET', 'POST'])
def inicio():
    if request.method == 'POST':
        session['tipo_envio'] = request.form['tipo_envio']
        return redirect(url_for('localidad'))
    return render_template('index.html')

@app.route('/localidad', methods=['GET', 'POST'])
def localidad():
    if 'tipo_envio' not in session:
        return redirect(url_for('inicio'))
    
    if request.method == 'POST':
        session['localidad'] = request.form['localidad']
        if session['tipo_envio'] == 'pallet':
            return redirect(url_for('pallet'))
        else:
            return redirect(url_for('cantidad_bultos'))
    
    localidades = list(PRECIOS.keys())
    return render_template('index.html', localidades=localidades)

@app.route('/pallet', methods=['GET', 'POST'])
def pallet():
    if request.method == 'POST':
        session['fragil'] = request.form.get('fragil') == 'si'
        session['pesado'] = request.form.get('pesado') == 'si'
        return redirect(url_for('valor_declarado'))
    return render_template('index.html')

@app.route('/cantidad_bultos', methods=['GET', 'POST'])
def cantidad_bultos():
    if request.method == 'POST':
        session['cantidad_bultos'] = int(request.form['cantidad'])
        return redirect(url_for('seleccion_categorias'))
    return render_template('index.html')

@app.route('/seleccion_categorias', methods=['GET', 'POST'])
def seleccion_categorias():
    cantidad = session.get('cantidad_bultos', 0)
    
    if request.method == 'POST':
        session['categorias'] = request.form.getlist('categoria')
        pesado = [str(i) in request.form.getlist('pesado') for i in range(cantidad)]
        session['pesado'] = pesado
        return redirect(url_for('valor_declarado'))
    
    return render_template('index.html', cantidad=cantidad)

@app.route('/valor_declarado', methods=['GET', 'POST'])
def valor_declarado():
    if request.method == 'POST':
        session['valor_declarado'] = float(request.form['valor'])
        return redirect(url_for('resultado'))
    return render_template('index.html')

@app.route('/resultado', methods=['GET', 'POST'])
def resultado():
    if request.method == 'POST':
        localidad = request.form['localidad']
        tipo_envio = request.form['tipo_envio']
        valor_declarado = float(request.form['valor'])
        cantidad_bultos = int(request.form['cantidad'])
        categorias = request.form.getlist('categorias')
        
        if tipo_envio == 'pallet':
            tipo_pallet = request.form.get('fragil', 'no') == 'si'
            precio = PRECIOS[localidad]["Pallet (frágil)" if tipo_pallet else "Pallet (no frágil)"]
            total_base = precio
        else:
            total_base = 0
            for categoria in categorias:
                precio = PRECIOS[localidad].get(categoria, 0)
                total_base += precio
        
        seguro = valor_declarado * 0.009
        subtotal = total_base + seguro
        iva = subtotal * 0.21
        total = subtotal + iva

        return render_template('index.html', total=total, valor_declarado=valor_declarado, seguro=seguro, iva=iva)
    
    return redirect(url_for('inicio'))

if __name__ == '__main__':
    app.run(debug=True)
