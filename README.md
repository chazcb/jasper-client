# Otto

A fork of the popular Jasper voice computing platform with a focus on:

 - Decoupling audio input processing, voice output and conversation handlers
 - Removal of features not required for the above to run (wifi setup, sudo, etc.)
 - PEP8 via Flake8, code modularization, DRY
 - Replacement of magic strings w/ settings
 - Portability and documentation for setup in the README
 - Tests

# Installation and Setup for Development
## Install PyAudio
PyAudio is currently used for writing and reading .wav files. It's not available on pip (because internet?). If you are _not_ using a virtual environment, you can just download and install PyAudio with the C bindings included. However, if you want to install in a non-standard package location, you'll need to build PortAudio and then install PyAudio:
1. Download and install PortAudio [http://www.portaudio.com/download.html](http://www.portaudio.com/download.html)
    ./configure && make
    make install # may need sudo here
2. Download and build PyAudio [http://people.csail.mit.edu/hubert/pyaudio/compilation.html](http://people.csail.mit.edu/hubert/pyaudio/compilation.html)
    python setup.py install

## Install pocketsphinx

## Install Python packages
1. Install requirements from prod.txt (and test.txt if you want to run tests - recommended)
2. Install PyAudio (it's not on pip) http://people.csail.mit.edu/hubert/pyaudio/#downloads
2. Clone the Otto repository into your Pi at ~/jasper (or set up the githooks to push to your Pi).
3. Run `manage.py compile` to build initial set of language files.
4. Run `manage.py run` to start Otto.

## Acknowledgements
Otto is currently developed by [Charles Covey-Brandt](http://github.com/chazcb) and [Stephanie Stroud](http://github.com/stroud109) with the help of lots of contributors.

Jasper is developed by [Shubhro Saha](http://www.princeton.edu/~saha/) and [Charles Marsh](http://www.princeton.edu/~crmarsh/). Both can be reached by email at [saha@princeton.edu](mailto:saha@princeton.edu) and [crmarsh@princeton.edu](mailto:crmarsh@princeton.edu) respectively.

## Contributions

Jasper has recieved contributions by:
- [FRITZ|FRITZ](http://www.fritztech.net) ( [fritz@fritztech.net](mailto:fritz@fritztech.net) )
- [Exadrid](https://github.com/Exadrid)

## License

Jasper is released under the MIT license, a permissive free software license that lets you do anything you want with the source code, as long as you provide back attribution and ["don't hold \[us\] liable"](http://choosealicense.com). Note that this licensing only refers to the Jasper client code (i.e.,  the code on GitHub) and not to the disk image itself (i.e., the code on SourceForge).

The MIT License (MIT)

Copyright (c) 2014 Charles Marsh & Shubhro Saha

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
