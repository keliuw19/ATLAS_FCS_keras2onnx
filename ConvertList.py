# import modules
import tensorflow as tf
import keras2onnx
import argparse

parser = argparse.ArgumentParser(description="Take list of files to convert")
parser.add_argument('inputs', nargs='+',
                    help='Input files in keras format')
parser.add_argument('--outputs', nargs='+', default=None,
                    help="optionally, specify output location")
args = parser.parse_args()

n_inputs = len(args.inputs)
if args.outputs is None:
    args.outputs = [inp + ".onnx" for inp in args.inputs]
else:
    assert len(args.outputs) == len(args.inputs), \
        "Need the same number of inputs and outputs, " + \
        f"found inputs {args.inputs} and outputs {args.outputs}"


# Loop over eta bins (models)
for inp, out in zip(args.inputs, args.outputs):
    print(f'Convert model {inp} to {out}')
    model = tf.keras.models.load_model(inp)
    onnx_model = keras2onnx.convert_keras(model, model.name)
    keras2onnx.save_model(onnx_model, out)
 
print('>>> ALL DONE <<<')
