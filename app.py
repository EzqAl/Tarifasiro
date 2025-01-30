from flask import Flask, render_template, request

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
def index():
    resultado = None

    if request.method == 'POST':
        data = request.form
        
        # Obtener datos del formulario
        tipo_envio = data.get('tipo_envio')
        localidad = data.get('localidad')
        cantidad = int(data.get('cantidad', 1))
        valor_declarado = float(data.get('valor_declarado', 0))
        
        # Calcular total base
        total_base = 0
        
        for i in range(cantidad):
            categoria = data.get(f'categoria_{i}')
            pesado = data.get(f'pesado_{i}') == 'si'
            fragil = data.get(f'fragil_{i}') == 'si'
            
            # Determinar precio base
            if tipo_envio == 'pallet':
                categoria = "Pallet (frágil)" if fragil else "Pallet (no frágil)"
            precio = PRECIOS[localidad][categoria]
            
            # Aplicar 15% si es pesado
            if pesado:
                precio *= 1.15
                
            total_base += precio
        
        # Calcular total final
        seguro = valor_declarado * 0.009
        iva = (total_base + seguro) * 0.21
        total = total_base + seguro + iva
        
        resultado = {
            'total_base': round(total_base, 2),
            'seguro': round(seguro, 2),
            'iva': round(iva, 2),
            'total': round(total, 2)
        }

    return render_template(
        'index.html',
        localidades=PRECIOS.keys(),
        resultado=resultado
    )
