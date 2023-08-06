import logging
import pandas as pd
import tensorflow as tf

def variable_summaries(var):
  """Attach a lot of summaries to a Tensor (for TensorBoard visualization)."""
  with tf.name_scope('summaries'):
    mean = tf.reduce_mean(var)
    tf.summary.scalar('mean', mean)
    with tf.name_scope('stddev'):
      stddev = tf.sqrt(tf.reduce_mean(tf.square(var - mean)))
    tf.summary.scalar('stddev', stddev)
    tf.summary.scalar('max', tf.reduce_max(var))
    tf.summary.scalar('min', tf.reduce_min(var))
    tf.summary.histogram('histogram', var)


def configure_logger(log_file: str):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=log_file,
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger('').addHandler(console)
    return logging


def log_columns_to_csv(columns: dict, output_file: str) -> None:
    df = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in columns.items()]))
    df.to_csv(output_file)


def declare_paperspace_format(log):
    log.info("{\"chart\": \"accuracy\", \"axis\": \"epoch\"}")
    log.info("{\"chart\": \"loss\", \"axis\": \"epoch\"}")


def log_to_paperspace_format(log, epoch, accuracy, loss):
    log.info("{{\"chart\": \"accuracy\", \"y\": {:.4f}, \"x\": {}}}".format(accuracy, epoch))
    log.info("{{\"chart\": \"loss\", \"y\": {:.4f}, \"x\": {}}}".format(loss, epoch))
