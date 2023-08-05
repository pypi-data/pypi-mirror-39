from collections.abc import MutableMapping, Mapping


class NestedDict(MutableMapping):

    mapping_class = dict
    sequence_class = list

    def __init__(self, data, *, mapping_class=None, sequence_class=None):
        self.mapping_class = mapping_class or self.mapping_class
        self.sequence_class = sequence_class or self.sequence_class

        self._container = mapping_class()

        for key, value in (data.items() if isinstance(data, Mapping) else data):
            self[key] = value


    def __getitem__(self, key):
        if not "." in key:
            return self.container[key]
        key, remainder = key.split(".", 1)
        container = self.container
        for key_component in key.split("."):
            if key_component.isdigit():
                key_component = int(key_component)
            container = container[key_component]

        content = container
        if not isinstance(content, Mapping):
            return content

        return self.__class__(
            content,
            mapping_class=self.mapping_class,
            sequence_class=self.sequence_class
        )[remainder]

    def __setitem__(self, key):

    def __delitem__(self, key):


    def __iter__(self):
        for key in self.container:
            yield key

    def walk(self):
        pass

    def __len__(self):
        return len(self.container)
