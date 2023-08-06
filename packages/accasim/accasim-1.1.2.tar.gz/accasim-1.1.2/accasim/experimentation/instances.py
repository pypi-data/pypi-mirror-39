"""
MIT License

Copyright (c) 2017 cgalleguillosm

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
"""
from accasim.utils.file import file_exists, dir_exists

class InstanceReader:
    
    def __init__(self):
        pass
    
class InstanceWriter:
    
    def __init__(self):
        pass

class InstanceGenerator:
    
    def __init__(self, name, overwrite=False):
        self.name = name
        self.overwerite = overwrite
        self.n_instances = 0
             
    def running_jobs(self, running_jobs):
        self.data['running_jobs'] = running_jobs
        self._check_data()
        
    def queued_jobs(self, queued_jobs):
        self.data['queued_jobs'] = queued_jobs
        self._check_data()
        
    def _read(self):
        pass
    
    def _write(self):
        self.n_instances += 1
        
    def _check_data(self):
        attrs = ['running_jobs', 'queued_jobs']
        if attr in attrs: 
            if not(attr in self.data):
                return False
        return self._write()
        
    def store(self, **kwargs):
        for k, v in kwargs.items():
            getattr(self, k)(v)
    
    
    
    
