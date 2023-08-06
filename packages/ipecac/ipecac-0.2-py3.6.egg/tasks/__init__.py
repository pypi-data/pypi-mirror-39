from invoke import Collection
from tasks import build, lint

ns = Collection()
ns.add_collection(Collection.from_module(build))
ns.add_collection(Collection.from_module(lint))
