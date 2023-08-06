# BeamNG.gym

## About

BeamNG.gym is a collection of [OpenAI Gym](https://gym.openai.com/)
environments that cover various driving tasks simulated in
[BeamNG.research](https://beamng.gmbh/research/).

##  Installation

Standard pip can be used to obtain the package of environments:

    pip install beamnggym

A copy of [BeamNG.research](https://beamng.gmbh/research/) is also required to
actually run the scenario. The basic version is freely available for *non-
commercial* use.

## Configuration

The environments assume an envirionment variable to be set that specifies where
[BeamNG.research](https://beamng.gmbh/research/) has been installed to. After
obtaining a copy, set an environment variable called `BNG_HOME` that contains
the path to your local installation's main directory -- the same that contains
the `EULA.odt` file.

## Usage

BeamNG.gym registers the environments with the OpenAI Gym registry, so after
the initial setup, the environments can be created using the factory method and
the respective environment's ID. For example:

```python
from random import uniform

import gym
import beamnggym

env = gym.make('BNG-WCA-Race-Geometry-v0')
env.reset()
total_reward, done = 0, False
# Drive around randomly until finishing
while not done:
    obs, reward, done, aux = env.step((uniform(-1, 1), uniform(-1, 1)))
    total_reward += reward
print('Achieved reward:', total_reward)
...
```

## Environments

Currently, the only environment is a time attack on the race track in the
West Coas USA level of BeamNG.drive. New environments are being developed.

### WCA Race

In this setting, the car spawns at the starting line of the race track in
West Coast USA and has to race one lap. A detailled description of the
observation and actions can be found in the documentation of the respective
class [WCARaceGeometry](https://github.com/BeamNG/BeamNG.gym).
