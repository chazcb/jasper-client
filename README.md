# Otto

A fork of the Jasper voice computing platform with a focus on:

 - Decoupling audio input processing, voice output and conversation handlers
 - Removal of features not required for the above to run (wifi setup, sudo, etc.)
 - PEP8 via Flake8, code modularization, DRY
 - Replacement of magic strings w/ settings
 - Portability and documentation for setup in the README
 - Tests

## Installation for development

We tried really hard to reduce dependencies and make this application installable inside a virtualenv only, but because of the large number of C-bindings and non-pip packages, it ends up being easier (sadly) to install requirements in system wide packages. For developing on a Mac:

### Install Homebrew

Because if you are on a Mac, you should use Homebrew [http://brew.sh/](http://brew.sh/).

### Install the Python binding for GStreamer

This is what we'll use to record, compress, and play audio files. GStreamer requires the Quartz framework, you'll have to grab it first before installing: `brew install gst-python010 gst-plugins-good010 gst-plugins-ugly010`

### Install CMU Pocket Sphinx

Pocketsphinx is what we'll be using to convert spoken word audio to text. It runs the conversion of speach-to-text _offline_. We'll be using this feature for detection of our onset phrase (defaults to "ok computer"). Install with `brew install cmu-pocketsphinx`.

Note: we are going to be using two gstreamer plugins from the Pocket Sphinx: 'pocketsphinx' and 'vader'. At compile time of CMU Pocket Sphinx, you'll need to make sure the libxml2 is available in your package path _or these plugins will silently fail to install_. You can check for libxml2 by running

    pkg-config --libs libxml-2.0

The command should result in output something like `-L/usr/local/Cellar/libxml2/2.9.1/lib -lxml2`. If it doesn't, take a look online for the latest way to link Homebrew's libxml2 to your package path.

### Using a virtual environment
If you want to use a virtualenv for the pip installable packages (recommended), you'll need to reference your Homebrew installed site-packages in the site-packages folder of your virtual environment. To do this:

1. Create a virtual environment and find the site-packages folder, then
2. Create a `homebrew.pth` path file that references Brew's site-packages folder, for instance:

    echo '/usr/local/lib/python2.7/site-packages' > $VIRTUAL_ENV/lib/python2.7/site-packages/homebrew.pth

### Install Python packages
Finally, you can run `pip install -r requirements.txt`

## Acknowledgements
Otto is developed by [Charles Covey-Brandt](http://github.com/chazcb) and [Stephanie Stroud](http://github.com/stroud109) with the help of lots of contributors.

Jasper is developed by [Shubhro Saha](http://www.princeton.edu/~saha/) and [Charles Marsh](http://www.princeton.edu/~crmarsh/). Both can be reached by email at [saha@princeton.edu](mailto:saha@princeton.edu) and [crmarsh@princeton.edu](mailto:crmarsh@princeton.edu) respectively.

## Contributions

Jasper has recieved contributions by:
- [FRITZ|FRITZ](http://www.fritztech.net) ( [fritz@fritztech.net](mailto:fritz@fritztech.net) )
- [Exadrid](https://github.com/Exadrid)

## Jasper Project License

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
