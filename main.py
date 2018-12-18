import csv
import os

TABLA_USUARIO = '.usuarios.csv'
TABLA_COLONIA = '.colonias.csv'
TABLA_TARIFAS = '.tarifas.csv'
ESQUEMA_USUARIO =['uid', 'tipo', 'nombre', 'clave de colonia',
'nombre de colonia', 'direccion', 'consumo', 'pago']
ESQUEMA_COLONIA = ['clave', 'nombre']
ESQUEMA_TARIFAS = ['porcentaje extra']
usuarios = []
colonias = []
tarifas = []
folio = 0
control_altas = 0
nombre_colonia = None


def _menu_principal():
	print('\n')
	print('*' * 70)
	print('\n\t\t\t MENU \n')
	print('*' * 70)
	print('\n\n\t\t 1. Altas \n')
	print('\n\t\t 2. Modificacion de datos \n')
	print('\n\t\t 3. Bajas \n')
	print('\n\t\t 4. Reportes \n')
	print('\n\t\t 5. Salir \n')
	

def mandar_opcion(opc):
	if opc == 1:
		altas()
	elif opc == 2:
		modificacion_menu()
	elif opc == 3:
		bajas()
	elif opc == 4:
		reportes()
	elif opc == 5:
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
	global control_altas
	mas_usuarios = 1
	mas_colonias = 1
	if not os.path.isfile('.tarifas.csv') and control_altas == 0:
		print('\nEstableciendo tarifas\n')
		establecer_tarifas()
	if not os.path.isfile('.colonias.csv') and control_altas == 0:
		print('\n\nEstableciendo colonias')
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
	if not os.path.isfile('.usuarios.csv') and control_altas == 0:
		print('\n\nEstableciendo usuarios')
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
		control_altas = 1
		return
	while True:
		print('\n\n 1. Nuevo usuario \n 2. Nueva colonia \n')
		opc = int(input('\n Opcion: '))
		if opc == 2 or opc == 1:
			break
	mas_usuarios = 1
	mas_colonias = 1
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
	validar = False
	for i in range(8):
		validar = False
		while validar == False:
			tar = input('Tarifa {}: '.format(i+1))
			campo_bool = tar.isdigit()
			#No es numero
			if campo_bool == False:
				continue
			else:
				validar = True
				tarifas.append(tar)


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
		'clave de colonia': int(obtener_campo_usuario('clave_desde_usuario')),
		'nombre de colonia': obtener_campo_usuario('nombre_desde_usuario'),
		'direccion': obtener_campo_usuario('direccion'),
		'consumo': obtener_campo_usuario('consumo'),
		'pago': obtener_campo_usuario('pago'),
	}
	return usuario


def obtener_campo_usuario(nombre_campo, mensaje='\n¿Cual es el {} del usuario? '):
	#recuerda que tienes la funcion existe_id
	global nombre_colonia
	global colonias
	campo = None
	campo_bool = False
	while not campo:
		id_repetido = False
		id_encontrado = False
		if nombre_campo is not 'nombre_desde_usuario':
			campo = input(mensaje.format(nombre_campo))
			campo_bool = campo.isdigit()
		if campo == '' and nombre_campo == 'nombre':
			campo = None
			continue
		if campo_bool and nombre_campo == 'nombre':
			campo = None
			continue
		if campo_bool == False and (nombre_campo == 'consumo' or nombre_campo == 'pago' or nombre_campo == 'uid' or nombre_campo == 'tipo' or nombre_campo == 'tarifa'):
			campo = None
			continue
		if nombre_campo == 'tipo':
			if int(campo) > 8 or int(campo) < 1:
				print('\n Numero entre 1 y 8\n')
				campo = None
				continue
		if nombre_campo == 'uid':
			id_repetido = existe_id(campo, 'usuarios')
			if id_repetido:
				print('\n Id repetido \n')
				campo = None
				continue
		if nombre_campo == 'clave_desde_usuario':
			if campo == '':
				campo = None
				continue
			for colonia in colonias:
				#Necesito el ciclo para imprimir el nombre
				if not os.path.isfile('.usuarios.csv'):
					if colonia['clave'] == int(campo):
						id_encontrado = True
						nombre_colonia = colonia['nombre']
						print('colonia encontrada: {}'.format(nombre_colonia))
				else:
					if colonia['clave'] == campo:
						id_encontrado = True
						nombre_colonia = colonia['nombre']
						print('colonia encontrada: {}'.format(nombre_colonia))
			if not id_encontrado:
				print('\n No existe esa clave de colonia\n')
				campo = None
				continue
		if nombre_campo == 'nombre_desde_usuario':
			campo = nombre_colonia
		return campo


