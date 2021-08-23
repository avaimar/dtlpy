import attr
import traceback
from collections import namedtuple

from .. import repositories, entities, services


@attr.s
class Feature(entities.BaseEntity):
    """
    Com entity
    """
    # platform
    id = attr.ib()
    entity_id = attr.ib()
    url = attr.ib(repr=False)
    context = attr.ib(repr=False)
    created_at = attr.ib()
    feature_set_id = attr.ib()
    feature_set = attr.ib()
    version = attr.ib()
    value = attr.ib()
    parent_id = attr.ib()

    # sdk
    _client_api = attr.ib(type=services.ApiClient, repr=False)
    _repositories = attr.ib(repr=False)

    ################
    # repositories #
    ################
    @_repositories.default
    def set_repositories(self):
        reps = namedtuple('repositories',
                          field_names=['features', 'features_sets'])
        features_repo = repositories.Features(client_api=self._client_api)
        r = reps(features=features_repo,
                 features_sets=repositories.FeatureSets(client_api=self._client_api))
        return r

    @property
    def features(self):
        assert isinstance(self._repositories.features, repositories.Features)
        return self._repositories.features

    @staticmethod
    def _protected_from_json(_json, client_api, is_fetched=True):
        """
        Same as from_json but with try-except to catch if error
        :param _json:
        :param client_api:
        :return:
        """
        try:
            feature = Feature.from_json(_json=_json,
                                        client_api=client_api,
                                        is_fetched=is_fetched)
            status = True
        except Exception:
            feature = traceback.format_exc()
            status = False
        return status, feature

    @classmethod
    def from_json(cls, _json, client_api, is_fetched=True):
        """
        Build a Feature entity object from a json

        :param is_fetched: is Entity fetched from Platform
        :param _json: _json response from host
        :param client_api: client_api
        :return: Feature object
        """
        inst = cls(
            id=_json.get('id', None),
            feature_set_id=_json.get('featureSetId', None),
            feature_set=_json.get('featureSet', None),
            entity_id=_json.get('entityId', None),
            url=_json.get('url', None),
            context=_json.get('context', None),
            created_at=_json.get('createdAt', None),
            version=_json.get('version', None),
            value=_json.get('value', None),
            parent_id=_json.get('parentId', None),
            client_api=client_api
        )
        inst.is_fetched = is_fetched
        return inst

    def to_json(self):
        """
        Returns platform _json format of object

        :return: platform json format of object
        """

        _json = {'createdAt': self.created_at,
                 'entityId': self.entity_id,
                 'id': self.id,
                 'featureSetId': self.feature_set_id,
                 'url': self.url,
                 'context': self.context,
                 'version': self.version,
                 'value': self.value,
                 }
        if self.parent_id is not None:
            _json['parentId'] = self.parent_id
        return _json
