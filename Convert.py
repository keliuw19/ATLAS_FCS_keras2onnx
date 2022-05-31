################################################################
#                                                              #
# Purpose: convert keras model to Onnx                         #
#                                                              #
# Author:  Jona Bossio (jbossios@cern.ch                       #
#                                                              #
################################################################

Particle = 'electronsANDphotons'
Version  = 'v26'

################################################################
# DO NOT MODIFY (below this line)
################################################################

import os
def ensure_folder_exists(folder):
    os.system(f"mkdir -p {folder}")

# Choose appropriate eta binning
if 'pions' in Particle or Particle == 'all':
  EtaBins = ['{}_{}'.format(x*5,x*5+5) for x in range(16)]
else:
  EtaBins = ['{}_{}'.format(x*5,x*5+5) for x in range(26)]

# find the inputs
input_folder = f'/eos/atlas/atlascerngroupdisk/proj-simul/AF3_Run3/Jona/Regression_Condor_Outputs/{Version}/'
input_names = [f"Real_relu_{Particle}_{etabin}_best_model.h5" for etabin in EtaBins]
input_paths = [os.path.join(input_folder, name) for name in input_names]

# Create output folder
output_base = '/eos/atlas/atlascerngroupdisk/proj-simul/AF3_Run3/Jona/Regression_Condor_ONNX'
output_folder = os.path.join(output_base, Particle, Version)
ensure_folder_exists(output_folder)
# and find the outputs
output_names = [f"{Particle}_{etabin}_model.onnx" for etabin in EtaBins]
output_paths = [os.path.join(output_folder, name) for name in output_names]

# need a temporary location to read and write from as
# the singularity doen't like writing directly to eos
temp_input = "temp_input"
ensure_folder_exists(temp_input)
temp_output = "temp_output"
ensure_folder_exists(temp_output)
temp_outputs = ' '.join(os.path.join(temp_output, name) for name in output_names)

# then more the inputs to a local location
print("Copying the inputs")
os.system(f"cp {' '.join(input_paths)} {temp_input}")
temp_inputs = ' '.join(os.path.join(temp_input, name) for name in input_names)

# send the command to the singularity
singularity_location = '/eos/atlas/atlascerngroupdisk/proj-simul/AF3_Run3/Jona/keras2onnx.sif'
command = f"singularity run {singularity_location} {temp_inputs} --outputs {temp_outputs}"
print(f"Running '{command}'")
os.system(command)

# first move the outputs to the intended eos directory
print(f"Moving outputs to {output_folder}")
os.system(f"mv {temp_output}/* {output_folder}")

# then clear the local input copies
print("Cleaning up")
os.system(f"rm -r {temp_input}")
os.system(f"rmdir {temp_output}")  # should be empty

print("Done")
