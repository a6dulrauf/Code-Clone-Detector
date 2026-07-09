# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 00:56:35 2019

@author: Syed Hassan Ali
"""

import os

from com.vsa.dataset_handler.dataset_handler import DatasetHandler
from com.vsa.plagiarism_tester import Plagiarism_Tester
from com.vsa.utilities.directories import Directory
from com.vsa.metrics.ngram_metrics import NGram_Metrics


class InternalClone:

    def __init__(self):
        self.features = {}

    def test_internal_clone(self, path, tech, ngram=1, language='java'):
        tester = Plagiarism_Tester()
        dirs = Directory.search_directories(path, '.csv')
        dataset_handler = DatasetHandler()
        # Cross-platform basename (was split('\\'), which broke on macOS/Linux).
        name = [os.path.basename(x) for x in dirs if x.strip()]
        dfs = dataset_handler.read_csv(file_name=name, address=path)
        duplicate = []
        result = {}

        # All-pairs comparison of the files within this one project.
        for i in range(len(dfs)):
            for j in range(len(dfs)):
                if (i, j) not in duplicate and (j, i) not in duplicate and not i == j:
                    duplicate.append((i, j))
                    duplicate.append((j, i))
                    feature1 = [x for x in dfs[i].values]
                    feature2 = [x for x in dfs[j].values]

                    res = tester.run_test(metrics=NGram_Metrics(ngram, language=language),
                                          plagiarism_technique=tech,
                                          features=[feature1, feature2], is_project=True)
                    res = float("{0:.2f}".format(res * 100))
                    result[name[i].replace('.csv', '') + "-" + name[j].replace('.csv', '')] = res

        result['dfs'] = dfs
        result['dfsnames'] = name
        self.features = self.generate_features(result)
        return result

    def generate_features(self, result):
        features = {}
        for key in result.keys():
            if key not in ('dfs', 'dfsnames'):
                filenames = key.split('-')
                file1Index = result['dfsnames'].index(filenames[0] + '.csv')
                file2Index = result['dfsnames'].index(filenames[1] + '.csv')
                if str(filenames[0] + '-' + filenames[1]) not in features:
                    features[str(filenames[0] + '-' + filenames[1])] = [result['dfs'][file1Index],
                                                                        result['dfs'][file2Index]]
        return features
