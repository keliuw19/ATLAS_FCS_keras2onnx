# keras2onnx_fcs

A singularity container holds the required environment for keras2onnx.
Please use with caution as this is untested (and currently non-functional).

## existing container

I have put a copy of the constructed container at
`/eos/atlas/atlascerngroupdisk/proj-simul/AF3_Run3/Jona/keras2onnx.sif`.
It's a large file though, so I anticipate that someone will delete it at some point.

## building the container

If the file is gone, you can build a new one.
The container requires sudo to build and is much easier to build on a linux box.
You will need singularity installed; follow the instructions on the [official webpage](https://sylabs.io/guides/3.0/user-guide/installation.html).

Then the build command is;

```bash
sudo singularity build keras2onnx.sif singularity.def
```

This takes the instructions from `singularity.def` and uses
them to construct a container object.
This process involves downloading an image of ubuntu and lots
of packages, so expect it to take some time.

## Running the container

The command to run the container has the form;

```bash
singularity run keras2onnx.sif /path/of/input/model_file.h5 /path/of/other_model.h5 --outputs /path/to/place/converted_model.onnx /path/to/place/other.onnx
```

The `--outputs` flag is optional, if you don't provide it the output files will go
to `/path/of/input/model_file.h5.onnx` (just getting `.onnx` appended to their path).


## current issues

It don't work right now because the command `tf.keras.models.load_model` needs
more definitions to run. The error message given by the container is;

```bash
$ singularity run keras2onnx.sif v49/Real_relu_pions_25_30_best_model.h5
Arguments received: v49/Real_relu_pions_25_30_best_model.h5
2022-05-27 09:39:07.330048: W tensorflow/stream_executor/platform/default/dso_loader.cc:64] Could not load dynamic library 'libcudart.so.11.0'; dlerror: libcudart.so.11.0: cannot open shared object file: No such file or directory; LD_LIBRARY_PATH: /.singularity.d/libs
2022-05-27 09:39:07.330070: I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
Traceback (most recent call last):
  File "ConvertList.py", line 2, in <module>
    import tensorflow as tf
  File "/home/henry/.local/lib/python3.8/site-packages/tensorflow/__init__.py", line 444, in <module>
    _ll.load_library(_main_dir)
  File "/home/henry/.local/lib/python3.8/site-packages/tensorflow/python/framework/load_library.py", line 154, in load_library
    py_tf.TF_LoadLibrary(lib)
tensorflow.python.framework.errors_impl.NotFoundError: /usr/local/lib/python3.8/dist-packages/tensorflow/core/kernels/libtfkernel_sobol_op.so: undefined symbol: _ZNK10tensorflow8OpKernel11TraceStringB5cxx11ERKNS_15OpKernelContextEb
Python returned 1
```

A more helpful error message is produced on my local machine (ipython helping I think);

```bash
...
    raise ValueError(
ValueError: Unknown loss function: weighted_mean_squared_error. Please ensure this object is passed to the `custom_objects` argument. See https://www.tensorflow.org/guide/keras/save_and_serialize#registering_the_custom_object for details.
```

For the full text, see `alternate_form_error.txt`.

