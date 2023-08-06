
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

from botocore.exceptions import ClientError

from collections import abc

from abc import ABCMeta, abstractmethod

from boto3.dynamodb.conditions import Key, Attr


class MgProject:
    '''
    A representation of a lot of MgObjects
    '''

    def __init__(self, project):
        self.project = project

        items = self.scanDB(filter_key='mg-identifier',
                    filter_value=self.project,
                    comparison='contains')

        self.reads = []
        self.assemblies = []
        self.samples = []
        self.association_map = {}

        for i in items:
            mg_identifier = i['mg-identifier']
            if any(x in mg_identifier  for x in ['-read', '-tran']):
                self.reads.append(MgRead(i))
            elif '-assm' in mg_identifier :
                self.assemblies.append(MgAssembly(i))
            elif '-samp' in mg_identifier :
                self.samples.append(MgSample(i))
            else:
                raise ValueError(f'object with id {mg_identifier} could not be assigned a type')

        self.derive_associations()


    def getRelatedAssemblies(self, sampleName=None):
        related = []
        if sampleName:
            for assembly in self.assemblies:
                if sampleName in assembly.getMgID():
                    related.append(assembly)
        return related


    def getAssociatedReads(self, mg_identifier):
        if isinstance(mg_identifier, str):
            query = self.getObjectFromID(mg_identifier)
        else:
            query = mg_identifier

        if isinstance(query, MgAssembly):
            return(self.association_map[query])
            # return query.getReads()
        else:
            raise ValueError('f{mg_identifier} is not an assembly object or id')


    def printAssociationMap(self):
        # Print in longform the association map
        for k,v in self.association_map.items():
            print(f'{k.getMgID()} : ')
            for v1 in v:
                print(f'\t{v1.getMgID()}')

    def getAssociationMapIDs(self):
        # Return dictionary of associations with only mg-identifiers
        d = {}
        for k,v in self.association_map.items():
            d[k.getMgID()] = []
            for v1 in v:
                d[k.getMgID()] = d[k.getMgID()] + [v1.getMgID()]
        return(d)

    def getAssociationMapMD(self):
        # Return dictionary of associations with metadata
        d = {}
        for k,v in self.association_map.items():
            d[k.getMetadata()] = []
            for v1 in v:
                d[k.getMetadata()] = d[k.getMetadata()] + [v1.getMetadata()]
        return(d)

    def getAssociationMap(self):
        return(self.association_map)

    def derive_associations(self):
        for assembly in self.assemblies:
            associated = assembly.getAssociated()
            for k,v in associated.items():
                for v1 in v:
                    connection =self.getObjectFromID(v1)
                    if assembly in self.association_map:
                        self.association_map[assembly] = self.association_map[assembly] + [connection]
                    else:
                        self.association_map[assembly] = [connection]

        for read in self.reads:
            associated = read.getAssociated()
            for k,v in associated.items():
                for v1 in v:
                    connection =self.getObjectFromID(v1)
                    if read in self.association_map:
                        self.association_map[read] = self.association_map[read] + [connection]
                    else:
                        self.association_map[read] = [connection]

        for sample in self.samples:
            associated = sample.getAssociated()
            for k,v in associated.items():
                for v1 in v:
                    connection =self.getObjectFromID(v1)
                    if sample in self.association_map:
                        self.association_map[sample] = self.association_map[sample] + [connection]
                    else:
                        self.association_map[sample] = [connection]


    def getObjectFromID(self, mg_identifier):
        if any(x in mg_identifier  for x in ['-read', '-tran']):
            for r in self.reads:
                if r.getMgID() == mg_identifier:
                    return r

        elif '-assm' in mg_identifier :
            for a in self.assemblies:
                if a.getMgID() == mg_identifier:
                    return a

        elif '-samp' in mg_identifier :
            for s in self.samples:
                if s.getMgID() == mg_identifier:
                    return s

        else:
            raise ValueError(f'object with id {mg_identifier} could not be assigned a type')


    # def __iter__(self):
    #     return(iter(self.))

    def scanDB(self, filter_key='mg-object', filter_value='assembly', comparison = 'equals', region='us-west-2', dbname='mg-project-metadata'):
        """
        Perform a scan operation on table.
        Can specify filter_key (col name) and its value to be filtered.
        This gets all pages of results. Returns list of items.
        https://martinapugliese.github.io/interacting-with-a-dynamodb-via-boto3/
        type: can be 'equals' or 'contains' so far
        """

        dynamodb = boto3.resource('dynamodb', region_name=region)
        table = dynamodb.Table(dbname)

        if filter_key and filter_value:
            if comparison == 'equals':
                filtering_exp = Key(filter_key).eq(filter_value)
            elif comparison == 'contains':
                filtering_exp = Attr(filter_key).contains(filter_value)

            response = table.scan(
                FilterExpression=filtering_exp)

        else:
            response = table.scan()

        items = response['Items']
        while True:
            # print(len(response['Items']))
            if response.get('LastEvaluatedKey'):
                response = table.scan(
                    ExclusiveStartKey=response['LastEvaluatedKey']
                    )
                items += response['Items']
            else:
                break

        return items


