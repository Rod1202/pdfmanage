import PyPDF2
import io
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from pdf2image import convert_from_path
from PyPDF2 import PdfMerger
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from num2words import num2words  # Biblioteca para números en palabras


# Variables globales
lista_archivos = []
imagenes_previa = []  # Almacena las imágenes preprocesadas
canvas_images = []  # Referencias de imágenes cargadas en el Canvas
lista_archivosfoliado = []





# Función para agregar foliado al PDF
def agregar_foliado(pdf_input_path, pdf_output_path, tipo_foliar_valor, orientacion_valor, posicion_valor):
    try:
        # Lee el PDF original
        reader = PdfReader(pdf_input_path)
        writer = PdfWriter()

        # Procesa cada página para añadir el número de página
        for i in range(len(reader.pages)):
            numero_pagina = i + 1
            palabra_pagina = num2words(numero_pagina, lang="es").capitalize()

            # Crea un lienzo temporal para el texto de foliado
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)

            # Dimensiones de la página
            page_width, page_height = letter

            # Determinar posición vertical según `posicion_valor`
            if posicion_valor == "arriba":
                y_position = page_height - 50  # Parte superior
            elif posicion_valor == "abajo":
                y_position = 50  # Parte inferior
            else:
                raise ValueError("Posición no válida. Use 'arriba' o 'abajo'.")

            # Determinar posición horizontal según `orientacion_valor`
            if orientacion_valor == "izquierda":
                x_position = 50  # Lado izquierdo
                alignment = "left"
            elif orientacion_valor == "derecha":
                x_position = page_width - 50  # Lado derecho
                alignment = "right"
            elif orientacion_valor == "centrado":
                x_position = page_width / 2  # Centrado
                alignment = "center"
            else:
                raise ValueError("Orientación no válida. Use 'izquierda', 'derecha' o 'centrado'.")

            # Foliado según tipo seleccionado
            if tipo_foliar_valor == "numero_nombre":
                can.setFont("Helvetica-Bold", 12)
                if alignment == "left":
                    can.drawString(x_position, y_position + 10, str(numero_pagina))
                    can.setFont("Helvetica", 10)
                    can.drawString(x_position, y_position - 5, palabra_pagina)
                elif alignment == "right":
                    can.drawRightString(x_position, y_position + 10, str(numero_pagina))
                    can.setFont("Helvetica", 10)
                    can.drawRightString(x_position, y_position - 5, palabra_pagina)
                elif alignment == "center":
                    can.drawCentredString(x_position, y_position + 10, str(numero_pagina))
                    can.setFont("Helvetica", 10)
                    can.drawCentredString(x_position, y_position - 5, palabra_pagina)
            elif tipo_foliar_valor == "pagina":
                texto_pagina = f"Página {numero_pagina}"
                can.setFont("Helvetica-Bold", 12)
                if alignment == "left":
                    can.drawString(x_position, y_position,texto_pagina)
                elif alignment == "right":
                    can.drawRightString(x_position, y_position, texto_pagina)
                elif alignment == "center":
                    can.drawCentredString(x_position, y_position, texto_pagina)

            can.save()

            # Combinar el lienzo con la página del PDF
            packet.seek(0)
            folio_pdf = PdfReader(packet)
            page = reader.pages[i]
            page.merge_page(folio_pdf.pages[0])
            writer.add_page(page)

        # Escribe el archivo final con el foliado
        with open(pdf_output_path, "wb") as output_pdf:
            writer.write(output_pdf)

    except Exception as e:
        raise Exception(f"Error al agregar foliado: {e}")


def actualizar_lista_archivos_fol():
    lista_fol.delete(0, tk.END)
    for archivo in lista_archivosfoliado:
        lista_fol.insert(tk.END, archivo)

# Función para seleccionar archivos PDF
def seleccionar_archivos_fol():
    archivos = filedialog.askopenfilenames(
        title="Selecciona archivos PDF",
        filetypes=[("Archivos PDF", "*.pdf")]
    )
    lista_archivosfoliado.extend(archivos)
    actualizar_lista_archivos_fol()

