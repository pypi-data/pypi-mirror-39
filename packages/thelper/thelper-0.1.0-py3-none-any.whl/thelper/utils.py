"""General utilities module.

This module only contains non-ML specific functions, i/o helpers,
and matplotlib/pyplot drawing calls.
"""
import copy
import glob
import importlib
import inspect
import itertools
import json
import logging
import math
import os
import platform
import re
import sys
import time

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
import PIL.Image
import sklearn.metrics
import torch

logger = logging.getLogger(__name__)


class Struct(object):
    """Generic runtime-defined C-like data structure (maps constructor elems to fields)."""

    def __init__(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)

    def __repr__(self):
        return self.__class__.__name__ + ": " + str(self.__dict__)


def get_available_cuda_devices(attempts_per_device=5):
    """
    Tests all visible cuda devices and returns a list of available ones.

    Returns:
        List of available cuda device IDs (integers). An empty list means no
        cuda device is available, and the app should fallback to cpu.
    """
    if not torch.cuda.is_available() or torch.cuda.device_count() == 0:
        return []
    devices_available = [False] * torch.cuda.device_count()
    attempt_broadcast = False
    for attempt in range(attempts_per_device):
        for device_id in range(torch.cuda.device_count()):
            if not devices_available[device_id]:
                if not attempt_broadcast:
                    logger.debug("testing availability of cuda device #%d (%s)" % (
                        device_id, torch.cuda.get_device_name(device_id)
                    ))
                try:
                    torch.cuda.set_device(device_id)
                    test_val = torch.cuda.FloatTensor([1])
                    if test_val.cpu().item() != 1.0:
                        raise AssertionError("sometime's really wrong")
                    devices_available[device_id] = True
                except Exception:
                    pass
        attempt_broadcast = True
    return [device_id for device_id, available in enumerate(devices_available) if available]


def setup_cudnn(config):
    """Parses the provided config for CUDNN flags and sets up PyTorch accordingly."""
    if "cudnn" in config and isinstance(config["cudnn"], dict):
        config = config["cudnn"]
        if "benchmark" in config:
            cudnn_benchmark_flag = str2bool(config["benchmark"])
            logger.debug("cudnn benchmark mode = %s" % str(cudnn_benchmark_flag))
            torch.backends.cudnn.benchmark = cudnn_benchmark_flag
        if "deterministic" in config:
            cudnn_deterministic_flag = str2bool(config["deterministic"])
            logger.debug("cudnn deterministic mode = %s" % str(cudnn_deterministic_flag))
            torch.backends.cudnn.deterministic = cudnn_deterministic_flag
    else:
        if "cudnn_benchmark" in config:
            cudnn_benchmark_flag = str2bool(config["cudnn_benchmark"])
            logger.debug("cudnn benchmark mode = %s" % str(cudnn_benchmark_flag))
            torch.backends.cudnn.benchmark = cudnn_benchmark_flag
        if "cudnn_deterministic" in config:
            cudnn_deterministic_flag = str2bool(config["cudnn_deterministic"])
            logger.debug("cudnn deterministic mode = %s" % str(cudnn_deterministic_flag))
            torch.backends.cudnn.deterministic = cudnn_deterministic_flag


def load_checkpoint(ckpt, map_location=None):
    """Loads a session checkpoint via PyTorch, check its compatibility, and returns its data.

    Args:
        ckpt: a file-like object or a path to the checkpoint file.
        map_location: a function, string or a dict specifying how to remap storage
            locations. See ``torch.load`` for more information.

    Returns:
        Content of the checkpoint (a dictionary).
    """
    ckptdata = torch.load(ckpt, map_location=map_location)
    if not isinstance(ckptdata, dict):
        raise AssertionError("unexpected checkpoint data type")
    if "version" not in ckptdata:
        raise AssertionError("checkpoint at '%s' missing internal version tag" % ckpt)
    if not isinstance(ckptdata["version"], str) or len(ckptdata["version"].split(".")) != 3:
        raise AssertionError("unexpected checkpoint version formatting")
    # by default, checkpoints should be from the same minor version, we warn otherwise
    import thelper
    vers = [thelper.__version__.split("."), ckptdata["version"].split(".")]
    if vers[0][0] != vers[1][0]:
        raise AssertionError("incompatible checkpoint, major version mismatch (%s vs %s)" % (thelper.__version__, ckptdata["version"]))
    if vers[0][1] != vers[1][1]:
        answer = query_yes_no("Checkpoint minor version mismatch (%s vs %s); do you want to "
                              "attempt to load it anyway?" % (thelper.__version__, ckptdata["version"]))
        if not answer:
            logger.error("checkpoint out-of-date; user aborted")
            sys.exit(1)
    if vers[0] != vers[1]:
        logger.warning("checkpoint version mismatch with current framework version (%s vs %s)" % (thelper.__version__, ckptdata["version"]))
    return ckptdata


