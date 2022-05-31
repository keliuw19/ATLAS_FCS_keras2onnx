# keras2onnx_fcs

A singularity container holds the required environment for keras2onnx.
Please use with caution as this is untested (it appears to work, but I haven't checked the `.onnx` files
that come out are well formed).

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
singularity run keras2onnx.sif /path/of/input/model_file.h5 /path/of/other_model.h5 --outputs /path/to/place/converted_model.onnx /path/to/place/other.onnx --custom /path/to/custom_objects.py
```

The `--outputs` flag is optional, if you don't provide it the output files will go
to `/path/of/input/model_file.h5.onnx` (just getting `.onnx` appended to their path).
The `--custom` flag is also optional, if given it should
be the path to a python file containing the attribute `custom_objects`
which is a dict of functions defining custom objects needed by tensorflow.
If the `--custom` flag is not given, some default custom objects
are passed.


