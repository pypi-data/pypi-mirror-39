import os
import yaml
from urllib.request import urlopen

from django.core.exceptions import ObjectDoesNotExist
from .models import ComputationalToolInputType, ComputationalToolInput, ComputationalWF
from .models import ComputationalTool, ComputationalWFStep, ComputationalWFStepInput


def get_type(type_dict):
    t = ''
    o = False
    a = False
    if 'type' in type_dict:
        t = type_dict['type']
        if '?' in t:
            t = t[:-1]
            o = True
        if '[]' in t:
            t = t[:-2]
            a = True
    return t, o, a


def insert_computationaltool_input_types(cwl):
    types = {}
    for name in cwl['inputs']:
        t, o, a = get_type(cwl['inputs'][name])
        if t:
            try:
                tt = ComputationalToolInputType.objects.get(type=t)
            except ObjectDoesNotExist:
                tt = ComputationalToolInputType.objects.create(type=t)
            types[tt.type] = tt.id
    return types


def insert_computationaltool_inputs(comptool):
    cwl = yaml.load(urlopen(comptool.cwl))
    types = insert_computationaltool_input_types(cwl)
    objects = []
    for name in cwl['inputs']:
        option = ''
        if 'inputBinding' in cwl['inputs'][name] and 'prefix' in \
                cwl['inputs'][name]['inputBinding']:
            option = cwl['inputs'][name]['inputBinding']['prefix']
        d = ''
        if 'doc' in cwl['inputs'][name]:
            d = cwl['inputs'][name]['doc'].replace('\n', ' ').strip()
        t, o, a = get_type(cwl['inputs'][name])
        if t in types:
            t = types[t]
        else:
            tt = ComputationalToolInputType.objects.create(type=t)
            types[tt.type] = tt.id
            t = tt.id
        objects.append(
            ComputationalToolInput(
                name=name,
                option=option,
                array=a,
                optional=o,
                doc=d,
                computationaltool=comptool,
                computationaltoolinputtype_id=t
            )
        )
    ComputationalToolInput.objects.bulk_create(objects)


def insert_computationalwf(wfl_location):
    cwl = yaml.load(urlopen(wfl_location))
    compwfl = ComputationalWF.objects.create(
        name=cwl['label'].replace('\n', ' ').strip(),
        description=cwl['doc'].replace('\n', ' ').strip(),
        cwl=wfl_location)

    order = 0
    for s in cwl['steps']:
        cwl_tool = os.path.basename(cwl['steps'][s]['run'])
        cwl_tool = ComputationalTool.objects.filter(cwl__endswith='/' + cwl_tool)
        order += 1
        cwl_tool = cwl_tool[0]
        d = ''
        if 'doc' in cwl['steps'][s]:
            d = cwl['steps'][s]['doc'].replace('\n', ' ').strip()
        step = ComputationalWFStep.objects.create(name=s,
                                                  order=order,
                                                  description=d,
                                                  computationaltool_id=cwl_tool.id,
                                                  computationalwf=compwfl)
        for i in cwl['steps'][s]['in']:
            cwl_tool_input = ComputationalToolInput.objects.get(
                name=i, computationaltool=cwl_tool)
            value = str(cwl['steps'][s]['in'][i])
            if type(cwl['steps'][s]['in'][i]) == dict:
                if 'default' in cwl['steps'][s]['in'][i]:
                    value = str(cwl['steps'][s]['in'][i]['default'])
            ComputationalWFStepInput.objects.create(value=value,
                                                    computationalwfstep=step,
                                                    computationaltoolinput=cwl_tool_input)
