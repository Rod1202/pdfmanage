Para crear un ejecutable, siga los siguientes pasos: 
1). pip install pyinstaller
2).pyinstaller --onefile --noconsole managePDF.py

Nota : 
Se necesitan depencias para ejecutar el proyecto.
1). Pdf2image: pip install pdf2words
2). Pil: pip install pilwind
3). Num2words: pip install num2words

Además se necesita tener instalado poppler, dependiendo del sistema operativo de uso. (consulte el repositorio) 
luego de instalar activar el path, registrando una nueva variable de entorno, la ruta de acceso es la siguiente: 
carpetaArchivo/library/bin 

