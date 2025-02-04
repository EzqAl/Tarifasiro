from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = "supersecretkey"

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
        "XXL": 39900, "M3": 113000, "Donación": 8250,
        "Pallet (no frágil)": 113000,  
        "Pallet (frágil)": 113000 * 1.15  
    },
    "Clorinda": {
        "Chica": 15300, "Mediana": 18000, "Grande": 26600, "XL": 36600,
        "XXL": 47500, "M3": 137000, "Donación": 8250,
        "Pallet (no frágil)": 137000,  
        "Pallet (frágil)": 137000 * 1.15  
    },
    # "Int. Formosa": {  # Comentado
    #     "Chica": 12075, "Mediana": 16065, "Grande": 25200, "XL": 33600,
    #     "XXL": 41895, "M3": 118650, "Donación": 8250
    # }  # No
}


@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    error = None

    if request.method == 'POST':
        try:
            data = request.form
            tipo_envio = data.get('tipo_envio')
            localidad = data.get('localidad')
            cantidad = int(data.get('cantidad', 1))
            valor_declarado = float(data.get('valor_declarado', 0))

            # Validaciones básicas
            if not tipo_envio or not localidad or cantidad <= 0 or valor_declarado < 0:
                raise ValueError("Complete todos los campos correctamente.")
            
            total_base = 0
            
            # Procesar cada ítem
            for i in range(cantidad):
                pesado = data.get(f'pesado_{i}') == 'si'
                fragil = data.get(f'fragil_{i}') == 'si'
                
                # Determinar categoría
                if tipo_envio == 'pallet':
                    categoria = "Pallet (frágil)" if fragil else "Pallet (no frágil)"
                else:
                    categoria = data.get(f'categoria_{i}')
                    if not categoria:
                        raise ValueError(f"Falta categoría en el ítem {i + 1}")

                # Validar categoría
                if categoria not in PRECIOS[localidad]:
                    raise ValueError(f"Categoría '{categoria}' no existe en {localidad}")
                
                precio = PRECIOS[localidad][categoria]
                
                # Aplicar recargo por peso
                if pesado:
                    precio *= 1.15
                
                total_base += precio

            # Cálculos finales
            seguro = valor_declarado * 0.009
            iva = (total_base + seguro) * 0.21
            total = total_base + seguro + iva

            resultado = {
                'total_base': round(total_base, 2),
                'seguro': round(seguro, 2),
                'iva': round(iva, 2),
                'total': round(total, 2)
            }

        except Exception as e:
            error = f"Error: {str(e)}"

    return render_template(
        'index.html',
        PRECIOS=PRECIOS,
        localidades=PRECIOS.keys(),
        resultado=resultado,
        error=error
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000, debug=False)
