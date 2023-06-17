import codecs
import json
import os

from django.core.exceptions import FieldDoesNotExist
from django.http import JsonResponse
from django.views.generic import ListView

from rest_framework.utils import model_meta

from main.settings import STATICFILES_DIRS

from yattag import Doc, indent


class DataTablesListView(ListView):
    """
    Класс для отображения таблицы с данными в формате DataTables
    """
    serializer_class = None
    template_name = 'table.html'
    filtered_fields = None
    fields = None
    exclude = None
    depth_fields = None

    def get_fields(self):
        if self.fields and self.exclude:
            raise TypeError('Cannot set both `fields` and `exclude`')
        elif not self.fields and not self.exclude:
            raise TypeError('You must set either `fields` or `exclude`')
        elif self.fields == '__all__':
            info = model_meta.get_field_info(self.model)
            fields = [field for field in info.fields]
        elif self.exclude:
            info = model_meta.get_field_info(self.model)
            fields = [field for field in info.fields if field not in self.exclude]
        else:
            fields = self.fields
        if self.depth_fields:
            fields += self.depth_fields
        return fields

    @staticmethod
    def filter_by_search_term(queryset, fields, search_term):
        if not fields:
            raise TypeError('You must set `filtered_fields`')
        new_queryset = queryset.none()
        for field in fields:
            new_queryset |= queryset.filter(**{f'{field}__icontains': search_term})
        return new_queryset

    def get_columns(self):
        columns = [{
            'data': 'url',
            'orderable': False,
        }, ]
        for field in self.get_fields():
            if '__' in field:
                field = field.replace('__', '.')
            columns.append({'data': field})
        return columns

    @staticmethod
    def get_verbose_name(model, field):
        try:
            return model._meta.get_field(field).verbose_name
        except FieldDoesNotExist:
            return field

    def get_table_by_fields(self):
        doc, tag, text = Doc().tagtext()
        with tag('table', klass='table table-bordered table-hover dataTable', id='datatable'):
            for tag_name in ['thead', 'tbody']:
                with tag(tag_name):
                    with tag('tr'):
                        with tag('th'):
                            text('')
                        for field in self.get_fields():
                            with tag('th'):
                                if '__' in field:
                                    split_field = field.split('__')
                                    if self.model._meta.get_field(split_field[0]).related_model:
                                        try:
                                            text(self.get_verbose_name(self.model._meta.get_field(
                                                split_field[0]).related_model, split_field[1]))
                                        except FieldDoesNotExist:
                                            text(split_field[1])
                                    else:
                                        raise TypeError(f'This field {field} is not related. Please check your '
                                                        f'"depth_fields". You can use only related fields')
                                else:
                                    text(self.get_verbose_name(self.model, field))
        return indent(doc.getvalue())

    @staticmethod
    def get_language_json():
        with codecs.open(os.path.join(STATICFILES_DIRS[0], 'dist/json/datatables_language.json'), 'r', 'UTF-8') as file:
            return json.load(file)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['table'] = self.get_table_by_fields()
        context['columns'] = json.dumps(self.get_columns())
        context['language'] = json.dumps(self.get_language_json())
        return context

    def post(self, *args, **kwargs):
        if not self.serializer_class:
            raise TypeError('You must set `serializer_class`')
        start = int(self.request.POST.get('start'))
        length = int(self.request.POST.get('length'))
        search_term = self.request.POST.get('search[value]')
        draw = int(self.request.POST.get('draw'))

        queryset = self.get_queryset()
        records_total = queryset.count()

        if search_term:
            queryset = self.filter_by_search_term(queryset, self.filtered_fields, search_term)

        ordering = self.request.POST.get('order[0][column]')
        if ordering:
            ordering = self.get_fields()[int(ordering)]
            ordering_direction = self.request.POST.get('order[0][dir]')
            if ordering_direction == 'desc':
                ordering = f'-{ordering}'
            queryset = queryset.order_by(ordering)
        records_filtered = queryset.count()
        queryset_page = queryset[start: start + length]
        serializer = self.serializer_class(queryset_page, many=True)
        data = serializer.data
        return JsonResponse({
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data})
