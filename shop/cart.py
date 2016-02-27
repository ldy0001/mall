#_*_coding:utf-8_*_
import models

class LineItem(models.Model):
    product = models.ForeignKey(Product)
    unit_price = models.DecimalField(max_digits=8,decimal_places=2)
    quantity = models.IntegerField()

class Cart(object):
    def __init__(self, *args, **kwargs):
        self.items = []
        self.total_price = 0
    def add_product(self,product):
        self.total_price += product.price
        for item in self.items:
            if item.product.id == product.id:
                item.quantity += 1
            return self.items.append(LineItem(product=product,unit_price=product.price,quantity=1))