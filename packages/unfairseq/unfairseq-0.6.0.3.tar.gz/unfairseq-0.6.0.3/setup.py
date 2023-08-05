#!/usr/bin/env python3
# Copyright (c) 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the LICENSE file in
# the root directory of this source tree. An additional grant of patent rights
# can be found in the PATENTS file in the same directory.

from setuptools import setup, find_packages, Extension
import sys


if sys.version_info < (3,):
    sys.exit('Sorry, Python3 is required for fairseq.')

with open('README.md') as f:
    readme = f.read()

#with open('LICENSE') as f:
#    license = f.read()

license='BSD License\n\nFor fairseq software\n\nCopyright (c) 2017-present, Facebook, Inc. All rights reserved.\n\nRedistribution and use in source and binary forms, with or without modification,\nare permitted provided that the following conditions are met:\n\n * Redistributions of source code must retain the above copyright notice, this\n    list of conditions and the following disclaimer.\n\n * Redistributions in binary form must reproduce the above copyright notice,\n    this list of conditions and the following disclaimer in the documentation\n       and/or other materials provided with the distribution.\n\n * Neither the name Facebook nor the names of its contributors may be used to\n    endorse or promote products derived from this software without specific\n       prior written permission.\n\nTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND\nANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED\nWARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE\nDISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR\nANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES\n(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;\nLOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON\nANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT\n(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS\nSOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n'

#with open('requirements.txt') as f:
#    reqs = f.read()


bleu = Extension(
    'fairseq.libbleu',
    sources=[
        'fairseq/clib/libbleu/libbleu.cpp',
        'fairseq/clib/libbleu/module.cpp',
    ],
    extra_compile_args=['-std=c++11'],
)


setup(
    name='unfairseq',
    version='0.6.0.3',
    description='Unofficial Pacakge of Facebook AI Research Sequence-to-Sequence Toolkit',
    long_description=readme,
    license=license,
    install_requires=['cffi', 'numpy', 'torch', 'tqdm'],
    packages=find_packages(),
    ext_modules=[bleu],
    test_suite='tests',
)
