from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=150)
    stock = models.PositiveIntegerField()


class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


"""'
we will follow this order:
1. Create the minimal Django project and app.
2. Implement the two models.
3. Create and inspect migrations.
4. Build the deliberately vulnerable purchase endpoint.
5. Test ordinary sequential purchases.
6. Reproduce the race with concurrent requests.
7. Inspect the incorrect database state.
8. Fix the endpoint using row-level locking.
9. Repeat the concurrent test and verify correctness.
"""