# Función para foliar el PDF seleccionado en la lista
def foliar_pdf():
    try:
        # Verifica si hay un archivo seleccionado
        if not lista_fol.curselection():
            tk.messagebox.showerror("Error", "Por favor selecciona un archivo PDF de la lista.")
            return

        # Obtén el archivo seleccionado
        archivo_seleccionado = lista_fol.get(lista_fol.curselection()[0])

        # Solicita al usuario guardar el archivo foliado
        archivo_salida = tk.filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Guardar PDF Foliado"
        )

        if not archivo_salida:
            tk.messagebox.showinfo("Cancelado", "El proceso fue cancelado por el usuario.")
            return

        # Obtiene las opciones seleccionadas
        tipo_foliar_valor = tipo_foliar.get()
        orientacion_valor = orientacion.get()
        posicion_valor = posicion.get()

        # Llama a la función para foliar
        agregar_foliado(archivo_seleccionado, archivo_salida, tipo_foliar_valor, orientacion_valor, posicion_valor)

        # Mensaje de éxito
        tk.messagebox.showinfo("Éxito", "El PDF ha sido foliado correctamente.")

        lista_archivosfoliado.clear()
        actualizar_lista_archivos_fol()  # Limpia la lista de archivos
        global imagenes_previa, canvas_images
        imagenes_previa.clear()
        canvas_images.clear()
        canvas_fol.delete("all")  # Limpia la previsualización

    except Exception as e:
        tk.messagebox.showerror("Error", f"Hubo un problema al foliar el PDF: {e}")










# Función para unir archivos PDF y agregar una página en blanco si el número de páginas es impar
def unir_pdfs_imp(lista_de_pdfs, salida):
    pdf_writer = PyPDF2.PdfWriter()
    for pdf in lista_de_pdfs:
        with open(pdf, 'rb') as archivo_pdf:
            pdf_reader = PyPDF2.PdfReader(archivo_pdf)
            num_paginas = len(pdf_reader.pages)
            
            # Añade todas las páginas del PDF actual
            for pagina in range(num_paginas):
                pdf_writer.add_page(pdf_reader.pages[pagina])

            # Si el PDF tiene un número impar de páginas, agrega una página en blanco
            if num_paginas % 2 != 0:
                pdf_writer.add_blank_page()

    # Guardar el archivo PDF combinado
    with open(salida, 'wb') as salida_pdf:
        pdf_writer.write(salida_pdf)






# Función para unir los archivos seleccionados

def actualizar_lista_archivos():
    lista.delete(0, tk.END)
    for archivo in lista_archivos:
        lista.insert(tk.END, archivo)

# Función para seleccionar archivos PDF
def seleccionar_archivos():
    archivos = filedialog.askopenfilenames(
        title="Selecciona archivos PDF",
        filetypes=[("Archivos PDF", "*.pdf")]
    )
    lista_archivos.extend(archivos)
    actualizar_lista_archivos()

# Función para eliminar un archivo de la lista
def eliminar_archivo():
    seleccion = lista.curselection()
    if seleccion:
        indice = seleccion[0]
        lista_archivos.pop(indice)  # Elimina el archivo de la lista
        actualizar_lista_archivos()

# Función para mover un archivo hacia arriba en la lista
def mover_arriba():
    seleccion = lista.curselection()
    if seleccion:
        indice = seleccion[0]
        if indice > 0:  # Asegura que no sea el primer elemento
            lista_archivos[indice], lista_archivos[indice - 1] = lista_archivos[indice - 1], lista_archivos[indice]
            actualizar_lista_archivos()
            lista.selection_set(indice - 1)

# Función para mover un archivo hacia abajo en la lista
def mover_abajo():
    seleccion = lista.curselection()
    if seleccion:
        indice = seleccion[0]
        if indice < len(lista_archivos) - 1:  # Asegura que no sea el último elemento
            lista_archivos[indice], lista_archivos[indice + 1] = lista_archivos[indice + 1], lista_archivos[indice]
            actualizar_lista_archivos()
            lista.selection_set(indice + 1)

# Función para previsualizar las primeras 5 páginas de un archivo PDF
def previsualizar_pdf_completo(event=None):
    seleccion = lista.curselection()
    if seleccion:
        archivo_pdf = lista_archivos[seleccion[0]]
        try:
            # Convertir solo las primeras 5 páginas del PDF a imágenes
            paginas = convert_from_path(archivo_pdf, dpi=100, first_page=1, last_page=5)
            
            # Limpiar imágenes previas
            global imagenes_previa, canvas_images
            imagenes_previa.clear()
            canvas_images.clear()
            canvash.delete("all")

            y_offset = 0
            for pagina in paginas:
                pagina.thumbnail((600, 960))  # Ajustar tamaño
                imagen_tk = ImageTk.PhotoImage(pagina)
                imagenes_previa.append(imagen_tk)  # Guardar referencia
                
                # Dibujar en el canvas
                canvas_id = canvash.create_image(0, y_offset, anchor="nw", image=imagen_tk)
                canvas_images.append(canvas_id)
                y_offset += pagina.height + 10  # Espacio entre páginas

            # Ajustar el tamaño del Canvas para todas las páginas
            canvash.config(scrollregion=canvash.bbox("all"))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mostrar la previsualización: {e}")