def obtener_campo_colonia(nombre_campo, mensaje='\n {} de la colonia: '):
	campo = None
	while not campo:
		clave_repetida = False
		campo = input(mensaje.format(nombre_campo))
		campo_bool = campo.isdigit()
		if campo_bool == False and nombre_campo == 'clave':
			campo = None
			continue
		if nombre_campo == 'clave':
			clave_repetida = existe_id(campo, 'colonias')
			if clave_repetida:
				print('\n Clave repetida\n')
				campo = None
				continue
	return campo





def existe_id(id_buscado, objeto):
	global usuarios
	encontrado = False
	if objeto == 'usuarios':
		for usuario in usuarios:
			if not os.path.isfile('.usuarios.csv'):
				if usuario['uid'] == int(id_buscado):
					encontrado = True
			if usuario['uid'] == id_buscado:
				encontrado = True
			if usuario['uid'] == int(id_buscado):
				encontrado = True
	elif objeto == 'colonias':
		for colonia in colonias:
			if not os.path.isfile('.colonias.csv'):
				if colonia['clave'] == int(id_buscado):
					encontrado = True
			if colonia['clave'] == id_buscado:
				encontrado = True
				#print('\n La clave si existe \n')
			if colonia['clave'] == int(id_buscado):
				encontrado = True
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
				if usuario['uid'] == int(id_buscado):
					print('\n Usuario encontrado. Nombre: {}'.format(usuario['nombre']))
					modificacion_submenus('usuario', usuario)
					break
		else:
			print('\n El id introducido no existe\n')	
	elif opc == 2:
		clave_buscada = input('\n Introduzca la clave la colonia: ')
		clave_encontrada = existe_id(clave_buscada, 'colonias')
		if clave_encontrada:
			#Este ciclo para encontrar la colonia, y luego se manda
			for colonia in colonias[1:]:
				if colonia['clave'] == clave_buscada:
					print('\n Colonia encontrada. Nombre: {}'.format(colonia['nombre']))
					modificacion_submenus('colonia', colonia)
					break
				if colonia['clave'] == int(clave_buscada):
					print('\n Colonia encontrada. Nombre: {}'.format(colonia['nombre']))
					modificacion_submenus('colonia', colonia)
					break
		else:
			print('\n La clave introducida no existe\n')
	

