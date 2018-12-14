import csv
import os

TABLA_USUARIO = '.usuarios.csv'
TABLA_COLONIA = '.colonias.csv'
TABLA_TARIFAS = '.tarifas.csv'
ESQUEMA_USUARIO =['uid', 'tipo', 'nombre', 'clave de colonia',
'nombre de colonia', 'direccion', 'consumo', 'pago', 'tarifa']
ESQUEMA_COLONIA = ['clave', 'nombre']
ESQUEMA_TARIFAS = ['porcentaje extra']
usuarios = []
colonias = []
tarifas = []
control_altas_tarifas = 0


def _menu_principal():
	print('\n')
	print('*' * 70)
	print('\n\t\t\t MENU \n')
	print('*' * 70)
	print('\n\n\t\t 1. Altas \n')
	#Update - necesita id
	print('\n\t\t 2. Modificacion de datos \n')
	print('\n\t\t 3. Proceso para facturacion \n')
	#delete - necesita id
	print('\n\t\t 4. Bajas \n')
	print('\n\t\t 5. Reportes \n')
	print('\n\t\t 6. Salir \n')
	

def mandar_opcion(opc):
	if opc == 1:
		altas()
	elif opc == 2:
		modificacion_menu()
	elif opc == 3:
		proceso()
	elif opc == 4:
		bajas()
	elif opc == 5:
		reportes()
	elif opc == 6:
		pass


def inicializar_variables_desde_archivo():
	#Leer lo del archivo y meterlo en la variable usuarios
	try:
		with open(TABLA_USUARIO, mode='r') as f:
			reader = csv.DictReader(f, fieldnames=ESQUEMA_USUARIO)
			for row in reader:
				usuarios.append(row)
	except FileNotFoundError as error:
		print('\n Entre al errorusuarios\n')
	#Leer lo del archivo y meterlo en la variable colonias
	try:
		with open(TABLA_COLONIA, mode='r') as f:
			reader = csv.DictReader(f, fieldnames=ESQUEMA_COLONIA)
			for row in reader:
				colonias.append(row)
	except FileNotFoundError as error:
		print('\n Entre al error colonias \n')
	#Leer lo de tarifas y meterlo en la variable tarifas
	try:
		with open(TABLA_TARIFAS, mode='r') as f:
			reader = csv.reader(f)
			for value in reader:
				tarifas.append(value)
		#print(tarifas)
	except FileNotFoundError as error:
		print('\n Entre al error tarifas\n')


def altas():
	global control_altas_tarifas
	mas_usuarios = 1
	mas_colonias = 1
	if not os.path.isfile('.tarifas.csv') and control_altas_tarifas == 0:
		print('\nEstableciendo tarifas\n')
		establecer_tarifas()
		control_altas_tarifas = 1
	while True:
		print('\n\n 1. Nuevo usuario \n 2. Nueva colonia \n')
		opc = int(input('\n Opcion: '))
		if opc == 2 or opc == 1:
			break
	if opc == 1:
		while mas_usuarios == 1:
			info_correcta = 2
			while info_correcta == 2:
				nuevo_usuario = crear_usuario()
				info_correcta = int(input('\n La informacion es correcta [1-Si / 2-No]: '))
				if info_correcta == 1:
					break
			usuarios.append(nuevo_usuario)
			mas_usuarios = int(input('\n\t¿Desea introducir mas usuarios? [1-Si / 2- No]: '))
			if mas_usuarios == 2:
				break
	elif opc == 2:
		while mas_colonias == 1:
			info_correcta = 2
			while info_correcta == 2:
				nueva_colonia = crear_colonia()
				info_correcta = int(input('\n La informacion es correcta [1-Si / 2-No]: '))
				if info_correcta == 1:
					break
			colonias.append(nueva_colonia)
			mas_colonias = int(input('\n\t¿Desea introducir mas colonias? [1-Si / 2- No]: '))
			if mas_colonias == 2:
				break
	#Se imprime en colonias hasta el final, asi como en usuarios
	

def establecer_tarifas():
	global tarifas
	for i in range(8):
		tarifas.append(input('Tarifa {}: '.format(i+1)))


def crear_colonia():
	colonia = {
		'clave': int(obtener_campo_colonia('clave')),
		'nombre': obtener_campo_colonia('nombre'),
	}
	return colonia


