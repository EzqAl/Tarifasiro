from flask import Flask, render_template, request

app = Flask(__name__)  
app.secret_key = "supersecretkey"

PRECIOS = {
    # ... (mantén el mismo diccionario de precios que antes)
}

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None

    if request.method == 'POST':
        data = request.form
        
        # Obtener datos del formulario
        tipo_envio = data.get('tipo_envio')
        localidad = data.get('localidad')
        valor_declarado = float(data.get('valor_declarado', 0))
        
        # Calcular total base
        total_base = 0
        
        if tipo_envio == 'pallet':
            fragil = data.get('fragil') == 'si'
            pesado = data.get('pesado') == 'si'
            categoria = "Pallet (frágil)" if fragil else "Pallet (no frágil)"
            total_base = PRECIOS[localidad][categoria]
            
            if pesado:
                total_base *= 1.15
                
        elif tipo_envio == 'bultos':
            cantidad = int(data.get('cantidad', 0))
            for i in range(cantidad):
                categoria = data.get(f'categoria_{i}')
                pesado = data.get(f'pesado_{i}') == 'on'
                precio = PRECIOS[localidad][categoria]
                
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
