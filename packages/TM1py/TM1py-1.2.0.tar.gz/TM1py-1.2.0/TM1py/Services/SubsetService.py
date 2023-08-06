# -*- coding: utf-8 -*-

from TM1py.Objects import Subset
from TM1py.Services.ObjectService import ObjectService
from TM1py.Services.ProcessService import ProcessService


class SubsetService(ObjectService):
    """ Service to handle Object Updates for TM1 Subsets (dynamic and static)
    
    """

    def __init__(self, rest):
        super().__init__(rest)
        self._process_service = ProcessService(rest)

    def create(self, subset, private=True):
        """ create subset on the TM1 Server

            :param subset: TM1py.Subset, the subset that shall be created
            :param private: boolean

            :return:
                string: the response
        """
        subsets = "PrivateSubsets" if private else "Subsets"
        request = '/api/v1/Dimensions(\'{}\')/Hierarchies(\'{}\')/{}' \
            .format(subset.dimension_name, subset.hierarchy_name, subsets)
        response = self._rest.POST(request, subset.body)
        return response

    def get(self, subset_name, dimension_name, hierarchy_name=None, private=True):
        """ get a subset from the TM1 Server

            :param subset_name: string, name of the subset
            :param dimension_name: string, name of the dimension
            :param hierarchy_name: string, name of the hierarchy
            :param private: Boolean

            :return: instance of TM1py.Subset
        """
        if not hierarchy_name:
            hierarchy_name = dimension_name
        subsets = "PrivateSubsets" if private else "Subsets"
        request = '/api/v1/Dimensions(\'{}\')/Hierarchies(\'{}\')/{}(\'{}\')?$expand=' \
                  'Hierarchy($select=Dimension,Name),' \
                  'Elements($select=Name)&$select=*,Alias'.format(dimension_name, hierarchy_name, subsets, subset_name)
        response = self._rest.GET(request=request)
        return Subset.from_dict(response.json())

    def get_all_names(self, dimension_name, hierarchy_name=None, private=True):
        """ get names of all private or public subsets in a hierarchy

        :param dimension_name:
        :param hierarchy_name:
        :param private: Boolean
        :return: List of Strings
        """
        hierarchy_name = hierarchy_name if hierarchy_name else dimension_name

        subsets = "PrivateSubsets" if private else "Subsets"
        request = '/api/v1/Dimensions(\'{}\')/Hierarchies(\'{}\')/{}?$select=Name' \
            .format(dimension_name, hierarchy_name, subsets)
        response = self._rest.GET(request=request)
        subsets = response.json()['value']
        return [subset['Name'] for subset in subsets]

    def update(self, subset, private=True):
        """ update a subset on the TM1 Server

        :param subset: instance of TM1py.Subset.
        :param private: Boolean
        :return: response
        """

        if private:
            # Just delete it and rebuild it, since there are no dependencies
            return self._update_private(subset)
        else:
            # Update it. Clear Elements with evil workaround
            return self._update_public(subset)

    def _update_private(self, subset):
        """ update a private subset on the TM1 Server

        :param subset: instance of TM1py.Subset
        :return: response
        """
        # Delete it
        request = '/api/v1/Dimensions(\'{}\')/Hierarchies(\'{}\')/PrivateSubsets(\'{}\')' \
            .format(subset.dimension_name, subset.hierarchy_name, subset.name)
        self._rest.DELETE(request, '')
        # Rebuild it
        return self.create(subset, True)

    def _update_public(self, subset):
        """ Update a public subset on the TM1 Server

        :param subset: instance of TM1py.Subset
        :return: response
        """
        # clear elements of subset. evil workaround! Should be done through delete on the Elements Collection
        # (which is currently not supported 10.2.2 FP6)
        ti = "SubsetDeleteAllElements(\'{}\', \'{}\');".format(subset.dimension_name, subset.name)
        self._process_service.execute_ti_code(lines_prolog=ti, lines_epilog='')
        # update subset
        request = '/api/v1/Dimensions(\'{}\')/Hierarchies(\'{}\')/Subsets(\'{}\')' \
            .format(subset.dimension_name, subset.hierarchy_name, subset.name)
        return self._rest.PATCH(request=request, data=subset.body)

    def delete(self, subset_name, dimension_name, hierarchy_name=None, private=True):
        """ Delete an existing subset on the TM1 Server

        :param subset_name: String, name of the subset
        :param dimension_name: String, name of the dimension
        :param hierarchy_name: String, name of the hierarchy
        :param private: Boolean
        :return:
        """
        hierarchy_name = hierarchy_name if hierarchy_name else dimension_name
        subsets = "PrivateSubsets" if private else "Subsets"
        request = '/api/v1/Dimensions(\'{}\')/Hierarchies(\'{}\')/{}(\'{}\')' \
            .format(dimension_name, hierarchy_name, subsets, subset_name)
        response = self._rest.DELETE(request=request, data='')
        return response

    def exists(self, subset_name, dimension_name, hierarchy_name=None, private=True):
        """checks if private or public subset exists

        :param subset_name: 
        :param dimension_name: 
        :param hierarchy_name:
        :param private:
        :return: boolean
        """
        hierarchy_name = hierarchy_name if hierarchy_name else dimension_name
        subset_type = 'PrivateSubsets' if private else "Subsets"
        request = "/api/v1/Dimensions('{}')/Hierarchies('{}')/{}('{}')" \
            .format(dimension_name, hierarchy_name, subset_type, subset_name)
        return self._exists(request)