def import_class(fullname):
    """
    General-purpose runtime class importer.

    Args:
        fullname: the fully qualified class name to be imported.

    Returns:
        The imported class.
    """
    modulename, classname = fullname.rsplit('.', 1)
    module = importlib.import_module(modulename)
    return getattr(module, classname)


def get_class_logger(skip=0):
    """Shorthand to get logger for current class frame."""
    return logging.getLogger(get_caller_name(skip + 1).rsplit(".", 1)[0])


def get_func_logger(skip=0):
    """Shorthand to get logger for current function frame."""
    return logging.getLogger(get_caller_name(skip + 1))


def get_caller_name(skip=2):
    # source: https://gist.github.com/techtonik/2151727
    """Returns the name of a caller in the format module.class.method.

    Args:
        skip: specifies how many levels of stack to skip while getting the caller.

    Returns:
        An empty string is returned if skipped levels exceed stack height; otherwise,
        returns the requested caller name.
    """

    def stack_(frame):
        framelist = []
        while frame:
            framelist.append(frame)
            frame = frame.f_back
        return framelist

    stack = stack_(sys._getframe(1))
    start = 0 + skip
    if len(stack) < start + 1:
        return ""
    parentframe = stack[start]
    name = []
    module = inspect.getmodule(parentframe)
    # `modname` can be None when frame is executed directly in console
    if module:
        name.append(module.__name__)
    # detect classname
    if "self" in parentframe.f_locals:
        # I don't know any way to detect call from the object method
        # XXX: there seems to be no way to detect static method call - it will
        #      be just a function call
        name.append(parentframe.f_locals["self"].__class__.__name__)
    codename = parentframe.f_code.co_name
    if codename != "<module>":  # top level usually
        name.append(codename)  # function or a method
    del parentframe
    return ".".join(name)


def get_key(key, config, msg=None):
    """Returns a value given a dictionary key, throwing if not available."""
    if isinstance(key, list):
        if len(key) <= 1:
            if msg is not None:
                raise AssertionError(msg)
            else:
                raise AssertionError("must provide at least two valid keys to test")
        for k in key:
            if k in config:
                return config[k]
        if msg is not None:
            raise AssertionError(msg)
        else:
            raise AssertionError("config dictionary missing a field named as one of '%s'" % str(key))
    else:
        if key not in config:
            if msg is not None:
                raise AssertionError(msg)
            else:
                raise AssertionError("config dictionary missing '%s' field" % key)
        else:
            return config[key]


def get_key_def(key, config, default=None, msg=None):
    """Returns a value given a dictionary key, or the default value if it cannot be found."""
    if isinstance(key, list):
        if len(key) <= 1:
            if msg is not None:
                raise AssertionError(msg)
            else:
                raise AssertionError("must provide at least two valid keys to test")
        for k in key:
            if k in config:
                return config[k]
        return default
    else:
        if key not in config:
            return default
        else:
            return config[key]


def get_log_stamp():
    """Returns a print-friendly and filename-friendly identification string containing platform and time."""
    return str(platform.node()) + "-" + time.strftime("%Y%m%d-%H%M%S")


def get_git_stamp():
    """Returns a print-friendly SHA signature for the framework's underlying git repository (if found)."""
    try:
        import git
        repo = git.Repo(search_parent_directories=True)
        sha = repo.head.object.hexsha
        return str(sha)
    except (ImportError, AttributeError):
        return "unknown"


def get_env_list():
    """Returns a list of all packages installed in the current environment.

    If the required packages cannot be imported, the returned list will be empty. Note that some
    packages may not be properly detected by this approach, and it is pretty hacky, so use it with
    a grain of salt (i.e. logging is fine).
    """
    try:
        import pip
        pkgs = pip.get_installed_distributions()
        return sorted(["%s %s" % (pkg.key, pkg.version) for pkg in pkgs])
    except (ImportError, AttributeError):
        try:
            import pkg_resources as pkgr
            return sorted([str(pkg) for pkg in pkgr.working_set])
        except (ImportError, AttributeError):
            return []


def str2size(input_str):
    """Returns a (WIDTH, HEIGHT) integer size tuple from a string formatted as 'WxH'."""
    if not isinstance(input_str, str):
        raise AssertionError("unexpected input type")
    display_size_str = input_str.split('x')
    if len(display_size_str) != 2:
        raise AssertionError("bad size string formatting")
    return tuple([max(int(substr), 1) for substr in display_size_str])