class MgObj:
    __metaclass__ = ABCMeta

    def __init__(self, d, mg_id=None):
        self.d = d
        self.mg_identifier = None
        self.type = None
        self.s3path = None
        self.sra_id = None
        self.associated = None
        self.project = None
        self.s3 = boto3.client('s3')

        if 'mg-identifier' in d:
            self.mg_identifier = d['mg-identifier']
        if 'mg-object' in d:
            self.type = d['mg-object']
        if 's3-path' in d:
            self.s3path = d['s3-path']
        if 'sra-id' in d:
            self.sra_id = d['sra-id']
        if 'associated' in d:
            self.associated = d['associated']
        if 'mg-project' in d:
            self.project = d['mg-project']

        self.fill_required()

    def fill_required(self):
        if self.mg_identifier == None:
            raise ValueError('Cannot initialize ')

        if self.project == None:
            self.project = self.mg_identifier[:4]

    def getMgID(self):
        return self.mg_identifier

    def getAssociated(self):
        return self.associated

    def getMetadata(self):
        return str(self.d)

    def getS3path(self):
        return self.s3path

    def __str__(self):
        return str(self.d)

    def check(self, path):
        bucket = path.split('/')[2]
        key = '/'.join(path.split('/')[3:])

        try:
            self.s3.head_object(Bucket=bucket, Key=key)
        except ClientError as e:
            return int(e.response['Error']['Code']) != 404
        return True


class MgAssembly(MgObj):
    def getReads(self):
        return(self.associated['read'])

    def print_stats(self):
        '''
        print out assembly stats as they appear in the assembly stat file
        '''
        print('Nonoperational function')
        return

    def LengthDistribution(self):
        '''
        Return pandas dataframe of length distributions
        '''
        pass

    def SequenceParameters(self):
        '''
        Return pandas dataframe of top 10 sequences and their parameters
        '''
        pass

    def N50(self):
        '''
        Return n50 value
        '''
        pass



class MgRead(MgObj):
    def print_stats(self):
        '''
        print out assembly stats as they appear in the assembly stat file
        '''
        print('Nonoperational function')
        return

    def LengthDistribution(self):
        '''
        Return pandas dataframe of length distributions
        '''
        pass

    def SequenceParameters(self):
        '''
        Return pandas dataframe of top 10 sequences and their parameters
        '''
        pass

    def N50(self):
        '''
        Return n50 value
        '''
        pass


    def getSampleName(self):
        if 'metadata' in self.d:
            if 'SampleName' in self.d['metadata']:
                return(self.d['metadata']['SampleName'])
        return None


    def ranNonpareil(self, queryForFile=False):
        if 'nonpareil_metadata' in self.d:
            if queryForFile:
                pass
            return True
        return False


class MgSample(MgObj):
    def print_stats(self):
        '''
        print out assembly stats as they appear in the assembly stat file
        '''
        print('Nonoperational function')
        return

    def LengthDistribution(self):
        '''
        Return pandas dataframe of length distributions
        '''
        pass

    def SequenceParameters(self):
        '''
        Return pandas dataframe of top 10 sequences and their parameters
        '''
        pass

    def N50(self):
        '''
        Return n50 value
        '''
        pass

