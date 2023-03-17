import sqlite3
from .entities.producto import Producto

class ModelProducto():
    
    @classmethod
    def get_productos(self):
        """
        Selecciona todos los productos de la base de datos
        Return:
                lista_productos: Lista de productos de tipo Producto
        """
        
        try:
            conexion=sqlite3.connect("src/database/gestion_productos_db.db")   
            cursor=conexion.cursor()
            sql="SELECT * FROM productos ORDER BY id DESC;"
            cursor.execute(sql)
            productos=cursor.fetchall()
            lista_productos=[]
            for producto in productos:
                product=Producto(producto[0], producto[1], producto[2])
                lista_productos.append(product)
            return lista_productos
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def add_product(self, descripcion, precio):
        """
        Inserta nuevo registro en la base de datos
        """
        try:

            conexion=sqlite3.connect("src/database/gestion_productos_db.db")
            cursor=conexion.cursor()
            sql="INSERT INTO productos VALUES(NULL,'{}',{});".format(descripcion, precio)
            cursor.execute(sql)
            conexion.commit()
        except Exception as ex:
            raise Exception(ex)
        
    @classmethod
    def delete_product(self, id):
        """
        Elimina registro de la base de datos
        """
        
        try:
            conexion=sqlite3.connect("src/database/gestion_productos_db.db")
            cursor=conexion.cursor()
            sql="DELETE FROM productos WHERE id={};".format(id)
            cursor.execute(sql)
            conexion.commit()
        except Exception as ex:
            raise Exception(ex)
        
    
    @classmethod
    def update_product(self, producto):
        """
        Edita producto en la base de datos
        Args:
             producto: Objeto tipo Producto, que contiene los nuevos valores del producto a editar
        """
        
        try:
            conexion=sqlite3.connect("src/database/gestion_productos_db.db")
            cursor=conexion.cursor()
            sql="UPDATE productos SET descripcion='{}', precio={} WHERE id={};".format(producto.descripcion, producto.precio, producto.id)
            cursor.execute(sql)
            conexion.commit()
        except Exception as ex:
            raise Exception(ex)

        
        


