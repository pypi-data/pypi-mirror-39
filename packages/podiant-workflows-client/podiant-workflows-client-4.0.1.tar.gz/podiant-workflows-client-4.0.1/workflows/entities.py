class Entity(object):
    def __init__(self, data):
        self.id = data['id']
        self.__kind = data['type']

        for key, value in data['attributes'].items():
            setattr(self, key.replace('-', '_'), value)

        self.links = data.get('links', {})

    def __repr__(self):
        return '<%sEntity %s>' % (
            self.__kind.replace('-', ' ').title().replace(' ', ''),
            self.id
        )
