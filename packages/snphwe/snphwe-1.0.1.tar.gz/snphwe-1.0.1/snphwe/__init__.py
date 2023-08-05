from pkg_resources import get_distribution

__version__ = get_distribution('snphwe').version

from snphwe.hwe_test import snphwe
