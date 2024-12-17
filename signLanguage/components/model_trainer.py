import os
import sys
import yaml
import shutil
import zipfile
from signLanguage.utils.main_utils import read_yaml_file
from signLanguage.logger import logging
from signLanguage.exception import SignException
from signLanguage.entity.config_entity import ModelTrainerConfig
from signLanguage.entity.artifact_entity import ModelTrainerArtifact


class ModelTrainer:
    def __init__(self, model_trainer_config: ModelTrainerConfig):
        self.model_trainer_config = model_trainer_config

    def initiate_model_trainer(self,) -> ModelTrainerArtifact:
        logging.info("Entered initiate_model_trainer method of ModelTrainer class")

        try:
            # Check if sign-language-data.zip exists
            if not os.path.exists("sign-language-data.zip"):
                raise FileNotFoundError("The file 'sign-language-data.zip' is missing.")

            # Unzipping data using zipfile
            logging.info("Unzipping data")
            with zipfile.ZipFile("sign-language-data.zip", 'r') as zip_ref:
                zip_ref.extractall("./")
            os.remove("sign-language-data.zip")

            # Check if data.yaml exists
            if not os.path.exists("data.yaml"):
                raise FileNotFoundError("The file 'data.yaml' is missing after extracting the ZIP.")

            # Read num_classes from data.yaml
            with open("data.yaml", 'r') as stream:
                num_classes = str(yaml.safe_load(stream)['nc'])

            model_config_file_name = self.model_trainer_config.weight_name.split(".")[0]
            logging.info(f"Model Config File Name: {model_config_file_name}")

            # Update YOLOv5 model configuration
            config = read_yaml_file(f"yolov5/models/{model_config_file_name}.yaml")
            config['nc'] = int(num_classes)

            # Save updated config
            with open(f'yolov5/models/custom_{model_config_file_name}.yaml', 'w') as f:
                yaml.dump(config, f)

            # Run YOLOv5 training with modified parameters
            train_command = (
                f"python yolov5/train.py --img 320 "  # Reduced image size
                f"--batch-size 4 "  # Reduced batch size
                f"--epochs {self.model_trainer_config.no_epochs} "
                f"--data data.yaml "
                f"--cfg yolov5/models/custom_{model_config_file_name}.yaml "
                f"--weights {self.model_trainer_config.weight_name} "
                f"--name yolov5s_results --cache"
            )
            logging.info(f"Running training command: {train_command}")
            os.system(train_command)

            # Copy trained weights to appropriate locations
            trained_weights_path = "yolov5/runs/train/yolov5s_results3/weights/best.pt"
            if not os.path.exists(trained_weights_path):
                raise FileNotFoundError("Trained model weights not found at the expected path.")

            shutil.copy(trained_weights_path, "yolov5/")
            os.makedirs(self.model_trainer_config.model_trainer_dir, exist_ok=True)
            shutil.copy(trained_weights_path, self.model_trainer_config.model_trainer_dir)

            # Clean up folders
            for folder in ['train', 'test', 'yolov5/runs']:
                if os.path.exists(folder) and os.path.isdir(folder):
                    shutil.rmtree(folder)

            # Remove data.yaml
            if os.path.exists("data.yaml"):
                os.remove("data.yaml")

            # Create ModelTrainerArtifact
            model_trainer_artifact = ModelTrainerArtifact(
                trained_model_file_path="yolov5/best.pt",
            )

            logging.info("Exited initiate_model_trainer method of ModelTrainer class")
            logging.info(f"Model trainer artifact: {model_trainer_artifact}")

            return model_trainer_artifact

        except Exception as e:
            raise SignException(e, sys)
