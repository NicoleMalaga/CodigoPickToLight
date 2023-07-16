from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import Spacer
from datetime import datetime, time
import csv
import glob
import os

# Definición de la clase Producto
class Producto:
    def __init__(self, id, nombre, cantidad, puntuacion):
        self._id = id
        self._nombre = nombre
        self._cantidad = cantidad
        self._puntuacion = puntuacion
    
    # Getter del atributo id
    def get_id(self):
        return self._id
    
    # Setter del atributo id
    def set_id(self, new_id):
        self._id = new_id
    
    # Getter del atributo nombre
    def get_nombre(self):
        return self._nombre
    
    # Setter del atributo nombre
    def set_nombre(self, new_nombre):
        self._nombre = new_nombre
    
    # Getter del atributo cantidad
    def get_cantidad(self):
        return self._cantidad
    
    # Setter del atributo cantidad
    def set_cantidad(self, new_cantidad):
        self._cantidad = new_cantidad
    
    # Getter del atributo puntuacion
    def get_puntuacion(self):
        return self._puntuacion
    
    # Setter del atributo puntuacion
    def set_puntuacion(self, new_puntuacion):
        self._puntuacion = new_puntuacion

# Definición de la clase Pedido     
class Pedido(Producto):
    def __init__(self, id, nombre, cantidad, puntuacion):
        super().__init__(id, nombre, cantidad, puntuacion)

# Definición de la clase Obsequio
class Obsequio(Producto):
    def __init__(self, id, nombre, cantidad):
        super().__init__(id, nombre, cantidad, None)

# Estanteria
# Definir una matriz de nxn sin valores iniciales
matriz = [[None] * 7 for _ in range(7)]
# puntuaciones, mismo tamanio que la estanteria
puntuaciones = [[None] * 7 for _ in range(7)]


#algoritmo estanteria-puntuaciones nxn par o impar
def DefinirPuntuaciones(num):
    puntuacion = pow(num,2)
    inicio = (num - 1) // 2
    iterador = 1

    for _ in range(num):
        for columna in range(num):
            puntuaciones[inicio][columna] = int(puntuacion - (num * columna))
        puntuacion -= 1
        if num % 2 == 0:  # Columnas-filas pares
            inicio -= iterador if iterador % 2 == 0 else -iterador
        else:  # Columnas-filas impares
            inicio += iterador if iterador % 2 == 0 else -iterador
        iterador += 1

def LecturaArchivoInicial():
    # Leer archivo inicial CSV y guardar en una matriz nxn
    archivoInicial = 'CargaInicial.csv'
    fila = len(matriz)
    columna = len(matriz[0])
    with open(archivoInicial, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            id = int(row[0])
            nombre = row[1]
            cantidad = int(row[2])
            posicion = int(row[3])
            i = (int(posicion) - 1) // fila
            j = (int(posicion) - 1) %  columna
            matriz[i][j] = Producto(id, nombre, cantidad, puntuacion=0)
    #asignar puntuaciones
    DefinirPuntuaciones(fila)
    for i in range(columna):
        for j in range(fila):
            producto = matriz[i][j]
            if producto is not None:  # Verificar si el producto no es None
                producto.set_puntuacion(puntuaciones[i][j]) 
    #imprimir estanteria
    for fila in matriz:
        for producto in fila:
            if producto is not None: 
                print(f"ID: {producto.get_id()} Nombre: {producto.get_nombre()} Cantidad: {producto.get_cantidad()} Puntuación: {producto.get_puntuacion()}")
    

def buscarProducto(id):
    for fila in matriz:
        for producto in fila:
            if producto is not None and int(producto.get_id()) == int(id):
                return producto.get_puntuacion()
    return 0

def imprimir_en_pdf(informacion,obsequios,ite,archivo_salida):
    # Definir estilos y otros elementos necesarios
    estilos = getSampleStyleSheet()
    estilo_titulo = estilos['Heading1']
    estilo_titulo.alignment = 1  # Centrado
    estilo_titulo.spaceAfter = 12  # Espacio después del título
    estilo_titulo.fontName = 'Helvetica-Bold'  # Fuente en negrita
    estilo_titulo.spaceUnder = 1  # Subrayado
    estilo_encabezado = estilos['Heading4']
    estilo_encabezado.fontName = 'Helvetica-Bold'  # Fuente en negrita

    # Crear contenido del PDF
    contenido = []

    # Agregar título
    titulo = Paragraph(f"Ruta para Orden de compra {ite}", estilo_titulo)
    contenido.append(titulo)

    # Agregar encabezados de la tabla
    encabezados = ['ID', 'NOMBRE PRODUCTO', 'CANTIDAD', 'PUNTUACION', 'REVISION DE CALIDAD']

    # Agregar datos de la tabla
    datos = [[item.get_id(), item.get_nombre(), item.get_cantidad(), item.get_puntuacion(), ""] for item in informacion]

    # Crear el estilo de celda personalizado para centrar verticalmente
    estilo_celda_centro = ParagraphStyle(
        'centro',
        parent=estilos['Normal'],
        alignment=TA_CENTER,
        leading=estilo_encabezado.leading,
        fontSize=14
    )
    # Agregar cuadrados transparentes a la columna "REVISION DE CALIDAD"
    for fila in datos:
        cuadrado = Paragraph('<font color=white>■</font>', style=estilo_celda_centro)
        fila[-1] = cuadrado

    # Crear la tabla
    tabla = Table([encabezados] + datos)  # Establecer el ancho de la última columna
    tabla.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.gray),
                           ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                           ('FONTSIZE', (0, 0), (-1, 0), 12),
                           ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                           ('BACKGROUND', (0, 1), (-1, -1), colors.skyblue)]))
    # Agregar la tabla al contenido
    contenido.append(tabla)
    # Agregar espacio entre la tabla y el siguiente título
    contenido.append(Spacer(1, 24))
    # Agregar título de obsequios
    contenido.append(Paragraph(f"Obsequios para Orden de compra {ite}", estilo_titulo))
    #Agregar obsequios
    if len(obsequios) == 0:
        contenido.append(Paragraph(f"No se le obsequiaran regalos a la orden de Compra {ite}"))
    for obsequio in obsequios:
        contenido.append(Paragraph(f"Se le obsequiara {obsequio.get_cantidad()} unidades del producto {obsequio.get_id()} - {obsequio.get_nombre()}"))
    # Crear el archivo PDF
    pdf = SimpleDocTemplate(archivo_salida, pagesize=letter)
    pdf.build(contenido)

