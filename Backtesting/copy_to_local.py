from datetime import datetime
import boto3 as aws
import os
import sys

s3 = aws.client("s3")


def getTickers(file_type, ticker_names, init_date, final_date):
    """AAAA-MM-DD"""

    init_date = datetime.strptime(init_date, "%Y-%m-%d")
    final_date = datetime.strptime(final_date, "%Y-%m-%d")

    bucket_files = []
    for ticker in ticker_names:
        pages = s3.get_paginator("list_objects").paginate(
            Bucket="dell-filtred-data")
        bucket_files.extend([file["Key"] for page in pages for file in page["Contents"]
                             if file["Key"].split("/")[3].split(".")[0] == "{0}_{1}".format(file_type, ticker)])

    to_download = []
    for file in bucket_files:
        d = file.split("/")[:3]
        file_date = datetime.strptime(
            "{0}-{1}-{2}".format(d[0], d[1], d[2]), "%Y-%m-%d")
        if file_date >= init_date and file_date <= final_date:
            to_download.append(file)

    for file in to_download:
        ticker = file.split("_")[1].split(".")[0]
        file_date = "".join(file.split("/")[:3])
        file_path = "data/{0}{1}{2}.parquet".format(
            file_type, file_date, ticker)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as f:
            s3.download_fileobj("dell-filtred-data", file, f)


def getArtifacts(model_name, model_run, strategy_name):
    try:
        pages = s3.get_paginator("list_objects").paginate(
            Bucket="dell-artifacts")
        bucket_objects = [file["Key"]
                          for page in pages for file in page["Contents"]]
    except Exception as e:
        print("Error listing bucket:", e)

    return_files = []
    for file in bucket_objects:
        artifact_type = file.split("/")[0]
        if artifact_type == "models":
            model = file.split("/")[1]
            if model == model_name:
                if file.split("/")[2] == "{0}.py".format(model):
                    return_files.append(
                        (file, "/".join(file.split("/")[0::2])))
                if file.split("/")[2] == "{0}-{1}.pkl".format(model.lower(), model_run):
                    return_files.append(
                        (file, "/".join(file.split("/")[0::2])))
        elif artifact_type == "strategies":
            if file.split("/")[1] == "{0}.py".format(strategy_name):
                return_files.append((file, file))

    for file in return_files:
        os.makedirs(os.path.dirname(file[1]), exist_ok=True)
        with open(file[1], 'wb') as f:
            s3.download_fileobj("dell-artifacts", file[0], f)

    return return_files


args = sys.argv
date_init = args[1]
date_end = args[2]

with open('relations.txt') as f:
    for line in f:
        print(line)
        getTickers("NEG", line.split(" ")[1:], date_init, date_end)
        sm_info = line.split(" ")[0].split(":")
        getArtifacts(sm_info[1].split('-')[0],
                     sm_info[1].split('-')[1], sm_info[0])