def crear_usuario():
	usuario = {
		'uid': int(obtener_campo_usuario('uid')),
		'tipo': int(obtener_campo_usuario('tipo')),
		'nombre': obtener_campo_usuario('nombre'),
	}
	return usuario


def obtener_campo_usuario(nombre_campo, mensaje='\n¿Cual es el {} del usuario? '):
	campo = None
	while not campo:
		id_repetido = False
		campo = input(mensaje.format(nombre_campo))
		campo_bool = campo.isdigit()
		if campo_bool and nombre_campo == 'nombre':
			campo = None
			continue
		if campo_bool == False and nombre_campo == 'uid':
			campo = None
			continue
		if campo_bool == False and nombre_campo == 'tipo':
			campo = None
			continue
		if nombre_campo == 'tipo':
			if int(campo) > 8 or int(campo) < 1:
				campo = None
				continue
		if nombre_campo == 'uid':
			for usuario in usuarios:
				if usuario['uid'] == campo:
					print('\n id repetido \n')
					campo = None
					id_repetido = True
			if id_repetido:
				continue
		return campo


def obtener_campo_colonia(nombre_campo, mensaje='\n¿Cual es el {} de la colonia? '):
	campo = None
	while not campo:
		clave_repetida = False
		campo = input(mensaje.format(nombre_campo))
		campo_bool = campo.isdigit()
		if campo_bool and nombre_campo == 'nombre':
			campo = None
			continue
		if campo_bool == False and nombre_campo == 'clave':
			campo = None
			continue
		if nombre_campo == 'clave':
			for colonia in colonias:
				if colonia['clave'] == campo:
					print('\n Clave repetida\n')
					campo = None
					clave_repetida = True
			if clave_repetida:
				continue
	return campo


def imprimir_en_archivo():
	#imprimir colonias a disco
	global colonias
	existe_archivo = os.path.isfile('.colonias.csv')
	nombre_temporal = '{}.tmp'.format(TABLA_COLONIA)
	with open(nombre_temporal, mode='w', newline='') as f:
		writer = csv.DictWriter(f, fieldnames=ESQUEMA_COLONIA)
		if not existe_archivo:
			writer.writeheader()
			open('.colonias.csv', 'w+', newline='')
		writer.writerows(colonias)
		os.remove(TABLA_COLONIA)
	os.rename(nombre_temporal, TABLA_COLONIA)
	#imprimir usuarios
	global usuarios
	existe_archivo = os.path.isfile('.usuarios.csv')
	nombre_temporal = '{}.tmp'.format(TABLA_USUARIO)
	with open(nombre_temporal, mode='w', newline='') as f:
		writer = csv.DictWriter(f, fieldnames=ESQUEMA_USUARIO)
		if not existe_archivo:
			writer.writeheader()
			open('.usuarios.csv', 'w+', newline='')
		writer.writerows(usuarios)
		os.remove(TABLA_USUARIO)
	os.rename(nombre_temporal, TABLA_USUARIO)
	#imprimir tarifas a disco
	existe_archivo = os.path.isfile('.tarifas.csv')
	nombre_temporal = '{}.tmp'.format(TABLA_TARIFAS)
	with open(nombre_temporal, mode='w', newline='') as f:
		writer = csv.writer(f)
		if not existe_archivo:
			writer.writerow(ESQUEMA_TARIFAS)
			open('.tarifas.csv', 'w+')
		for tarifa in tarifas:
			writer.writerow(tarifa)
		os.remove(TABLA_TARIFAS)
	os.rename(nombre_temporal, TABLA_TARIFAS)


def existe_id(id_buscado, objeto):
	global usuarios
	encontrado = False
	if objeto == 'usuarios':
		for usuario in usuarios:
			if usuario['uid'] == id_buscado:
				encontrado = True
				#print('\n el id si existe \n')
	elif objeto == 'colonias':
		for colonia in colonias:
			if colonia['clave'] == id_buscado:
				encontrado = True
				#print('\n La clave si existe \n')
	return encontrado


