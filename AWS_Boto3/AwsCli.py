#!/usr/bin/env python3
from menu import Menu
from Logger import Logger
import getpass
from Config import AWS_REGION, WINDOWS_AMI_ID, LINUX_AMI_ID, WINDOWS_FREE_TIER_INSTANCE_TYPE, \
    LINUX_FREE_TIER_INSTANCE_TYPE, OWNER_ID, AVAILABILITY_ZONE, UPLOAD_DIR_FOR_S3, DOWNLOAD_DIR_FOR_S3, \
    CPU_ALARM_TOPIC_NAME
import os
import Resources
import EC2
import S3
import SNS
import CloudWatch
import Volumes
import RDS

# -----Constants--------------#
# String constants
STR_HEADER = "--------------------------------------------------------------------"
STR_FOOTER = "--------------------------------------------------------------------"
STR_PROMPT = ">>"
STR_HELLO = "Hello"
STR_SUFFIX = ": "
STR_INPUT_USERNAME = "Username"
STR_INPUT_PASSWD = "Password"
STR_WINDOWS = "windows"
STR_LINUX = "linux"
STR_CWD = "[CWD:'{}']"
STR_RDS = "\n<Amazon RDS>"
# Password file name
PASSWD_TXT = "passwd.txt"
# Menu Titles
TITLE_MAIN_MENU = "\n[Main Menu]"
TITLE_EC2_MENU = "\n[EC2 Menu]"
TITLE_EBS_MENU = "\n[EBS Menu]"
TITLE_S3_MENU = "\n[S3 Menu]"
TITLE_MONITORING_MENU = "\n[Monitoring Menu]"
TITLE_SETTING_MENU = "\n[Setting Menu]"
SETTING_MENU_ITEM1 = "Disable Color Menu"
SETTING_MENU_ITEM2 = "Enable Color Menu"
SETTING_MENU_ITEM3 = "Display Volume Attachment Data"
SETTING_MENU_ITEM4 = "Hide Volume Attachment Data"
SETTING_MENU_ITEM5 = "Set local upload dir path for S3"
SETTING_MENU_ITEM6 = "Set local download dir path for S3"
# BACK
COMMON_MENU_BACK = "Go back"
# Main Menu Items
MAIN_MENU_ITEM1 = "EC2 Instances"
MAIN_MENU_ITEM2 = "EBS Storage"
MAIN_MENU_ITEM3 = "S3 Storage"
MAIN_MENU_ITEM4 = "Monitoring"
MAIN_MENU_ITEM5 = "Logout"
MAIN_MENU_ITEM6 = "Exit"
MAIN_MENU_ITEM7 = "Setting"
# EC2 Menu Items
EC2_MENU_ITEM1 = "List all instances"
EC2_MENU_ITEM2 = "Start a specific instance"
EC2_MENU_ITEM3 = "Stop a specific instance"
EC2_MENU_ITEM4 = "Create an AMI from an existing Instance"
EC2_MENU_ITEM5 = "Launch a new instance from an existing (free tier) AMI"
# EBS Menu Items
EBS_MENU_ITEM1 = "List all volumes"
EBS_MENU_ITEM2 = "Attach an existing volume to an instance"
EBS_MENU_ITEM3 = "Detach a volume from an instance"
EBS_MENU_ITEM4 = "Take a snapshot of a specific volume"
EBS_MENU_ITEM5 = "Create a volume from a snapshot"
# S3 Storage Menu Items
S3_MENU_ITEM1 = "List all buckets"
S3_MENU_ITEM2 = "List all objects in a bucket"
S3_MENU_ITEM3 = "Upload an object"
S3_MENU_ITEM4 = "Download an object"
S3_MENU_ITEM5 = "Delete an object"
# Monitoring Menu Items
MON_MENU_ITEM1 = "Display EC2 performance metrics({} and {})"
MON_MENU_ITEM2 = "Set an alarm for CPU utilization"
MON_MENU_ITEM3 = "Relational DB Service"
# RDS Menu Items
RDS_MENU_ITEM1 = "List RDS instances"
RDS_MENU_ITEM2 = "Create RDS instance"
RDS_MENU_ITEM3 = "Start Instance"
RDS_MENU_ITEM4 = "Stop Instance"
# Key used in Dict for AWS password
KEY_AWS_PASSWORD = "password"
# Key used in Dict for AWS key
KEY_AWS_KEY = "aws_key"
# Key used in Dict for AWS secret
KEY_AWS_SECRET = "aws_secret"
# Messages
MSG_PROMPT_INPUT_S3_LOCAL_FILE_NAME = "Input local file name Name(Optional)"
MSG_PROMPT_INPUT_S3_OBJECT_KEY = "Input Key Name({})"
MSG_PROMPT_INPUT_DESC_ID = "Input Description for {}[{}]"
MSG_PROMPT_INPUT_DEVICE_NAME = "Input Device Name(Press Enter for back)"
MSG_PROMPT_INPUT_ID = "Input {} id from above list(Press Enter for back)"
MSG_PROMPT_INPUT_DB_INSTANCE_NAME = "Input DB instance Name{}(Press Enter for back)"
MSG_PROMPT_INPUT_DB_USER_NAME = "Input DB master username(Press Enter for back)"
MSG_PROMPT_INPUT_DB_PASSWORD = "Input DB master password(Press Enter for back)"
MSG_PROMPT_INPUT_DB_ENGINE = "Input DB engine from above list(Press Enter for back)"
MSG_PROMPT_INPUT_OBJECT = "Input '{}' bucket's object from above list(Press Enter for back)"
MSG_PROMPT_INPUT_EMAIL = "Input email for Alarm Notifications of '{}' topic(Optional)"
MSG_PROMPT_INPUT_BUCKET = "Input Bucket Name from the above list(Press Enter for back)"
MSG_PROMPT_INPUT_IMAGE_NAME = "Input image name(3~128 len)(Press Enter for back)"
MSG_PROMPT_AMI_OS_TYPE = "Input 'OS' type['windows' or 'linux'] for instance creation(Press Enter for back)"
MSG_PROMPT_INPUT_S3_LOCAL_DIR = "Input path of local {} dir for S3"
MSG_PROMPT_OVERRIDE_FILE = "File '{}' already exist in local dir '{}'.Do you want to override(Y/N):"
MSG_INFO_S3_SET_LOCAL_DIR = "Setting  dir '{}' as local {} dir for S3"
MSG_INFO_WELCOME_MESSAGE = ""
MSG_INFO_LOGIN_MESSAGE = "Please provide login details:"
MSG_INFO_LOGGED_IN_MESSAGE = "Logged In Successfully."
MSG_INFO_LOGOUT_MESSAGE = "Logout Successfully."
MSG_INFO_FILES_IN_DIR = "Files in local dir '{}' : {}"
MSG_INFO_FILE_OVERRIDE = "Overriding file '{}' in local dir '{}'."
MSG_INFO_SETTING_CPU_ALARM = "Setting CPU utilization alarm on instance '{}'"
MSG_ERR_FILE_DOES_NOT_HAVE_VALID_DATA = "File '{}' does not have valid data."
MSG_ERR_FILE_DOES_NOT_EXIST = "File '{}' does not exist."
MSG_ERR_DIR_DOES_NOT_EXIST = "Dir '{}' does not exist."
MSG_ERR_INVALID_INSTANCE_ID = "Invalid instance id: {}"
MSG_ERR_INVALID_VOLUME_ID = "Invalid volume id: {}"
MSG_ERR_INCORRECT_PASSWORD = "Incorrect password."
MSG_ERR_USER_NOT_EXIST = "User does not exist."
MSG_ERR_INVALID_INPUT = "Incorrect username or password(invalid input)."
MSG_ERR_INVALID_AMI_INPUT = "Incorrect AMI OS type input."
MSG_ERR_WRONG_INPUT = "Wrong Input:{}"
MSG_ERR_DEV_NAME_ALREADY_IN_USE = "Device Name already in use: {}"
MSG_WARN_DETACH_ROOT_ON_RUNNING = "instance '{}' is running currently.EBS root volume '{}' can be detached by " \
                                  "stopping the instance."
