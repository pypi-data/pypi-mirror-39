from invoke import Collection
from tasks import build, test

ns = Collection()
ns.add_collection(Collection.from_module(build))
ns.add_collection(Collection.from_module(test))
