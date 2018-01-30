from django.db import models


class Result(models.Model):

    petal_width = models.DecimalField(max_digits=3, decimal_places=2)
    petal_length = models.DecimalField(max_digits=3, decimal_places=2)
    classification = models.CharField(max_length=25, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return f'{self.petal_width} - {self.petal_length} - {self.classification}'
