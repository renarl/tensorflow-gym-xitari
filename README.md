# tensorflow-gym-xitari
A Docker image with TensorFlow, OpenAI Gym, and DeepMind Xitari

## Why I wrote this?
DeepMind uses the Xitari Atari emulator in their experiments with the Atari games. The Xitari environment has a slightly different behaviour from the Atari environment used in the OpenAI Gym. To reproduce the DeepMind results we need to use the Xitari environment. However, it is much easier to work with the API of the OpenAI Gym. To solve this problem, this image contains both the OpenAI Gym and the Xitari environment with bindings to python.
