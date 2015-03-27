from app.models import *
import datetime



def get_permisos_sistema(user):
    roles = UsuarioRolSistema.objects.filter(usuario = user).only('rol')
    permisos_obj = []
    for i in roles:
        permisos_obj.extend(i.rol.permisos.all())
    permisos = []
    for i in permisos_obj:
        permisos.append(i.nombre)
    return permisos

def registrar_version(itm, relaciones, archivos):
    """Se ingresa la version antigua al registro"""
    reg = RegistroHistorial()
    reg.version = itm.version
    reg.estado = itm.estado
    reg.complejidad = itm.complejidad
    reg.descripcion_corta = itm.descripcion_corta
    reg.descripcion_larga = itm.descripcion_larga
    reg.habilitado = itm.habilitado
    reg.icono = itm.icono
    reg.tipo = itm.tipo
    reg.fecha_modificacion = datetime.datetime.today()
    historial = Historial.objects.get(item = itm)
    reg.historial = historial
    reg.save()
    if (relaciones):
        for i in relaciones:
            nuevo = RegHistoRel()
            nuevo.itm_padre = i.padre
            nuevo.itm_hijo = i.hijo
            nuevo.registro = reg
            nuevo.save()
    if (archivos):
        for i in archivos:
            adj = RegHistoAdj()
            adj.nombre = i.nombre
            adj.contenido = i.contenido
            adj.tamano = i.tamano
            adj.mimetype = i.mimetype
            adj.i = itm
            adj.registro = reg
            adj.save()
    """Se cambia el estado del item"""
    itm.estado = 2            
    """Se incrementa la version actual"""
    itm.version = itm.version + 1
    itm.save()           


def tiene_hijo (padre, hijos):
    for i in hijos:
        if (i.fase.id == padre.fase.id + 1):
            return True
        else:
            relaciones = RelItem.objects.filter(padre=i, habilitado=True).values_list('hijo', flat=True)
            if (relaciones):
                hijos = Item.objects.filter(id__in = relaciones)
                return tiene_hijo (i, hijos)
    return False
