import shutil
import boto3
import os
import sys


def GetFilesToLocal(strategies, local, bucket, extension):
    """
    params:
    - prefix: pattern to match in s3
    - local: local path to folder in which to place files
    - bucket: s3 bucket with target contents
    - client: initialized s3 client object
    """
    client = boto3.client('s3')
    keys = []
    dirs = []
    next_token = ''
    base_kwargs = {
        'Bucket': bucket,
        'Prefix': "",
    }
    while next_token is not None:
        kwargs = base_kwargs.copy()
        if next_token != '':
            kwargs.update({'ContinuationToken': next_token})
        results = client.list_objects_v2(**kwargs)
        contents = results.get('Contents')
        for i in contents:
            k = i.get('Key')
            if k[-1] != '/':
                keys.append(k)
            else:
                dirs.append(k)
        next_token = results.get('NextContinuationToken')
        tempKeys = []
        for key in keys:
            if key.split(extension)[0] in strategies:
                tempKeys.append(key)
        keys = tempKeys
    for d in dirs:
        dest_pathname = os.path.join(local, d)
        if not os.path.exists(os.path.dirname(dest_pathname)):
            os.makedirs(os.path.dirname(dest_pathname))
    for k in keys:
        dest_pathname = os.path.join(local, k)
        if not os.path.exists(os.path.dirname(dest_pathname)):
            os.makedirs(os.path.dirname(dest_pathname))
        client.download_file(bucket, k, dest_pathname)


args = sys.argv
relationNames = args[1:]
strategyNames = [x.split(':')[0] for x in relationNames]
modelClassesNames = [x.split(':')[1].lower().capitalize() for x in relationNames]
modelObjectNames = [x.split(':')[1].lower()for x in relationNames]
GetFilesToLocal(strategyNames, 'strategies', 'simuladorestrategias', '.py')
GetFilesToLocal(modelClassesNames, 'models', 'simuladormodelos', '.py')
GetFilesToLocal(modelObjectNames, 'models', 'simuladormodelos', '.pkl')
