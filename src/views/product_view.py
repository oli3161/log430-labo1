"""
Product view
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from models.product import Product
from controllers.product_controller import ProductController

class ProductView:
    @staticmethod
    def show_options():
        """ Show product menu with operation options """
        controller = ProductController()
        while True:
            print("\n1. Montrer la liste d'items\n2. Ajouter un item\n3. Supprimer un item\n4. Retour au menu principal")
            choice = input("Choisissez une option: ")

            if choice == '1':
                products = controller.list_products()
                ProductView.show_products(products)
            elif choice == '2':
                name, brand, price = ProductView.get_inputs()
                product = Product(None, name, brand, price)
                controller.create_product(product)
            elif choice == '3':
                pid = input("ID de l'item à supprimer: ").strip()
                if pid:
                    controller.delete_product(pid)
            elif choice == '4':
                controller.shutdown()
                break
            else:
                print("Cette option n'existe pas.")

    @staticmethod
    def show_products(products):
        """ List products """
        print("\n".join(f"{product.id}: {product.name} ({product.brand}) - {product.price}" for product in products))

    @staticmethod
    def get_inputs():
        """ Prompt user for inputs necessary to add a new product """
        name = input("Nom de l'item : ").strip()
        brand = input("Marque : ").strip()
        price_str = input("Prix : ").strip()
        try:
            price = float(price_str)
        except Exception:
            price = 0.0
        return name, brand, price
