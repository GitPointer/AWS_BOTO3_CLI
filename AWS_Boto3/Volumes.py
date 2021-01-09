import botocore
import botocore.exceptions
from Logger import Logger


class Volumes:
    # A class which functions as a controller for AWS EBS volumes
    VOLUMES_DISPLAY_FORMAT = '  {0}({1})  \t {2}-{3} <ZoneInfo:{4}>  \t <Created On:{5}>'
    VOLUMES_ATTACH_DISPLAY_FORMAT = '\t\t Attachment-{0}:\t{1}({2})\t<Attached On:{3}>'
    VOLUME_ATTACH_DISPLAY_FORMAT = "\t\t<InstanceId:{}>\t <Device Name:{}>"
    SNAP_DISPLAY_FORMAT = '  {0}({1})  \t {2}-{3}  \t <StartTime:{4}>'
    CREATED_SNAP_DISPLAY_FORMAT = "<Snapshot {} {}[{}({}GB)]>"
    STR_ATTACH_DATA = "\t<Attachment Data>"
    STR_EBS_VOLUMES = "<EBS Volumes>"
    STR_AVAIL_SNAP = "<Snapshot>"
    MSG_WARN_NO_EBS_VOLUME = "No EBS Volumes Detected!"
    MSG_WARN_NO_AVAILABLE_VOLUMES = "There is no available volume for attachment.."
    MSG_INFO_AVAILABLE_VOLUMES = "Available Volumes: {}"
    MSG_INFO_VOLUME_TO_INSTANCE = "Volume({}) is {} to instance {}.Please wait.."
    MSG_WARN_NO_IN_USE_VOLUMES = "There is no volume for detachment.."
    MSG_INFO_IN_USE_VOLUMES = "In-use Volumes: {}"
    MSG_WARN_NO_AVAILABLE_SNAP = "There is no available snapshot."

    def __init__(self, ec2res, ec2client):
        # Volumes Constructor for  EC2 Resource "ec2res" and "ec2client" Client
        self.ec2_res = ec2res
        self.ec2_client = ec2client

    def list_volumes(self, show_attachment_data):
        # List all volumes associated with the with self.ec2 Resource
        count = 0
        # The state of the volume (creating | available | in-use | deleting | deleted | error )
        all_volumes = []
        for volume in self.ec2_res.volumes.all():
            all_volumes.append(volume)
            count += 1
        if count == 0:
            Logger.warn(self.MSG_WARN_NO_EBS_VOLUME)
        else:
            # Logger.header(self.VOLUMES_DISPLAY_SEP)
            Logger.header(self.STR_EBS_VOLUMES)
            for volume in all_volumes:
                Logger.info(self.VOLUMES_DISPLAY_FORMAT.format(volume.volume_id, volume.state, volume.volume_type,
                                                               str(volume.size) + "GB", volume.availability_zone,
                                                               volume.create_time))
                if show_attachment_data:
                    attach_data = volume.attachments
                    # display the attachment info
                    attach_count = 0
                    for attachment in attach_data:
                        attach_count += 1
                        Logger.sub_info(
                            self.VOLUMES_ATTACH_DISPLAY_FORMAT.format(attach_count, attachment["InstanceId"],
                                                                      attachment["Device"], attachment["AttachTime"]))
        return count

    def volume_attachment_data(self, volume_id):
        # display the attachment info
        volume = self.ec2_res.Volume(volume_id)
        attach_data = volume.attachments
        attach_list = []
        attach_count = 0
        Logger.sub_info(self.STR_ATTACH_DATA)
        for attachment in attach_data:
            attach_count += 1
            attach_list.append(attachment)
            Logger.sub_info(
                self.VOLUME_ATTACH_DISPLAY_FORMAT.format(attachment["InstanceId"], attachment["Device"]))
        return attach_list

    def list_in_use_volumes(self):
        # list the in-use volumes
        count = 0
        in_use_volumes = []
        volumes = self.ec2_res.volumes.filter(
            Filters=[{'Name': 'status', 'Values': ['in-use']}])
        for volume in volumes:
            in_use_volumes.append(volume.volume_id)
            count += 1
        if count == 0:
            Logger.warn(self.MSG_WARN_NO_IN_USE_VOLUMES)
        else:
            Logger.avail_info(self.MSG_INFO_IN_USE_VOLUMES.format(in_use_volumes))
        return in_use_volumes

    def list_available_volumes(self):
        # list the available volumes
        count = 0
        available_volumes = []
        volumes = self.ec2_res.volumes.filter(
            Filters=[{'Name': 'status', 'Values': ['available']}])
        for volume in volumes:
            available_volumes.append(volume.volume_id)
            count += 1
        if count == 0:
            Logger.warn(self.MSG_WARN_NO_AVAILABLE_VOLUMES)
        else:
            Logger.avail_info(self.MSG_INFO_AVAILABLE_VOLUMES.format(available_volumes))
        return available_volumes

    def attach_volume(self, instance_id, volume_id, dev_name):
        # Attach volume with id "volume_id" to the EC2 instance with
        # id "instance_id", where it is the device "dev_name",using the Resource "ec2"
        try:
            volume = self.ec2_res.Instance(instance_id).attach_volume(VolumeId=volume_id,
                                                                      Device=dev_name)
            Logger.info(
                self.MSG_INFO_VOLUME_TO_INSTANCE.format(volume['VolumeId'], volume['State'],
                                                        volume['InstanceId']))
            waiter = self.ec2_client.get_waiter("volume_in_use")
            waiter.wait(VolumeIds=[volume_id])
        except botocore.exceptions.ClientError as error:
            Logger.err(str(error))

    def detach_volume(self, instance_id, volume_id, dev_name):
        # Detach the volume with id "volume_id" from the EC2 instance with
        # id "instance_id" where it is device "dev_name"
        try:
            volume = self.ec2_res.Instance(instance_id).detach_volume(VolumeId=volume_id,
                                                                      Device=dev_name)
            Logger.info(
                self.MSG_INFO_VOLUME_TO_INSTANCE.format(volume['VolumeId'], volume['State'],
                                                        volume['InstanceId']))
            waiter = self.ec2_client.get_waiter("volume_available")
            waiter.wait(VolumeIds=[volume_id])
        except botocore.exceptions.ClientError as error:
            Logger.err(str(error))

    def create_snapshot(self, volume_id, description):
        # Creates and returns a snapshot, with the given 'description',
        # of the EBS volume 'volume_id'.
        try:
            snapshot = self.ec2_res.create_snapshot(VolumeId=volume_id, Description=description)
            Logger.info(
                self.CREATED_SNAP_DISPLAY_FORMAT.format(snapshot.description, snapshot.state, snapshot.volume_id,
                                                        snapshot.volume_size))
            snapshot.wait_until_completed()
            return snapshot
        except botocore.exceptions.ClientError as error:
            Logger.err(str(error))

    def list_snapshots(self, owner_id):
        # Prints out a list of all snapshots
        count = 0
        snapshots = []
        for snapshot in self.ec2_res.snapshots.filter(OwnerIds=[owner_id]):
            snapshots.append(snapshot)
            count += 1
        if count == 0:
            Logger.warn(self.MSG_WARN_NO_AVAILABLE_SNAP)
        else:
            Logger.header(self.STR_AVAIL_SNAP)
            for snapshot in snapshots:
                Logger.info(self.SNAP_DISPLAY_FORMAT.format(snapshot.snapshot_id, snapshot.state, snapshot.volume_id,
                                                            str(snapshot.volume_size) + "GB", snapshot.start_time))
        return count