def modificacion_submenus(objeto_tipo, obj_encontrado):
	#FALTAN Validaciones
	#Recuerda que tienes una funcion llamada existe_id
	opc = 0
	if objeto_tipo == 'usuario':
		print('\n\n\t\t MENU MODIFICACION USUARIO \n 1. Nombre \n 2. Tipo \n 3. id \n 4. Colonia \n 5.Direccion \n 6. Consumo \n 7. Pago')
		opc = int(input('\n\tOpcion: '))
		if opc == 1:
			while True:
				nuevo_nombre = input('\n Introduzca el nuevo nombre: ')
				campo_bool = nuevo_nombre.isdigit()
				if campo_bool:
					continue
				if nuevo_nombre is not '':
					break;
			obj_encontrado['nombre'] = nuevo_nombre
			print('\n Nombre modificado \n')
		elif opc == 2:
			while True:
				nuevo_tipo = input('\n Introduzca el nuevo tipo: ')
				campo_bool = nuevo_tipo.isdigit()
				if campo_bool == False:
					continue
				nuevo_tipo_int = int(nuevo_tipo)
				if nuevo_tipo_int >= 1 and nuevo_tipo_int <= 8:
					break;
			obj_encontrado['tipo'] = nuevo_tipo
			print('\n tipo modificado \n')
		elif opc == 3:
			ya_existe_id = False
			while True:
				nuevo_id = input('\n Introduzca el nuevo id: ')
				campo_bool = nuevo_id.isdigit()
				if nuevo_id == '' or campo_bool == False:
					continue
				if not os.path.isfile('.usuarios.csv'):
					if obj_encontrado['uid'] == int(nuevo_id):
						print('\n Error. Es el mismo id\n')
						continue
				else:
					if obj_encontrado['uid'] == nuevo_id:
						print('\n Error. Es el mismo id\n')
						continue
					else:
						break
			ya_existe_id = existe_id(nuevo_id, 'usuarios')
			while ya_existe_id == True:
				print('\n El id introducido ya esta en uso \n')
				nuevo_id = input('\n Introduzca el nuevo id: ')
				ya_existe_id = existe_id(nuevo_id, 'usuarios')
			obj_encontrado['uid'] = nuevo_id
			print('\n id modificado \n')
		elif opc == 4: #colonia
			col_encontrada = False
			#print(type(obj_encontrado['clave de colonia'])) #Es string si se agarra del archivo, int si se agarra de la variable
			while True:
				nueva_colonia = input('\n Introduzca la clave de la nueva colonia: ')
				campo_bool = nueva_colonia.isdigit()
				if campo_bool == False:
					continue
				if nueva_colonia == '':
					continue
				if obj_encontrado['clave de colonia'] == nueva_colonia or obj_encontrado['clave de colonia'] == int(nueva_colonia):
					print('\n Error. Es la clave actual \n')
					continue
				for usuario in usuarios:
					if usuario['clave de colonia'] == nueva_colonia or usuario['clave de colonia'] == int(nueva_colonia):
						print('\n Nueva colonia: {}'.format(usuario['nombre de colonia']))
						col_encontrada = True
						obj_encontrado['clave de colonia'] = nueva_colonia
						obj_encontrado['nombre de colonia'] = usuario['nombre de colonia']
						break
				if col_encontrada:
					break
				else:
					print('\n Tiene que ingresar una clave que exista \n')
					continue
		elif opc == 5:
			while True:
				nueva_direccion = input('\n Introduzca la nueva direccion: ')
				if nueva_direccion == '':
					continue
				else:
					break
			obj_encontrado['direccion'] = nueva_direccion
			print('\n Direccion modificada \n')
		elif opc == 6:
			while True:
				nuevo_consumo = input('\n Introduzca el nuevo consumo: ')
				campo_bool = nuevo_consumo.isdigit()
				if campo_bool == False:
					continue
				if nuevo_consumo == '':
					continue
				else:
					break
			obj_encontrado['consumo'] = nuevo_consumo
			print('\n Consumo modificado \n')
		elif opc == 7:
			while True:
				nuevo_pago = input('\n Introduzca el pago: ')
				campo_bool = nuevo_pago.isdigit()
				if campo_bool == False:
					continue
				if nuevo_consumo == '':
					continue
				else:
					break
			obj_encontrado['pago'] = nuevo_pago
			print('\n Pago modificado \n')
	elif objeto_tipo == 'colonia':
		print('\n\n\t\t MENU MODIFICACION COLONIA \n 1. Nombre \n 2. clave \n')
		opc = int(input('\n\tOpcion: '))	
		if opc == 1:
			nombre_original = obj_encontrado['nombre']
			while True:
				nuevo_nombre = input('\n Introduzca el nuevo nombre: ')
				if nuevo_nombre == nombre_original:
					print('\n Error. Introdujo el nombre que ya tiene \n')
					continue
				if nuevo_nombre == '':
					continue
				else:
					break
			for colonia in colonias:
				if colonia['nombre'] == nombre_original:
					#print('\n Ya se cambió el nombre')
					colonia['nombre'] = nuevo_nombre
					break
			for usuario in usuarios:
				if usuario['nombre de colonia'] == nombre_original:
					usuario['nombre de colonia'] = nuevo_nombre
					#print('\n Ya se cambió el nombre en los usuarios')
			print('\n Nombre modificado \n')
		elif opc == 2:
			clave_original = obj_encontrado['clave']
			while True:
				nueva_clave = input('\n Introduzca la nueva clave: ')
				campo_bool = nueva_clave.isdigit()
				if campo_bool == False:
					continue
				if nueva_clave == clave_original or int(nueva_clave) == int(clave_original):
					print('\n Error. Introdujo la misma clave \n')
					continue
				if existe_id(nueva_clave, 'colonias'):
					print('\n La clave ya esta en uso \n')
					continue
				if nueva_clave == '':
					continue
				else:
					break

			#Cambiarlo en la colonia
			for colonia in colonias:
				if colonia['clave'] == clave_original or colonia['clave'] == int(clave_original):
					colonia['clave'] = nueva_clave
					break
			for usuario in usuarios:
				if usuario['clave de colonia'] == clave_original or usuario['clave de colonia'] == int(clave_original):
					usuario['clave de colonia'] = nueva_clave
			print('\n clave modificada \n')


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