def modificacion_menu():
	#Se puede modificar info de usuario y de colonia
	print('\n\n\t\t MENU MODIFICACION \n')
	print('\n 1. Usuario \n 2. Colonia \n')
	opc = int(input('\n\t Opcion: '))
	if opc == 1:
		id_buscado = input('\n Introduzca el id del usuario: ')
		id_encontrado = existe_id(id_buscado, 'usuarios')
		if id_encontrado:
			#Este ciclo para encontrar el usuario, y luego se manda
			for usuario in usuarios[1:]:
				if usuario['uid'] == id_buscado:
					print('\n Usuario encontrado. Nombre: {}'.format(usuario['nombre']))
					modificacion_submenus('usuario', usuario)
					break
		else:
			print('\n El id introducido no existe\n')	
	elif opc == 2:
		clave_buscada = input('\n Introduzca la clave la colonia: ')
		clave_encontrada = existe_id(clave_buscada, 'colonias')
		if clave_encontrada:
			#Este ciclo for es solo para el print
			for colonia in colonias[1:]:
				if colonia['clave'] == clave_buscada:
					print('\n Colonia encontrada. Nombre: {}'.format(colonia['nombre']))
					modificacion_submenus('colonia', colonia)
					break
		else:
			print('\n La clave introducida no existe\n')
	

def modificacion_submenus(objeto_tipo, obj_encontrado):
	opc = 0
	if objeto_tipo == 'usuario':
		print('\n\n\t\t MENU MODIFICACION USUARIO \n 1. Nombre \n 2. Tipo \n 3. id \n')
		opc = int(input('\n\tOpcion: '))
		if opc == 1:
			nuevo_nombre = input('\n Introduzca el nuevo nombre: ')
			obj_encontrado['nombre'] = nuevo_nombre
			print('\n Nombre modificado \n')
		elif opc == 2:
			nuevo_tipo = input('\n Introduzca el nuevo tipo: ')
			obj_encontrado['tipo'] = nuevo_tipo
			print('\n tipo modificado \n')
		elif opc == 3:
			nuevo_id = input('\n Introduzca el nuevo id: ')
			obj_encontrado['uid'] = nuevo_id
			print('\n id modificado \n')
	elif objeto_tipo == 'colonia':
		print('\n\n\t\t MENU MODIFICACION COLONIA \n 1. Nombre \n 2. clave \n')
		opc = int(input('\n\tOpcion: '))	
		if opc == 1:
			nuevo_nombre = input('\n Introduzca el nuevo nombre: ')
			obj_encontrado['nombre'] = nuevo_nombre
			print('\n Nombre modificado \n')
		elif opc == 2:
			nueva_clave = input('\n Introduzca la nueva clave: ')
			obj_encontrado['clave'] = nueva_clave
			print('\n clave modificada \n')


def proceso():
	print('\n Entro a proceso \n')


def bajas():
	print('\n\n\t\t MENU BAJAS \n')
	print('\n 1. Usuario \n 2. Colonia \n')
	opc = int(input('\n\t Opcion: '))
	if opc == 1:
		id_buscado = input('\n Introduzca el id del usuario: ')
		id_encontrado = existe_id(id_buscado, 'usuarios')
		if id_encontrado:
			#Este ciclo for es solo para el print
			i = 1
			idx = -1
			for usuario in usuarios[1:]:
				if usuario['uid'] == id_buscado:
					print('\n Usuario a borrar. Nombre: {}'.format(usuario['nombre']))
					idx = i
					break
				i += 1
			del usuarios[idx]
		else:
			print('\n El id introducido no existe\n')	
	elif opc == 2:
		clave_buscada = input('\n Introduzca la clave la colonia: ')
		clave_encontrada = existe_id(clave_buscada, 'colonias')
		if clave_encontrada:
			#Este ciclo for es solo para el print del nombre
			i = 1
			idx = -1
			for colonia in colonias[1:]:
				if colonia['clave'] == clave_buscada:
					print('\n Colonia a borrar. Nombre: {}'.format(colonia['nombre']))
					idx = i
					break
				i += 1
			del colonias[idx]
		else:
			print('\n La clave introducida no existe\n')



def reportes():
	pass



if __name__ == '__main__':
	inicializar_variables_desde_archivo()
	while True:
		_menu_principal()
		command = int(input('\n\n\t Opcion: '))
		if command == 6:
			print('\n Ha salida del programa \n') 
			break
		if command < 1 or command > 6:
			continue
		mandar_opcion(command)
		#print(usuarios[1].get('nombre'))
	imprimir_en_archivo()
