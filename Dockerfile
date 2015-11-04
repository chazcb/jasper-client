FROM debian:wheezy

RUN apt-get update
RUN apt-get install -y build-essential

# Python things
RUN apt-get install -y python-setuptools python-dev

# Basic make things
RUN apt-get install -y libasound2 alsa-utils alsa-oss
RUN apt-get install -y git

# Install Pocketsphinx
WORKDIR /usr/src

# 1) download lots of stuff
RUN git clone --depth 1 https://github.com/cmusphinx/sphinxbase.git
RUN git clone --depth 1 https://github.com/cmusphinx/pocketsphinx.git

# 2) install things we need to make Pocketsphinx
RUN apt-get install -y bison bzip2 swig

RUN apt-get install -y autoconf automake libtool

# 3) make sphinx base, test and install
WORKDIR /usr/src/sphinxbase
RUN ./autogen.sh
RUN make clean
RUN ./configure --enable-fixed --without-lapack
RUN make
RUN make check
#RUN make -C sphinxbase install

# Install accoustic and language models
# RUN curl -L http://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/US%20English%20Generic%20Language%20Model/cmusphinx-5.0-en-us.lm.gz/download | tar -xz
# RUN curl -L http://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/US%20English%20Generic%20Acoustic%20Model/en-us.tar.gz/download | tar -xz