MSG_WARN_NO_ATTACHMENT_DATA_FOR_VOL = "No attachment data for volume {}"
MSG_WARN_LOCAL_DIR_NOT_EXIST = "dir '{}' does not exist.Setting  dir '{}' as local {} dir for S3"
MSG_WARN_NO_FILE_TO_UPLOAD = "There is no file in '{}' dir for upload.."
MSG_WARN_DOWNLOAD_CANCEL = "Downloading of file '{}' cancelled"
MSG_WARN_PASSWORD_LEN_MIN = "Password Must contain equal or greater than 8 char."
SUGGESTION_WINDOWS = "\n--->[Device Name range for selected instance({}): 'xvd[f-p]']"
SUGGESTION_LINUX = "\n--->[Device Name range for selected instance({}): '/dev/sd[f-p]']"
SUGGESTION_AS_ROOT_DEVICE = "\n--->[Instance({}) does not have a volume attached at root.Better to attach at root " \
                            "first '{}'.] "
CPU_UTILIZATION = "CPUUtilization"
MEM_UTILIZATION = "MemoryUtilization"
RDS_DESCRIPTION = "Amazon Relational Database Service (Amazon RDS) is a web service that makes it easier to set up, " \
                  "operate, and scale a relational database in the cloud. It provides cost-efficient, resizeable " \
                  "capacity for an industry-standard relational database and manages common database administration " \
                  "tasks, freeing up developers to focus on what makes their applications and businesses " \
                  "unique.\n\nAmazon RDS was first released in October 2009, with support for MySQL databases. " \
                  "Subsequent releases have added support for additional database types, with PostgreSQL and " \
                  "MariaDB being the most recent.\n\nRDS is designed to reduce operational costs and overcome some " \
                  "common challenges that businesses experience when running databases through tools like MySQL."
RDS_DB_ENGINE = ['mysql', 'mariadb', 'postgres']


