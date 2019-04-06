from django.db import models


class Cell(models.Model):
    column = models.PositiveIntegerField('Column')
    row = models.PositiveIntegerField('Row')
    column_span = models.PositiveIntegerField('Column span')
    row_span = models.PositiveIntegerField('Row span')
    advanced = models.CharField('Advanced', max_length=3)
    font_size = models.PositiveSmallIntegerField('Font size')
    direction = models.BooleanField('Direction')

    VERTICAL_ALIGN = (
        ('t', 'Top'),
        ('m', 'Middle'),
        ('b', 'Bottom'),
    )

    HORIZONTAL_ALIGN = (
        ('l', 'Left'),
        ('c', 'Center'),
        ('r', 'Right')
    )

    vertical_align = models.CharField('Vertical align', max_length=1, choices=VERTICAL_ALIGN, blank=True,
                                      default='m')
    horizontal_align = models.CharField('Horizontal align', max_length=1, choices=HORIZONTAL_ALIGN, blank=True,
                                        default='h')
    width = models.PositiveIntegerField('Width')
    height = models.PositiveIntegerField('Height')
    value = models.CharField('Value', max_length=500)
    owner = models.ForeignKey('pback_auth.User', null=True, default=None, on_delete=models.SET_NULL)

    def __str__(self):
        return 'Cell {0}:{1} for template'.format(self.column, self.row)
