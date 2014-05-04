#!/usr/bin/env python
import csv
from operator import itemgetter
import sys

from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.modelfactory import ModelFactory

MODEL_PARAMS = {
  'model': "CLA",
  'version': 1,
  'predictAheadTime': None,
  'modelParams': {
    'inferenceType': 'TemporalMultiStep',
    'sensorParams': {
      'verbosity' : 0,
      'encoders': {
        'token': {
          'fieldname': u'token',
          'name': u'token',
          'type': 'CategoryEncoder',
          'categoryList': list(set(map(str.strip, open("tokens.txt").readlines()))),
          'w': 21
        }
      },
      'sensorAutoReset' : None,
    },
      'spEnable': True,
      'spParams': {
        'spVerbosity' : 0,
        'globalInhibition': 1,
        'columnCount': 2048,
        'inputWidth': 0,
        'numActivePerInhArea': 40,
        'seed': 1956,
        'coincInputPoolPct': 0.5,
        'synPermConnected': 0.1,
        'synPermActiveInc': 0.1,
        'synPermInactiveDec': 0.01,
    },

    'tpEnable' : True,
    'tpParams': {
      'verbosity': 0,
        'columnCount': 2048,
        'cellsPerColumn': 32,
        'inputWidth': 2048,
        'seed': 1960,
        'temporalImp': 'cpp',
        'newSynapseCount': 20,
        'maxSynapsesPerSegment': 32,
        'maxSegmentsPerCell': 128,
        'initialPerm': 0.21,
        'permanenceInc': 0.1,
        'permanenceDec' : 0.1,
        'globalDecay': 0.0,
        'maxAge': 0,
        'minThreshold': 12,
        'activationThreshold': 16,
        'outputType': 'normal',
        'pamLength': 1,
      },
      'clParams': {
        'implementation': 'cpp',
        'regionName' : 'CLAClassifierRegion',
        'clVerbosity' : 0,
        'alpha': 0.0001,
        'steps': '1',
      },
      'trainSPNetOnlyIfRequested': False,
    },
}

model = ModelFactory.create(MODEL_PARAMS)
model.enableInference({"predictedField": "token"})
shifter = InferenceShifter()
out = csv.writer(sys.stdout)

with open("tokens.txt") as inp:
  for line in inp:
    token = line.strip()
    modelInput = {'token': token}
    result = shifter.shift(model.run(modelInput))
    if result.inferences["multiStepPredictions"][1]:
      out.writerow([token] + [y for x in sorted(result.inferences["multiStepPredictions"][1].items(), key=itemgetter(1)) for y in x])
