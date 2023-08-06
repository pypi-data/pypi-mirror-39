# Rest Framework
from rest_framework.exceptions import ValidationError


class IncludeMixin(object):
    @staticmethod
    def include_fields(request):
        if request is None:
            return []
        return request.GET.getlist('include[]')


class SerializerIncludeMixin(IncludeMixin):
    @property
    def fields(self):
        """Add requested extra fields."""
        fields = super(SerializerIncludeMixin, self).fields

        is_view_serializer = (
            self.root == self
            or (
                    self.parent == self.root
                    and getattr(self.parent, 'many', False)
            )
        )
        if not is_view_serializer:
            return fields

        try:
            request = self.context['request']
            extra_objects = self.extra_objects
        except (AttributeError, LookupError):
            return fields

        include_fields = self.include_fields(request)
        if not include_fields:
            return fields

        existing_fields = list(fields.keys())

        for included_field in existing_fields:
            real_field = included_field
            included_field = real_field

            if included_field.endswith('_id'):
                included_field = included_field[:-3]

            if included_field in include_fields:
                del fields[real_field]

        for included_field in include_fields:
            try:
                fields[included_field] = extra_objects[included_field]
            except KeyError:
                raise ValidationError('Wrong include: "%s".' % included_field)

        return fields


class QueryOptimizerMixin(IncludeMixin):
    def get_queryset(self):
        """Optimized DB query."""
        queryset = super(QueryOptimizerMixin, self).get_queryset()
        include = self.include_fields(self.request)

        try:
            select_related = self.select_related
        except AttributeError:
            pass
        else:
            for key, select in select_related.items():
                if key in include:
                    queryset = queryset.select_related(select)

        try:
            prefetch_related = self.prefetch_related
        except AttributeError:
            pass
        else:
            for key, prefetch in prefetch_related.items():
                if key in include:
                    queryset = queryset.prefetch_related(prefetch)

        return queryset
