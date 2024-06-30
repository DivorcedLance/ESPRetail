from sqlalchemy import Column, Integer, String, ForeignKey, Float, Boolean
from Conexion import Base

class User(Base):
    __tablename__ = 'users'
    id_user = Column(Integer, primary_key=True)
    nombre = Column(String(200))
    apellidos = Column(String(200))
    numero_celular = Column(String(20))
    direccion = Column(String(200))
    id_tienda = Column(Integer, ForeignKey('tiendas.id_tienda'))

class Operator(User):
    __tablename__ = 'operators'
    user_id = Column(Integer, ForeignKey('users.id_user'))
    operador = Column(String(4))
    clave = Column(String(16))

class Shopper(User):
    __tablename__ = 'shoppers'
    user_id = Column(Integer, ForeignKey('users.id_user'))
    usuario = Column(String(10))
    clave = Column(String(16))
    
class Autorizador(Base):
    __tablename__ = 'autorizadores'
    id_autorizador = Column(Integer, primary_key=True)
    id_operador = Column(Integer, ForeignKey('operators.operador'))
    clave_autoriador = Column(String(16))

class Tienda(Base):
    __tablename__ = 'tiendas'
    id_tienda = Column(Integer, primary_key=True)
    nombre_tienda = Column(String(200))

class Cupon(Base):
    __tablename__ = 'cupones'
    id_cupon = Column(Integer, primary_key=True)
    codigo = Column(String(13))
    usos_restantes = Column(Integer)
    descuento_soles = Column(Integer)
    id_categoria_producto = Column(Integer, ForeignKey('categorias_productos.id_categoria_producto'))
    fecha_vencimiento = Column(String(10))
    
class CategoriaProducto(Base):
    __tablename__ = 'categorias_productos'
    id_categoria_producto = Column(Integer, primary_key=True)
    nombre_categoria_producto = Column(String(200))

class Descuento(Base):
    __tablename__ = 'descuentos'
    id_producto = Column(Integer, primary_key=True)
    descuento_soles = Column(Integer)
    id_tipo_descuento = Column(Integer, ForeignKey('tipos_descuentos.id_tipo_descuento'))
    id_medio_de_pago = Column(Integer, ForeignKey('medios_de_pago.id_medio_de_pago'))
    fecha_vencimiento = Column(String(10))

class TipoDescuento(Base):
    __tablename__ = 'tipos_descuentos'
    id_tipo_descuento = Column(Integer, primary_key=True)
    nombre_tipo_descuento = Column(String(200))
    descripcion_tipo_descuento = Column(String(200))

class MedioDePago(Base):
    __tablename__ = 'medios_de_pago'
    id_medio_de_pago = Column(Integer, primary_key=True)
    nombre_medio_de_pago = Column(String(200))

class Producto(Base):
    __tablename__ = 'productos'
    id_producto = Column(String(13), primary_key=True)
    nombre_producto = Column(String(200))
    stock = Column(Float)
    id_categoria_producto = Column(Integer, ForeignKey('categorias_productos.id_categoria_producto'))
    id_tienda = Column(Integer, ForeignKey('tiendas.id_tienda'))
    precio = Column(Float)
    seMideEnKg = Column(Boolean)

class OrdenCompra(Base):
    __tablename__ = 'ordenes_compra'
    id_orden_compra = Column(Integer, primary_key=True)
    fecha_orden_compra = Column(String(10))
    id_cliente = Column(Integer, ForeignKey('users.id_cliente'))
    entregado = Column(Boolean)
    id_creador = Column(Integer, ForeignKey('users.id_user'))

class ProductoOrdenCompra(Base):
    __tablename__ = 'productos_ordenes_compra'
    id_producto = Column(String(13), ForeignKey('productos.id_producto'), primary_key=True)
    id_orden_compra = Column(Integer, ForeignKey('ordenes_compra.id_orden_compra'), primary_key=True)
    cantidad = Column(Float)

class Cliente(User):
    __tablename__ = 'clientes'
    id_cliente = Column(Integer, primary_key=True)
    nro_doc = Column(String(12))
    id_tipo_doc = Column(Integer, ForeignKey('tipos_doc.id_tipo_doc'))
    nombre_razon_social = Column(String(200))

