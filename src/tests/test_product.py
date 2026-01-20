from daos.product_dao import ProductDAO
from models.product import Product

dao = ProductDAO()

def test_product_select():
    # insert some products to ensure there are at least 3
    product1 = Product(None, 'Product One', 'Brand A', 10.99)
    product2 = Product(None, 'Product Two', 'Brand B', 15.49)
    product3 = Product(None, 'Product Three', 'Brand C', 7.99)
    dao.insert(product1)
    dao.insert(product2)
    dao.insert(product3)
    product_list = dao.select_all()
    assert len(product_list) >= 3

def test_product_insert():
    product = Product(None, 'Test Product', 'Test Brand', 9.99)
    dao.insert(product)
    product_list = dao.select_all()
    names = [p.name for p in product_list]
    assert product.name in names

def test_product_update():
    
    product = Product(None, 'Old Product', 'Old Brand', 19.99)
    assigned_id = dao.insert(product)

    corrected_name = 'Updated Product'
    product.id = assigned_id
    product.name = corrected_name
    dao.update(product)

    product_list = dao.select_all()
    names = [p.name for p in product_list]
    assert corrected_name in names

    # cleanup
    dao.delete(assigned_id)

def test_product_delete():
    
    test_name = 'Delete Product'
    # Clean up any existing products with the test name before the test
    for p in dao.select_all():
        if p.name == test_name:
            dao.delete(p.id)

    product = Product(None, test_name, 'Delete Brand', 29.99)
    assigned_id = dao.insert(product)
    dao.delete(assigned_id)

    # Clean up any products with the test name after the test (in case of failure)
    for p in dao.select_all():
        if p.name == test_name:
            dao.delete(p.id)

    product_list = dao.select_all()
    names = [p.name for p in product_list]
    assert product.name not in names