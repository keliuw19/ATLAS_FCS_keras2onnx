# import modules
import tensorflow as tf
import keras.backend
import keras2onnx
import argparse

parser = argparse.ArgumentParser(description="Take list of files to convert")
parser.add_argument('inputs', nargs='+',
                    help='Input files in keras format')
parser.add_argument('--outputs', nargs='+', default=None,
                    help="optionally, specify output location")
parser.add_argument('--custom', '--customobjects', default=None,
                    help="File path to a python file that countains a "
                    "custom object dict, must be stored in a top level "
                    "attribute called `custom_objects`.")
args = parser.parse_args()


n_inputs = len(args.inputs)
if args.outputs is None:
    args.outputs = [inp + ".onnx" for inp in args.inputs]
else:
    assert len(args.outputs) == len(args.inputs), \
        "Need the same number of inputs and outputs, " + \
        f"found inputs {args.inputs} and outputs {args.outputs}"

if args.custom is None:
    def get_custom_objects():
        # Define custom loss
        def weighted_mean_squared_error(y_true, y_pred):
            return keras.backend.mean(keras.backend.square(y_true-y_pred)*weights)

        custom = {'weighted_mean_squared_error': weighted_mean_squared_error}
        return custom
else:
    def get_custom_objects():
        import importlib.util
        import sys
        module_name = "custom_objects_module"

        spec = importlib.util.spec_from_file_location(module_name, args.custom)
        module = importlib.util.module_from_spec(spec)
        sys.modules[module_name] = module
        spec.loader.exec_module(module)
        if not hasattr(module, 'custom_objects'):
            message = "Could not find attribute " + \
                      "'custom_objects' in {}".format(args.custom)
            raise AttributeError(message)
        return module.custom_objects

custom_objects = get_custom_objects()

# Loop over eta bins (models)
for inp, out in zip(args.inputs, args.outputs):
    print(f'Convert model {inp} to {out}')
    model = tf.keras.models.load_model(inp, custom_objects=custom_objects)
    onnx_model = keras2onnx.convert_keras(model, model.name)
    keras2onnx.save_model(onnx_model, out)
 
print('>>> ALL DONE <<<')
