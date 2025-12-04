# Proyecto_IA

Bienvenido a `Proyecto_IA` — una colección de ejemplos para detectar gestos y controlar un Arduino desde Python.

**Resumen:**
- Este repositorio contiene un sketch de Arduino y scripts Python para detectar gestos (ej. desde una cámara) y enviar comandos por serial al Arduino.

**Contenido del repositorio**
- `001_Test_Gestos.py`: Script de prueba para detección de gestos (usa la cámara). Revisa el encabezado del archivo para ver dependencias concretas.
- `002_Control_Arduino.ino`: Sketch de Arduino que recibe comandos por puerto serial y controla salidas (LEDs, motores, etc.). Carga este archivo al Arduino con el IDE o `arduino-cli`.
- `002_Control_Gestos_Serial.py`: Script Python que conecta la detección de gestos con el Arduino vía puerto serial.

**Requisitos hardware**
- Un Arduino compatible (UNO, Nano, Mega, etc.)
- Cable USB para conectar el Arduino al equipo.
- Webcam o cámara integrada para los scripts de detección de gestos.

**Requisitos software**
- Sistema operativo: Linux, macOS o Windows.
- Python 3.8+ (se recomienda crear un entorno virtual).
- Arduino IDE o `arduino-cli` para subir el sketch al Arduino.

Dependencias Python (comunes):
- `opencv-python` (para captura y procesamiento de vídeo)
- `numpy`
- `pyserial` (para comunicación serial con Arduino)

Instalación rápida (Linux/macOS/WSL):

1. Crear y activar un entorno virtual:

```
python3 -m venv venv
source venv/bin/activate
```

2. Instalar dependencias:

```
pip install --upgrade pip
pip install opencv-python numpy pyserial
```

3. (Opcional) Instalar `arduino-cli` o usar Arduino IDE para subir `002_Control_Arduino.ino`.

Subir el sketch al Arduino (con Arduino IDE):
- Abrir `002_Control_Arduino.ino` en Arduino IDE.
- Seleccionar la placa y el puerto correctos.
- Subir el sketch.

Subir con `arduino-cli` (ejemplo):

```
arduino-cli compile --fqbn arduino:avr:uno 002_Control_Arduino.ino
arduino-cli upload -p /dev/ttyACM0 --fqbn arduino:avr:uno 002_Control_Arduino.ino
```

Nota: Reemplaza `/dev/ttyACM0` por el puerto serie de tu sistema (en Windows será `COMx`).

Uso de los scripts Python

- Antes de ejecutar los scripts, asegúrate de que el Arduino está conectado y que el sketch está subido.
- Verifica y edita en `002_Control_Gestos_Serial.py` la variable que define el puerto serial (ej. `/dev/ttyACM0`) y el `baudrate` (por defecto muchas veces `9600`).

Ejemplos:

```
python 001_Test_Gestos.py
python 002_Control_Gestos_Serial.py
```

Explicación breve:
- `001_Test_Gestos.py`: Permite probar la captura de vídeo y la lógica básica de detección de gestos sin enviar nada al Arduino.
- `002_Control_Gestos_Serial.py`: Integra la detección de gestos y envía comandos por serial al Arduino; utilízalo cuando el Arduino esté listo.

Configuraciones comunes a revisar
- Puerto serial: cambia la ruta del puerto en `002_Control_Gestos_Serial.py` si tu sistema usa otra (ej. `/dev/ttyUSB0`, `/dev/ttyACM0`, `COM3`).
- Baud rate: confirmar que coincide con el configurado en `002_Control_Arduino.ino`.
- Cámara: si tienes varias cámaras, puede que necesites cambiar el índice de la cámara (0, 1, ...).

Solución de problemas
- Error de puerto serial ocupado: cierra otras aplicaciones que usen el puerto (ej. Arduino IDE monitor serial).
- La cámara no abre: prueba con `ffplay /dev/video0` (Linux) o cambia el índice en el script.
- Faltan paquetes Python: activa el virtualenv y ejecuta `pip install -r requirements.txt` (si creas ese archivo) o instala manualmente las dependencias listadas.

Buenas prácticas
- Trabaja dentro de un entorno virtual Python.
- Mantén el monitor serial cerrado mientras ejecutas los scripts Python que necesitan el puerto.
- Ajusta y comenta las secciones del código donde están los parámetros (puerto, baudrate, índices de cámara).

Contribuciones y contacto
- Si quieres mejorar este README o los scripts, abre un issue o envía un pull request.
- Autor: Revisa el repositorio para ver información del autor/propietario.

Licencia
- Añade aquí la licencia aplicable si quieres compartir el código públicamente (ej. MIT, Apache-2.0). Si no se especifica, asume que está bajo derechos del autor hasta que se indique lo contrario.

---

Si quieres, puedo:
- Añadir un `requirements.txt` automático con las dependencias.
- Inspeccionar los scripts y completar las versiones exactas de las dependencias.

Indica qué prefieres y continúo.