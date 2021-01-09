import botocore
import botocore.exceptions
from Logger import Logger
from Config import AWS_REGION


class EC2Controller:
    #  A class for controlling interactions with the boto3 EC2  Resource and Client Interface

    INSTANCES_DISPLAY_FORMAT = '  {0}({1})  \t {2} - {3} <RegionInfo:{4}>  \t <Launched On:{5}>'
    DEVICE_DISPLAY_FORMAT = "\t\t'{}'\t '{}'"
    MSG_INFO_AMI_CREATED = "AMI created: {}['{}']"
    MSG_INFO_INSTANCE_CREATED = "Instance created.{}"
    MSG_INFO_INSTANCE_STARTING = "Starting instance:'{}'.Please wait.."
    MSG_INFO_INSTANCE_STARTED = "Instance started:'{}'"
    MSG_INFO_INSTANCE_STOPPING = "Stopping instance:'{}'.Please wait.."
    MSG_INFO_INSTANCE_STOPPED = "Instance stopped:'{}'"
    MSG_INFO_RUNNING_INSTANCE = "Running EC2 Instances: {}"
    MSG_INFO_STOPPED_INSTANCE = "Stopped EC2 Instances: {}"
    MSG_INFO_STOPPED_RUNNING_INSTANCE = "Available EC2 Instances: {}"
    MSG_WARN_NO_INSTANCE = "There is no EC2 Instance at this moment.."
    MSG_WARN_NO_RUNNING_INSTANCE = "There is no running EC2 Instance at this moment.."
    MSG_WARN_NO_STOPPED_INSTANCE = "There is no stopped EC2 Instance at this moment.."
    MSG_WARN_NO_INSTANCE_FOR_EMI = "There is no EC2 Instance for AMI creation at this moment.."
    MSG_INFO_VOL_FROM_SNAP_CREATED = "Volume created: {0}({1})  \t {2}-{3} <ZoneInfo:{4}>  \t <Created On:{5}>"
    STR_AWS_INSTANCE = "<AWS EC2 Instances>"
    STR_ATTACHED_DEVICE = "\t\t<Instance({}) attached block devices Info>"

    def __init__(self, ec2res, ec2client):
        # EC2Controller Constructor, assigns the ec2 Resource "ec2res" and "ec2client" Client to this controller
        self.ec2_res = ec2res
        self.ec2_client = ec2client

    def start_instance(self, instance_id):
        # Start instance with id 'instance_id'
        try:
            instance = self.ec2_res.Instance(instance_id)
            instance.start()
            Logger.info(self.MSG_INFO_INSTANCE_STARTING.format(instance_id))
            # Wait for instance start operation to complete
            instance.wait_until_running()
            Logger.info(self.MSG_INFO_INSTANCE_STARTED.format(instance_id))
        except botocore.exceptions.ClientError as error:
            Logger.err(str(error))

    def stop_instance(self, instance_id):
        # Stop instance with id 'instance_id'
        try:
            instance = self.ec2_res.Instance(instance_id)
            instance.stop()
            Logger.info(self.MSG_INFO_INSTANCE_STOPPING.format(instance_id))
            # Wait for instance stop operation to complete
            instance.wait_until_stopped()
            Logger.info(self.MSG_INFO_INSTANCE_STOPPED.format(instance_id))
        except botocore.exceptions.ClientError as error:
            Logger.err(str(error))

    def list_instances(self):
        # List all EC2 instances
        return self.list_all_instances(self.ec2_res.instances.all())

    def list_all_instances(self, instances):
        count = 0
        running_instances = []
        pending_instances = []
        shutting_down_instances = []
        terminated_instances = []
        stopping_instances = []
        stopped_instances = []
        # Loop through all EC2 instances
        for instance in instances:
            instance_info = [instance.id, instance.state['Name'], instance.image_id, instance.instance_type,
                             AWS_REGION, instance.launch_time]
            if instance.state['Name'] == "running":
                running_instances.append(instance_info)
            elif instance.state['Name'] == "pending":
                pending_instances.append(instance_info)
            elif instance.state['Name'] == "shutting-down":
                shutting_down_instances.append(instance_info)
            elif instance.state['Name'] == "terminated":
                terminated_instances.append(instance_info)
            elif instance.state['Name'] == "stopping":
                stopping_instances.append(instance_info)
            elif instance.state['Name'] == "stopped":
                stopped_instances.append(instance_info)
            count += 1
        if count == 0:
            Logger.warn(self.MSG_WARN_NO_INSTANCE)
        else:
            Logger.header(self.STR_AWS_INSTANCE)
            for running_instance in running_instances:
                Logger.info(self.INSTANCES_DISPLAY_FORMAT.format(*running_instance))
            for pending_instance in pending_instances:
                Logger.info(self.INSTANCES_DISPLAY_FORMAT.format(*pending_instance))
            for stopping_instance in stopping_instances:
                Logger.info(self.INSTANCES_DISPLAY_FORMAT.format(*stopping_instance))
            for stopped_instance in stopped_instances:
                Logger.info(self.INSTANCES_DISPLAY_FORMAT.format(*stopped_instance))
            for shutting_down_instance in shutting_down_instances:
                Logger.info(self.INSTANCES_DISPLAY_FORMAT.format(*shutting_down_instance))
            for terminated_instance in terminated_instances:
                Logger.info(self.INSTANCES_DISPLAY_FORMAT.format(*terminated_instance))
        return count

    def list_running_instance(self):
        # List all running EC2 instances
        count = 0
        running_instances = []
        all_instances = self.ec2_res.instances.all()
        total_instances = self.list_all_instances(all_instances)
        if total_instances > 0:
            for instance in all_instances:
                if instance.state['Name'] == "running":
                    running_instances.append(instance.id)
                    count += 1
            if count == 0:
                Logger.warn(self.MSG_WARN_NO_RUNNING_INSTANCE)
            else:
                Logger.avail_info(self.MSG_INFO_RUNNING_INSTANCE.format(running_instances))
        return running_instances

    def list_stopped_instance(self):
        # List all stopped EC1 instances
        count = 0
        stopped_instances = []
        all_instances = self.ec2_res.instances.all()
        total_instances = self.list_all_instances(all_instances)
        if total_instances > 0:
            for instance in all_instances:
                if instance.state['Name'] == "stopped":
                    stopped_instances.append(instance.id)
                    count += 1
            if count == 0:
                Logger.warn(self.MSG_WARN_NO_STOPPED_INSTANCE)
            else:
                Logger.avail_info(self.MSG_INFO_STOPPED_INSTANCE.format(stopped_instances))
        return stopped_instances

    def list_stopped_running_instances(self):
        # List all stopped and running EC2 instances
        count = 0
        available_instances = []
        all_instances = self.ec2_res.instances.all()
        total_instances = self.list_all_instances(all_instances)
        if total_instances > 0:
            for instance in all_instances:
                if instance.state['Name'] == "running" or instance.state['Name'] == "stopped":
                    available_instances.append(instance.id)
                    count += 1
            if count == 0:
                Logger.warn(self.MSG_WARN_NO_INSTANCE_FOR_EMI)
            else:
                Logger.avail_info(self.MSG_INFO_STOPPED_RUNNING_INSTANCE.format(available_instances))
        return available_instances

    def instance_attached_block_devices(self, instance_id):
        # Any block device mapping entries for the instance
        count = 0
        instance = self.ec2_res.Instance(instance_id)
        attached_block_devices = []
        attached_devices_details = []
        bdm = instance.block_device_mappings
        for device in bdm:
            attached_block_devices.append(device['DeviceName'])
            ebs = device['Ebs']
            device_info = [device['DeviceName'], ebs['VolumeId']]
            attached_devices_details.append(device_info)
            count += 1
        if count > 0:
            Logger.header(self.STR_ATTACHED_DEVICE.format(instance_id))
            for devices_detail in attached_devices_details:
                Logger.sub_info(self.DEVICE_DISPLAY_FORMAT.format(*devices_detail))
        return attached_block_devices

    def instance_platform_name(self, instance_id):
        # instance platform name
        platform = self.ec2_res.Instance(instance_id).platform
        return platform

    def instance_state(self, instance_id):
        # instance state name
        state = self.ec2_res.Instance(instance_id).state['Name']
        return state

    def instance_root_device_name(self, instance_id):
        # instance root device name
        root_device_name = self.ec2_res.Instance(instance_id).root_device_name
        return root_device_name

    def create_instance(self, image_id, instance_type):
        # create a new EC2 instance with the given AMI Image ID
        try:
            instance = self.ec2_res.create_instances(ImageId=image_id, MinCount=1, MaxCount=1,
                                                     InstanceType=instance_type)
            Logger.info(self.MSG_INFO_INSTANCE_CREATED.format(instance))
        except botocore.exceptions.ClientError as error:
            Logger.err(str(error))

    def create_image(self, instance_id, image_name):
        # create a new AMI from the given instance ID
        try:
            image_id = self.ec2_client.create_image(InstanceId=instance_id, Name=image_name)
            Logger.info(self.MSG_INFO_AMI_CREATED.format(image_name, image_id['ImageId']))
        except botocore.exceptions.ClientError as error:
            Logger.err(str(error))

    def create_volume(self, availability_zone, snapshot_id):
        # Create a volume from a snapshot
        try:
            volume = self.ec2_client.create_volume(AvailabilityZone=availability_zone, SnapshotId=snapshot_id)
            Logger.info(
                self.MSG_INFO_VOL_FROM_SNAP_CREATED.format(volume['VolumeId'], volume['State'], volume['VolumeType'],
                                                           str(volume['Size']) + "GB",
                                                           volume['AvailabilityZone'],
                                                           volume['CreateTime']))
        except botocore.exceptions.ClientError as error:
            Logger.err(str(error))
