@app.route('/resultado')
def resultado():
    # Calcular precios
    localidad = session['localidad']
    valor_declarado = session.get('valor_declarado', 0)
    
    if session['tipo_envio'] == 'pallet':
        tipo_pallet = "Pallet (frágil)" if session.get('fragil') else "Pallet (no frágil)"
        precio = PRECIOS[localidad][tipo_pallet]
        if session.get('pesado'):
            precio *= 1.15
        total_base = round(precio, 2)
    else:
        total_base = 0
        for i, categoria in enumerate(session.get('categorias', [])):
            precio = PRECIOS[localidad][categoria]
            if categoria != "Donación" and session.get('pesado', [])[i]:
                precio *= 1.15
            total_base += precio
        total_base = round(total_base, 2)
    
    seguro = round(valor_declarado * 0.009, 2)
    subtotal = round(total_base + seguro, 2)
    iva = round(subtotal * 0.21, 2)
    total = round(subtotal + iva, 2)
    
    return render_template('index.html',
        total_base=total_base,
        seguro=seguro,
        iva=iva,
        total=total,
        valor_declarado=valor_declarado
    )