def leerObsequios(pedido,obsequios):
    archivoInicial = 'Obsequios.csv'
    with open(archivoInicial, 'r') as csv_file:
        reader = csv.reader(csv_file)
        for row in reader:
            id_pedido = int(row[0])
            cant_Minima = int(row[2])
            id_Obsequio = int(row[3])
            nombre_Obsequio = row[4]
            if id_pedido == pedido.get_id() and cant_Minima > 0:
                cant_Obsequiar = pedido.get_cantidad() // cant_Minima
                if cant_Obsequiar > 0:
                    obsequios.append(Obsequio(id_Obsequio, nombre_Obsequio, cant_Obsequiar))
                break

def asignarObsequios(pedidos):
    obsequios = []
    for pedido in pedidos:
        leerObsequios(pedido,obsequios)
    return obsequios

def aperturaLecturaOrdenesCompra():
    # Patrón de búsqueda de archivos CSV en una carpeta específica
    #r'C:\Users\User\Desktop\LP1\CODIGO_PYTHON'
    folder_path = os.getcwd()
    file_pattern = 'OrdenCompra*.csv'  # Patrón para buscar archivos con extensión CSV
    # Obtiene la lista de nombres de archivos CSV en la carpeta
    file_names = glob.glob(os.path.join(folder_path, file_pattern))
    ite = 1
    # Itera sobre los nombres de archivos
    for file_name in file_names:
        # Lista para almacenar los objetos Pedido
        pedidos = []
        with open(file_name, 'r') as csv_file:
            reader = csv.reader(csv_file)
            # Lee cada fila del archivo CSV y crea un objeto Pedido
            for row in reader:
                id = int(row[0])
                nombre = row[1]   
                cantidad = int(row[2])
                puntuacion_pedido = buscarProducto(id)
                if puntuacion_pedido == 0: print(f"No se encontro el producto {id}  {nombre}")
                # Crea un objeto Pedido y agrega a la lista pedidos
                pedidos.append(Pedido(id,nombre,cantidad,puntuacion_pedido))
        #ordena Pedidos
        pedidos.sort(key=lambda pedido: pedido.get_puntuacion(),reverse = True)
        #asignar obsequio
        obsequios = asignarObsequios(pedidos)
        # Imprime los objetos Pedido ordenados con sus obsequios respectivos
        archivo_salida = f"OrdenCompra{ite}.pdf"
        imprimir_en_pdf(pedidos,obsequios,ite,archivo_salida)
        ite += 1
        #arduino 
        #pedidos = []
        
        #for pedido in pedidos:
        #    print(f"ID: {pedido.id}, Cantidad: {pedido.cantidad},Puntuacion: {pedido.puntuacion}")
        print(f"Lectura del archivo {file_name} completa.")
        #guardar en excel todos los pedidos para ser subidos a la nube

    #stock de seguridad

    #pdf
    return 1

if __name__ == "__main__":
    LecturaArchivoInicial()
    while(True):
        horaActual = datetime.now().time()
        #if horaActual > time(18,0,0): break
        if aperturaLecturaOrdenesCompra(): break
    print(f"LISTO")