class AwsCli:
    # A class for CLI operations on AWS services.
    # This AWS CLI class used Menu package for creating the Menu for AWS operations.
    # Please refer the below link for more details about Menu package
    # https://pypi.org/project/Menu/#description

    def __init__(self):
        # init
        self.logged_in = False
        self.username = None
        self.passwdDict = dict()
        self.aws_res = None
        self.ec2_res = None
        self.s3_res = None
        self.cw_client = None
        self.ec2_client = None
        self.sns_client = None
        self.rds_client = None
        self.ec2_cont = None
        self.ebs_cont = None
        self.s3_cont = None
        self.sns_cont = None
        self.rds_cont = None
        self.cw_cont = None
        self.show_attachment_data = False
        self.local_dir_for_s3_upload = UPLOAD_DIR_FOR_S3
        self.local_dir_for_s3_download = DOWNLOAD_DIR_FOR_S3
        # -------------EC2-------------
        # Options of EC2 Menu
        self.ec2_menu_options = [
            (EC2_MENU_ITEM1, self.ec2_list),
            (EC2_MENU_ITEM2, self.ec2_start_instance),
            (EC2_MENU_ITEM3, self.ec2_stop_instance),
            (EC2_MENU_ITEM4, self.ec2_create_ami),
            (EC2_MENU_ITEM5, self.ec2_create_instance),
            (COMMON_MENU_BACK, Menu.CLOSE)
        ]
        # EC2 Menu
        self.ec2_menu = Menu(
            options=self.ec2_menu_options,
            title=TITLE_EC2_MENU,
            auto_clear=False
        )
        # -------------EBS-------------
        # Options of EBS Menu
        self.ebs_menu_options = [
            (EBS_MENU_ITEM1, self.ebs_list_volumes),
            (EBS_MENU_ITEM2, self.ebs_attach_volume),
            (EBS_MENU_ITEM3, self.ebs_detach_volume),
            (EBS_MENU_ITEM4, self.ebs_create_snapshot),
            (EBS_MENU_ITEM5, self.ebs_create_volume),
            (COMMON_MENU_BACK, Menu.CLOSE)
        ]
        # EBS Menu
        self.ebs_menu = Menu(
            options=self.ebs_menu_options,
            title=TITLE_EBS_MENU,
            auto_clear=False
        )
        # -------------S3-------------
        # Options of S3 Menu
        self.s3_menu_options = [
            (S3_MENU_ITEM1, self.s3_list_bucket),
            (S3_MENU_ITEM2, self.s3_list_bucket_objects),
            (S3_MENU_ITEM3, self.s3_upload_object),
            (S3_MENU_ITEM4, self.s3_download_object),
            (S3_MENU_ITEM5, self.s3_delete_object),
            (COMMON_MENU_BACK, Menu.CLOSE)
        ]
        # S3 Menu
        self.s3_menu = Menu(
            options=self.s3_menu_options,
            title=TITLE_S3_MENU,
            auto_clear=False
        )
        # Amazon RDS Menu Options
        self.amazon_rds_menu_options = [
            (RDS_MENU_ITEM1, self.list_db_instances),
            (RDS_MENU_ITEM2, self.create_db_instance),
            (RDS_MENU_ITEM3, self.start_db_instance),
            (RDS_MENU_ITEM4, self.stop_db_instance),
            (COMMON_MENU_BACK, Menu.CLOSE)
        ]
        # Amazon RDS Menu
        self.monitoring_rds_menu = Menu(
            options=self.amazon_rds_menu_options,
            title=STR_RDS,
            message=RDS_DESCRIPTION,
            auto_clear=False
        )
        # -------------Monitoring-------------
        # Options of Monitoring Menu
        self.monitoring_menu_options = [
            (MON_MENU_ITEM1.format(CPU_UTILIZATION, MEM_UTILIZATION), self.monitoring_display_metrics),
            (MON_MENU_ITEM2, self.monitoring_set_alarm),
            (MON_MENU_ITEM3, self.monitoring_rds_menu.open),
            (COMMON_MENU_BACK, Menu.CLOSE)
        ]
        # Monitoring Menu
        self.monitoring_menu = Menu(
            options=self.monitoring_menu_options,
            title=TITLE_MONITORING_MENU,
            auto_clear=False
        )

        # Options of Setting Menu
        self.setting_menu_options = [
            (SETTING_MENU_ITEM1, self.setting_disable_color_menu),
            (SETTING_MENU_ITEM2, self.setting_enable_color_menu),
            (SETTING_MENU_ITEM3, self.setting_display_attachment_of_volume),
            (SETTING_MENU_ITEM4, self.setting_hide_attachment_of_volume),
            (SETTING_MENU_ITEM5, self.setting_local_upload_dir_path),
            (SETTING_MENU_ITEM6, self.setting_local_download_dir_path),
            (COMMON_MENU_BACK, Menu.CLOSE)
        ]

        # Setting Menu
        self.setting_menu = Menu(
            options=self.setting_menu_options,
            title=TITLE_SETTING_MENU,
            refresh=self.check_user,
            auto_clear=False
        )
        # -------------Main Menu-------------
        # Options of Main Menu
        self.main_menu_options = [
            (MAIN_MENU_ITEM1, self.ec2_menu.open),
            (MAIN_MENU_ITEM2, self.ebs_menu.open),
            (MAIN_MENU_ITEM3, self.s3_menu.open),
            (MAIN_MENU_ITEM4, self.monitoring_menu.open),
            (MAIN_MENU_ITEM7, self.setting_menu.open),
            (MAIN_MENU_ITEM5, self.logout),
            (MAIN_MENU_ITEM6, Menu.CLOSE)
        ]
        # Main Menu
        self.main_menu = Menu(
            title=TITLE_MAIN_MENU,
            message=MSG_INFO_WELCOME_MESSAGE,
            refresh=self.check_user,
            auto_clear=False)

        self.main_menu.set_prompt(STR_PROMPT)

    def ec2_controller(self):
        # get EC2 Controller
        if self.ec2_cont is None:
            self.ec2_cont = EC2.EC2Controller(self.ec2_res, self.ec2_client)
        return self.ec2_cont

    def ec2_list(self):
        # Get the EC2 list
        cont = self.ec2_controller()
        Logger.header(STR_HEADER)
        cont.list_instances()
        Logger.header(STR_FOOTER)

    def ec2_start_instance(self):
        # Start the EC2 instance
        cont = self.ec2_controller()
        while True:
            Logger.header(STR_HEADER)
            stopped_instances = cont.list_stopped_instance()
            if len(stopped_instances) > 0:
                instance_id = input(MSG_PROMPT_INPUT_ID.format("stopped-instance") + STR_SUFFIX)
                if instance_id is not None and len(instance_id) != 0:
                    if instance_id not in stopped_instances:
                        Logger.err(MSG_ERR_INVALID_INSTANCE_ID.format(instance_id))
                    else:
                        cont.start_instance(instance_id)
                else:
                    break
            else:
                break
        Logger.header(STR_FOOTER)

    def ec2_stop_instance(self):
        # Stop the EC2 instance
        cont = self.ec2_controller()
        while True:
            Logger.header(STR_HEADER)
            running_instances = cont.list_running_instance()
            if len(running_instances) > 0:
                instance_id = input(MSG_PROMPT_INPUT_ID.format("running-instance") + STR_SUFFIX)
                if instance_id is not None and len(instance_id) != 0:
                    if instance_id not in running_instances:
                        Logger.err(MSG_ERR_INVALID_INSTANCE_ID.format(instance_id))
                    else:
                        cont.stop_instance(instance_id)
                else:
                    break
            else:
                break
        Logger.header(STR_FOOTER)

    def ec2_create_ami(self):
        # Create the AMI from instance
        cont = self.ec2_controller()
        while True:
            Logger.header(STR_HEADER)
            instances_for_ami = cont.list_stopped_running_instances()
            if len(instances_for_ami) > 0:
                instance_id = input(MSG_PROMPT_INPUT_ID.format("instance") + STR_SUFFIX)
                image_name = input(MSG_PROMPT_INPUT_IMAGE_NAME + STR_SUFFIX)
                if (instance_id is not None and len(instance_id) != 0) and (
                        image_name is not None and len(image_name) != 0):
                    if instance_id not in instances_for_ami:
                        Logger.err(MSG_ERR_INVALID_INSTANCE_ID.format(instance_id))
                    else:
                        cont.create_image(instance_id, image_name)
                else:
                    break
            else:
                break

        Logger.header(STR_FOOTER)

    def ec2_create_instance(self):
        # Create a new EC2 instance
        cont = self.ec2_controller()
        while True:
            Logger.header(STR_HEADER)
            ami_type = input(MSG_PROMPT_AMI_OS_TYPE + STR_SUFFIX)
            if ami_type == STR_LINUX:
                cont.create_instance(LINUX_AMI_ID, LINUX_FREE_TIER_INSTANCE_TYPE)
            elif ami_type == STR_WINDOWS:
                cont.create_instance(WINDOWS_AMI_ID, WINDOWS_FREE_TIER_INSTANCE_TYPE)
            elif ami_type is None or len(ami_type) == 0:
                break
            else:
                Logger.err(MSG_ERR_INVALID_AMI_INPUT)
        Logger.header(STR_FOOTER)

    def ebc_controller(self):
        # get EBS Controller
        if self.ebs_cont is None:
            self.ebs_cont = Volumes.Volumes(self.ec2_res, self.ec2_client)
        return self.ebs_cont

    def ebs_list_volumes(self):
        # List all volumes
        Logger.header(STR_HEADER)
        vol = self.ebc_controller()
        vol.list_volumes(self.show_attachment_data)
        Logger.header(STR_FOOTER)

    def ebs_attach_volume(self):
        # Attach an existing volume to an instance
        cont = self.ec2_controller()
        vol = self.ebc_controller()
        while True:
            Logger.header(STR_HEADER)
            volume_count = vol.list_volumes(self.show_attachment_data)
            # list all volumes
            if volume_count > 0:
                available_volumes = vol.list_available_volumes()
                if len(available_volumes) > 0:
                    # list all available volumes
                    volume_id = input(MSG_PROMPT_INPUT_ID.format("available volume") + STR_SUFFIX)
                    if volume_id is not None and len(volume_id) != 0:
                        # Error message if user input wrong volume id
                        if volume_id not in available_volumes:
                            Logger.err(MSG_ERR_INVALID_VOLUME_ID.format(volume_id))
                        else:
                            instances = cont.list_stopped_running_instances()
                            # list all available instances for Attaching the volume
                            if len(instances) > 0:
                                while True:
                                    instance_id = input(MSG_PROMPT_INPUT_ID.format("instance") + STR_SUFFIX)
                                    if instance_id is not None and len(instance_id) != 0:
                                        if instance_id not in instances:
                                            # Error message if user input wrong instance id
                                            Logger.err(MSG_ERR_INVALID_INSTANCE_ID.format(instance_id))
                                        else:
                                            attached_block_devices = cont.instance_attached_block_devices(instance_id)
                                            # list the all block devices attached to user specified instance
                                            platform_name = cont.instance_platform_name(instance_id)
                                            # platform name of instance to display device name's suggestion
                                            root_device_name = cont.instance_root_device_name(instance_id)
                                            if root_device_name not in attached_block_devices:
                                                # check if root device name exist in attached block devices
                                                Logger.info(
                                                    SUGGESTION_AS_ROOT_DEVICE.format(instance_id, root_device_name))
                                            elif platform_name == "windows":
                                                Logger.info(SUGGESTION_WINDOWS.format(instance_id))
                                            else:
                                                Logger.info(SUGGESTION_LINUX.format(instance_id))
                                            dev_name = input(MSG_PROMPT_INPUT_DEVICE_NAME + STR_SUFFIX)
                                            if dev_name is not None and len(dev_name) != 0:
                                                if dev_name in attached_block_devices:
                                                    # Error message if user input device name that is already in use
                                                    Logger.err(MSG_ERR_DEV_NAME_ALREADY_IN_USE.format(dev_name))
                                                else:
                                                    vol.attach_volume(instance_id, volume_id, dev_name)
                                                    # attach volume to instance
                                            break
                                    else:
                                        break
                            else:
                                break
                    else:
                        break
                else:
                    break
            else:
                break
        Logger.header(STR_FOOTER)

    def ebs_detach_volume(self):
        # Detach a volume from an instance
        vol = self.ebc_controller()
        while True:
            Logger.header(STR_HEADER)
            volume_count = vol.list_volumes(self.show_attachment_data)
            if volume_count > 0:
                # list all volumes
                in_use_volumes = vol.list_in_use_volumes()
                if len(in_use_volumes) > 0:
                    # list all in-use volumes
                    volume_id = input(MSG_PROMPT_INPUT_ID.format("in-use volume") + STR_SUFFIX)
                    if volume_id is not None and len(volume_id) != 0:
                        # Error message if user input wrong volume id
                        if volume_id not in in_use_volumes:
                            Logger.err(MSG_ERR_INVALID_VOLUME_ID.format(volume_id))
                        else:
                            attach_list = vol.volume_attachment_data(volume_id)
                            if len(attach_list) == 1:
                                attachment = attach_list[0]
                                instance_id = attachment["InstanceId"]
                                dev_name = attachment["Device"]
                                self.validate_n_detach_volume(dev_name, instance_id, vol, volume_id)
                            elif len(attach_list) > 1:
                                # Not in our case but considering this case
                                # https://aws.amazon.com/blogs/aws/new-multi-attach-for-provisioned-iops-io1-amazon-ebs-volumes/
                                instance_id = input(MSG_PROMPT_INPUT_ID.format("instance") + STR_SUFFIX)
                                if instance_id is not None and len(instance_id) != 0:
                                    dev_name = input(MSG_PROMPT_INPUT_DEVICE_NAME + STR_SUFFIX)
                                    if dev_name is not None and len(dev_name) != 0:
                                        self.validate_n_detach_volume(dev_name, instance_id, vol, volume_id)
                                    else:
                                        break
                                else:
                                    break
                            else:
                                Logger.warn(MSG_WARN_NO_ATTACHMENT_DATA_FOR_VOL.format(volume_id))
                    else:
                        break
                else:
                    break
            else:
                break
        Logger.header(STR_FOOTER)

    def ebs_create_snapshot(self):
        # Take a snapshot of a specific volume
        vol = self.ebc_controller()
        while True:
            Logger.header(STR_HEADER)
            volume_count = vol.list_volumes(self.show_attachment_data)
            if volume_count > 0:
                volume_id = input(MSG_PROMPT_INPUT_ID.format("volume") + STR_SUFFIX)
                if volume_id is not None and len(volume_id) != 0:
                    volume_desc = input(MSG_PROMPT_INPUT_DESC_ID.format("volume", "optional") + STR_SUFFIX)
                    vol.create_snapshot(volume_id, volume_desc)
                else:
                    break
            else:
                break
        Logger.header(STR_FOOTER)

    def ebs_create_volume(self):
        # Create a volume from a snapshot
        vol = self.ebc_controller()
        cont = self.ec2_controller()
        while True:
            Logger.header(STR_HEADER)
            snap_count = vol.list_snapshots(OWNER_ID)
            if snap_count > 0:
                snapshot_id = input(MSG_PROMPT_INPUT_ID.format("snapshot") + STR_SUFFIX)
                if snapshot_id is not None and len(snapshot_id) != 0:
                    cont.create_volume(AVAILABILITY_ZONE, snapshot_id)
                else:
                    break
            else:
                break
        Logger.header(STR_FOOTER)

    def s3_controller(self):
        # get S3 Controller
        if self.s3_cont is None:
            self.s3_cont = S3.S3Controller(self.s3_res)
        return self.s3_cont

    def s3_list_bucket(self):
        # list all buckets
        s3cont = self.s3_controller()
        Logger.header(STR_HEADER)
        s3cont.list_buckets()
        Logger.header(STR_FOOTER)

    def s3_list_bucket_objects(self):
        # Display all objects of the S3 bucket
        s3_cont = self.s3_controller()
        while True:
            Logger.header(STR_HEADER)
            bucket_list = s3_cont.list_buckets()
            if len(bucket_list) > 0:
                if len(bucket_list) == 1:
                    s3_cont.list_bucket_objects(bucket_list[0])
                    break
                else:
                    bucket_name = input(MSG_PROMPT_INPUT_BUCKET + STR_SUFFIX)
                    if bucket_name is not None and len(bucket_name) != 0:
                        s3_cont.list_bucket_objects(bucket_name)
                    else:
                        break
            else:
                break
        Logger.header(STR_FOOTER)

    def s3_upload_object(self):
        # Upload object in a bucket
        s3_cont = self.s3_controller()
        object_list = []
        if os.path.exists(self.local_dir_for_s3_upload):
            # check local upload dir exist
            for file in os.listdir(self.local_dir_for_s3_upload):
                if not os.path.isdir(os.path.join(self.local_dir_for_s3_upload, file)):
                    # exclude dir inside download dir
                    object_list.append(file)
            if len(object_list) > 0:
                while True:
                    Logger.header(STR_HEADER)
                    bucket_list = s3_cont.list_buckets()
                    # get all buckets as list
                    if len(bucket_list) > 0:
                        if len(bucket_list) == 1:
                            bucket_name = bucket_list[0]
                            # if only 1 bucket exist than not need to prompt for input
                        else:
                            bucket_name = input(MSG_PROMPT_INPUT_BUCKET + STR_SUFFIX)
                            # more than 1 buckets.prompt for input
                        if bucket_name is not None and len(bucket_name) != 0:
                            Logger.sub_info(
                                MSG_INFO_FILES_IN_DIR.format(self.local_dir_for_s3_upload, str(object_list)))
                            # list all objects from local upload dir
                            target_object = input(MSG_PROMPT_INPUT_OBJECT.format(bucket_name) + STR_SUFFIX)
                            if target_object is not None and len(target_object) != 0:
                                object_with_path = os.path.join(self.local_dir_for_s3_upload, target_object)
                                if os.path.exists(object_with_path):
                                    key_name = input(MSG_PROMPT_INPUT_S3_OBJECT_KEY.format("Optional") + STR_SUFFIX)
                                    # prompt for key.
                                    if key_name is None or len(key_name) == 0:
                                        key_name = target_object
                                        # if key_name is not input by user.It will be same as selected object from
                                        # from bucket
                                    s3_cont.upload_file(bucket_name, object_with_path, key_name)
                                else:
                                    Logger.warn(MSG_ERR_WRONG_INPUT.format(target_object))
                            else:
                                break
                        else:
                            break
                    else:
                        break
                Logger.header(STR_FOOTER)
            else:
                Logger.warn(MSG_WARN_NO_FILE_TO_UPLOAD.format(self.local_dir_for_s3_upload))
                Logger.header(STR_FOOTER)
        else:
            Logger.err(MSG_ERR_DIR_DOES_NOT_EXIST.format(self.local_dir_for_s3_upload))
            Logger.header(STR_FOOTER)

    def s3_download_object(self):
        # download object from a bucket
        s3_cont = self.s3_controller()
        while True:
            object_list = []
            if os.path.exists(self.local_dir_for_s3_download):
                # check local download dir exist
                for file in os.listdir(self.local_dir_for_s3_download):
                    if not os.path.isdir(os.path.join(self.local_dir_for_s3_download, file)):
                        # exclude dir inside download dir
                        object_list.append(file)
                Logger.header(STR_HEADER)
                if len(object_list) > 0:
                    Logger.sub_info(MSG_INFO_FILES_IN_DIR.format(self.local_dir_for_s3_download, str(object_list)))
                bucket_list = s3_cont.list_buckets()
                # get all buckets as list
                if len(bucket_list) > 0:
                    if len(bucket_list) == 1:
                        bucket_name = bucket_list[0]
                        # if only 1 bucket exist than not need to prompt for input
                    else:
                        bucket_name = input(MSG_PROMPT_INPUT_BUCKET + STR_SUFFIX)
                        # more than 1 buckets.prompt for input
                    if bucket_name is not None and len(bucket_name) != 0:
                        bucket_objects = s3_cont.list_bucket_objects(bucket_name)
                        # list all objects of bucket 'bucket_name'
                        target_object = input(MSG_PROMPT_INPUT_OBJECT.format(bucket_name) + STR_SUFFIX)
                        # prompt for the target object
                        if target_object is not None and len(target_object) != 0:
                            if target_object in bucket_objects:
                                local_file_name = input(MSG_PROMPT_INPUT_S3_LOCAL_FILE_NAME + STR_SUFFIX)
                                if local_file_name is None or len(local_file_name) == 0:
                                    local_file_name = target_object
                                local_file_path = os.path.join(self.local_dir_for_s3_download, local_file_name)
                                if os.path.exists(local_file_path):
                                    # if file already exist in local dir.prompt for override
                                    user_opt = input(MSG_PROMPT_OVERRIDE_FILE.format(local_file_name,
                                                                                     self.local_dir_for_s3_download))
                                    if user_opt == 'Y' or user_opt == 'y':
                                        Logger.info(MSG_PROMPT_OVERRIDE_FILE.format(local_file_name,
                                                                                    self.local_dir_for_s3_download))
                                        s3_cont.download_file(bucket_name, target_object, local_file_path)
                                        Logger.sub_info(str(object_list))
                                    elif user_opt == 'N' or user_opt == 'n':
                                        Logger.warn(MSG_WARN_DOWNLOAD_CANCEL.format(local_file_name))
                                    else:
                                        Logger.warn(MSG_ERR_WRONG_INPUT.format(user_opt))
                                else:
                                    s3_cont.download_file(bucket_name, target_object, local_file_path)
                            else:
                                Logger.warn(MSG_ERR_WRONG_INPUT.format(target_object))
                        else:
                            break
                    else:
                        break
                else:
                    break
            else:
                Logger.err(MSG_ERR_DIR_DOES_NOT_EXIST.format(self.local_dir_for_s3_download))
        Logger.header(STR_FOOTER)

    def s3_delete_object(self):
        # Delete the file from the bucket 'bucket_name'
        s3_cont = self.s3_controller()
        while True:
            Logger.header(STR_HEADER)
            bucket_list = s3_cont.list_buckets()
            if len(bucket_list) > 0:
                if len(bucket_list) == 1:
                    bucket_name = bucket_list[0]
                else:
                    bucket_name = input(MSG_PROMPT_INPUT_BUCKET + STR_SUFFIX)
                if bucket_name is not None and len(bucket_name) != 0:
                    bucket_objects = s3_cont.list_bucket_objects(bucket_name)
                    target_object = input(MSG_PROMPT_INPUT_OBJECT.format(bucket_name) + STR_SUFFIX)
                    if target_object is not None and len(target_object) != 0:
                        if target_object in bucket_objects:
                            s3_cont.delete_file(bucket_name, target_object)
                        else:
                            Logger.warn(MSG_ERR_WRONG_INPUT.format(target_object))
                    else:
                        break
                else:
                    break
            else:
                break
        Logger.header(STR_FOOTER)

    def sns_controller(self):
        # get SNS Controller
        if self.sns_cont is None:
            self.sns_cont = SNS.SNSController(self.sns_client)
        return self.sns_cont

    def cw_controller(self):
        # get Cloud Watch Controller
        if self.cw_cont is None:
            self.cw_cont = CloudWatch.CWController(self.cw_client)
        return self.cw_cont

    def monitoring_display_metrics(self):
        # get CPU Utilization and Memory Utilization metrics
        ec2_cont = self.ec2_controller()
        cw_cont = self.cw_controller()
        while True:
            Logger.header(STR_HEADER)
            instances_list = ec2_cont.list_stopped_running_instances()
            # Display running and stopped instances
            if len(instances_list) > 0:
                instance_id = input(MSG_PROMPT_INPUT_ID.format("instance") + STR_SUFFIX)
                if instance_id is not None and len(instance_id) != 0:
                    if instance_id not in instances_list:
                        Logger.err(MSG_ERR_INVALID_INSTANCE_ID.format(instance_id))
                        # Input instance id is wrong
                    else:
                        cw_cont.get_metric_statistics(instance_id, CPU_UTILIZATION)
                        cw_cont.get_metric_statistics(instance_id, MEM_UTILIZATION)
                else:
                    break
            else:
                break
        Logger.header(STR_FOOTER)

    def monitoring_set_alarm(self):
        # set CPU Utilization alarm
        ec2_cont = self.ec2_controller()
        sns_cont = self.sns_controller()
        cw_cont = self.cw_controller()
        while True:
            Logger.header(STR_HEADER)
            instances_list = ec2_cont.list_stopped_running_instances()
            # Display running and stopped instances
            if len(instances_list) > 0:
                instance_id = input(MSG_PROMPT_INPUT_ID.format("instance") + STR_SUFFIX)
                if instance_id is not None and len(instance_id) != 0:
                    if instance_id not in instances_list:
                        Logger.err(MSG_ERR_INVALID_INSTANCE_ID.format(instance_id))
                        # Input instance id is wrong
                    else:
                        topic_arn = sns_cont.create_topic(CPU_ALARM_TOPIC_NAME)
                        # create SNS topic for email notification
                        end_point = input(MSG_PROMPT_INPUT_EMAIL.format(CPU_ALARM_TOPIC_NAME) + STR_SUFFIX)
                        # ask for email input
                        if end_point is not None and len(end_point) != 0:
                            sns_cont.email_sub_to_topic(topic_arn, end_point)
                            # subscribe email account to SNS topic
                            Logger.info(MSG_INFO_SETTING_CPU_ALARM.format(instance_id))
                            cw_cont.set_cpu_alarm(instance_id, topic_arn)
                            # set CPU alarm
                else:
                    break
            else:
                break
        Logger.header(STR_FOOTER)

    def rds_controller(self):
        # get RDS Controller
        if self.rds_cont is None:
            self.rds_cont = RDS.RDSController(self.rds_client)
        return self.rds_cont

    def list_db_instances(self):
        # List DB instances
        rds_cont = self.rds_controller()
        Logger.header(STR_HEADER)
        rds_cont.list_db_instances()
        Logger.header(STR_FOOTER)

    def create_db_instance(self):
        # Create DB instance
        rds_cont = self.rds_controller()
        while True:
            Logger.header(STR_HEADER)
            db_instance_name = input(MSG_PROMPT_INPUT_DB_INSTANCE_NAME.format("") + STR_SUFFIX)
            if db_instance_name is not None and len(db_instance_name) != 0:
                db_master_user_name = input(MSG_PROMPT_INPUT_DB_USER_NAME + STR_SUFFIX)
                if db_master_user_name is not None and len(db_master_user_name) != 0:
                    db_master_password = getpass.getpass(MSG_PROMPT_INPUT_DB_PASSWORD + STR_SUFFIX)
                    if db_master_password is not None and len(db_master_password) != 0:
                        if len(db_master_password) < 8:
                            Logger.warn(MSG_WARN_PASSWORD_LEN_MIN)
                        else:
                            Logger.info(str(RDS_DB_ENGINE))
                            db_engine = input(MSG_PROMPT_INPUT_DB_ENGINE + STR_SUFFIX)
                            if db_engine is not None and len(db_engine) != 0:
                                if db_engine in RDS_DB_ENGINE:
                                    rds_cont.create_db_instances(db_instance_name, db_master_user_name,
                                                                 db_master_password, db_engine)
                                else:
                                    Logger.warn(MSG_ERR_WRONG_INPUT.format(db_engine))
                            else:
                                break
                    else:
                        break
                else:
                    break
            else:
                break
        Logger.header(STR_FOOTER)

    def start_db_instance(self):
        # Start DB instance
        rds_cont = self.rds_controller()
        while True:
            Logger.header(STR_HEADER)
            db_instances = rds_cont.list_db_instances()
            if len(db_instances) > 0:
                db_instance_name = input(MSG_PROMPT_INPUT_DB_INSTANCE_NAME.format(" for start ") + STR_SUFFIX)
                if db_instance_name is not None and len(db_instance_name) != 0:
                    rds_cont.start_db_instances(db_instance_name)
                else:
                    break
            else:
                break
        Logger.header(STR_FOOTER)

    def stop_db_instance(self):
        # Stop DB instance
        rds_cont = self.rds_controller()
        while True:
            Logger.header(STR_HEADER)
            db_instances = rds_cont.list_db_instances()
            if len(db_instances) > 0:
                db_instance_name = input(MSG_PROMPT_INPUT_DB_INSTANCE_NAME.format(" for stop ") + STR_SUFFIX)
                if db_instance_name is not None and len(db_instance_name) != 0:
                    rds_cont.stop_db_instances(db_instance_name)
                else:
                    break
            else:
                break
        Logger.header(STR_FOOTER)

    def validate_n_detach_volume(self, dev_name, instance_id, vol, volume_id):
        # validate if device is root device and instance is in running state.if yes then error message will display
        root_device_name = self.ec2_controller().instance_root_device_name(instance_id)
        instance_state = self.ec2_controller().instance_state(instance_id)
        if dev_name == root_device_name and instance_state == "running":
            Logger.warn(MSG_WARN_DETACH_ROOT_ON_RUNNING.format(instance_id, dev_name))
        else:
            vol.detach_volume(instance_id, volume_id, dev_name)

    def setting_enable_color_menu(self):
        # Enable color Menu
        if self.logged_in:
            Logger.enable_color()

    def setting_disable_color_menu(self):
        # Enable color Menu to make simple
        if self.logged_in:
            Logger.disable_color()

    def setting_display_attachment_of_volume(self):
        # display additional attachment info of volumes
        if self.logged_in:
            self.show_attachment_data = True

    def setting_hide_attachment_of_volume(self):
        # Hide additional attachment info of volumes
        if self.logged_in:
            self.show_attachment_data = False

    def setting_local_upload_dir_path(self):
        # set local upload dir path for s3 upload operation
        curr_working_dir = os.getcwd()
        Logger.sub_info(STR_CWD.format(curr_working_dir))
        upload_dir_path = input(MSG_PROMPT_INPUT_S3_LOCAL_DIR.format("upload") + STR_SUFFIX)
        if os.path.exists(upload_dir_path):
            self.local_dir_for_s3_upload = upload_dir_path
            Logger.info(MSG_INFO_S3_SET_LOCAL_DIR.format(upload_dir_path, "upload"))
        else:
            self.local_dir_for_s3_upload = UPLOAD_DIR_FOR_S3
            Logger.err(MSG_WARN_LOCAL_DIR_NOT_EXIST.format(upload_dir_path,
                                                           UPLOAD_DIR_FOR_S3,
                                                           "upload"))

    def setting_local_download_dir_path(self):
        # set local download dir path for s3 download operation
        curr_working_dir = os.getcwd()
        Logger.sub_info(STR_CWD.format(curr_working_dir))
        download_dir_path = input(MSG_PROMPT_INPUT_S3_LOCAL_DIR.format("download") + STR_SUFFIX)
        if os.path.exists(download_dir_path):
            self.local_dir_for_s3_download = download_dir_path
            Logger.info(MSG_INFO_S3_SET_LOCAL_DIR.format(download_dir_path, "download"))
        else:
            self.local_dir_for_s3_download = DOWNLOAD_DIR_FOR_S3
            Logger.err(MSG_WARN_LOCAL_DIR_NOT_EXIST.format(download_dir_path, DOWNLOAD_DIR_FOR_S3, "download"))

    def check_user(self):
        # Method will display main menu if user is login successfully
        if self.logged_in:
            self.main_menu.set_options(self.main_menu_options)
            self.main_menu.set_message(STR_HELLO + " " + self.username)

    def login(self):
        # Method will validate the input username and password from password stored in file.
        Logger.info(MSG_INFO_LOGIN_MESSAGE)
        while not self.logged_in:
            user_input = input(STR_INPUT_USERNAME + STR_SUFFIX)
            if user_input is None or len(user_input) == 0:
                exit()
            pass_input = getpass.getpass(STR_INPUT_PASSWD + STR_SUFFIX)
            if user_input is None or pass_input is None or len(user_input) == 0 or len(pass_input) == 0:
                Logger.warn(MSG_ERR_INVALID_INPUT)
            elif user_input not in self.passwdDict.keys():
                # user not exist
                Logger.warn(MSG_ERR_USER_NOT_EXIST)
            elif self.passwdDict[user_input].get(KEY_AWS_PASSWORD) != pass_input:
                # password incorrect
                Logger.warn(MSG_ERR_INCORRECT_PASSWORD)
            else:
                self.username = user_input
                self.logged_in = True
                self.aws_res = Resources.Resource(AWS_REGION, self.passwdDict[self.username].get(KEY_AWS_KEY),
                                                  self.passwdDict[self.username].get(KEY_AWS_SECRET))
                self.ec2_res = self.aws_res.ec2_resource()
                # set ec2 resource
                self.s3_res = self.aws_res.s3_resource()
                # set S3 resource
                self.cw_client = self.aws_res.cw_client()
                # set cloud watch client
                self.ec2_client = self.aws_res.ec2_client()
                # set ec2 client
                self.sns_client = self.aws_res.sns_client()
                # set sns client
                self.rds_client = self.aws_res.rds_client()
                # set rds client
                Logger.info(MSG_INFO_LOGGED_IN_MESSAGE)
                self.main_menu.open()

    def read_file(self):
        # Method will read the password file and create the dictionary having username as key
        try:
            pass_file = open(PASSWD_TXT, "r")
        except FileNotFoundError:
            Logger.err(MSG_ERR_FILE_DOES_NOT_EXIST.format(PASSWD_TXT))
            return False
        while True:
            line = pass_file.readline()
            if line is None or len(line) <= 0:
                break
            split_val = line.strip().split("\t")
            if len(split_val) != 4:
                continue
            self.passwdDict[split_val[0]] = {
                KEY_AWS_PASSWORD: split_val[1],
                KEY_AWS_KEY: split_val[2],
                KEY_AWS_SECRET: split_val[3]
            }
        # Close opened file
        pass_file.close()
        data_exist = True if (len(self.passwdDict) > 0) else False
        if not data_exist:
            Logger.err(MSG_ERR_FILE_DOES_NOT_HAVE_VALID_DATA.format(PASSWD_TXT))
        return data_exist

    def logout(self):
        # Method for handling the logout operation
        self.logged_in = False
        self.clear_console()
        Logger.info(MSG_INFO_LOGOUT_MESSAGE)
        self.login()

    @staticmethod
    def clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')

    def run(self):
        # Main method
        if self.read_file():
            self.clear_console()
            self.login()


if __name__ == "__main__":
    try:
        AwsCli().run()
    except KeyboardInterrupt as error:
        Logger.err(str(error))
    except Exception as e:
        Logger.err(str(e))
