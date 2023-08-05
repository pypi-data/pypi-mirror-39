"""
BenchExec is a framework for reliable benchmarking.
This file is part of BenchExec.

Copyright (C) 2007-2015  Dirk Beyer
All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import benchexec.util as util
from . import cseq

class Tool(cseq.CSeqTool):
    """
    Tool info for Lazy-CSeq (http://github.com/omainv/cseq/releases).
    """

    REQUIRED_PATHS = [
                  "cbmc",
                  "core",
                  "cseq.py",
                  "lazy-cseq.py",
                  "pycparser",
                  "modules"
                  ]

    def executable(self):
        return util.find_executable('lazy-cseq.py')

    def name(self):
        return 'Lazy-CSeq'
