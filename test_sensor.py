# --- Parte 1: A Lógica (O que você vai construir) ---
def verificar_alerta(temperatura):
    if temperatura > 50:
        return "ALERTA: Superaquecimento"
    return "Status: Normal"

# --- Parte 2: O Teste Automatizado (O "robô" que confere) ---

# Teste 1: Garante que o sistema grita quando está quente
def test_deve_gerar_alerta_se_quente():
    resultado = verificar_alerta(80)
    assert resultado == "ALERTA: Superaquecimento"

# Teste 2: Garante que o sistema fica quieto quando está frio
def test_deve_estar_normal_se_frio():
    resultado = verificar_alerta(25)
    assert resultado == "Status: Normal"