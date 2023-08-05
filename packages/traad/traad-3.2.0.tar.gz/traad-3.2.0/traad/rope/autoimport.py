import rope.contrib.autoimport

from traad.rope.validate import validate
import traad.trace


class AutoImportMixin:
    def init(self):
        self._autoimport = rope.contrib.autoimport.AutoImport(self.proj)
        self._autoimport.generate_cache()

    @traad.trace.trace
    @validate
    def import_assist(self, starting):
        return self._autoimport.import_assist(starting)

    @traad.trace.trace
    @validate
    def get_modules(self, name):
        return self._autoimport.get_modules(name)
