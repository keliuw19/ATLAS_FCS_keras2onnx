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

# Path to models
PATH = f'/eos/atlas/atlascerngroupdisk/proj-simul/AF3_Run3/Jona/Regression_Condor_Outputs/{Version}/'

# import modules
import tensorflow as tf
import keras2onnx

# Create output folders
import os
os.system('mkdir -p Outputs/{}/{}/'.format(Particle,Version))

# Loop over eta bins (models)
for etabin in EtaBins:
  InputFileName = f'{PATH}Real_relu_{Particle}_{etabin}_best_model.h5'
  print('Convert model in {}'.format(InputFileName))
  model         = tf.keras.models.load_model(InputFileName)
  onnx_model    = keras2onnx.convert_keras(model, model.name)
  outFile       = f'Outputs/{Particle}/{Version}/{Particle}_{etabin}_model.onnx'
  keras2onnx.save_model(onnx_model, outFile)

print('>>> ALL DONE <<<')