def pagos_no_realizados():
	global usuarios
	global tarifas
	suma_totales = 0
	total_debio_pagar = 0
	hay_un_usuario = False
	nombre_reporte_generado = input('\n Nombre para el archivo del reporte: ')
	with open(nombre_reporte_generado, mode='w') as f:
		print('\n\n\t\t REPORTE DE PAGOS NO REALIZADOS \n\n')
		f.write('\n\t\t REPORTE DE PAGOS NO REALIZADOS \n\n')
		print('\n\t Id  Nombre \t Colonia   Pago realizado   Total a pagar')
		f.write('\n\t Id  Nombre \t Colonia   Pago realizado   Total a pagar')
		
		if not os.path.isfile('.usuarios.csv'):
			for usuario in usuarios:
				#Agarro el index
				idx_tipo = int(usuario['tipo'])
				#Agarro la lista (el row, por que asi estan acomodados)
				lista_tarifa = tarifas[idx_tipo]
				#Agarro la celda 0, donde esta el valor
				valor_tarifa = lista_tarifa[0]
				total_usuario = int(usuario['consumo']) * float(valor_tarifa)
				if int(usuario['pago']) < total_usuario:
					print('\n\t {} | {} | {} |          {}           | {}'.format(usuario['uid'], usuario['nombre'], usuario['nombre de colonia'], usuario['pago'], total_usuario))
					f.write('\n\t {} | {} | {} |        {}          | {}'.format(usuario['uid'], usuario['nombre'], usuario['nombre de colonia'], usuario['pago'], total_usuario))
					suma_totales += int(usuario['pago'])
					total_debio_pagar += total_usuario
					hay_un_usuario = True
		else:	
			for usuario in usuarios[1:]:
				#Agarro el index
				idx_tipo = int(usuario['tipo'])
				#Agarro la lista (el row, por que asi estan acomodados)
				lista_tarifa = tarifas[idx_tipo]
				#Agarro la celda 0, donde esta el valor
				valor_tarifa = lista_tarifa[0]
				total_usuario = int(usuario['consumo']) * float(valor_tarifa)
				if int(usuario['pago']) < total_usuario:
					print('\n\t {} | {} | {} |         {}         | {}'.format(usuario['uid'], usuario['nombre'], usuario['nombre de colonia'], usuario['pago'], total_usuario))
					f.write('\n\t {} | {} | {} |        {}        | {}'.format(usuario['uid'], usuario['nombre'], usuario['nombre de colonia'], usuario['pago'], total_usuario))
					suma_totales += int(usuario['pago'])
					total_debio_pagar += total_usuario
					hay_un_usuario = True
		if hay_un_usuario: 
			print('\n\n Total pagos realizados: {}'.format(suma_totales))
			print('\n\n Total que se debio pagar: {}'.format(total_debio_pagar))
			f.write('\n\n\n Total general: {}'.format(suma_totales))
			f.write('\n\n Total que se debio pagar: {}'.format(total_debio_pagar))
		else:
			print('\t ---  -----       ---      ---               ---')
			print('\n Todos los usuarios pagaron')
			f.write('\t ---  -----       ---      ---             ---')
			f.write('\n Todos los usuarios pagaron')