def str2bool(s):
    """Converts a string to a boolean.

    If the lower case version of the provided string matches any of 'true', '1', or
    'yes', then the function returns ``True``.
    """
    if isinstance(s, bool):
        return s
    if isinstance(s, (int, float)):
        return s != 0
    if isinstance(s, str):
        positive_flags = ["true", "1", "yes"]
        return s.lower() in positive_flags
    raise AssertionError("unrecognized input type")


def clipstr(s, size, fill=" "):
    """Clips a string to a specific length, with an optional fill character."""
    if len(s) > size:
        s = s[:size]
    if len(s) < size:
        s = fill * (size - len(s)) + s
    return s


def lreplace(string, old_prefix, new_prefix):
    """Replaces a single occurrence of `old_prefix` in the given string by `new_prefix`."""
    return re.sub(r'^(?:%s)+' % re.escape(old_prefix), lambda m: new_prefix * (m.end() // len(old_prefix)), string)


def query_yes_no(question, default=None):
    """Asks the user a yes/no question and returns the answer.

    Args:
        question: the string that is presented to the user.
        default: the presumed answer if the user just hits ``<Enter>``. It must be 'yes',
            'no', or ``None`` (meaning an answer is required).

    Returns:
        ``True`` for 'yes', or ``False`` for 'no' (or their respective variations).
    """
    valid = {"yes": True, "ye": True, "y": True, "no": False, "n": False}
    if (isinstance(default, bool) and default) or \
       (isinstance(default, str) and default.lower() in ["yes", "ye", "y"]):
        prompt = " [Y/n] "
    elif (isinstance(default, bool) and not default) or \
         (isinstance(default, str) and default.lower() in ["no", "n"]):
        prompt = " [y/N] "
    else:
        prompt = " [y/n] "
    sys.stdout.flush()
    sys.stderr.flush()
    time.sleep(0.01)
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            if isinstance(default, str):
                return valid[default]
            else:
                return default
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes/y' or 'no/n'.\n")


def query_string(question, choices=None, default=None, allow_empty=False):
    """Asks the user a question and returns the answer (a generic string).

    Args:
        question: the string that is presented to the user.
        choices: a list of predefined choices that the user can pick from. If
            ``None``, then whatever the user types will be accepted.
        default: the presumed answer if the user just hits ``<Enter>``. If ``None``,
            then an answer is required to continue.
        allow_empty: defines whether an empty answer should be accepted.

    Returns:
        The string entered by the user.
    """
    sys.stdout.flush()
    sys.stderr.flush()
    time.sleep(0.01)
    while True:
        msg = question
        if choices is not None:
            msg += "\n\t(choices=%s)" % str(choices)
        if default is not None:
            msg += "\n\t(default=%s)" % default
        sys.stdout.write(msg + "\n")
        answer = input()
        if answer == "":
            if default is not None:
                return default
            elif allow_empty:
                return answer
        elif choices is not None:
            if answer in choices:
                return answer
        else:
            return answer
        sys.stdout.write("Please respond with a valid string.\n")


def get_save_dir(out_root, dir_name, config=None, resume=False):
    """Returns a directory path in which the app can save its data.

    If a folder with name ``dir_name`` already exists in the directory ``out_root``, then the user will be
    asked to pick a new name. If the user refuses, ``sys.exit(1)`` is called. If config is not None, it will
    be saved to the output directory as a json file. Finally, a ``logs`` directory will also be created in
    the output directory for writing logger files.

    Args:
        out_root: path to the directory root where the save directory should be created.
        dir_name: name of the save directory to create. If it already exists, a new one will be requested.
        config: dictionary of app configuration parameters. Used to overwrite i/o queries, and will be
            written to the save directory in json format to test writing. Default is ``None``.
        resume: specifies whether this session is new, or resumed from an older one (in the latter
            case, overwriting is allowed, and the user will never have to choose a new folder)

    Returns:
        The path to the created save directory for this session.
    """
    logger = get_func_logger()
    save_dir = out_root
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    save_dir = os.path.join(save_dir, dir_name)
    if not resume:
        overwrite = str2bool(config["overwrite"]) if config is not None and "overwrite" in config else False
        time.sleep(0.5)  # to make sure all debug/info prints are done, and we see the question
        while os.path.exists(save_dir) and not overwrite:
            overwrite = query_yes_no("Training session at '%s' already exists; overwrite?" % save_dir)
            if not overwrite:
                save_dir = query_string("Please provide a new save directory path:")
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        if config is not None:
            config_backup_path = os.path.join(save_dir, "config.latest.json")
            with open(config_backup_path, "w") as fd:
                json.dump(config, fd, indent=4, sort_keys=False)
    else:
        if not os.path.exists(save_dir):
            os.mkdir(save_dir)
        if config is not None:
            config_backup_path = os.path.join(save_dir, "config.latest.json")
            if os.path.exists(config_backup_path):
                config_backup = json.load(open(config_backup_path, "r"))
                if config_backup != config:
                    query_msg = "Config backup in '%s' differs from config loaded through checkpoint; overwrite?" % config_backup_path
                    answer = query_yes_no(query_msg)
                    if answer:
                        logger.warning("config mismatch with previous run; will overwrite latest backup in save directory")
                    else:
                        logger.error("config mismatch with previous run; user aborted")
                        sys.exit(1)
            with open(config_backup_path, "w") as fd:
                json.dump(config, fd, indent=4, sort_keys=False)
    logs_dir = os.path.join(save_dir, "logs")
    if not os.path.exists(logs_dir):
        os.mkdir(logs_dir)
    return save_dir


def safe_crop(image, tl, br, bordertype=cv.BORDER_CONSTANT, borderval=0):
    """Safely crops a region from within an image, padding borders if needed.

    Args:
        image: the image to crop (provided as a numpy array).
        tl: a tuple or list specifying the (x,y) coordinates of the top-left crop corner.
        br: a tuple or list specifying the (x,y) coordinates of the bottom-right crop corner.
        bordertype: border copy type to use when the image is too small for the required crop size.
            See ``cv2.copyMakeBorder`` for more information.
        borderval: border value to use when the image is too small for the required crop size. See
            ``cv2.copyMakeBorder`` for more information.

    Returns:
        The cropped image.
    """
    if not isinstance(image, np.ndarray):
        raise AssertionError("expected input image to be numpy array")
    if isinstance(tl, tuple):
        tl = list(tl)
    if isinstance(br, tuple):
        br = list(br)
    if not isinstance(tl, list) or not isinstance(br, list):
        raise AssertionError("expected tl/br coords to be provided as tuple or list")
    if tl[0] < 0 or tl[1] < 0 or br[0] > image.shape[1] or br[1] > image.shape[0]:
        image = cv.copyMakeBorder(image, max(-tl[1], 0), max(br[1] - image.shape[0], 0),
                                  max(-tl[0], 0), max(br[0] - image.shape[1], 0),
                                  borderType=bordertype, value=borderval)
        if tl[0] < 0:
            br[0] -= tl[0]
            tl[0] = 0
        if tl[1] < 0:
            br[1] -= tl[1]
            tl[1] = 0
    return image[tl[1]:br[1], tl[0]:br[0], ...]


def get_bgr_from_hsl(hue, sat, light):
    """Converts a single HSL triplet (0-360 hue, 0-1 sat & lightness) into an 8-bit RGB triplet."""
    # this function is not intended for fast conversions; use OpenCV's cvtColor for large-scale stuff
    if hue < 0 or hue > 360:
        raise AssertionError("invalid hue")
    if sat < 0 or sat > 1:
        raise AssertionError("invalid saturation")
    if light < 0 or light > 1:
        raise AssertionError("invalid lightness")
    if sat == 0:
        return (int(np.clip(round(light * 255), 0, 255)),) * 3
    if light == 0:
        return 0, 0, 0
    if light == 1:
        return 255, 255, 255

    def h2rgb(p, q, t):
        if t < 0:
            t += 1
        if t > 1:
            t -= 1
        if t < 1 / 6:
            return p + (q - p) * 6 * t
        if t < 1 / 2:
            return q
        if t < 2 / 3:
            return p + (q - p) * (2 / 3 - t) * 6
        return p

    q = light * (1 + sat) if (light < 0.5) else light + sat - light*sat
    p = 2 * light - q
    h = hue / 360
    return (int(np.clip(round(h2rgb(p, q, h - 1 / 3) * 255), 0, 255)),
            int(np.clip(round(h2rgb(p, q, h) * 255), 0, 255)),
            int(np.clip(round(h2rgb(p, q, h + 1 / 3) * 255), 0, 255)))


def draw_histogram(data, bins=50, xlabel="", ylabel="Proportion"):
    """Draws and returns a histogram figure using pyplot."""
    fig, ax = plt.subplots()
    ax.hist(data, density=True, bins=bins)
    if len(ylabel) > 0:
        ax.set_ylabel(ylabel)
    if len(xlabel) > 0:
        ax.set_xlabel(xlabel)
    ax.set_xlim(xmin=0)
    fig.show()
    return fig


def draw_popbars(labels, counts, xlabel="", ylabel="Pop. Count"):
    """Draws and returns a bar histogram figure using pyplot."""
    fig, ax = plt.subplots()
    xrange = range(len(labels))
    ax.bar(xrange, counts, align="center")
    if len(ylabel) > 0:
        ax.set_ylabel(ylabel)
    if len(xlabel) > 0:
        ax.set_xlabel(xlabel)
    ax.set_xticks(xrange)
    ax.set_xticklabels(labels)
    ax.tick_params(axis="x", labelsize="8", labelrotation=45)
    fig.show()
    return fig


def draw_classifs(images, labels_gt, labels_pred=None, labels_map=None):
    """Draws and returns a figure of classification results using pyplot."""
    nb_imgs = len(images) if isinstance(images, list) else images.shape[images.ndim - 1]
    if nb_imgs < 1:
        return
    grid_size_x = int(math.ceil(math.sqrt(nb_imgs)))
    grid_size_y = int(math.ceil(nb_imgs / grid_size_x))
    if grid_size_x * grid_size_y < nb_imgs:
        raise AssertionError("bad gridding for subplots")
    fig, axes = plt.subplots(grid_size_y, grid_size_x)
    plt.tight_layout()
    if nb_imgs == 1:
        axes = np.array(axes)
    for ax_idx, ax in enumerate(axes.reshape(-1)):
        if ax_idx < nb_imgs:
            if isinstance(images, list):
                ax.imshow(images[ax_idx], interpolation='nearest')
            else:
                ax.imshow(images[ax_idx, ...], interpolation='nearest')
            if labels_gt is not None:
                curr_label_gt = labels_map[labels_gt[ax_idx]] if labels_map else labels_gt[ax_idx]
            else:
                curr_label_gt = "<unknown>"
            if labels_pred is not None:
                curr_label_pred = labels_map[labels_pred[ax_idx]] if labels_map else labels_pred[ax_idx]
                xlabel = "GT={0}\nPred={1}".format(curr_label_gt, curr_label_pred)
            else:
                xlabel = "GT={0}".format(curr_label_gt)
            ax.set_xlabel(xlabel)
        ax.set_xticks([])
        ax.set_yticks([])
    fig.show()
    return fig


def draw_sample(sample, preds=None, image_key="image", label_key="label", mask_key="mask", block=False):
    """Draws and returns a figure of image samples using pyplot."""
    if not isinstance(sample, dict):
        raise AssertionError("expected dict-based sample")
    if image_key not in sample and label_key not in sample and len(sample) == 2:
        get_func_logger().warning("bad or missing image/label keys, will try to guess them for visualization")
        key1, key2 = sample.keys()
        if (isinstance(sample[key1], torch.Tensor) and sample[key1].dim() > 1) and \
           (isinstance(sample[key2], list) or (isinstance(sample[key2], torch.Tensor) and sample[key2].dim() == 1)):
            image_key, label_key = key1, key2
        elif (isinstance(sample[key2], torch.Tensor) and sample[key2].dim() > 1) and \
             (isinstance(sample[key1], list) or (isinstance(sample[key1], torch.Tensor) and sample[key1].dim() == 1)):
            image_key, label_key = key2, key1
        else:
            raise AssertionError("missing classification-related fields in sample dict, and could not find proper default types")
    if image_key not in sample:
        raise AssertionError("images not available in sample via key '%s'" % image_key)
    images = sample[image_key]
    if label_key not in sample:
        labels = None
    else:
        labels = sample[label_key]
        if not isinstance(labels, list) and not (isinstance(labels, torch.Tensor) and labels.dim() == 1):
            raise AssertionError("expected classification labels to be in list or 1-d tensor format")
        if isinstance(labels, torch.Tensor):
            labels = labels.tolist()
        if preds:
            if not isinstance(preds, list) and not (isinstance(preds, torch.Tensor) and preds.dim() == 1):
                raise AssertionError("expected classification predictions to be in list or 1-d tensor format")
            if isinstance(preds, torch.Tensor):
                preds = preds.tolist()
    # here we assume the sample's data has been tensor'd (so images are 4D, BxCxHxW)
    if isinstance(images, list) and all([isinstance(t, torch.Tensor) for t in images]):
        # if we have a list, it must be due to a duplicate/augmentation transformation stage
        if not all([image.shape == images[0].shape for image in images]):
            raise AssertionError("image shape mismatch throughout list")
        if labels:
            if not all([image.shape[0] == len(labels) for image in images]):
                raise AssertionError("image count mistmatch with label count")
            labels = labels * len(images)
        if preds:
            if not all([image.shape[0] == len(preds) for image in images]):
                raise AssertionError("image count mistmatch with pred count")
            preds = preds * len(images)
        images = torch.cat(images, 0)
    if not isinstance(images, torch.Tensor):
        raise AssertionError("expected classification images to be in 4-d tensor format")
    images = images.numpy().copy()
    if images.ndim != 4:
        raise AssertionError("unexpected dimension count for input images tensor")
    if labels and images.shape[0] != len(labels):
        raise AssertionError("images/labels count mismatch")
    if preds and images.shape[0] != len(preds):
        raise AssertionError("images/predictions count mismatch")
    images = np.transpose(images, (0, 2, 3, 1))  # BxCxHxW to BxHxWxC
    masks = None
    if mask_key in sample:
        if isinstance(sample[mask_key], torch.Tensor):
            masks = sample[mask_key].numpy().copy()
        if isinstance(sample[mask_key], np.ndarray):
            masks = sample[mask_key].copy()
    if masks is not None:
        # masks should have same dim count, but 2nd always equal to 1 (single channel)
        if masks.ndim != 4 or masks.shape[1] != 1:
            raise AssertionError("image/mask ndim mismatch")
        if (images.shape[0:3] != np.asarray(masks.shape)[[0, 2, 3]]).any():
            raise AssertionError("image/mask shape mismatch")
    image_list = []
    for batch_idx in range(images.shape[0]):
        image = images[batch_idx, ...]
        if image.ndim != 3:
            raise AssertionError("indexing should return a pre-squeezed array")
        if image.shape[2] == 2:
            image = np.dstack((image, image[:, :, 0]))
        elif image.shape[2] > 3:
            image = image[..., :3]
        image_normalized = np.empty_like(image, dtype=np.uint8).copy()  # copy needed here due to ocv 3.3 bug
        cv.normalize(image, image_normalized, 0, 255, cv.NORM_MINMAX, dtype=cv.CV_8U)
        image_list.append(image_normalized)
    fig = draw_classifs(image_list, labels, labels_pred=preds)  # normalize & pass mask to draw func also? todo
    if block:
        plt.show(block=block)
    else:
        plt.pause(0.01)
    return fig


def draw_errbars(labels, min, max, stddev, mean, xlabel="", ylabel="Raw Value"):
    """Draws and returns an error bar histogram figure using pyplot."""
    if min.shape != max.shape or min.shape != stddev.shape or min.shape != mean.shape:
        raise AssertionError("input dim mismatch")
    if len(min.shape) != 1 and len(min.shape) != 2:
        raise AssertionError("input dim unexpected")
    if len(min.shape) == 1:
        np.expand_dims(min, 1)
        np.expand_dims(max, 1)
        np.expand_dims(stddev, 1)
        np.expand_dims(mean, 1)
    nb_subplots = min.shape[1]
    fig, axs = plt.subplots(nb_subplots)
    xrange = range(len(labels))
    for ax_idx in range(nb_subplots):
        ax = axs[ax_idx]
        ax.locator_params(nbins=nb_subplots)
        ax.errorbar(xrange, mean[:, ax_idx], stddev[:, ax_idx], fmt='ok', lw=3)
        ax.errorbar(xrange, mean[:, ax_idx], [mean[:, ax_idx] - min[:, ax_idx], max[:, ax_idx] - mean[:, ax_idx]],
                    fmt='.k', ecolor='gray', lw=1)
        ax.set_xticks(xrange)
        ax.set_xticklabels(labels, visible=(ax_idx == nb_subplots - 1))
        ax.set_title("Band %d" % (ax_idx + 1))
        ax.tick_params(axis="x", labelsize="6", labelrotation=45)
    plt.tight_layout()
    fig.show()
    return fig


def draw_roc_curve(fpr, tpr, labels=None, size_inch=(5, 5), dpi=320):
    """Draws and returns an ROC curve figure using pyplot."""
    if not isinstance(fpr, np.ndarray) or not isinstance(tpr, np.ndarray):
        raise AssertionError("invalid inputs")
    if fpr.shape != tpr.shape:
        raise AssertionError("mismatched input sizes")
    if fpr.ndim == 1:
        fpr = np.expand_dims(fpr, 0)
    if tpr.ndim == 1:
        tpr = np.expand_dims(tpr, 0)
    if labels is not None:
        if isinstance(labels, str):
            labels = [labels]
        if len(labels) != fpr.shape[0]:
            raise AssertionError("should have one label per curve")
    else:
        labels = [None] * fpr.shape[0]
    fig = plt.figure(num="roc", figsize=size_inch, dpi=dpi, facecolor="w", edgecolor="k")
    fig.clf()
    ax = fig.add_subplot(1, 1, 1)
    for idx, label in enumerate(labels):
        auc = sklearn.metrics.auc(fpr[idx, ...], tpr[idx, ...])
        if label is not None:
            ax.plot(fpr[idx, ...], tpr[idx, ...], "b", label=("%s [auc = %0.3f]" % (label, auc)))
        else:
            ax.plot(fpr[idx, ...], tpr[idx, ...], "b", label=("auc = %0.3f" % auc))
    ax.legend(loc="lower right")
    ax.plot([0, 1], [0, 1], 'r--')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_ylabel("True Positive Rate")
    ax.set_xlabel("False Positive Rate")
    fig.set_tight_layout(True)
    return fig


def draw_confmat(confmat, class_list, size_inch=(5, 5), dpi=320, normalize=False, keep_unset=False):
    """Draws and returns an a confusion matrix figure using pyplot."""
    if not isinstance(confmat, np.ndarray) or not isinstance(class_list, list):
        raise AssertionError("invalid inputs")
    if confmat.ndim != 2:
        raise AssertionError("invalid confmat shape")
    if not keep_unset and "<unset>" in class_list:
        unset_idx = class_list.index("<unset>")
        del class_list[unset_idx]
        np.delete(confmat, unset_idx, 0)
        np.delete(confmat, unset_idx, 1)
    if normalize:
        row_sums = confmat.sum(axis=1)[:, np.newaxis]
        confmat = np.nan_to_num(confmat.astype(np.float) / np.maximum(row_sums, 0.0001))
    fig = plt.figure(num="confmat", figsize=size_inch, dpi=dpi, facecolor="w", edgecolor="k")
    fig.clf()
    ax = fig.add_subplot(1, 1, 1)
    ax.imshow(confmat, cmap=plt.cm.Blues)
    labels = [clipstr(label, 9) for label in class_list]
    tick_marks = np.arange(len(labels))
    ax.set_xlabel("Predicted", fontsize=7)
    ax.set_xticks(tick_marks)
    ax.set_xticklabels(labels, fontsize=4, rotation=-90, ha="center")
    ax.xaxis.set_label_position("bottom")
    ax.xaxis.tick_bottom()
    ax.set_ylabel("Real", fontsize=7)
    ax.set_yticks(tick_marks)
    ax.set_yticklabels(labels, fontsize=4, va="center")
    ax.yaxis.set_label_position("left")
    ax.yaxis.tick_left()
    thresh = confmat.max() / 2.
    for i, j in itertools.product(range(confmat.shape[0]), range(confmat.shape[1])):
        if not normalize:
            txt = ("%d" % confmat[i, j]) if confmat[i, j] != 0 else "."
        else:
            if confmat[i, j] >= 0.01:
                txt = "%.02f" % confmat[i, j]
            else:
                txt = "~0" if confmat[i, j] > 0 else "."
        color = "white" if confmat[i, j] > thresh else "black"
        ax.text(j, i, txt, horizontalalignment="center", fontsize=4, verticalalignment="center", color=color)
    fig.set_tight_layout(True)
    return fig


def draw_bboxes(image, rects, labels=None, confidences=None, win_size=None, thickness=1, show=True):
    """Draws and returns an image with bounding boxes via OpenCV."""
    if isinstance(image, PIL.Image.Image):
        image = np.asarray(image)
    if not isinstance(image, np.ndarray):
        raise AssertionError("expected input image to be numpy array")
    if not isinstance(rects, list) or not all([isinstance(r, (tuple, list)) and len(r) == 4 for r in rects]):
        raise AssertionError("expected input rectangles to be list of 4-elem tuples/lists (x,y,w,h)")
    if labels is not None and (not isinstance(labels, list) or len(labels) != len(rects)):
        raise AssertionError("bad labels list (check type/length)")
    if confidences is not None and (not isinstance(confidences, list) or len(confidences) != len(confidences)):
        raise AssertionError("bad confidences list (check type/length)")
    display_image = np.copy(image)
    if labels is None and confidences is None:
        # draw all bboxes with unique colors (shuffled)
        rects = copy.deepcopy(rects)
        np.random.shuffle(rects)
        for idx, rect in enumerate(rects):
            cv.rectangle(display_image, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]),
                         get_bgr_from_hsl(idx / len(rects) * 360, 1.0, 0.5), thickness)
    else:
        raise NotImplementedError  # TODO
    if win_size is not None:
        display_image = cv.resize(display_image, win_size)
    if show:
        cv.imshow("bboxes", display_image)
    return display_image


