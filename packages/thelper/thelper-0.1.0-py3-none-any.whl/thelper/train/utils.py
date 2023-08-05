"""Training/evaluation utilities module.

This module contains utilities and tools used to instantiate training sessions.
"""

import logging

import thelper.utils

logger = logging.getLogger(__name__)


def create_trainer(session_name, save_dir, config, model, loaders, ckptdata=None):
    """Instantiates the trainer object based on the type contained in the config dictionary.

    The trainer type is expected to be in the configuration dictionary's `trainer` field, under the `type` key. For more
    information on the configuration, refer to :class:`thelper.train.trainers.Trainer`. The instantiated type must be
    compatible with the constructor signature of :class:`thelper.train.trainers.Trainer`. The object's constructor will
    be given the full config dictionary and the checkpoint data for resuming the session (if available).

    Args:
        session_name: name of the training session used for printing and to create internal tensorboardX directories.
        save_dir: path to the session directory where logs and checkpoints will be saved.
        config: full configuration dictionary that will be parsed for trainer parameters and saved in checkpoints.
        model: model to train/evaluate; should be compatible with :class:`thelper.nn.utils.Module`.
        loaders: a tuple containing the training/validation/test data loaders (a loader can be ``None`` if empty).
        ckptdata: raw checkpoint to parse data from when resuming a session (if ``None``, will start from scratch).

    Returns:
        The fully-constructed trainer object, ready to begin model training/evaluation.

    .. seealso::
        | :class:`thelper.train.trainers.Trainer`

    """
    if "trainer" not in config or not config["trainer"]:
        raise AssertionError("config missing 'trainer' field")
    trainer_config = config["trainer"]
    if "type" not in trainer_config or not trainer_config["type"]:
        raise AssertionError("trainer config missing 'type' field")
    trainer_type = thelper.utils.import_class(trainer_config["type"])
    return trainer_type(session_name, save_dir, model, loaders, config, ckptdata=ckptdata)
