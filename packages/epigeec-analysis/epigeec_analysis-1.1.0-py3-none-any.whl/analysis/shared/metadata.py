import json
import re
from analysis.shared.exception.geecanalysiserror import GeecAnalysisError
from analysis.shared.ihecjson import IhecJson

class MetadataFormatError(GeecAnalysisError):
    pass

class MetadataIOError(GeecAnalysisError):
    pass

class Metadata:

    def __init__(self, metadata={'datasets':{}}):
        self.metadata = _Metadata.make_metadata(metadata)

    @staticmethod
    def parse_metadatafile(filename):
        try:
            with open(filename, 'r') as json_file:
                return Metadata.load_from_file(json_file)
        except IOError as e:
            raise MetadataIOError(e)

    @staticmethod
    def load_from_file(json_file):
        try:
            data = json.load(json_file)
        except ValueError:
            raise MetadataFormatError('The metadata file is not a valid JSON.')

        try:
            if 'hub_description' in data:
                data = IhecJson.epigeec_format(data)

            if type(data['datasets']) is dict:
                return Metadata(data)
            elif type(data['datasets']) is list:
                data['datasets'] = {dataset['file_name']:dataset for dataset in data['datasets']}
                return Metadata(data)
        except KeyError:
            # The exception is raised later
            pass

        raise MetadataFormatError('The metadata file format is not supported.')

    def __str__(self):
        return self.metadata.to_json()

    def __eq__(self, other):
        if isinstance(other, Metadata):
            return self.metadata == other.metadata
        return False

    def __ne__(self, other):
        if isinstance(other, Metadata):
            return self.metadata != other.metadata
        return False

    def __cmp__(self, other):
        if isinstance(other, Metadata):
            return self.metadata == other.metadata
        return False

    def __len__(self):
        return len(self.metadata['datasets'])

    def __add__(self, other):
        return Metadata(self.metadata + other.metadata)

    @property
    def filenames(self):
        return self.metadata['datasets'].keys()

    def key_intersection(self, collection):
        return set(self.metadata['datasets'].keys()).intersection(collection)

    def find(self, patterns, is_inverted):
        md5lists = [self._find(pattern, is_inverted)
                    for pattern in patterns]

        file_names = self._fusion_md5lists(md5lists, is_inverted)

        return self.extract(file_names)

    def _find(self, pattern, is_inverted):
        return [file_name
                for file_name, dataset in self.metadata['datasets'].items()
                if any([str(data).find(pattern) >= 0
                        for data in dataset.values()]) != is_inverted]

    def match(self, regexs, is_inverted):
        md5lists = [self._match(regex, is_inverted)
                    for regex in regexs]

        file_names = self._fusion_md5lists(md5lists, is_inverted)

        return self.extract(file_names)

    def _match(self, regex, is_inverted):
        compiled_re = re.compile(regex)
        return [file_name
                for file_name, dataset in self.metadata['datasets'].items()
                if any([compiled_re.match(str(data))
                        for data in dataset.values()]) != is_inverted]

    def _fusion_md5lists(self, md5lists, is_inverted):
        if md5lists:
            first = set(md5lists[0])
            others = md5lists[1:]

            if is_inverted:
                file_names = first.intersection(*others)
            else:
                file_names = first.union(*others)
        else:
            file_names = []

        return file_names

    def extract(self, file_names):
        return Metadata(self.metadata.extract(file_names))

    def make_usable_categories(self, file_names, wanted_categories=None, unwanted_categories=[], ordered_categories=[]):
        all_categories = self.list_categories(file_names)

        filtered_categories = [a_cat for a_cat in all_categories if a_cat not in unwanted_categories]

        # if None or empty
        if not wanted_categories:
            return ([o_cat for o_cat in ordered_categories if o_cat in filtered_categories] +
                    [f_cat for f_cat in filtered_categories if f_cat not in ordered_categories])
        else:
            return [w_cat for w_cat in wanted_categories if w_cat in filtered_categories]

    def list_categories(self, file_names):
        categories_name = set()
        datasets = self.metadata['datasets']

        for file_name in file_names:
            if file_name in datasets:
                dataset = datasets[file_name]
                categories_name.update(dataset.keys())

        return list(categories_name)

    def obtain_formated_dataset(self, file_name, categories_names):
        return [self.obtain_dataset_item(file_name, category_name)
                for category_name in categories_names]

    def obtain_dataset_item(self, file_name, category_name):
        return self.metadata['datasets'][file_name][category_name]

    def extract_tag_names_file_names(self, file_names, category_name):
        tags = {}

        for file_name in file_names:
            tag_name = self.obtain_dataset_item(file_name, category_name)

            if tag_name not in tags:
                tags[tag_name] = [file_name]
            else:
                tags[tag_name].append(file_name)

        return tags

class _Metadata(dict):
    def __add__(self, other):
        generic_keys = self._extract_generic_keys(other)
        datasets = self['datasets'] + other['datasets']

        tuples = [('datasets', datasets),
                  ('count', len(datasets))]
        tuples += self._fusion_metadata_values(other, generic_keys)

        return _Metadata(tuples)

    def extract(self, file_names):
        generic_keys = self._extract_generic_keys()
        datasets = self['datasets'].extract(file_names)

        tuples = [('datasets', datasets),
                  ('count', len(datasets))]
        tuples += [(generic_key, self[generic_key])
                   for generic_key in generic_keys]

        return _Metadata(tuples)

    def _extract_generic_keys(self, other={}):
        fusioned_keys = set(self.keys()).union(other.keys())
        return fusioned_keys.difference(['datasets', 'count'])

    def _fusion_metadata_values(self, other, keys):
        return [(k, self._fusion_metadata_value(other, k))
                for k in keys]

    def to_json(self):
        data = self.convert_export_format()
        return json.dumps(data)

    def convert_export_format(self):
        datadict = {k:v
                    for k, v in self.items()
                    if k != 'datasets'}
        datadict['datasets'] = list(self['datasets'].values())
        return datadict

    def _fusion_metadata_value(self, other, key):
        a = self.get(key, 'NA')
        b = other.get(key, 'NA')
        return '{};{}'.format(a, b)

    @staticmethod
    def make_metadata(raw_metadata):
        tuples = [(k, v)
                  for k, v in raw_metadata.items()
                  if k != 'datasets']
        tuples.append(('datasets',
                       _Datasets.make_datasets(raw_metadata['datasets'])))
        return _Metadata(tuples)

class _Datasets(dict):
    def __missing__(self, key):
        return _UserDataset([('file_name', key)])

    def __add__(self, other):
        datasets = _Datasets()
        datasets.update(self)
        datasets.update(other)
        return datasets

    def extract(self, file_names):
        return _Datasets([(k, self[k])
                          for k in file_names
                          if k in self])

    @staticmethod
    def make_datasets(raw_datasets):
        return _Datasets([(k, _Dataset(v))
                          for k, v in raw_datasets.items()])

class _Dataset(dict):
    def __missing__(self, key): 
        return 'NA'

class _UserDataset(_Dataset):
    def __missing__(self, key):
        return 'User'