def apply_color_map(image, colormap, dst=None):
    """Applies a color map to an image of 8-bit color indices; works similarily to cv2.applyColorMap (v3.3.1)."""
    if image is None or not isinstance(image, np.ndarray) or image.ndim != 2 or image.dtype != np.uint8:
        raise AssertionError("invalid input image")
    if colormap is None or not isinstance(colormap, np.ndarray) or colormap.shape != (256, 1, 3) or colormap.dtype != np.uint8:
        raise AssertionError("invalid color map")
    out_shape = (image.shape[0], image.shape[1], 3)
    if dst is None:
        dst = np.empty(out_shape, dtype=np.uint8)
    elif not isinstance(dst, np.ndarray) or dst.shape != out_shape or dst.dtype != np.uint8:
        raise AssertionError("invalid output image")
    # using np.take might avoid an extra allocation...
    np.copyto(dst, colormap.squeeze()[image.ravel(), :].reshape(out_shape))
    return dst


def stringify_confmat(confmat, class_list, hide_zeroes=False, hide_diagonal=False, hide_threshold=None):
    """Transforms a confusion matrix array obtained in list or numpy format into a printable string."""
    if not isinstance(confmat, np.ndarray) or not isinstance(class_list, list):
        raise AssertionError("invalid inputs")
    columnwidth = 9
    empty_cell = " " * columnwidth
    fst_empty_cell = (columnwidth - 3) // 2 * " " + "t/p" + (columnwidth - 3) // 2 * " "
    if len(fst_empty_cell) < len(empty_cell):
        fst_empty_cell = " " * (len(empty_cell) - len(fst_empty_cell)) + fst_empty_cell
    res = "\t" + fst_empty_cell + " "
    for label in class_list:
        res += ("%{0}s".format(columnwidth) % clipstr(label, columnwidth)) + " "
    res += ("%{0}s".format(columnwidth) % "total") + "\n"
    for idx_true, label in enumerate(class_list):
        res += ("\t%{0}s".format(columnwidth) % clipstr(label, columnwidth)) + " "
        for idx_pred, _ in enumerate(class_list):
            cell = "%{0}d".format(columnwidth) % int(confmat[idx_true, idx_pred])
            if hide_zeroes:
                cell = cell if int(confmat[idx_true, idx_pred]) != 0 else empty_cell
            if hide_diagonal:
                cell = cell if idx_true != idx_pred else empty_cell
            if hide_threshold:
                cell = cell if confmat[idx_true, idx_pred] > hide_threshold else empty_cell
            res += cell + " "
        res += ("%{0}d".format(columnwidth) % int(confmat[idx_true, :].sum())) + "\n"
    res += ("\t%{0}s".format(columnwidth) % "total") + " "
    for idx_pred, _ in enumerate(class_list):
        res += ("%{0}d".format(columnwidth) % int(confmat[:, idx_pred].sum())) + " "
    res += ("%{0}d".format(columnwidth) % int(confmat.sum())) + "\n"
    return res