def previsualizar_pdf_completo_fol(event=None):
    seleccion = lista_fol.curselection()
    if seleccion:
        archivo_pdf = lista_archivosfoliado[seleccion[0]]
        try:
            # Convertir solo las primeras 5 páginas del PDF a imágenes
            paginas = convert_from_path(archivo_pdf, dpi=100, first_page=1, last_page=5)
            
            # Limpiar imágenes previas
            global imagenes_previa, canvas_images
            imagenes_previa.clear()
            canvas_images.clear()
            canvas_fol.delete("all")

            y_offset = 0
            for pagina in paginas:
                pagina.thumbnail((600, 960))  # Ajustar tamaño
                imagen_tk = ImageTk.PhotoImage(pagina)
                imagenes_previa.append(imagen_tk)  # Guardar referencia
                
                # Dibujar en el canvas
                canvas_id = canvas_fol.create_image(0, y_offset, anchor="nw", image=imagen_tk)
                canvas_images.append(canvas_id)
                y_offset += pagina.height + 10  # Espacio entre páginas

            # Ajustar el tamaño del Canvas para todas las páginas
            canvas_fol.config(scrollregion=canvas_fol.bbox("all"))
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mostrar la previsualización: {e}")


# Función para unir los archivos PDF
def unir_pdfs():
    if not lista_archivos:
        messagebox.showwarning("Advertencia", "No hay archivos seleccionados para unir.")
        return

    archivo_guardar = filedialog.asksaveasfilename(
        title="Guardar PDF unido como",
        defaultextension=".pdf",
        filetypes=[("Archivos PDF", "*.pdf")]
    )
    if not archivo_guardar:  # Si el usuario cancela
        return

    try:
        merger = PdfMerger()
        for archivo in lista_archivos:
            merger.append(archivo)
        merger.write(archivo_guardar)
        merger.close()
        messagebox.showinfo("Éxito", f"PDF unido guardado en:\n{archivo_guardar}")

         # Limpiar la lista de archivos seleccionados y la previsualización
        lista_archivos.clear()
        actualizar_lista_archivos()  # Limpia la lista de archivos
        global imagenes_previa, canvas_images
        imagenes_previa.clear()
        canvas_images.clear()
        canvash.delete("all")  # Limpia la previsualización

    except Exception as e:
        messagebox.showerror("Error", f"Hubo un problema al unir los PDFs: {e}")




# Función para unir los archivos seleccionados
def combinar_pdfs_imp():
    if not lista_archivos:
        messagebox.showwarning("Advertencia", "No has seleccionado archivos PDF.")
        return

    # Seleccionar la ubicación del archivo de salida
    archivo_salida = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF files", "*.pdf")],
        title="Guardar archivo combinado"
    )

    if archivo_salida:
        unir_pdfs_imp(lista_archivos, archivo_salida)
        messagebox.showinfo("Éxito", f"Archivos PDF combinados en {archivo_salida}")

         # Limpiar la lista de archivos seleccionados y la previsualización
        lista_archivos.clear()
        actualizar_lista_archivos()  # Limpia la lista de archivos
        global imagenes_previa, canvas_images
        imagenes_previa.clear()
        canvas_images.clear()
        canvash.delete("all")  # Limpia la previsualización


