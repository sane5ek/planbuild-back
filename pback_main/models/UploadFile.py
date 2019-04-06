from django.db import models

import pyexcel as p


class UploadFile(models.Model):
    file = models.FileField(upload_to='files/loads/%Y/%m/%d')
    owner = models.ForeignKey('pback_auth.User', null=True, default=None, on_delete=models.SET_NULL)

    def convert_file_to_xlsx(self):
        if self.file.name.endswith('xls'):
            # xls to xlsx
            p.save_book_as(file_name=self.file.name,
                           dest_file_name=self.file.name + 'x')
            self.file.name += 'x'
            self.save()

        elif not str(self.file).endswith('xlsx'):
            raise ValueError('Not Excel file')
