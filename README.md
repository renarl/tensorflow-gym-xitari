# tensorflow-gym-xitari
A Docker image with TensorFlow, OpenAI Gym, and DeepMind Xitari

## Why I wrote this?
DeepMind uses the Xitari Atari emulator in their experiments with the Atari games. The Xitari environment has a slightly different behaviour from the Atari environment used in the OpenAI Gym. To reproduce the DeepMind results we need to use the Xitari environment. However, it is much easier to work with the API of the OpenAI Gym. To solve this problem, this image contains both the OpenAI Gym and the Xitari environment with bindings to python.

## Build
`docker build -f Dockerfile.gpu -t renarl/tensorflow-openai-gym-xitari:tf1.1.0-gym0.8.1-gpu-py3 .`

`docker build -f Dockerfile -t renarl/tensorflow-openai-gym-xitari:tf1.1.0-gym0.8.1-py3 .`

## RUN
`nvidia-docker run --name renars_xitari_gpu0 -it -v "$(pwd)/notebooks:/notebooks/host_dir -e PASSWORD=password -p 6007:6006 -p 8889:8888 --rm renarl/tensorflow-openai-gym-xitari:tf1.1.0-gym0.8.1-gpu-py3`

`docker run --name renars_xitari_cpu -it -v "$(pwd)/notebooks:/notebooks/host_dir -e PASSWORD=password -p 6007:6006 -p 8889:8888 renarl/tensorflow-openai-gym-xitari:tf1.1.0-gym0.8.1-py3`