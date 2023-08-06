## Introduction(简介)

Awskit is aws auxiliary tool implements to s3 and ec2 and bucket, VPN, subnet configures multiple functions such as operations.
Can be a multithreaded, resuming from download s3 file to the local, and upload a local file to s3, implements the batch 
application by yml configuration file format, release the cloud server, etc.Implements the aws s3 file hash algorithm etc.

awskit 是aws辅助工具，实现了对s3 ,ec2 以及bucket,vpn,subnet的操作等多个功能。可以多线程，断点续传来下载s3文件到本地，
以及上传本地文件到s3，实现了通过yml配置文件格式来批量申请，释放，重启云服务器等操作。实现了aws s3 文件的hash算法

## Installation(安装)
1. apt-get install python-pip 
2. pip install libaws


## Usage(用法)

1. s3 operation 操作s3

	a) upload file to s3 bucket 上传本地文件到s3的桶

	```	
	awskit -s3 -upload -h 
		useage:
		  -file FILE_PATH, --file FILE_PATH [Required]
		  -bucket BUCKET, --bucket BUCKET
								dest bucket to upload [Required]
		  -part PART_NUM, --part PART_NUM
								part num of file [DEFAULT 6]
		  -key KEY, --key KEY   dest bucket key 
		  -ignore-bucket-file, --ignore-bucket-file
								when file exist in bucket ,ignore it or not [DEFAULT False]
		  -force-again-upload, --force-again-upload
								need to upload again when upload is exists [DEFAULT False]

	```

	b) download bucket file to local 下载s3文件到本地 

	```
	awskit -s3 -download -h 
	useage:
	  -bucket BUCKET, --bucket BUCKET
							dest bucket to download file [Required]
	  -key KEY, --key KEY   bucket file to download [Required]
	  -path PATH, --path PATH
							file download path to save [Default .]
	  -filename FILENAME, --filename FILENAME
							download file name [DEFAULT False]
	  -force-again-download, --force-again-download
							need to download again when download is exists[DEFAULT False]

	```

	c) awskit -s3 -md5 -h

	```
	caculate file md5 hash value
	useage:
		-path FILE_PATH, --path FILE_PATH
	            file path to caculate md5
		-part PART_NUMBER, --part PART_NUMBER
				divide part number of file
	```

2. ec2 operation 操作ec2

	a) awskit -s3 -bucket -h 

	```
	operation on bucket
	useage:

		name BUCKET, --name BUCKET
						dest bucket to operate
		-put-bucket-policy, --put-bucket-policy
							set bucket policy
		-json BUCKET_POLICY_JSON, --json BUCKET_POLICY_JSON
									bucket policy json file
	```

	b) awskit -ec2 -h

	```
		create instance vpc subnet route security from config
		a):
			create instance
				awskit -ec2 --instance -c xxxxxxx (create and lanuch instance from config)
			create vpc
				awskit -ec2 --vpc -c xxxxxx  (create vpc from config) 
			create subnet
				awskit -ec2 --subnet -c  (create subnet from config)
			create route:
				awskit -ec2 --route -c  (create route from config)
			create security group
				awskit -ec2 -security -c (create security group from config)
	```

## Examples(示例)

```
awskit -s3 -download
下载所有历史未完成的下载任务
awskit -s3 -download -b ExampleBucket  -k test.txt
awskit -s3 -download --bucket ExampleBucket  --key test.txt
下载s3桶ExampleBucket上的文件test.txt到本地
awskit -s3 -download -b ExampleBucket  -k test/ 
awskit -s3 -download --bucket ExampleBucket  --key test/
下载s3桶ExampleBucket上的test文件夹中的所有子文件和子文件夹到本地，下载文件夹的时key必须以斜干/结尾
awskit -s3 -download -b ExampleBucket  -k test.txt -p /xxxx/to_path
awskit -s3 -download -b ExampleBucket  -k test.txt --path /xxxx/to_path
下载s3桶ExampleBucket上的文件test.txt到指定目录
awskit -s3 -download -b ExampleBucket  -k test.txt -t ThreadNum
awskit -s3 -download -b ExampleBucket  -k test.txt --thread ThreadNum
指定下载文件的线程个数，默认是10个
awskit -s3 -download -b ExampleBucket  -k test.txt -d 
awskit -s3 -download -b ExampleBucket  -k test.txt --daemon 
设置下载进程后台运行
awskit -s3 -download -b ExampleBucket  -k test.txt -debug 
awskit -s3 -download -b ExampleBucket  -k test.txt --enable-debug-log
以调试状态下载文件,可以查看下载日志
awskit -s3 -download -b ExampleBucket  -k test.txt -force 
awskit -s3 -download -b ExampleBucket  -k test.txt --force-again-download 
强制重新下载文件
awskit -s3 -download -a stop|restart|delete 
awskit -s3 -download --action stop|restart|delete 
停止/重启/删除所有下载记录
awskit -s3 -download -b ExampleBucket  -k test.txt -a stop|restart|delete 
awskit -s3 -download -b ExampleBucket  -k test.txt --action stop|restart|delete 
停止/重启/删除当前下载
awskit -s3 -download -h
下载命令帮助
```

