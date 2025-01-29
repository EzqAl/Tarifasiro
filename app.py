from flask import Flask, render_template, request, session, jsonify

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
        session['localidad'] = request.form['localidad']
        session['cantidad_bultos'] = int(request.form['cantidad'])
        session['categorias'] = request.form.getlist('categorias')
        session['valor_declarado'] = float(request.form['valor'])
        session['fragil'] = request.form.get('fragil') == 'si'
        session['pesado'] = request.form.get('pesado') == 'si'
        return jsonify(calcular_resultado())
    localidades = list(PRECIOS.keys())
    return render_template('index.html', localidades=localidades)

def calcular_resultado():
    localidad = session['localidad']
    valor_declarado = session['valor_declarado']
    
    if session['tipo_envio'] == 'pallet':
        tipo_pallet = "Pallet (frágil)" if session['fragil'] else "Pallet (no frágil)"
        precio = PRECIOS[localidad][tipo_pallet]
        if session['pesado']:
            precio *= 1.15
        total_base = precio
    else:
        total_base = 0
        for categoria in session['categorias']:
            precio = PRECIOS[localidad][categoria]
            if categoria != "Donación" and session['pesado']:
                precio *= 1.15
            total_base += precio
    
    seguro = valor_declarado * 0.009
    subtotal = total_base + seguro
    iva = subtotal * 0.21
    total = subtotal + iva
    
    return {
        "total_base": total_base,
        "seguro": seguro,
        "iva": iva,
        "total": total,
        "valor_declarado": valor_declarado
    }

if __name__ == '__main__':
    app.run(debug=True)
