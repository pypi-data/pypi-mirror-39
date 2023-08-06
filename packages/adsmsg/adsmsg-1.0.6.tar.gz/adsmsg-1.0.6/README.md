[![Build Status](https://travis-ci.org/adsabs/ADSPipelineMsg.svg)](https://travis-ci.org/adsabs/ADSPipelineMsg)
[![Coverage Status](https://coveralls.io/repos/adsabs/ADSPipelineMsg/badge.svg)](https://coveralls.io/r/adsabs/ADSPipelineMsg)


# adsmsg

## Short Summary

Message definitions based on [Google Protocol Buffers](https://developers.google.com/protocol-buffers/) to be used by ADS Pipelines.


## Development

To modify message definition, Protocol Buffers compiler should be installed:

```
sudo apt-get install autoconf automake libtool curl make g++ unzip
wget https://github.com/google/protobuf/releases/download/v3.3.0/protobuf-python-3.3.0.tar.gz
tar -zxvf protobuf-python-3.3.0.tar.gz
cd protobuf-3.3.0/
./configure
make
sudo make install
sudo ldconfig # refresh shared library cache.
```

Alternatively, a docker container can be built:

```
docker build -t adsmsg .
docker run -it --name adsmsg adsmsg
```
Or better, just run:

```
./rebuild.sh
```

Every time the protocol buffers specifications are changed.


### Testing

Travis will run tests automatically. You can manually run them in your machine with:

```
py.test
```

### Releasing new version to pypi

When a new release is ready, it should be uploaded to pypi. First, try the test environment:

```
virtualenv python
source python/bin/activate
pip install --upgrade setuptools wheel
python setup.py sdist bdist_wheel
pip install --upgrade twine
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
twine upload dist/*
```

Verify the [testing pypi repository](https://test.pypi.org/project/adsmsg/) and if everything looks good, you can proceed to upload to the [official repository](https://pypi.org/project/adsmsg/):

```
twine upload dist/*
```


## Maintainer(s)

Sergi
