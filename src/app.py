from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from models.ModelProducto import ModelProducto
from models.entities.producto import Producto


class Interfaz():
    def __init__(self, root):
        #Inicializa interfaz grafica
        self.root=root
        self.root.title('Gestion de productos')
        self.root.geometry("600x600")
        
        #MENU-------------------------------------------------------------------------
        self.barra_menu=Menu(root)
        self.root.config(menu=self.barra_menu, width=300, height=300)

        self.crudMenu=Menu(self.barra_menu, tearoff=0)
        self.crudMenu.add_command(label='Agregar producto', command=self.agregar_producto)
        
        self.barra_menu.add_cascade(label='Productos', menu=self.crudMenu)
        self.barra_menu.add_cascade(label='Salir', command=self.cerrar_app)

        #TABLA-------------------------------------------------------------------------
        self.tabla=ttk.Treeview( height=20, columns=('1','2','3'), show='headings')
        self.tabla.grid(row=1, column=0, columnspan=3)
        self.tabla.heading('#1', text='ID', anchor=CENTER)
        self.tabla.heading('#2', text='DESCRIPCION', anchor=CENTER)
        self.tabla.heading('#3', text='PRECIO', anchor=CENTER)

        #MENSAJES DE SALIDA
        self.message=Label(text='', fg='red')
        self.message.grid(row=3, column=1,  sticky=W+E)
       
        #BOTONES----------------------------------------------------------------------
        self.boton_eliminar=Button(self.root, text='Eliminar', command=self.eliminar_producto, width=10, cursor='hand2', activebackground='#FF0000')
        self.boton_eliminar.grid(row=2, column=0, padx=10, pady=10)

        self.boton_editar=Button(self.root, text='Editar', command=self.actualizar_producto, width=10, cursor='hand2', activebackground='#0000FF')
        self.boton_editar.grid(row=2, column=1, padx=10, pady=10)

        self.boton_agregar=Button(self.root, text='Agregar', command=self.agregar_producto , width=10, cursor='hand2', activebackground='#008000')
        self.boton_agregar.grid(row=2, column=2, padx=10, pady=10)

        self.insertar_productos()



    def agregar_producto(self):
        """
        Genera ventana emergente para crear un nuevo producto
        """
        self.ventana_emergente=Toplevel()
        self.ventana_emergente.geometry("600x300")

        #Labels Ventana emergente
        label_descripcion=Label(self.ventana_emergente, text='Descripcion')
        label_descripcion.grid(row=0, column=0, padx=10, pady=10)

        label_descripcion=Label(self.ventana_emergente, text='Precio')
        label_descripcion.grid(row=1, column=0, padx=10, pady=10)
        #Enttrys Ventana emergente
        self.descripcion=StringVar()
        self.precio=StringVar()

        self.entrada_descripcion=Entry(self.ventana_emergente, width=50, textvariable=self.descripcion)
        self.entrada_descripcion.grid(row=0, column=1, padx=10, pady=10)

        self.entrada_precio=Entry(self.ventana_emergente, textvariable=self.precio)
        self.entrada_precio.grid(row=1, column=1, padx=10, pady=10, sticky=W)

        #Botones
        self.boton_agregar_producto=Button(self.ventana_emergente, text='Agregar producto',command=self.agregar_productos_ ,cursor='hand2', activebackground='#008000')
        self.boton_agregar_producto.grid(row=2, column=1, padx=10, pady=10)

        self.boton_cancelar=Button(self.ventana_emergente, text='Cancelar', command=self.cerrar_ventana, cursor='hand2', activebackground='#FF0000')
        self.boton_cancelar.grid(row=2, column=0, padx=10, pady=10)

    def insertar_productos(self):
        """
        Insertar productos en tabla Treeview
        """
        
        registros=self.tabla.get_children()
        for registro in registros:
            self.tabla.delete(registro)
        for producto in ModelProducto.get_productos():
            self.tabla.insert('',0, values=(producto.id, producto.descripcion, producto.precio))
   
    def agregar_productos_(self):
        """
        Ejecuta funcion para la generacion de los nuevos registros en la DB y actualiza tabla Treeview
        """
        ModelProducto.add_product(self.descripcion.get(), self.precio.get())
        self.insertar_productos()
        self.limpiar_campos()
        return None
    
    
    def limpiar_campos(self):
        #Resetea los campos luego de agregar un producto
        self.descripcion.set("")
        self.precio.set("")

    
    def eliminar_producto(self):
        """
        Ejecuta funcion para eliminar registros en DB y actualiza tabla Treeview
        """
        self.message['text']=''
        try:
            self.tabla.item(self.tabla.selection())['values'][0]

        except IndexError as e:
            self.message['text']='Selecciona un producto a eliminar'
            return None
        self.message['text']=''
        id=self.tabla.item(self.tabla.selection())['values'][0]
        
        ModelProducto.delete_product(id)
        self.insertar_productos()
        return None
    
    def cerrar_ventana(self):
        #Cierra ventana emergente
        self.ventana_emergente.destroy()
       
    
    def cerrar_app(self):
        valor=messagebox.askquestion('Salir', 'Desea salir de la aplicacion?')
        if valor=='yes':
            self.root.destroy()

    def actualizar_producto(self):
        """
        Genera ventana emergente para editar producto cuando se selecciona un producto a editar de lo contrario se informa situacion
        """
        self.message['text']=""
        try:
            self.tabla.item(self.tabla.selection())['values'][0]
            producto_seleccionado_editar=Producto(self.tabla.item(self.tabla.selection())['values'][0], self.tabla.item(self.tabla.selection())['values'][1], self.tabla.item(self.tabla.selection())['values'][2])
            
            self.ventana_emergente_editar=Toplevel()
            self.ventana_emergente_editar.geometry("600x300")

            self.id_editar=StringVar()
            self.desc_editar=StringVar()
            self.precio_editar=StringVar()
            

            #Labels
            self.label_id_editar=Label(self.ventana_emergente_editar, text='Id')
            self.label_id_editar.grid(row=0, column=0, padx=10, pady=10)    

            self.label_desc=Label(self.ventana_emergente_editar, text='Descripcion')
            self.label_desc.grid(row=1, column=0, padx=10, pady=10)

            self.label_prec=Label(self.ventana_emergente_editar, text='Precio')
            self.label_prec.grid(row=2, column=0, padx=10, pady=10)
            #Entrys
            self.entrada_id_editar=Entry(self.ventana_emergente_editar, textvariable=self.id_editar, state='disabled')
            self.entrada_id_editar.grid(row=0, column=1, padx=10, pady=10)

            self.entrada_desc=Entry(self.ventana_emergente_editar, textvariable=self.desc_editar)
            self.entrada_desc.grid(row=1, column=1, padx=10, pady=10)

            self.entrada_prec=Entry(self.ventana_emergente_editar, textvariable=self.precio_editar)
            self.entrada_prec.grid(row=2, column=1, padx=10, pady=10)
            
            self.id_editar.set(producto_seleccionado_editar.id)
            self.desc_editar.set(producto_seleccionado_editar.descripcion)
            self.precio_editar.set(producto_seleccionado_editar.precio)

            #Botones
            self.boton_editar_cancelar=Button(self.ventana_emergente_editar, text='Cancelar', command=self.cerrar_ventana2)
            self.boton_editar_cancelar.grid(row=3, column=0, padx=10, pady=10)

            self.boton_editar_aceptar=Button(self.ventana_emergente_editar, text='Aceptar', command=self.editar_producto)
            self.boton_editar_aceptar.grid(row=3, column=1, padx=10, pady=10)

        except IndexError as e:
            self.message['text']='Seleccione un producto a editar'

    def editar_producto(self):
        """
        Ejecuta funcion para modificar los registros en DB, cierra ventana emergete, actualiza tabla Treeview
        """
        producto_editado=Producto(self.id_editar.get(),self.desc_editar.get(), self.precio_editar.get() )
        ModelProducto.update_product(producto_editado)
        self.ventana_emergente_editar.destroy()
        self.insertar_productos()
        self.message['text']='Producto actualizado correctamente'

    def cerrar_ventana2(self):
        self.ventana_emergente_editar.destroy()

        
        
        


        
        


if __name__=='__main__':
    root=Tk()
    app=Interfaz(root)
    root.mainloop()