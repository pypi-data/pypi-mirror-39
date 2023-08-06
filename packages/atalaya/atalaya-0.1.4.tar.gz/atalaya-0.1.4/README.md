# Atalaya

This framework provides a logger for pytorch models, it allows you to save the parameters, the state of the network, the state of the optimizer and allows also to visualize your data using tensorboardX or visdom.

## Install
```bash
pip install atalaya
```

## Example
Examples are provided in [examples](https://bitbucket.org/dmmlgeneva/frameworks/src/master/atalaya/examples/) directory, where we simply add the logger to an example of a pytorch implemetation ([source](https://github.com/pytorch/examples/blob/master/mnist/main.py)) in [example_1](https://bitbucket.org/dmmlgeneva/frameworks/src/master/atalaya/examples/example_1). In each [directory](https://bitbucket.org/dmmlgeneva/frameworks/src/master/atalaya/examples/) you have also the files created by the logger. There is a directory named logs and one named vizualize. The first one contains the logs of each experiment and the second one the files needed to visualize e.g. in tensorboard.

### Init
```python
from atalaya import Logger

logger = Logger()

# by default Logger uses tensorboardX as graher
# you can use visdom by changing the default value
logger = Logger(grapher='visdom')
```

### Parameters
You can add parameters (save directly when addParams is called), you can also load parameters from a previous experiment.
```python
args = parser.parse_args()

# add parameters to the logger
logger.add_parameters(args)

# load from previous experiment
args = logger.restore_parameters(args.path_of_previous_experiment)
```

### Informations
You can log information instead of use print, this way you will see the information in terminal and it will also be logged in train.log file for a later consultation.
```python
logger.info("message to log and print", "like in a print")

# you can also use it for warnings
logger.warning("message")
```

### store and restore (models and optimizers)
To save checkpoints and the best model you need to call save method in traning loop. You can choose with wich frequency to save a checkpoint and if we want to overwrite the previous and keep always the last saved.
```python
# before store, you need to add to the logger all you want to store using the logger.add('name', object) method

logger.add('model', model)
logger.add('optimizer', optimizer)

# and in the training loop
for epoch in epochs:
    ...
    # pay attention it really recomended to keep overwrite=True
    # if not you may have memory problems if e.g. you save your model
    # every epoch and you have 2000 epochs
    logger.store(train_loss, val_loss, save_every=1, overwrite=True)

```
And after the training you can load the best model and test it or before training you can load from a previous experience.
```python
logger.restore(best=True)
#or
logger.restore(path_to_a_checkpoint)
```

### visualizer
This logger as a wrapper to tensorboardX and visdom. It allows you to better visualize your experiments.
By default, for visdom, the server is localhost and the port is 8097. You can change them if you want when
you intitialize the Logger.
```python
# to add a scalar
logger.add_scalar('my_scalar', value, epoch)

# to add many scalars in a dictionary
values = {'mse_scalar':123.45, 'kl_scalar':32.33}
logger.register_plots(values, epoch, prefix='train')
# or to add list of scalars wit apply_mean argument
values = {'mse':[123.4, ..., 234.5], 'kl':[345.4, ..., 456.5]}
logger.register_plots(values, epoch, prefix='train', apply_mean=True)
```
