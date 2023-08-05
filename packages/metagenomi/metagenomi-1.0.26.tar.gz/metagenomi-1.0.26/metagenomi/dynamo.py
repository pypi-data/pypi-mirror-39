
import pandas as pd
import boto3
import json
import shlex
import subprocess
import time
import datetime
import doctest
import os
import stat

from collections import abc

from boto3.dynamodb.conditions import Key, Attr


class MgObj:
    def __init__():
        pass

class MgAssembly(MgObj):
    pass

class MgRead(MgObj):
    pass

class MgSample(MgObj):
    pass

def get_mg_id(sra, dbname='mg-project-metadata',
                   region='us-west-2',
                   index='sra-id-index'):


    '''Given an SRA id, return mg-identifer'''


    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(dbname)

    response = table.query(
                        IndexName=index,
                        KeyConditionExpression=Key('sra-id').eq(sra)
                        )

    if len(response['Items']) <1:
        return('NA')
    else:
        if len(response['Items']) > 1:
            raise ValueError(f'Multiple entries for {value} exist in {dbname} \
                            (index = {index})')
        else:
            return(response['Items'][0]['mg-identifier'])

def index_query(items):
    item_dict = {}
    for i in items:
        item_dict[i['mg-identifier']] = i
    return(item_dict)




def flatten(d):
    final_d  = {}
    for k,v in d.items():
        final_d[k] = flatten1(v, {})
    return(final_d)



def flatten1(d, fulld):
    newd = fulld
    for k,v in d.items():
        if isinstance(v, dict):
            if 'Length distribution' in k:
                newd[k]=v
                continue
            if 'Sequence parameters' in k:
                newd[k]=v
                continue
            else:
                newd.update(flatten1(v, newd))
        else:
            newd[k]=v
    return newd

def get_sample_metadata(read_id):
    i = get_mg_id_metadata(read_id)
    a = i['associated']
    s = a['sample'][0]
    md = get_mg_id_metadata(s)['metadata']
    return(md)


def get_bioproject(read_id):
    i = get_mg_id_metadata(read_id)
    bp = i['metadata']['BioProject']
    return(bp)


def nested_dict_iter(nested):
    for key, value in nested.items():
        print(value)
        if isinstance(value, abc.Mapping):
            print(value)
            yield from nested_dict_iter(value)
        else:
            yield key, value


def get_tuple_from_value(my_dict):
    new_dict = {}
    for term, nested_dict in my_dict.items():
        for id, n in nested_dict.items():
            new_dict[id] = [term, n]
    return new_dict



def get_metadata(value, index='mg-project-mg-object-index',
                region='us-west-2', dbname='mg-project-metadata'):
    '''
    Checks if a key:value for a given index exists in the DynamoDB
    TO DO: make index= a parameter. Will break all the import_object calls
    :param key: key to search for. Generally 'sra-id'
    :param value: value to search for.
    returns: 'NA' if value does not exist in the DB, mg-identifier if it does.
    '''

    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(dbname)

    response = table.query(
                        IndexName=index,
                        KeyConditionExpression=Key('mg-project').eq(value)
                        )


    if len(response['Items']) <1:
        return None
    else:
        return(index_query(response['Items']))


def get_mg_id_metadata(value, region='us-west-2', dbname='mg-project-metadata'):
    '''
    Checks if a key:value for a given index exists in the DynamoDB
    TO DO: make index= a parameter. Will break all the import_object calls
    :param key: key to search for. Generally 'sra-id'
    :param value: value to search for.
    returns: 'NA' if value does not exist in the DB, mg-identifier if it does.
    '''

    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(dbname)

    response = table.query(
                        KeyConditionExpression=Key('mg-identifier').eq(value)
                        )

    if len(response['Items']) <1:
        return None
    else:
        return(response['Items'][0])


'''def get_by_type(proj, type, region='us-west-2', dbname='mg-project-metadata'):

    Example: Retrieve all assemblies from a certain project


    items = scan_table_allpages(filter_key='mg-object', filter_value='assembly', proj = 'PREY')
    print(items)

'''

def scan_in_project(project, filter_key='mg-object', filter_value='assembly', region='us-west-2', dbname='mg-project-metadata'):
    """
    Perform a scan operation on table.
    Can specify filter_key (col name) and its value to be filtered.
    This gets all pages of results. Returns list of items.
    https://martinapugliese.github.io/interacting-with-a-dynamodb-via-boto3/
    """

    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(dbname)

    if filter_key and filter_value and project:
        filtering_exp = Key(filter_key).eq(filter_value)
        project_exp = Key('mg-project').eq(project)

        response = table.scan(
            FilterExpression=filtering_exp & project_exp)
    else:
        response = table.scan()

    items = response['Items']
    while True:
        print(len(response['Items']))
        if response.get('LastEvaluatedKey'):
            response = table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey']
                )
            items += response['Items']
        else:
            break

    return items
