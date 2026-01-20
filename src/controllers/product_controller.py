


from daos.product_dao import ProductDAO


class ProductController:
    def __init__(self):
        self.dao = ProductDAO()

    def list_products(self):
        """ List all products """
        return self.dao.select_all()
    
    def create_product(self, product):
        """ Create a new product based on product inputs """
        self.dao.insert(product)

    def delete_product(self, product_id):
        """ Delete a product by id """
        try:
            pid = int(product_id)
        except Exception:
            pid = product_id
        self.dao.delete(pid)

    def shutdown(self):
        """ Close database connection """
        self.dao.close()