# p = MgProject('PREY')
# reads = p.getAssociatedReads('PREY_ES01_USA_MGQ-assm')
# print(reads[0].getS3path())
#
# d = {'bbmap_metadata': {'quality_trimming': {'done': True, 'cmd_run': '/tmp/bbmap/bbduk.sh qtrim=f trimq=6 -in1=/scratch/4e4d4c64-e292-4470-9291-f0737c60833a/ES_8_DNA_Q.1.fastq.g_trim.fastq.g_trim_clean.fastq.gz -out1=/scratch/4e4d4c64-e292-4470-9291-f0737c60833a/ES_8_DNA_Q.1.fastq.g_trim.fastq.g_trim_clean.fastq.g_trim_clean_qual.fastq.gz -in2=/scratch/4e4d4c64-e292-4470-9291-f0737c60833a/ES_8_DNA_Q.2.fastq.g_trim.fastq.g_trim_clean.fastq.gz -out2=/scratch/4e4d4c64-e292-4470-9291-f0737c60833a/ES_8_DNA_Q.2.fastq.g_trim.fastq.g_trim_clean.fastq.g_trim_clean_qual.fastq.gz t=16', 'total_removed_reads': '0'}, 'contaminant_removal': {'contaminants': '712', 'cmd_run': '/tmp/bbmap/bbduk.sh ref=/tmp/bbmap/resources/phix174_ill.ref.fa.gz,/tmp/bbmap/resources/sequencing_artifacts.fa.gz k=31 hdist=1 -in1=/scratch/4e4d4c64-e292-4470-9291-f0737c60833a/ES_8_DNA_Q.1.fastq.g_trim.fastq.gz -out1=/scratch/4e4d4c64-e292-4470-9291-f0737c60833a/ES_8_DNA_Q.1.fastq.g_trim.fastq.g_trim_clean.fastq.gz -in2=/scratch/4e4d4c64-e292-4470-9291-f0737c60833a/ES_8_DNA_Q.2.fastq.g_trim.fastq.gz -out2=/scratch/4e4d4c64-e292-4470-9291-f0737c60833a/ES_8_DNA_Q.2.fastq.g_trim.fastq.g_trim_clean.fastq.gz t=16', 'total_removed_reads': '712'}, 'adapter_removal': {'trimmed_by_overlap_reads': '347056', 'cmd_run': '/tmp/bbmap/bbduk.sh ref=/tmp/bbmap/resources/adapters.fa k=23 mink=11 hdist=1 tbo tpe ktrim=r ftm=5 -in1=/scratch/4e4d4c64-e292-4470-9291-f0737c60833a/ES_8_DNA_Q.1.fastq.gz -out1=/scratch/4e4d4c64-e292-4470-9291-f0737c60833a/ES_8_DNA_Q.1.fastq.g_trim.fastq.gz -in2=/scratch/4e4d4c64-e292-4470-9291-f0737c60833a/ES_8_DNA_Q.2.fastq.gz -out2=/scratch/4e4d4c64-e292-4470-9291-f0737c60833a/ES_8_DNA_Q.2.fastq.g_trim.fastq.gz t=16', 'total_reads': '130498240', 'total_bases': '19574736000', 'KTrimmed_reads': '1448604', 'FTrimmed_reads': '0', 'total_removed_reads': '52920'}}, 'mg-identifier': 'PREY_ES08_USA_MGQ-read', 's3-path': 's3://metagenomi/projects/rey/reads/qc/PREY_ES08_USA_MGQ-read_trim_clean'}

# o = MgAssembly(d)
# i = o.get_mgID()
# print(i)

# print(o.get_mgID())

# class MgProject():
#     def __init__(project):
#
#         filtering_exp = Key('mg-project').eq(project)
#
#         response = table.query(
#             IndexName='mg-project-mg-object-index',
#             FilterExpression=filtering_exp)
#
#         items = response['Items']
#         while True:
#             print(len(response['Items']))
#             if response.get('LastEvaluatedKey'):
#                 response = table.query(
#                     ExclusiveStartKey=response['LastEvaluatedKey']
#                     )
#                 items += response['Items']
#             else:
#                 break
#
#         return items
#
#
#     def

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

def scanDB(filter_key='mg-object', filter_value='assembly', comparison = 'equals', region='us-west-2', dbname='mg-project-metadata'):
    """
    Perform a scan operation on table.
    Can specify filter_key (col name) and its value to be filtered.
    This gets all pages of results. Returns list of items.
    https://martinapugliese.github.io/interacting-with-a-dynamodb-via-boto3/
    type: can be 'equals' or 'contains' so far
    """

    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(dbname)

    if filter_key and filter_value:
        if comparison == 'equals':
            filtering_exp = Key(filter_key).eq(filter_value)
        elif comparison == 'contains':
            filtering_exp = Attr(filter_key).contains(filter_value)

        response = table.scan(
            FilterExpression=filtering_exp)

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

def get_read_paths(mg_id, region='us-west-2', dbname='mg-project-metadata'):
    """

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

def test(project, region='us-west-2', dbname='mg-project-metadata'):
    dynamodb = boto3.resource('dynamodb', region_name=region)
    table = dynamodb.Table(dbname)

    response = table.query(
        IndexName='mg-project-mg-object-index',
        KeyConditionExpression = Key('mg-project').eq(project))

    print(len(response['Items']))

    items = response['Items']
    while True:
        print(len(response['Items']))
        if response.get('LastEvaluatedKey'):
            response = table.query(
                ExclusiveStartKey=response['LastEvaluatedKey']
                )
            items += response['Items']
        else:
            break

    return items
