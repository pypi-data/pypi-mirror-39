"""
 * $Id: 0.8+6 model_data_service.py 49f30166ec7f 2018-11-30 od $
 *
 * This file is part of the Cloud Services Integration Platform (CSIP),
 * a Model-as-a-Service framework, API and application suite.
 *
 * 2012-2018, Olaf David and others, OMSLab, Colorado State University.
 *
 * OMSLab licenses this file to you under the MIT license.
 * See the LICENSE file in the project root for more information.
"""
import json, os
from collections import OrderedDict
from typing import AnyStr

from csip.utils import Client

class Service(object):
    
    REQUEST = ".request.json"
    RESULT = ".result.json"
    
    """
    Utility for reading request files and writing response files..

    """
    def __init__(self, workdir: AnyStr = None, request_fname: AnyStr = REQUEST):
        """
        :param workdir: Workspace directory
        """
        self.workdir = workdir or os.getcwd()
        self.request = {}
        self.resources = OrderedDict()
        self.response = OrderedDict()
        
        if self.workdir.find('/work/') > 1:
            path = self.workdir.replace('/work/','/results/') 
            if os.path.exists(path):
                self.workdir = path
        
        self.load_request()
#        self.load_resource_map()

    def load_request(self, request_fname: AnyStr = REQUEST):
        """
        Import the CSIP request
        :param request_fname: The source file
        :return:
        """
        
        path = os.path.join(self.workdir, request_fname)
        if not os.path.exists(path):
            raise Exception("No request file found.")
            
        with open(path) as fp:
                data = json.load(fp)
        
        csip = Client(data=data['parameter'])
        self.request = csip.data

    def load_resource_map(self, resource_fname: AnyStr = 'resources.json'):
        """
        Import the resource map, stored on disk as a dictionary of <resource_id>: <resource_path>
        :return:
        """
        path = os.path.join(self.workdir, resource_fname)
        if os.path.exists(path):
            with open(path) as fp:
                data = json.load(fp)
        csip = Client(data=data)
        self.resources = csip.data

    def get_param(self, param, def_value=None, typ=None):
        """
        Return the value of the parameter
        :param param: THe request parameter
        :param def_value: If the parameter is optional, then this is the default value
        :param typ: Type cast to apply if value is not a string
        :return: string
        """
        oparam = self.request.get(param, {'value': def_value})
        v = oparam['value']
        if typ:
            try:
                v = typ(v)
            except TypeError:
                v = None
        return v

    def get_int_param(self, *args):
        """
        Apply type cast to get_param
        :param args:
        :return: int
        """
        return self.get_param(*args, typ=int)

    def get_float_param(self, *args):
        """
        App.y float cast to value
        :param args:
        :return: float
        """
        return self.get_param(*args, typ=float)

    def get_resource_file(self, resource_id):
        return self.resources.get(resource_id, None)

    def put_result(self, name, value, units=None, desc=None):
        """
        Add value to result response
        :param name:
        :param value:
        :param units:
        :param desc:
        :return:
        """
        self.response[name] = {
            'value': value,
        }
        if units:
            self.response[name]['units'] = units
        if desc:
            self.response[name]['description'] = desc

    # put this into an exithook?
    def write_results(self, result_fname: AnyStr = RESULT):
        """
        Write response object to disk.
        :return:
        """
        result = []
        for name, oparam in self.response.items():
            result.append({
                'name': name,
                **oparam,
            })
        path = os.path.join(self.workdir, result_fname)
        with open(path, 'w') as fp:
            json.dump({'result': result}, fp, indent=2)
        return result

if __name__ == '__main__':
    # test
    md = {
        "metainfo": {},
        "parameter": [{
            "name": "param1",
            "value": 23,
        }, {
            "name": "optparam1",
            "value": 25.6,
            "description": "optional",
        }]
    }

    test_dir = '/tmp/mds_test'
    if not os.path.exists(test_dir):
#        shutil.rmtree(test_dir)
        os.makedirs(test_dir)

    request_path = os.path.join(test_dir, Service.REQUEST)
    with open(request_path, 'w') as req_fp:
        json.dump(md, req_fp, indent=2)

    mds = Service(test_dir)
    param1 = mds.get_int_param('param1')
    assert param1 == 23, "Failed to extract parameter, expected 23, got {0}".format(param1)
    optparam1 = mds.get_float_param('optparam1', 57)
    assert optparam1 == 25.6, "Failed to extract parameter with default value, expected 25.6, got {0}".format(optparam1)
    nonexistentparam = mds.get_int_param('nonexistentparam', 57)
    assert nonexistentparam == 57, "Failed to extract optional parameter, expected 57, got {0}".format(nonexistentparam)

    # Write some results
    mds.put_result("result", 47)
    testunits = "someunits"
    mds.put_result("result_with_units", 45.55, testunits)
    testdesc = "a description for result_with_units_and_desc"
    mds.put_result("result_with_units_and_desc", 33.33, "units!", testdesc)

    results = mds.write_results()
    assert results[0]['value'] == 47, "Failed to set result to 47"
    assert results[1]['units'] == testunits, "Failed to set units to {0}".format(testunits)
    assert results[2]['description'] == testdesc, "Failed to set description to {0}".format(testdesc)

    with open(os.path.join(test_dir, Service.RESULT)) as resp_fp:
        oresult = json.load(resp_fp)

    assert 'result' in oresult

    print("All tests passed...")
