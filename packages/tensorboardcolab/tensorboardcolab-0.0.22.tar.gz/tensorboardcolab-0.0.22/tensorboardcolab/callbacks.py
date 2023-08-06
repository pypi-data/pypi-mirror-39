import tensorflow as tf
from keras.callbacks import TensorBoard
import time
import os
import io

from tensorboardcolab.core import TensorBoardColab


class TensorBoardColabCallback(TensorBoard):
    def __init__(self, tbc=None, write_graph=True, **kwargs):
        # Make the original `TensorBoard` log to a subdirectory 'training'

        if tbc is None:
            return

        self.tbc = tbc

        log_dir = tbc.get_graph_path()

        training_log_dir = os.path.join(log_dir, 'training')
        super(TensorBoardColabCallback, self).__init__(training_log_dir, **kwargs)

        # Log the validation metrics to a separate subdirectory
        self.val_log_dir = os.path.join(log_dir, 'validation')

    def set_model(self, model):
        # Setup writer for validation metrics
        if self.tbc.is_eager_execution():
            self.val_writer = tf.contrib.summary.create_file_writer(self.val_log_dir)
        else:
            self.val_writer = tf.summary.FileWriter(self.val_log_dir)

        super(TensorBoardColabCallback, self).set_model(model)

    def on_epoch_end(self, epoch, logs=None):
        # Pop the validation logs and handle them separately with
        # `self.val_writer`. Also rename the keys so that they can
        # be plotted on the same figure with the training metrics
        logs = logs or {}
        val_logs = {k.replace('val_', ''): v for k, v in logs.items() if k.startswith('val_')}

        for name, value in val_logs.items():
            if self.tbc.is_eager_execution():
                self.val_writer.set_as_default()
                global_step = tf.train.get_or_create_global_step()
                global_step.assign(epoch)
                with tf.contrib.summary.always_record_summaries():
                    tf.contrib.summary.scalar(name, value.item())
            else:
                summary = tf.Summary()
                summary_value = summary.value.add()
                summary_value.simple_value = value.item()
                summary_value.tag = name
                self.val_writer.add_summary(summary, epoch)

        self.val_writer.flush()

        # Pass the remaining logs to `TensorBoard.on_epoch_end`
        logs = {k: v for k, v in logs.items() if not k.startswith('val_')}
        super(TensorBoardColabCallback, self).on_epoch_end(epoch, logs)

    def on_train_end(self, logs=None):
        super(TensorBoardColabCallback, self).on_train_end(logs)
        self.val_writer.close()
