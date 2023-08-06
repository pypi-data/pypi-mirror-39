import unittest  
from libaws.ec2 import instance 
import os
from libaws.common.logger import logger,enable_debug_log
import libaws.common.config as config
import libaws.base.basedb as basedb
import datetime

class TestInstanceFunctions(unittest.TestCase):  

    def setUp(self):  
        self.test_dir = os.path.abspath(os.path.split(__file__)[0])
                
    def ___test_create_instance(self):  
        yaml_config_file = os.path.join(self.test_dir,'instance_config.yaml')
        self.instance = instance.create_default_instance_from_config(yaml_config_file)
        instance.ssh_connect_instance(self.instance)
    
    def ___test_connect_instance(self):  
        instance.ssh_connect_instance(self.instance)
        

    def ___test_create_instance_with_args(self):
        # import json
        #print json.dumps(d,indent=4)
        args = {
            "input": {
                "instance_type": "t2.micro", 
                "name": "test_wukan_machine", 
                "tags": [
                    {
                        "tag": {
                            "key": "Name", 
                            "value": "wukan_test_instance"
                        }
                    }
                ], 
                "subnet_id": {
                    "value": "subnet-3b83ff5e"
                }, 
                "image_id": "ami-fce3c696", 
                "security_group_ids": {
                    "value": [
                        "sg-706ed00a"
                    ]
                }, 
                "number": 1,
                'spot': {
                'price':0.1,
                'wait_until_complete':1
            }
            }, 
            "keypair": {
                "delete_exists": "true", 
                "key": "test_wukan_key"
            }
##            "volumes": [
##                {
##                    "volume": {
##                        "name": "/dev/sda1", 
##                        "size": 10
##                    }
##                }
##            ]
        }
        enable_debug_log(True)
        print instance.create_instance(args)
        

    def test_get_db_info(self):
        
        base_app_data_path = os.getenv('HOME','.')
        app_data_path = os.path.join(base_app_data_path,'.libaws')
        db_path = os.path.join(app_data_path,'data',config.DEFAULT_INSTANCE_CONFIG_DB_NAME)
        db_conn = basedb.BaseDb(db_path)
        result = db_conn.fetchone("select instance_id,available_zone,price,created_time from %s where private_ip=\"%s\"" % (config.DEFAULT_INSTANCE_CONFIG_TABLE_NAME,'14.12.68.99'))
        print result
        if result is None:
            print 'sorry there is no instance ip address is',ip_addr
        else:
            instance_id,available_zone,price,create_time = result
            end_time = datetime.datetime.now()
            
            ISO_8601_DATE_FORMAT = "%Y-%m-%d"
            ISO_8601_TIME_FORMAT = "%H:%M:%S"
            ISO_8601_DATETIME_FORMAT = "%s %s" %(ISO_8601_DATE_FORMAT,
                                                 ISO_8601_TIME_FORMAT)
            start_time = datetime.datetime.strptime(create_time, ISO_8601_DATETIME_FORMAT)
            print end_time,start_time,end_time-start_time
            
            time_delta = end_time-start_time
            total_seconds = time_delta.total_seconds()
            total_price = (total_seconds/3600.0) * float(price)
            print total_price*7.9
                            
if __name__ == '__main__':  
    unittest.main()