def fig2array(fig):
    """Transforms a pyplot figure into a numpy-compatible RGBA array."""
    fig.canvas.draw()
    w, h = fig.canvas.get_width_height()
    buf = np.fromstring(fig.canvas.tostring_argb(), dtype=np.uint8)
    buf.shape = (w, h, 4)
    buf = np.roll(buf, 3, axis=2)
    return buf


def get_glob_paths(input_glob_pattern, can_be_dir=False):
    """Parse a wildcard-compatible file name pattern for valid file paths."""
    glob_file_paths = glob.glob(input_glob_pattern)
    if not glob_file_paths:
        raise AssertionError("invalid input glob pattern '%s'" % input_glob_pattern)
    for file_path in glob_file_paths:
        if not os.path.isfile(file_path) and not (can_be_dir and os.path.isdir(file_path)):
            raise AssertionError("invalid input file at globbed path '%s'" % file_path)
    return glob_file_paths


def get_file_paths(input_path, data_root, allow_glob=False, can_be_dir=False):
    """Parse a wildcard-compatible file name pattern at a given root level for valid file paths."""
    if os.path.isabs(input_path):
        if '*' in input_path and allow_glob:
            return get_glob_paths(input_path)
        elif not os.path.isfile(input_path) and not (can_be_dir and os.path.isdir(input_path)):
            raise AssertionError("invalid input file at absolute path '%s'" % input_path)
    else:
        if not os.path.isdir(data_root):
            raise AssertionError("invalid dataset root directory at '%s'" % data_root)
        input_path = os.path.join(data_root, input_path)
        if '*' in input_path and allow_glob:
            return get_glob_paths(input_path)
        elif not os.path.isfile(input_path) and not (can_be_dir and os.path.isdir(input_path)):
            raise AssertionError("invalid input file at path '%s'" % input_path)
    return [input_path]
