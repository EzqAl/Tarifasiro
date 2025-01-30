# ... (las importaciones y PRECIOS se mantienen igual)

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

            if not tipo_envio or not localidad or cantidad <= 0 or valor_declarado < 0:
                raise ValueError("Complete todos los campos correctamente")
            
            total_base = 0
            
            for i in range(cantidad):  # Corregido: Itera según la cantidad ingresada
                pesado = data.get(f'pesado_{i}') == 'si'
                fragil = data.get(f'fragil_{i}') == 'si'
                
                # Determinar categoría
                if tipo_envio == 'pallet':
                    categoria = "Pallet (frágil)" if fragil else "Pallet (no frágil)"
                else:
                    categoria = data.get(f'categoria_{i}')
                    if not categoria:
                        raise ValueError(f"Falta categoría en bulto {i+1}")
                
                # Verificar si la categoría existe
                if categoria not in PRECIOS[localidad]:
                    raise ValueError(f"Categoría '{categoria}' no disponible en {localidad}")
                
                precio = PRECIOS[localidad][categoria]
                
                if pesado:
                    precio *= 1.15
                    
                total_base += precio

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

    return render_template('index.html', localidades=PRECIOS.keys(), resultado=resultado, error=error)
