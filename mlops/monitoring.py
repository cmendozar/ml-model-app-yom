import os
import neptune


class NepMonitoring:
    def __init__(self):
        self.project = os.environ.get("NEPTUNE_PROJECT")
        self.api_token = os.environ.get("NEPTUNE_API_TOKEN")
        self.model_id = os.environ.get("NEPTUNE_MODEL_ID")
        if not self.project or not self.api_token or not self.model_id:
            raise ValueError(
                "Environment variables for Neptune not set correctly"
            )
        self.model = neptune.init_model(
            with_id=self.model_id
        )

    def log_results_to_neptune(self, results, step):
        for col, metrics in results.items():
            self.model[f"comparison_results/{col}/{step}/k2"] = metrics['k2']
            self.model[f"comparison_results/{col}/{step}/p_value"] = metrics['p_value']
            if 'df1_descriptive' in metrics and metrics['df1_descriptive']:
                for stat, value in metrics['df1_descriptive'].items():
                    self.model[f"comparison_results/{col}/{step}/df1_descriptive/{stat}"] = value
            if 'df2_descriptive' in metrics and metrics['df2_descriptive']:
                for stat, value in metrics['df2_descriptive'].items():
                    self.model[f"comparison_results/{col}/{step}/df2_descriptive/{stat}"] = value
            if 'error' in metrics:
                self.model[f"comparison_results/{col}/{step}/error"] = metrics['error']

    def stop_model(self):
        self.model.stop()
