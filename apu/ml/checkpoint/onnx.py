import onnx
import onnxsim
from pathlib import Path
import torch
from loguru import logger

from apu.ml.checkpoint.baseModel import ExportBaseCallback

class ONNXExportCallback(ExportBaseCallback):
    """
    Erbt von ModelCheckpoint und exportiert das beste Modell nach ONNX **direkt nach dem Speichern des Checkpoints**.
    """

    def __init__(self, output_dir="models", simplify = False, **kwargs):
        """
        :param output_dir: Verzeichnis für exportierte Modelle.
        :param kwargs: Zusätzliche Parameter für ModelCheckpoint.
        """
        super().__init__(**kwargs)  
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.simplify = simplify   
        self.best_onnx_model_path = None


    def on_validation_end(self, trainer, pl_module):
        '''
        Exportiert das Modell nach ONNX.

        :param trainer: PyTorch Lightning Trainer.
        :param pl_module: PyTorch Lightning Modul.

        :example:
        ```python
        from pytorch_lightning import Trainer
        from apu.ml.checkpoint import ONNXExportCallback

        trainer = Trainer(callbacks=[ONNXExportCallback()])
        trainer.fit(model)
        ```
        '''

        super().on_validation_end(trainer, pl_module)

        best_checkpoint_path = self.best_model_path
        if not best_checkpoint_path or not Path(best_checkpoint_path).exists():
            logger.warning("❌ Kein gültiger Checkpoint gefunden. Export übersprungen.")
            return

        logger.info(f"🔹 Konvertiere bestes Modell: {best_checkpoint_path}")

        # Lade das Modell und setze es in eval-Modus
        pl_module.load_state_dict(torch.load(best_checkpoint_path)["state_dict"])
        pl_module.eval()

        # Beispiel-Input automatisch holen
        example_input = self.get_example_input(trainer)
        if example_input is None:
            logger.warning("❌ Kein Beispiel-Input verfügbar. TensorRT-Export übersprungen.")
            return  

        # Exportiere das Modell zu ONNX
        checkpoint_name = Path(best_checkpoint_path).stem
        onnx_path = self.output_dir / f"{checkpoint_name}.onnx"
        logger.info(f"🔹 Exportiere ONNX: {onnx_path}")

        try:
            torch.onnx.export(
                pl_module,
                example_input,
                onnx_path,
                opset_version=11,
                export_params=True,
                input_names=["input"],
                output_names=["output"],
                dynamic_axes={"input": {0: "batch_size"}, "output": {0: "batch_size"}}
            )
            logger.info(f"✅ ONNX-Modell gespeichert: {onnx_path}")
        except Exception as e:
            logger.error(f"❌ Fehler beim ONNX-Export: {e}")
            return

        # ONNX vereinfachen
        if self.simplify:
            logger.info("🔹 ONNX-Modell wird optimiert...")
            try:
                simplified_model, check = onnxsim.simplify(onnx_path)
                if check:
                    onnx.save(simplified_model, onnx_path)
                    logger.info(f"✅ Vereinfachtes ONNX-Modell gespeichert: {onnx_path}")
                else:
                    logger.warning("❌ ONNX-Simplifikation fehlgeschlagen.")
            except Exception as e:
                logger.error(f"❌ Fehler bei ONNX-Simplifikation: {e}")

        self.best_onnx_model_path = onnx_path
        logger.info(f"✅ ONNX-Modell gespeichert: {onnx_path}")
