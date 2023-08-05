import datetime
import gzip

import xlwt
from django.http import HttpResponse
from django.utils.http import urlquote
from django.utils.six import BytesIO

from acmin.utils import attr, display, decorators, get_model_fields, Field
from .list import AdminListView


@decorators.memorize
def get_export_fields(cls) -> list:
    names = attr(cls, "export_fields", attr(cls, "list_fields"))
    model_fields = get_model_fields(cls)
    if not names:
        export_fields = [f.name for f in model_fields]
        excludes = attr(cls, "export_exclude", attr(cls, "list_exclude", [])) + ['created', 'modified']
        names = [f for f in export_fields if f not in excludes]

    fields_dict = {f.name: f.verbose_name for f in model_fields}
    return [Field(name, fields_dict.pop(name, name), name) for name in names]


class AdminExportView(AdminListView):
    paginate_by = None

    def get_fields(self):
        return get_export_fields(self.model)

    def get(self, request, *args, **kwargs):
        return self.export_excel(self.get_queryset())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["view_type"] = 'export'
        return context

    def export_excel(self, objects):
        fields = self.get_fields()
        model_verbose = attr(self.model, '_meta.verbose_name')
        wb = xlwt.Workbook(encoding='utf-8')
        sheet = wb.add_sheet('%s列表' % model_verbose)
        style_heading = xlwt.easyxf("""
            font:name Arial,colour_index white,bold on,height 0xA0;
            align:wrap off,vert center,horiz center;
            pattern:pattern solid,fore-colour 0x19;
            borders:left THIN,right THIN,top THIN,bottom THIN;
            """)
        style_body = xlwt.easyxf("""
                font:name Arial,bold off,height 0XA0;
                align:wrap on,vert center,horiz left;
                borders:left THIN,right THIN,top THIN,bottom THIN;
                """)
        # style_green = xlwt.easyxf(" pattern: pattern solid,fore-colour 0x11;")
        # style_red = xlwt.easyxf(" pattern: pattern solid,fore-colour 0x0A;")
        fmts = [
            'M/D/YY', 'D-MMM-YY', 'D-MMM', 'MMM-YY',
            'h:mm AM/PM', 'h:mm:ss AM/PM', 'h:mm', 'h:mm:ss', 'M/D/YY h:mm', 'mm:ss', '[h]:mm:ss', 'mm:ss.0',
        ]
        style_body.num_format_str = fmts[0]

        for column, field in enumerate(fields):
            sheet.write(0, column, str(field.verbose), style_heading)

        for row, obj in enumerate(objects, 1):
            for column, field in enumerate(fields, 0):
                sheet.write(row, column, str(display(obj, field.name)), style_body)

        buf = BytesIO()
        wb.save(buf)
        buf.seek(0)
        response = HttpResponse(gzip.compress(buf.getvalue()), content_type="application/vnd.ms-excel")
        filename = model_verbose + "-" + datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        response['Content-Disposition'] = 'attachment;filename=%s.xls' % urlquote(filename)
        response['Content-Encoding'] = 'gzip'
        return response
