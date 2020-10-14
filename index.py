from tkinter import ttk
from tkinter import *

import sqlite3


class Producto:

    db_name = 'database.db'

    def __init__(self, window):
        print("estoy en el init")
        self.wind = window
        self.wind.title("Products Application")

        # Contenedor
        frame = LabelFrame(self.wind, text="Register a new Product")

        # Grilla
        frame.grid(row=0, column=0, columnspan=3, pady=20)

        # Name int
        Label(frame, text='Name: ').grid(row=1, column=0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row=1, column=1)

        # Price int
        Label(frame, text='Price: ').grid(row=2, column=0)
        self.price = Entry(frame)
        self.price.grid(row=2, column=1)

        # Button Add Product
        ttk.Button(frame, text="Save  Product", command=self.addProduct).grid(
            row=3, columnspan=2, sticky=W + E)

        # Output Messages
        self.message = Label(text='', fg='red')
        self.message.grid(row=3, column=0, columnspan=2, sticky=W + E)

        # Table
        self.tree = ttk.Treeview(height=10, columns=2)
        self.tree.grid(row=4, column=0, columnspan=2)
        self.tree.heading("#0", text="Name", anchor=CENTER)
        self.tree.heading("#1", text="Price", anchor=CENTER)

        ttk.Button(text="Eliminar", command=self.deleteProduct).grid(
            row=5, column=0, sticky=W + E)

        ttk.Button(text="Editar", command=self.edit_product).grid(
            row=5, column=1, sticky=W + E)

        # filling the row
        self.getProducts()

    def run_query(self, query, parameters=()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    def validation(self):
        return len(self.name.get()) != 0 and len(self.price.get()) != 0

    def addProduct(self):
        if self.validation():
            query = 'INSERT INTO product VALUES(NULL, ?,?)'
            parameters = (self.name.get(), self.price.get())
            self.run_query(query, parameters)
            self.getProducts()
            self.message['text'] = 'product {} added Successfully'.format(
                self.name.get())
            self.name.delete(0, END)
            self.price.delete(0, END)

            print("datos guardados")

        else:
            self.message['text'] = 'El nombre y el precio son requeridos'

    def deleteProduct(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]

        except IndexError as e:
            self.message['text'] = 'Please select a Record'
            return

        self.message['text'] = ''
        name = self.tree.item(self.tree.selection())['text'][0]
        query = 'DELETE FROM product WHERE name = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record {} se ha eliminado '.format(name)
        self.getProducts()

    def edit_product(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text'][0]

        except IndexError as e:
            self.message['text'] = 'Please select a Record'
            return
        old_name = self.tree.item(self.tree.selection())['text']
        old_price = self.tree.item(self.tree.selection())['values'][0]

        self.edit_wind = Toplevel()
        nueva_ventana = self.edit_wind
        nueva_ventana.title = 'Edit Product'

        # Old Name
        Label(nueva_ventana, text="Old Name: ").grid(row=0, column=1)
        Entry(nueva_ventana, textvariable=StringVar(
            nueva_ventana, value=old_name),  state='readonly').grid(row=0, column=2)

        print("el precio actuale s "+old_name + "  - "+old_price)

        # NEW NAME
        Label(nueva_ventana, text="New Name: ").grid(row=1, column=1)
        new_name = Entry(nueva_ventana)
        new_name.grid(row=1, column=2)

        # OLD PRICE
        Label(nueva_ventana, text="Old Price: ").grid(row=2, column=1)
        Entry(nueva_ventana, textvariable=StringVar(
            nueva_ventana, value=old_price),  state='readonly').grid(row=2, column=2)

        # NEW PRICE
        Label(nueva_ventana, text="New Price: ").grid(row=3, column=1)
        new_price = Entry(nueva_ventana)
        new_price.grid(row=3, column=2)

        Button(nueva_ventana, text='Update', command=lambda: self.edit_records(
            new_name.get(), old_name, new_price.get(), old_price)).grid(row=4, column=2, sticky=W)

    def edit_records(self, new_name, old_name, new_price, old_price):

        query = 'UPDATE product SET name = ?, price = ? WHERE name = ? AND price = ?'
        paramets = (new_name, new_price, old_name, old_price)

        self.run_query(query, paramets)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} update successfully'.format(old_name)
        self.getProducts()

    def getProducts(self):

        # Cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        # Consultando los datos
        query = 'SELECT * FROM product ORDER BY name DESC'
        db_rows = self.run_query(query)

        # Rellenando los datos
        for row in db_rows:
            self.tree.insert('', 0, text=row[1], value=row[2])

    def __del__(self):
        print("Se cerrara")


if __name__ == '__main__':
    window = Tk()
    application = Producto(window)
    window.mainloop()
