from com.vsa.metrics.ngram_metrics import NGram_Metrics
from com.vsa.plagiarism_techniques.cosine_distance import CosineDistance
from com.vsa.projects_cloning.project_clone.project_clone import ProjectClone
from com.vsa.projects_cloning.internal_clone.internal_clone import InternalClone

import os
import tempfile

from com.vsa.utilities.directories import Directory


class ProjectViewModel:

    def __init__(self):
        self.result = None
        self.features1 = []
        self.features2 = []

    def run_test_Project(self, username, dirs=[], ngram=1):
        project_clone = ProjectClone()
        nGram = NGram_Metrics(n=ngram)

        res = project_clone.test_project_clone(file_names=['project1.csv', 'project2.csv'], username=username, dirs=dirs, metrics=nGram,
                                               tech=CosineDistance())
        res = float("{0:.2f}".format(res*100))

        features1 = project_clone.features[0]
        features2 = project_clone.features[1]

        self.set_features(features1, features2)
        self.set_result(res)

        return res

    def set_features(self, features1, features2):
        self.features1 = features1
        self.features2 = features2

    def get_features(self):
        return self.features

    def set_result(self, result):
        self.result = result

    def get_result(self):
        return self.result

class InternalProjectViewModel:

    def __init__(self):
        self.result = None
        self.features = None

    def run_test_Project(self, username, project_no, tech=CosineDistance()):
        internal_clone = InternalClone()
        if project_no == 1:
            path = Directory.get_directory_of('com/vsa/datasets/'+str(username)+'/multiple_csv_project1/')
        elif project_no == 2 :
            path = Directory.get_directory_of('com/vsa/datasets/'+str(username)+'/multiple_csv_project2/')

        result_dict = internal_clone.test_internal_clone(path, tech)
        #print(result_dict)
        self.features = internal_clone.features
        self.set_result(result_dict)

        return result_dict

    def get_result(self):
        return self.result

    def set_result(self, result):
        self.result = result

class HelperViewModel:
    view_model = None
    project_files = []

    def __init__(self):
        pass

    @staticmethod
    def is_file_java(filename):
        if filename is not None and len(filename) > 0:
            if filename.endswith('.java'):
                return True
            return False

    @staticmethod
    def path_tempFile(data):
        tup = tempfile.mkstemp()  # make a tmp file
        f = os.fdopen(tup[0], 'w')  # open the tmp file for writing
        f.write(str(data.read()))  # write the tmp file
        f.close()

        ### return the path of the file
        filepath = tup[1]  # get the filepath
        return filepath

    @staticmethod
    def get_project_view_model(self):
        return self.view_model

    @staticmethod
    def project_view_model(model=None):
        view_model = model
        if model is None:
            return view_model


if __name__ == "__main__":

    Directory.delete_all_files('/Users/tabahi_user@generics.com/projects/project1')
