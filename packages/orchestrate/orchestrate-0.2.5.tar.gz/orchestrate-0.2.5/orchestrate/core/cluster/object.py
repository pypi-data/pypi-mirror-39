from orchestrate.core.provider.constants import (
  Provider,
  provider_to_string,
)


class Cluster(object):
  @property
  def name(self):
    raise NotImplementedError()

  @property
  def provider(self):
    raise NotImplementedError()

  @property
  def provider_string(self):
    return provider_to_string(self.provider)

class AWSCluster(Cluster):
  def __init__(self, underlying):
    self._underlying = underlying

  @property
  def name(self):
    return self._underlying['name']

  @property
  def provider(self):
    return Provider.AWS

class CustomCluster(Cluster):
  def __init__(self, name):
    self._name = name

  @property
  def name(self):
    return self._name

  @property
  def provider(self):
    return Provider.CUSTOM
