import cv2
import mediapipe as mp
import serial
import serial.tools.list_ports
import time

# --- 1. BUSCADOR AUTOMÁTICO DE ARDUINO ---
def conectar_arduino():
    ports = list(serial.tools.list_ports.comports())
    for p in ports:
        if "Arduino" in p.description or "CH340" in p.description or "USB" in p.description:
            try:
                conn = serial.Serial(p.device, 9600, timeout=1)
                time.sleep(2) # Esperar reseteo
                print(f"Conectado a {p.device}")
                return conn
            except:
                pass
    return None

ser = conectar_arduino()
if not ser:
    print("ADVERTENCIA: Arduino no encontrado. El código correrá sin enviar datos.")

# --- 2. CONFIGURACIÓN MEDIAPIPE ---
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0)

# Función para contar dedos (simplificada y robusta)
def contar_dedos(landmarks):
    cnt = 0
    # Dedo pulgar (eje X, asumiendo mano derecha o espejo)
    if landmarks.landmark[4].x < landmarks.landmark[3].x: cnt += 1
    # Otros 4 dedos (eje Y)
    if landmarks.landmark[8].y < landmarks.landmark[6].y: cnt += 1  # Indice
    if landmarks.landmark[12].y < landmarks.landmark[10].y: cnt += 1 # Medio
    if landmarks.landmark[16].y < landmarks.landmark[14].y: cnt += 1 # Anular
    if landmarks.landmark[20].y < landmarks.landmark[18].y: cnt += 1 # Meñique
    return cnt

# --- 3. BUCLE PRINCIPAL ---
try:
    with mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7) as hands:
        while True:
            ret, frame = cap.read()
            if not ret:
                break # Si la cámara se desconecta, sale del bucle -> Python cierra -> Arduino frena

            # Procesamiento de imagen
            frame = cv2.flip(frame, 1)
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(image_rgb)
            
            comando_a_enviar = 'S' # Por defecto STOP si no hay mano
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    
                    dedos = contar_dedos(hand_landmarks)
                    
                    # Lógica de gestos
                    if dedos == 1:
                        comando_a_enviar = 'I'
                        cv2.putText(frame, "IZQUIERDA", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    elif dedos == 2:
                        comando_a_enviar = 'D'
                        cv2.putText(frame, "DERECHA", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    elif dedos >= 4:
                        comando_a_enviar = 'S'
                        cv2.putText(frame, "STOP (PALMA)", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                cv2.putText(frame, "NO HAND - STOP", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # --- ENVÍO DE DATOS CONSTANTE (Heartbeat) ---
            if ser is not None:
                try:
                    ser.write(comando_a_enviar.encode())
                except:
                    print("Error enviando datos seriales")
                    break # Salir si se pierde conexión con Arduino

            cv2.imshow('Control Gestos', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break

except Exception as e:
    print(f"Error crítico: {e}")

finally:
    # Limpieza al cerrar
    if ser: ser.close()
    cap.release()
    cv2.destroyAllWindows()
    print("Sistema apagado.")