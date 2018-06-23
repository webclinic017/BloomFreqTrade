FROM python:3.6-slim-stretch

# Install build deps
RUN apt-get update && \
  apt-get install -y --no-install-recommends curl build-essential && \
  rm -rf /var/lib/apt/lists/*

# Install TA-lib
RUN curl -L http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz | \
  tar xzvf - && cd ta-lib && \
  ./configure --prefix=/usr && \
  make && make install && \
  cd .. && rm -rf ta-lib

WORKDIR /freqtrade

# Install dependencies and freqtrade
COPY . /freqtrade/
RUN pip install --no-cache-dir -Ur /freqtrade/requirements.txt && \
  python setup.py install --optimize=1 && \
  apt-get remove -y curl build-essential && \
  apt-get autoremove -y

ENTRYPOINT ["freqtrade"]
