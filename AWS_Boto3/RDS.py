import botocore
import botocore.exceptions

from Logger import Logger


class RDSController:
    RDS_INSTANCES_DISPLAY_FORMAT = '  {0}({1})\t{2}({3}) - {4}\t<Created On:{5}>'
    STR_RDS_INSTANCE = "<AWS RDS Instances>"
    STR_STORAGE_FORMAT = "{} GB"
    ENGINE_NAME = 'mysql'
    DB_INSTANCE_TYPE = 'db.t2.micro'
    DB_ALLOCATE_STORAGE = 20
    MSG_INFO_DB_CREATED = "Successfully create DB instance '{}'"
    MSG_INFO_DB_STATUS = "Instance '{}' is '{}' "
    MSG_WARN_NO_RDS_INSTANCE = "There is no RDS Instance at this moment.."
    MSG_ERR_DB_NOT_CREATED = "Couldn't create DB instance"

    def __init__(self, rds_res):
        # RDSController Constructor
        self.rds = rds_res

    def list_db_instances(self):
        # list RDS instances
        db_instances = []
        try:
            response = self.rds.describe_db_instances()
            db_instances = response['DBInstances']
            if len(db_instances) == 0:
                Logger.warn(self.MSG_WARN_NO_RDS_INSTANCE)
            else:
                Logger.header(self.STR_RDS_INSTANCE)
                for instance in db_instances:
                    created_on = "NA"
                    if instance['DBInstanceStatus'] != 'creating':
                        created_on = instance['InstanceCreateTime']
                    Logger.info(self.RDS_INSTANCES_DISPLAY_FORMAT.format(instance['DBInstanceIdentifier'],
                                                                         instance['DBInstanceStatus'],
                                                                         instance['DBInstanceClass'],
                                                                         self.STR_STORAGE_FORMAT.format(
                                                                             instance['AllocatedStorage']),
                                                                         instance['Engine'], created_on))
        except botocore.exceptions.ClientError as error:
            Logger.err(str(error))
        return db_instances

    def create_db_instances(self, db_instance_name, db_master_user_name, db_master_password, engine_name):
        # Create DB instance
        try:
            response = self.rds.create_db_instance(DBInstanceIdentifier=db_instance_name,
                                                   DBInstanceClass=self.DB_INSTANCE_TYPE,
                                                   DBName="{}_db".format(engine_name),
                                                   Engine=engine_name,
                                                   MasterUsername=db_master_user_name,
                                                   MasterUserPassword=db_master_password,
                                                   AllocatedStorage=self.DB_ALLOCATE_STORAGE
                                                   )

            # check Create DB instance returned successfully
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                Logger.info(self.MSG_INFO_DB_CREATED.format(db_instance_name))
            else:
                Logger.err(self.MSG_ERR_DB_NOT_CREATED)
        except botocore.exceptions.ClientError as error:
            Logger.err(str(error))

    def start_db_instances(self, db_instance_name):
        try:
            response = self.rds.start_db_instance(DBInstanceIdentifier=db_instance_name)
            instance = response['DBInstance']
            Logger.info(self.MSG_INFO_DB_STATUS.format(db_instance_name, instance['DBInstanceStatus']))
        except botocore.exceptions.ClientError as error:
            Logger.err(str(error))

    def stop_db_instances(self, db_instance_name):
        try:
            response = self.rds.stop_db_instance(DBInstanceIdentifier=db_instance_name)
            instance = response['DBInstance']
            Logger.info(self.MSG_INFO_DB_STATUS.format(db_instance_name, instance['DBInstanceStatus']))
        except botocore.exceptions.ClientError as error:
            Logger.err(str(error))
