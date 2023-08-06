from uuid import uuid4
from .exceptions import ConfigurationException
from .constants import SLUGIFIER
from geonode.people.models import Profile


class LayerConfig(object):
    def __init__(self, config={}):
        if not isinstance(config, dict):
            raise ConfigurationException("config_dict should be dict")
        self.config_dict = config
        self.name = getattr(self.config_dict, 'name', None)
        self.permissions = getattr(self.config_dict, 'permissions', None)
        self.overwrite = getattr(self.config_dict, 'overwrite', False)
        self.temporary = getattr(self.config_dict, 'temporary', False)
        self.launder = getattr(self.config_dict, 'launder', False)
        self.username = getattr(self.config_dict, 'username', False)

    def get_user(self):
        if not self.username:
            user_query = Profile.objects.filter(is_superuser=True)
            if user_query.count():
                user = user_query.first()
            else:
                pass
            self.username = user.username
        else:
            user = Profile.objects.get(username=self.username)
        return user

    def _unique_name(self):
        from .layers import OSGEOLayer
        if len(self.name) > 63:
            self.name = self.name[:63]
        if not OSGEOLayer.check_geonode_layer(self.name):
            return str(self.name)
        suffix = uuid4().__str__().split('-').pop()
        if len(self.name) < (63 - (len(suffix) + 1)):
            self.name += "_" + suffix
        else:
            self.name = self.name[:((63 - len(suffix)) - 2)] + "_" + suffix

        return self._unique_name()

    def get_new_name(self):
        self.name = SLUGIFIER(self.name.lower())
        if not self.overwrite:
            return self._unique_name()
        return self.name

    def as_dict(self):
        d = vars(self)
        d.pop('config_dict')
        return d
