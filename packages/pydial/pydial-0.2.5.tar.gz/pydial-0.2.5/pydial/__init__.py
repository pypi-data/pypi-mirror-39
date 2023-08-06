# declare dynamic version
#  Tuple with version number : main_version, subversion, iteration_number, ...,  branch (test|prod|...)
#  Connect all information except last-one using a "." (dot). Last one is dash-connected if not none
__version_info__ = (0, 2, 5, None)

__version__ = '.'.join([str(i) for i in __version_info__[:-1]])
if __version_info__[-1] is not None:
    __version__ += ('-%s' % (__version_info__[-1],))
