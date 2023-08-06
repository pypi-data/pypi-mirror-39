import os
import random
from ibm_ai_openscale.supporting_classes import Feature

class DrugSelectionModel():

    def __init__(self, target_env, model_name=None):
        self._target_env = target_env
        if model_name is None:
            model_name = 'DrugSelectionModel'
        self._model_dir = os.path.join(os.path.dirname(__file__), model_name)

    def get_metadata(self):
        name = 'DrugSelectionModel'
        env_name = '' if self._target_env['name'] == 'YPPROD' else self._target_env['name']
        metadata = {
            'pipeline_metadata_file': os.path.join(self._model_dir, 'pipeline-meta.json'),
            'pipeline_file': os.path.join(self._model_dir, 'pipeline-content.tgz'),
            'model_name': name + env_name,
            'model_metadata_file': os.path.join(self._model_dir, 'model-meta.json'),
            'model_file': os.path.join(self._model_dir, 'model-content.gzip'),
            'deployment_name': name + env_name,
            'deployment_description': 'Created by aios fast path.'
        }
        return metadata

    def get_fairness_monitoring_params(self):
        params = {
            'features': [
                Feature('AGE', majority=[[49, 59], [60, 75]], minority=[[0, 48], [76, 99]], threshold=0.8),
                Feature('SEX', majority=['M'], minority=['F'], threshold=0.8)
            ],
            'prediction_column': 'predictedLabel',
            'favourable_classes': ['drugX', 'drugC'],
            'unfavourable_classes': ['drugY', 'drugA', 'drugB'],
            'min_records': 40
        }
        return params

    def get_feedback_params(self):
        params = {
            'fields': ['AGE', 'SEX', 'BP', 'CHOLESTEROL', 'NA', 'K', 'DRUG'],
            'values': [
                [58.0, 'F', 'HIGH', 'NORMAL', 0.868924, 0.061023, 'drugB'],
                [68.0, 'F', 'HIGH', 'NORMAL', 0.77541, 0.0761, 'drugB'],
                [65.0, 'M', 'HIGH', 'NORMAL', 0.635551, 0.056043, 'drugB'],
                [60.0, 'F', 'HIGH', 'HIGH', 0.800607, 0.060181, 'drugB'],
                [70.0, 'M', 'HIGH', 'HIGH', 0.658606, 0.047153, 'drugB'],
                [60.0, 'M', 'HIGH', 'HIGH', 0.805651, 0.057821, 'drugB'],
                [59.0, 'M', 'HIGH', 'HIGH', 0.816356, 0.058583, 'drugB'],
                [72.0, 'M', 'HIGH', 'NORMAL', 0.72142, 0.074552, 'drugB'],
                [53.0, 'F', 'HIGH', 'NORMAL', 0.760809, 0.060889, 'drugB'],
                [55.0, 'F', 'HIGH', 'HIGH', 0.637231, 0.058054, 'drugB'],
                [51.0, 'M', 'HIGH', 'NORMAL', 0.832467, 0.073392, 'drugB'],
                [49.0, 'M', 'HIGH', 'NORMAL', 0.500169, 0.079788, 'drugA'],
                [39.0, 'M', 'HIGH', 'HIGH', 0.731091, 0.075652, 'drugA'],
                [26.0, 'F', 'HIGH', 'NORMAL', 0.781928, 0.063535, 'drugA'],
                [49.0, 'M', 'HIGH', 'NORMAL', 0.538183, 0.061859, 'drugA'],
                [31.0, 'M', 'HIGH', 'NORMAL', 0.749717, 0.06678, 'drugA'],
                [20.0, 'F', 'HIGH', 'HIGH', 0.887426, 0.078798, 'drugA'],
                [42.0, 'M', 'HIGH', 'NORMAL', 0.85794, 0.067203, 'drugA'],
                [48.0, 'M', 'HIGH', 'NORMAL', 0.769197, 0.073633, 'drugA'],
                [47.0, 'M', 'HIGH', 'HIGH', 0.56332, 0.054152, 'drugA'],
                [23.0, 'M', 'HIGH', 'HIGH', 0.53406, 0.066666, 'drugA'],
                [68.0, 'M', 'LOW', 'HIGH', 0.726677, 0.070616, 'drugC'],
                [26.0, 'F', 'LOW', 'HIGH', 0.578002, 0.040819, 'drugC'],
                [32.0, 'F', 'LOW', 'HIGH', 0.730854, 0.075256, 'drugC'],
                [47.0, 'F', 'LOW', 'HIGH', 0.539774, 0.05362, 'drugC'],
                [28.0, 'F', 'LOW', 'HIGH', 0.656292, 0.049997, 'drugC'],
                [22.0, 'M', 'LOW', 'HIGH', 0.526672, 0.064617, 'drugC'],
                [49.0, 'M', 'LOW', 'HIGH', 0.655222, 0.062181, 'drugC'],
                [18.0, 'F', 'NORMAL', 'NORMAL', 0.553567, 0.063265, 'drugX'],
                [49.0, 'M', 'LOW', 'NORMAL', 0.625889, 0.056828, 'drugX'],
                [53.0, 'M', 'NORMAL', 'HIGH', 0.644936, 0.045632, 'drugX'],
                [46.0, 'M', 'NORMAL', 'NORMAL', 0.526226, 0.072234, 'drugX'],
                [39.0, 'M', 'LOW', 'NORMAL', 0.604973, 0.043404, 'drugX'],
                [39.0, 'F', 'NORMAL', 'NORMAL', 0.517515, 0.053301, 'drugX'],
                [15.0, 'M', 'NORMAL', 'HIGH', 0.64236, 0.07071, 'drugX'],
                [23.0, 'M', 'NORMAL', 'HIGH', 0.593596, 0.048417, 'drugX'],
                [50.0, 'F', 'NORMAL', 'NORMAL', 0.601915, 0.048957, 'drugX'],
                [66.0, 'F', 'NORMAL', 'NORMAL', 0.611333, 0.075412, 'drugX'],
                [67.0, 'M', 'NORMAL', 'NORMAL', 0.846892, 0.077711, 'drugX'],
                [60.0, 'M', 'NORMAL', 'NORMAL', 0.645515, 0.063971, 'drugX'],
                [45.0, 'M', 'LOW', 'NORMAL', 0.532632, 0.063636, 'drugX'],
                [17.0, 'M', 'NORMAL', 'NORMAL', 0.722286, 0.06668, 'drugX'],
                [24.0, 'F', 'NORMAL', 'HIGH', 0.80554, 0.07596, 'drugX']
            ]
        }
        return params

    def get_explainability_params(self):
        return ['SEX', 'BP', 'CHOLESTEROL']

    def get_history_payload_file(self):
        return os.path.join(self._model_dir, 'historypayloads.json')

    def get_history_fairness_file(self):
        return os.path.join(self._model_dir, 'historyfairness.json')

    def get_score_input(self):
        return {
            'fields': ['AGE', 'SEX', 'BP', 'CHOLESTEROL', 'NA', 'K'],
            'values': [[random.randint(15, 80),
                      random.choice(['F', 'M']),
                      random.choice(['HIGH', 'LOW', 'NORMAL']),
                      random.choice(['HIGH', 'NORMAL']),
                      random.uniform(0.5, 0.9),
                      random.uniform(0.02, 0.08)]]
        }