def pagos_realizados():
	global usuarios
	global tarifas
	suma_totales = 0
	hay_pago = False
	nombre_reporte_generado = input('\n Nombre para el archivo del reporte: ')
	with open(nombre_reporte_generado, mode='w') as f:
		print('\n\n\t\t REPORTE DE PAGOS REALIZADOS \n\n')
		f.write('\n\n\t\t REPORTE DE PAGOS REALIZADOS \n\n')
		print('\n\t Id  Nombre \t Colonia   Pago')
		f.write('\n\t Id  Nombre \t Colonia   Pago')
		
		if not os.path.isfile('.usuarios.csv'):
			for usuario in usuarios:
				#Agarro el index
				print(usuario)
				idx_tipo = int(usuario['tipo'])
				print(idx_tipo)
				#Agarro la lista (el row, por que asi estan acomodados)
				lista_tarifa = tarifas[idx_tipo]
				#Agarro la celda 0, donde esta el valor
				valor_tarifa = lista_tarifa[0]
				print(valor_tarifa)
				total_usuario = int(usuario['consumo']) * float(valor_tarifa)
				print(total_usuario)
				if int(usuario['pago']) == total_usuario or (int(usuario['pago']) > total_usuario):
					print('\n\t {} | {} | {}  | {}'.format(usuario['uid'], usuario['nombre'], usuario['nombre de colonia'], usuario['pago']))
					f.write('\n\t {} | {} | {}  | {}'.format(usuario['uid'], usuario['nombre'], usuario['nombre de colonia'], usuario['pago']))
					suma_totales += int(usuario['pago'])
					hay_pago = True
		else:
			for usuario in usuarios[1:]:
				#Agarro el index
				idx_tipo = int(usuario['tipo'])
				#Agarro la lista (el row, por que asi estan acomodados)
				lista_tarifa = tarifas[idx_tipo]
				#Agarro la celda 0, donde esta el valor
				valor_tarifa = lista_tarifa[0]
				total_usuario = int(usuario['consumo']) * float(valor_tarifa)
				if int(usuario['pago']) == total_usuario or (int(usuario['pago']) > total_usuario):
					print('\n\t {} | {} | {} | {}'.format(usuario['uid'], usuario['nombre'], usuario['nombre de colonia'], usuario['pago']))
					f.write('\n\t {} | {} | {} | {}'.format(usuario['uid'], usuario['nombre'], usuario['nombre de colonia'], usuario['pago']))
					suma_totales += int(usuario['pago'])
					hay_pago = True
		if hay_pago:
			print('\n\n Total general: {}'.format(suma_totales))
			f.write('\n\n\n Total general: {}'.format(suma_totales))
		else:
			print('\t ---  -----       ---      ---')
			print('\n Ningun usuario cumplio con el pago establecido \n')
			f.write('\t ---  -----       ---      ---')
			f.write('\n Ningun usuario cumplio con el pago establecido \n')