```
awskit -s3 -upload -p /xxx/src_path/test.txt -b upload_to_bucket
awskit -s3 -upload --path /xxx/src_path/test.txt --bucket upload_to_bucket
将本地文件test.txt上传至桶upload_to_bucket
awskit -s3 -upload -p /xxx/src_path/test.txt -b upload_to_bucket -k xxx/test.txt
awskit -s3 -upload -p /xxx/src_path/test.txt -b upload_to_bucket --key xxx/test.txt
将本地文件test.txt上传至桶upload_to_bucket的xxx文件夹
awskit -s3 -upload --path /xxx/src_path/test.txt --bucket upload_to_bucket -i
awskit -s3 -upload --path /xxx/src_path/test.txt --bucket upload_to_bucket --ignore-bucket-file
如果桶上已经存在该上传的文件，强制覆盖该文件
awskit -s3 -upload --path /xxx/src_path/test.txt --bucket upload_to_bucket -force
awskit -s3 -upload --path /xxx/src_path/test.txt --bucket upload_to_bucket --force-again-upload 
强制重新上传文件
awskit -s3 -upload --path /xxx/src_path/test.txt --bucket upload_to_bucket -d
awskit -s3 -upload --path /xxx/src_path/test.txt --bucket upload_to_bucket --daemon
设置上传进程后台运行
awskit -s3 -upload --path /xxx/src_path/test.txt --bucket upload_to_bucket -debug
awskit -s3 -upload --path /xxx/src_path/test.txt --bucket upload_to_bucket --enable-debug-log
以调试状态上传文件,可以查看上传日志
awskit -s3 -upload --path /xxx/src_path/test.txt --bucket upload_to_bucket -t THREAD_NUM 
awskit -s3 -upload --path /xxx/src_path/test.txt --bucket upload_to_bucket --thread THREAD_NUM 
设置上传文件的线程个数，默认是10个
awskit -s3 -upload --path /xxx/src_path/test.txt --bucket upload_to_bucket -n PART_NUM 
awskit -s3 -upload --path /xxx/src_path/test.txt --bucket upload_to_bucket --num PART_NUM 
按固定分块个数的方式上传文件
awskit -s3 -upload --path /xxx/src_path/test.txt --bucket upload_to_bucket -z PART_SIZE 
awskit -s3 -upload --path /xxx/src_path/test.txt --bucket upload_to_bucket --size PART_SIZE 
按固定分块大小的方式上传文件,默认时8M，这也是默认的上传文件方式，最好不要修改默认分块大小
awskit -s3 -upload -h
上传命令帮助
```

```
awskit -ec2 -instance -c ./xxx.yml
通过yaml配置文件申请亚马逊机器
yaml配置文件格式如下：

- instance:
    input:
        name: genetalk_db_machine 
        image_id: ami-fce3c696 
        keyname: gcta-us-east-1-access-key   
        subnet_id:
            value: subnet-3698831c 
        number: 1
        instance_type: m4.large 
        security_group_ids:
            value: [sg-706ed00a]
        tags:
            - tag:
                key: Name
                value: genetalk_test_instance 

        spot:
            price: 0.1
            wait_until_complete: 1

awskit -ec2 -instance -a reboot|stop|term|start -i INSTANCE_ID 
awskit -ec2 -instance -a reboot|stop|term|start --id INSTANCE_ID 
重启/关机/释放/启动某个id的机器
awskit -ec2 -instance -a find -tag TAG_NAME -o x
查找所有包含TAG_NAME的机器，并以x符号分割输出，可选项是n换行，和c逗号
awskit -ec2 -instance -a reboot|stop|term|start -i `awskit -ec2 -instance -a find -tag TAG_NAME -o x`
重启/关机/释放/启动 所有包含TAG_NAME的机器
awskit -ec2 -instance -h 
ec2命令帮助
```

## 设置亚马逊AccessKey

```
export AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
export AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXX
export AWS_DEFAULT_REGION=xxxxxxx

```
| Region | Name|
|-----|------|
|us-east-1|US East (N. Virginia)|
|us-west-1|美国西部（加利福尼亚北部）|
|us-west-2|美国西部（俄勒冈）|
|eu-west-1|欧洲（爱尔兰）|
|eu-central-1|欧洲（法兰克福）|
|ap-northeast-1|亚太地区（东京）|
|ap-northeast-2|亚太区域 (首尔)|
|ap-southeast-1|亚太地区（新加坡）|
|ap-southeast-2|亚太地区（悉尼）|
|sa-east-1|南美洲（圣保罗）|

