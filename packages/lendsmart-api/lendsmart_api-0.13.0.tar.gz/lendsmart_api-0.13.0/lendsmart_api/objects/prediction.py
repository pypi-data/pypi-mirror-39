from __future__ import absolute_import

from lendsmart_api.objects import Base, Property


class PredictionChunk(Base):

    api_endpoint = '/prediction_chunks'

    properties = {
        "id": Property(identifier=True),
        "created": Property(is_datetime=True),
        "updated": Property(is_datetime=True),
        "label": Property(mutable=True, filterable=True),
        "install_code": Property(),
        "apps": Property(),
        "api_key": Property(),
    }


class PredictionWorkflow(Base):
    api_endpoint = 'prediction_workflows'
    properties = {
        "id": Property(identifier=True),
        "label": Property(),
        "clients_included": Property(),
        "price": Property()
    }