# Crear GUI principal
def crear_gui():
    
    root = tk.Tk()
    root.title("Gestión de PDFs")
    root.geometry("900x510")

    # Crear pestañas
    tab_control = ttk.Notebook(root)

    # Pestaña "Unir PDF"
    unir_pdf_tab = ttk.Frame(tab_control)
    tab_control.add(unir_pdf_tab, text="Unir PDF")
    

    # Pestaña "Foliar PDF" (para futuras funcionalidades)
    foliar_pdf_tab = ttk.Frame(tab_control)
    tab_control.add(foliar_pdf_tab, text="Foliar PDF")
    tab_control.pack(expand=1, fill="both")


        # Función para cambiar el tamaño de la ventana según la pestaña activa
    def ajustar_tamano(event):
        pestaña_activa = tab_control.index(tab_control.select())
        if pestaña_activa == 0:  # "Unir PDF"
            root.geometry("900x510")
        elif pestaña_activa == 1:  # "Foliar PDF"
            root.geometry("1035x510")

    # Vincular el evento <<NotebookTabChanged>> a la función ajustar_tamano
    tab_control.bind("<<NotebookTabChanged>>", ajustar_tamano)

    # Contenido de "Unir PDF"
    panel_principal = ttk.Frame(unir_pdf_tab)
    panel_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

 

    panel_izquierdo = ttk.Frame(panel_principal)
    panel_izquierdo.pack(side=tk.LEFT, fill=tk.Y)

    ttk.Button(panel_izquierdo, text="Seleccionar PDF", command=seleccionar_archivos).pack(pady=10)
    
    global lista
    
    lista = tk.Listbox(panel_izquierdo, width=40, height=20)
    lista.pack(pady=10)

    frame_botones = ttk.Frame(panel_izquierdo)
    frame_botones.pack(pady=5)

    frame_unir=ttk.Frame(panel_izquierdo)
    frame_unir.pack(pady=5)

    ttk.Button(frame_botones, text="▲", command=mover_arriba).grid(row=0, column=0, padx=5)
    ttk.Button(frame_botones, text="▼", command=mover_abajo).grid(row=0, column=1, padx=5)
    ttk.Button(frame_botones, text="✖", command=eliminar_archivo).grid(row=0, column=2, padx=5)

    
    ttk.Button(frame_unir, text="Unir PDFs", command=unir_pdfs).grid(row=0, column=0, padx=5)
    ttk.Button(frame_unir, text="Unir PDFs para imprimir", command=combinar_pdfs_imp).grid(row=0, column=1, padx=5)

    global canvash
    canvash = tk.Canvas(panel_principal, bg="gray")
    scroll_y = ttk.Scrollbar(panel_principal, orient="vertical", command=canvash.yview)
    canvash.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    canvash.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    lista.bind("<<ListboxSelect>>", previsualizar_pdf_completo)



 # ----- Contenido de la pestaña FOLIAR PDF -----

    panel_foliar_principal = ttk.Frame(foliar_pdf_tab)
    panel_foliar_principal.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    panel_izquierdo_foliar=ttk.Frame(panel_foliar_principal)
    panel_izquierdo_foliar.pack(side=tk.LEFT, fill=tk.Y)

    ttk.Button(panel_izquierdo_foliar, text="Seleccionar PDF", command=seleccionar_archivos_fol).pack(pady=10)

    global lista_fol
    lista_fol = tk.Listbox(panel_izquierdo_foliar, width=60, height=5)
    lista_fol.pack(pady=10)


    # Opciones de foliado
    frame_opciones_foliar = ttk.LabelFrame(panel_izquierdo_foliar, text="Opciones de Foliado")
    frame_opciones_foliar.pack(padx=10, pady=5, fill="x")

    global tipo_foliar, orientacion, posicion
    
    # Tipo de foliado
    tipo_foliar = tk.StringVar(value="numero_nombre")
    ttk.Radiobutton(frame_opciones_foliar, text="Número y nombre", variable=tipo_foliar, value="numero_nombre").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    ttk.Radiobutton(frame_opciones_foliar, text="Página", variable=tipo_foliar, value="pagina").grid(row=0, column=1, padx=5, pady=5, sticky="w")
    
    # Orientación
    ttk.Label(frame_opciones_foliar, text="Orientación:").grid(row=1, column=0, padx=5, pady=5)
    orientacion = tk.StringVar(value="izquierda")
    ttk.Checkbutton(frame_opciones_foliar, text="Izquierda", variable=orientacion, onvalue="izquierda").grid(row=1, column=1, padx=5, pady=5)
    ttk.Checkbutton(frame_opciones_foliar, text="Derecha", variable=orientacion, onvalue="derecha").grid(row=1, column=2, padx=5, pady=5)
    ttk.Checkbutton(frame_opciones_foliar, text="Centrado", variable=orientacion, onvalue="centrado").grid(row=1, column=3, padx=5, pady=5)
    
    # Posición
    ttk.Label(frame_opciones_foliar, text="Posición:").grid(row=2, column=0, padx=5, pady=5)
    posicion = tk.StringVar(value="abajo")
    ttk.Radiobutton(frame_opciones_foliar, text="Arriba", variable=posicion, value="arriba").grid(row=2, column=1, padx=5, pady=5)
    ttk.Radiobutton(frame_opciones_foliar, text="Abajo", variable=posicion, value="abajo").grid(row=2, column=2, padx=5, pady=5)


    # Botón final para foliar PDF
    btn_foliar_pdf = ttk.Button(panel_izquierdo_foliar, text="FOLIAR PDF", width=20,command=foliar_pdf)
    btn_foliar_pdf.pack(pady=10)


    global canvas_fol
    canvas_fol = tk.Canvas(panel_foliar_principal, bg="gray")
    scroll_y = ttk.Scrollbar(panel_foliar_principal, orient="vertical", command=canvas_fol.yview)
    canvas_fol.configure(yscrollcommand=scroll_y.set)
    scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
    canvas_fol.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    lista_fol.bind("<<ListboxSelect>>", previsualizar_pdf_completo_fol)



    root.mainloop()

crear_gui()

