################################################################
#                                                              #
# Purpose: convert keras model to Onnx                         #
#                                                              #
# Author:  Jona Bossio (jbossios@cern.ch                       #
#                                                              #
################################################################

Particle = 'photonsANDelectrons'
Version  = 'v26'

################################################################
# DO NOT MODIFY (below this line)
################################################################

# Choose appropriate eta binning
if 'pions' in Particle or Particle == 'all':
  EtaBins = ['{}_{}'.format(x*5,x*5+5) for x in range(16)]
else:
  EtaBins = ['{}_{}'.format(x*5,x*5+5) for x in range(26)]

# find the inputs
input_path = f'/eos/atlas/atlascerngroupdisk/proj-simul/AF3_Run3/Jona/Regression_Condor_Outputs/{Version}/'
input_file_format = os.path.join(input_path, f"{Particle}_{{}}_best_model.h5")
input_files = [input_file_format.format(etabin) for etabin in EtaBins]

# Create output folder
import os
output_path = os.path.join('Outputs', Particle, Version)
os.system(f'mkdir -p {output_path}')
# and find the outputs
output_file_format = os.path.join(output_path, f"{Particle}_{{}}_model.onnx")
output_files = [output_file_format.format(etabin) for etabin in EtaBins]

# send the command to the singularity
inputs = ' '.join(input_files)
outputs = ' '.join(output_files)
singularity_location = '/eos/atlas/atlascerngroupdisk/proj-simul/AF3_Run3/Jona/keras2onnx.sif'
command = f"singularity {singularity_location} {inputs} --outputs {outputs}"
os.system(command)
