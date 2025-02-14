import pytorch_lightning as pl
from pathlib import Path
from loguru import logger

class ExportBaseCallback(pl.callbacks.ModelCheckpoint):
    """
    Basis-Export-Callback, der automatisch einen Batch aus dem Trainer zieht.
    """

    def __init__(self, output_dir="models", **kwargs):
        super().__init__(**kwargs)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.example_input = None  # Wird später automatisch gesetzt

    def get_example_input(self, trainer:pl.Trainer):
        """
        Holt sich einen Batch aus dem DataModule und speichert ihn als `self.example_input`.
        
        :param trainer: PyTorch Lightning Trainer.
        :return: Beispiel-Batch.

        :example:
        ```python
        from pytorch_lightning import Trainer
        from apu.ml.checkpoint import ExportBaseCallback

        trainer = Trainer(callbacks=[ExportBaseCallback()])
        trainer.fit(model)
        ```
        """
        if self.example_input is None:  # Nur einmal holen
            try:
                datamodule = trainer.datamodule
                if datamodule is None:
                    logger.error("❌ Kein DataModule gefunden.")
                    return None

                dataloader = datamodule.train_dataloader()
                if dataloader is None:
                    logger.error("❌ Kein train_dataloader() gefunden.")
                    return None
            
                batch = next(iter(dataloader))  # Nimm einen Batch
                if isinstance(batch, (tuple, list)):  # Falls (X, y)-Format
                    self.example_input = batch[0]
                else:
                    self.example_input = batch  # Falls nur X existiert

                logger.info("✅ Beispiel-Batch automatisch geladen.")

            except Exception as e:
                logger.error(f"❌ Konnte Beispiel-Batch nicht laden: {e}")
                return None
            
        return self.example_input