def facturacion_todos_usuarios():
	global usuarios
	total_general = 0
	print('\t\t\tREPORTE DE FACTURACION TODOS LOS USUARIOS\n\n')
	print('\t id  Nombre     Colonia    Consumo   Importe   Sobreconsumo   Total')
	for usuario in usuarios[1:]:
		consumo = int(usuario['consumo'])
		idx_tipo = int(usuario['tipo'])
		lista_tarifa = tarifas[idx_tipo]
		valor_tarifa = int(lista_tarifa[0])
		importe = valor_tarifa * consumo
		if consumo > 300:
			sobrecon = importe * .50
			total = importe + sobrecon
		elif consumo > 200:
			sobrecon = importe * .30
			total = importe + sobrecon
		elif consumo > 100:
			sobrecon = importe * .20
			total = importe + sobrecon
		elif consumo > 50:
			sobrecon = importe * .10
			total = importe + sobrecon
		else:
			sobrecon = 0
			total = importe + sobrecon
		total_general = total_general + total
		print('\t {} | {}   |  {}  | {}  |  {}      | {}    |  {}  '.format(usuario['uid'], usuario['nombre'], usuario['nombre de colonia'],
			consumo, importe, sobrecon, total))
	print('\n Total general: {}'.format(total_general))



def facturacion_individual():
	global usuarios
	id_encontrado = False
	obj_encontrado_bool = False
	while id_encontrado == False:
		id_buscado = input('\n Id del usuario: ')
		id_encontrado = existe_id(id_buscado, 'usuarios')
		if id_encontrado == False:
			print('\n Introduzca un id valido \n')
	for usuario in usuarios[1:]:
		if usuario['uid'] == id_buscado:
			obj_encontrado = usuario
			obj_encontrado_bool = True
	if obj_encontrado_bool:
		consumo = int(obj_encontrado['consumo'])
		idx_tipo = int(obj_encontrado['tipo'])
		lista_tarifa = tarifas[idx_tipo]
		valor_tarifa = int(lista_tarifa[0])
		importe = valor_tarifa * consumo
		if consumo > 300:
			sobrecon = importe * .50
			total = importe + sobrecon
		elif consumo > 200:
			sobrecon = importe * .30
			total = importe + sobrecon
		elif consumo > 100:
			sobrecon = importe * .20
			total = importe + sobrecon
		elif consumo > 50:
			sobrecon = importe * .10
			total = importe + sobrecon
		else:
			sobrecon = 0
			total = importe + sobrecon
			
	print('\n\n COMPAÑIA DE AGUA POTABLE ACME\t\t\tFACTURA')
	print('\n Av. Matamoros 2004\t\t\t\tFolio: {}'.format(folio+1))
	print('\n Fraccionamiento Colinas del Valle\n Monterrey, NL.')
	print('\n RFC: PAA 141120 S4')
	print('\n Monterrey, NL. a')
	print('\n\n id: {} \n Nombre: {} \n Colonia: {} \n Direccion: {} \n '.format(obj_encontrado['uid'], obj_encontrado['nombre'], obj_encontrado['nombre de colonia'], obj_encontrado['direccion']))
	print('\n Tipo de usuario: {} \n Consumo: {} \n Importe: {} \n Sobreconsumo: {}'.format(obj_encontrado['tipo'], consumo, importe, sobrecon))
	print('\n Total a pagar: {}'.format(total))
	print('\n Paguese antes de: 22/may/19')
	




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


def reportes():
	print('\n\n\t\t MENU REPORTES \n')
	print('\n 1. Pagos realizados \n 2. Pagos no realizados \n 3. Facturacion \n')
	opc = int(input('\n\t Opcion: '))
	if opc == 1:
		pagos_realizados()
	elif opc == 2:
		pagos_no_realizados()
	elif opc == 3:
		print('\n Tipo de facturacion \n 1. Facturacion individual \n 2. Todos los usuarios')
		opcf = int(input('\n Opcion: '))
		if opcf == 1:
			facturacion_individual()
		elif opcf == 2:
			facturacion_todos_usuarios()




if __name__ == '__main__':
	inicializar_variables_desde_archivo()
	while True:
		_menu_principal()
		command = int(input('\n\n\t Opcion: '))
		if command == 5:
			print('\n Ha salido del programa \n') 
			break
		if command < 1 or command > 5:
			continue
		mandar_opcion(command)
		#print(usuarios[1].get('nombre'))
	imprimir_en_archivo()
