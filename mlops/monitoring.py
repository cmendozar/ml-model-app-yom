import os
import neptune


class NepMonitoring:
    def __init__(self):
        self.project = os.environ.get("NEPTUNE_PROJECT")
        self.api_token = os.environ.get("NEPTUNE_API_TOKEN")
        if not self.project or not self.api_token:
            raise ValueError(
                "Environment variables for Neptune not set correctly"
            )
        self.run = None

    def start_run(self):
        self.run = neptune.init_run(
            project=self.project,
            api_token=self.api_token
        )
        return self.run

    def log_results_to_neptune(self, results):
        if self.run:
            for col, metrics in results.items():
                self.run[f"comparison_results/{col}/k2"] = metrics['k2']
                self.run[f"comparison_results/{col}/p_value"] = metrics['p_value']
                if 'df1_descriptive' in metrics and metrics['df1_descriptive']:
                    for stat, value in metrics['df1_descriptive'].items():
                        self.run[f"comparison_results/{col}/df1_descriptive/{stat}"] = value
                if 'df2_descriptive' in metrics and metrics['df2_descriptive']:
                    for stat, value in metrics['df2_descriptive'].items():
                        self.run[f"comparison_results/{col}/df2_descriptive/{stat}"] = value
                if 'error' in metrics:
                    self.run[f"comparison_results/{col}/error"] = metrics['error']

    def stop_run(self):
        if self.run:
            self.run.stop()
