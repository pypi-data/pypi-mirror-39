from projex.lazymodule import lazy_import
from ..psqlconnection import PSQLStatement

orb = lazy_import('orb')


class CREATE_NAMESPACE(PSQLStatement):
    def __call__(self, namespace):
        """
        Modifies the table to add and remove the given columns.

        :param model: <orb.Model>
        :param add: [<orb.Column>, ..]
        :param remove: [<orb.Column>, ..]

        :return: <bool>
        """
        return 'CREATE SCHEMA IF NOT EXISTS "{0}"'.format(namespace), {}


PSQLStatement.registerAddon('CREATE NAMESPACE', CREATE_NAMESPACE())
