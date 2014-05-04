FROM numenta/nupic
ADD . /home/docker/fee-fi-fo-fun
WORKDIR /home/docker/fee-fi-fo-fun
CMD python run.py
