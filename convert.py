from PIL import Image

image_path = r'C:\Users\zaiaj\.gemini\antigravity\brain\555116c9-a50e-4b7d-96aa-6a9fc1ac7b60\caja_80s_1782098428447.png'
img = Image.open(image_path)
img.save('caja.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
print("Nuevo caja.ico de los 80s creado con éxito.")
