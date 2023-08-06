from libaws.common.boto import *


def list_as_dir(bucket,key):

    paginator = client_s3.get_paginator('list_objects')
    if key == "/":
        key = ""
    results = paginator.paginate(Bucket=bucket,Delimiter='/',Prefix=key)
    for prefix in results.search('CommonPrefixes'):
        if prefix is None:
            continue
        prefix = prefix.get('Prefix')
        for child_key in list_as_dir(bucket,prefix):
            yield child_key

    for res in results:
        ####print res
        if res.has_key('CommonPrefixes'):
            print "key %s is not exist in bucket %s" % (key,bucket)
            continue
        contents = res['Contents']
        for content in contents:
            child_key = content['Key']
            if child_key == key:
                continue
            yield child_key
            
def IsKeyDir(bucket,key):
    is_dir = False
    for key_path in list_as_dir(bucket,key):
        is_dir = True
        break  
    return is_dir
    
def IsKeyFile(bucket,key):
    if not IsKeyDir(bucket,key):
        s3_file_obj = s3.Object(bucket,key)
        s3_file_obj.content_length
        return True
    return False

def main():
    bucket = "biz-gene-data"
    
    key = "lianchuan/wes-21/A2018083001"
    print key,"is dir:",IsKeyDir(bucket,key),'is file:',IsKeyFile(bucket,key)

    key = "lianchuan/wes-21/A2018083001/"
    print key,"is dir:",IsKeyDir(bucket,key),'is file:',IsKeyFile(bucket,key)
    
    key = "lianchuan/wes-21/A2018083001/A2018083001_BH5T3JDSXX_S1_L001_R1_001.fastq.gz"
    print key,"is dir:",IsKeyDir(bucket,key),'is file:',IsKeyFile(bucket,key)

    key = "lianchuan/wes-21/A2018083001/A2018083001_BH5T3JDSXX_S1_L001_R1_001.fastq.gz/"
    print key,"is dir:",IsKeyDir(bucket,key),'is file:',IsKeyFile(bucket,key)
    
    key = "lianchuan/wes-21/A2018083001/A2018083001_BH5T3JDSXX_S1_L001_R1_001.fastq.gz111"
    print key,"is dir:",IsKeyDir(bucket,key),'is file:',IsKeyFile(bucket,key)
    
    ####key = "lianchuan/wes-21/A2018083001"
    #s3_file_obj = s3.Object(bucket,key)
    #print s3_file_obj.content_length

if __name__ == "__main__":
    main()
