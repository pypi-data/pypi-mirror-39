class ComparisonObject:

    def __init__(self):
        self.ucs = None
        self.value = None
        self.comparison_str = None
        self.operator = None
        self.reference = None
        self.difference = None

    def set_comparison(self, value, operator, reference_dn, difference_dn, ucs):
        self.ucs = ucs
        self.value = value
        self.operator = operator
        self.reference = reference_dn
        self.difference = difference_dn
        self.comparison_str = "{} {} {}".format(reference_dn, operator, difference_dn)

    def __str__(self):
        return "{}: {}".format(self.value, self.comparison_str)


class ListComparison:

    def __init__(self, reference_dict, difference_dict, ucs):
        self.ucs = ucs
        self.reference_dict = reference_dict
        self.difference_dict = difference_dict
        self.reference_dn = list(self.reference_dict.keys())[0]
        self.difference_dn = list(self.difference_dict.keys())[0]
        self.reference_list = list(self.reference_dict.values())[0]
        self.difference_list = list(self.difference_dict.values())[0]
        self.difference_results = []

    def compare(self, ignore_same=False):
        if not ignore_same:
            self._comparison_format(set(self.reference_list).intersection(self.difference_list), ['same'])

        self._comparison_format(set(self.reference_list).difference(self.difference_list), ['difference'])
        self._comparison_format(set(self.difference_list).difference(self.reference_list), ['reverse'])

        return self.difference_results

    def _comparison_format(self, set_data, comparison_type):
        if not isinstance(set_data, set):
            raise ValueError("Parameter 'set_data' expected type {} and received {}".format(
                set,
                type(set_data)
            ))

        if isinstance(comparison_type, list):
            if not [True for s in comparison_type if s in ['same', 'difference', 'reverse']]:
                raise ValueError("Parameter 'comparison_type' expected value {} and received {}".format(
                    ['difference', 'reverse', 'same'],
                    comparison_type
                ))

            for item in set_data:
                if 'difference' in comparison_type:
                    # what is in reference_list that is not in difference_list
                    comp_obj = ComparisonObject()
                    comp_obj.set_comparison(item, '<=', self.reference_dn, self.difference_dn, self.ucs)
                    self.difference_results.append(comp_obj)
                if 'reverse' in comparison_type:
                    # what is in difference_list that is not in reference_list
                    comp_obj = ComparisonObject()
                    comp_obj.set_comparison(item, '=>', self.reference_dn, self.difference_dn, self.ucs)
                    self.difference_results.append(comp_obj)
                if 'same' in comparison_type:
                    # what is in reference_list that is not in difference_list
                    comp_obj = ComparisonObject()
                    comp_obj.set_comparison(item, '==', self.reference_dn, self.difference_dn, self.ucs)
                    self.difference_results.append(comp_obj)
        else:
            raise ValueError("Parameter 'comparison_type' expected value {} and received {}".format(
                ['difference', 'reverse', 'same'],
                comparison_type
            ))

