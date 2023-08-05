from wagtail.wagtailadmin.edit_handlers import BaseFieldPanel

from wagtailgeowidget.widgets import (
    GeoField,
)

from wagtailgeowidget.app_settings import (
    GEO_WIDGET_ZOOM
)


class GeoPanel(BaseFieldPanel):
    def __init__(self, field_name, classname="", address_field="",
            zoom=GEO_WIDGET_ZOOM):
        self.field_name = field_name
        self.classname = classname
        self.address_field = address_field
        self.zoom = zoom

    def bind_to_model(self, model):
        field = model._meta.get_field(self.field_name)

        srid = getattr(field, 'srid', 4326)

        widget = type(str('_GeoField'), (GeoField,), {
            'address_field': self.address_field,
            'zoom': self.zoom,
            'srid': srid,
            'id_prefix': 'id_',
        })

        base = {
            'model': model,
            'field_name': self.field_name,
            'classname': self.classname,
            'widget': widget,
        }

        out = type(str('_GeoPanel'), (BaseFieldPanel,), base)
        return out
