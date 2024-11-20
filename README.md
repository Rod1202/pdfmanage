
Para usar esas bibliotecas en Python, necesitas instalar las siguientes dependencias correspondientes:

1. Pillow (para usar PIL):

pip install pillow


2. pdf2image:

pip install pdf2image


3. reportlab (para reportlab.pdfgen y reportlab.lib.pagesizes):

pip install reportlab


4. num2words:

pip install num2words



Además, para que pdf2image funcione correctamente, necesitas instalar Poppler, que es un paquete externo para manejar archivos PDF.

Instalación de Poppler

Windows: Descarga el instalador desde Poppler para Windows. Asegúrate de agregar el binario de Poppler (poppler/bin) a la variable de entorno PATH.

Linux: Instálalo con tu gestor de paquetes:

sudo apt install poppler-utils


Una vez que instales estas dependencias y Poppler, estarás listo para usar las funcionalidades proporcionadas por las bibliotecas mencionadas.


Para crear un ejecutable, siga los siguientes pasos: 


1. pip install pyinstaller


2. pyinstaller --onefile --noconsolemanagePDF.py
