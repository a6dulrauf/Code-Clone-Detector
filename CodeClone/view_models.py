from com.vsa.metrics.ngram_metrics import NGram_Metrics
from com.vsa.plagiarism_techniques.cosine_distance import CosineDistance
from com.vsa.projects_cloning.project_clone.project_clone import ProjectClone
from com.vsa.projects_cloning.internal_clone.internal_clone import InternalClone

import os
import tempfile

from com.vsa.utilities.directories import Directory
from com.vsa.elements import languages

# Marker file written into a project folder to remember its language.
LANG_MARKER = '.ccd_language'


class ProjectViewModel:

    def __init__(self):
        self.result = None
        self.features1 = []
        self.features2 = []

    def run_test_Project(self, username, dirs=[], ngram=1, language='java'):
        project_clone = ProjectClone()
        nGram = NGram_Metrics(n=ngram, language=language)

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

    def run_test_Project(self, username, source_dir, project_no, language='java', tech=None):
        from com.vsa.multiple_files.csv_generator import CSVGenerator
        from com.vsa.metrics.ngram_metrics import NGram_Metrics
        if tech is None:
            tech = CosineDistance()

        # Regenerate the per-file feature CSVs straight from the project's source
        # files, so internal clone works on its own (no prior project comparison
        # needed) and can't read stale files from an earlier run.
        csv_dir = 'com/vsa/datasets/' + str(username) + '/multiple_csv_project' + str(project_no)
        Directory.delete_dir(csv_dir)
        CSVGenerator.generate_multiples_csv(source_dir, NGram_Metrics(2, language=language),
                                            username=username, project_no=project_no)

        internal_clone = InternalClone()
        result_dict = internal_clone.test_internal_clone(
            Directory.get_directory_of(csv_dir), tech, language=language)
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
    def is_supported_file(filename, language='java'):
        """True if filename has an extension for the given language."""
        if filename and len(str(filename)) > 0:
            return str(filename).lower().endswith(languages.get(language).extensions)
        return False

    @staticmethod
    def set_project_language(project_dir, language):
        """Persist a project's language in a marker file; returns the canonical name."""
        name = languages.get(language).name
        os.makedirs(project_dir, exist_ok=True)
        with open(os.path.join(project_dir, LANG_MARKER), 'w') as f:
            f.write(name)
        return name

    @staticmethod
    def get_project_language(project_dir):
        """Read a project's language marker; default 'java' if absent (old projects)."""
        try:
            with open(os.path.join(project_dir, LANG_MARKER)) as f:
                return languages.get(f.read().strip()).name
        except (OSError, IOError):
            return languages.DEFAULT

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