class TipoDoc(Base):
    __tablename__ = 'tipos_doc'
    id_tipo_doc = Column(Integer, primary_key=True)
    nombre_tipo_doc = Column(String(200))

class MedioPago(Base):
    __tablename__ = 'medios_pago'
    id_medio_pago = Column(Integer, primary_key=True)
    nombre_medio_pago = Column(String(200))

class Recibo(Base):
    __tablename__ = 'recibos'
    id_recibo = Column(Integer, primary_key=True)
    fecha_recibo = Column(String(10))

class Factura(Recibo):
    __tablename__ = 'facturas'
    id_factura = Column(Integer, ForeignKey('recibos.id_recibo'), primary_key=True)
    ruc = Column(String(11))

class Boleta(Recibo):
    __tablename__ = 'boletas'
    id_boleta = Column(Integer, ForeignKey('recibos.id_recibo'), primary_key=True)
    igv_total = Column(Float)
    subtotal_sin_igv = Column(Float)
    total = Column(Float)

class ComprobanteDePago(Base):
    __tablename__ = 'comprobantes_de_pago'
    id_comprobante = Column(Integer, primary_key=True)
    id_orden_compra = Column(Integer, ForeignKey('ordenes_compra.id_orden_compra'))
    id_medio_pago = Column(Integer, ForeignKey('medios_pago.id_medio_pago'))
    id_recibo = Column(Integer, ForeignKey('recibos.id_recibo'))
    id_cajero = Column(Integer, ForeignKey('users.id_user'))
    id_caja = Column(Integer, ForeignKey('cajas.id_caja'))
    monto = Column(Float)
    fecha_pago = Column(String(10))

class Caja(Base):
    __tablename__ = 'cajas'
    id_caja = Column(Integer, primary_key=True)
    id_tienda = Column(Integer, ForeignKey('tiendas.id_tienda'))
    numero_caja = Column(Integer)

class Sobre(Base):
    __tablename__ = 'sobres'
    id_sobre = Column(Integer, primary_key=True)
    id_operador = Column(Integer, ForeignKey('operators.operador'))
    id_autorizador = Column(Integer, ForeignKey('autorizadores.id_autorizador'))
    fecha_hora_emision = Column(String(19))
    n_sobre = Column(Integer)
    monto = Column(Float)
    depositado = Column(Boolean)
    id_responsable_deposito = Column(Integer, ForeignKey('autorizadores.id_autorizador'))
    id_medio_pago = Column(Integer, ForeignKey('medios_pago.id_medio_pago'))
    fecha_hora_deposito = Column(String(19))


class ReporteDeCaja(Base):
    __tablename__ = 'reportes_de_caja'
    id_reporte_de_caja = Column(Integer, primary_key=True)
    id_operador = Column(Integer, ForeignKey('operators.operador'))
    id_autorizador = Column(Integer, ForeignKey('autorizadores.id_autorizador'))
    fecha_hora_ingreso_caja = Column(String(19))
    fecha_hora_reporte = Column(String(19))
    n_reporte = Column(Integer)
    id_observacion = Column(Integer, ForeignKey('observaciones.id_observacion'))

    monto_de_sobre = Column(Float)
    monto_soles = Column(Float)
    monto_dolares = Column(Float)
    monto_euros = Column(Float)
    monto_qr = Column(Float)
    monto_tarjeta_creditoX = Column(Float)
    monto_tarjeta_debitoX = Column(Float)
    monto_ncx = Column(Float)
    monto_tarjeta_alimentos = Column(Float)
    monto_vale_mercaderia = Column(Float)


class Observacion(Base):
    __tablename__ = 'observaciones'
    id_observacion = Column(Integer, primary_key=True)
    descripcion = Column(String(200))

class ValeMercaderia(Base):
    __tablename__ = 'vales_mercaderia'
    id_vale = Column(Integer, primary_key=True)
    ean13 = Column(String(13))
    monto = Column(Float)

class TipoCambio(Base):
    __tablename__ = 'tipos_cambio'
    id_tipo_cambio = Column(Integer, primary_key=True)
    nombreDivisa = Column(String(3))
    valorSoles = Column(Float)

