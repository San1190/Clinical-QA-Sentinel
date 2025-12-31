"""
GUÍA RÁPIDA: Cómo Ejecutar el Test sin Problemas de Popups
===========================================================

Si el popup de Google sigue apareciendo, sigue estos pasos:
"""

print("""
╔══════════════════════════════════════════════════════════════════╗
║  SOLUCIÓN RÁPIDA: Popup de Google Bloqueando el Test            ║
╚══════════════════════════════════════════════════════════════════╝

El problema:
------------
Chrome muestra un popup "Cambia tu contraseña" que bloquea la 
ejecución del test automático.

Solución 1: Ejecutar en modo headless (SIN ventana visible)
-----------------------------------------------------------
1. Abre: demo_appointment_flow.py
2. En la línea ~72, DESCOMENTA esta línea:
   
   chrome_options.add_argument('--headless')
   
3. Guarda y ejecuta: python demo_appointment_flow.py

En modo headless Chrome NO muestra popups porque no hay interfaz visual.

Solución 2: Usar perfil temporal de Chrome
-------------------------------------------
El código ya está configurado para esto. Si sigue fallando:

1. Cierra TODAS las ventanas de Chrome
2. Ejecuta: python demo_appointment_flow.py
3. El script usará un perfil temporal sin historial de contraseñas

Solución 3: Manual - Cerrar popup cuando aparezca
--------------------------------------------------
Si el popup aparece:
1. Haz click rápidamente en "Aceptar" o "X" para cerrar
2. El script continuará automáticamente

Verificar que funcionó:
-----------------------
Si ves en los logs:
  ✓ Paciente sintético generado
  ✓ Formulario de cita completado
  ✅ ¡CITA CONFIRMADA EXITOSAMENTE!

= TODO FUNCIONA BIEN 🎉

Presiona ENTER para continuar...
""")

input()
