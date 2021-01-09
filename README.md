## Installation
 1. **Prerequisite**
 		
		1. Python 3.x(Recommended 3.4 and above)
		2. PIP(PIP is a package manager for Python packages)
      
      > **Note:** If you have Python version 3.4 or later, PIP is included by default.


 2. **Installation**
	 1. **Manual**
	 
			>py(or python) -m pip install boto3
			>py(or python) -m pip install menu

		
		> **Note:** This AWS CLI tool used Menu package for creating the Menu for AWS operations.  
Please refer the below link for more details about Menu package . 
https://pypi.org/project/Menu/#description.

	 2. **Using requirements.txt file**
	 		
		1. Go to root dir  `AWS_Boto3`
			
		2. Run requirements.txt file
	 		 
				 
				 >py(or python) -m pip install -r requirements.txt 
    
    > **Note:** `py` usually does not exist on Linux, unless you set an alias or symlink yourself. You can check with `which python` and `which py` to see what these commands actually are.

## Configuration

### 1. `config.py`

#### Below are the config parameter defined in `config.py`.

 1. AWS_REGION **(default `eu-west-1`)**
 2. WINDOWS_AMI_ID **(default `ami-035e11a5d21b976ed`)**
 3. LINUX_AMI_ID **(default `ami-0ce1e3f77cd41957e`)**
 4. WINDOWS_FREE_TIER_INSTANCE_TYPE **(default `t2.micro`)**
 5. LINUX_FREE_TIER_INSTANCE_TYPE **(default `t2.micro`)**
 6. OWNER_ID
 7. AVAILABILITY_ZONE **(default `eu-west-1a`)**
 8. UPLOAD_DIR_FOR_S3 **(default `'./s3_upload/'`)**
 9. DOWNLOAD_DIR_FOR_S3 **(default `'./s3_download/'`)**
 10. CPU_ALARM_TOPIC_NAME **(default `cpu_alarm`)**


### 2. `passwd.txt` file

 - Valid usernames and passwords will to be stored in `passwd.txt` file. 
 - Each line of which will contain a username+password pair, and their AWS access key id and secret access key, all separated by tabs.

## RUN
 1. Go to root dir  `AWS_Boto3` 
 2. Run below command 
		  
		  >`py(or python) AwsCli.py`
		  
3. Input User Name and Password for Login

## Menu Description

#### Main Menu
![enter image description here](https://raw.githubusercontent.com/GitPointer/aws_boto3/main/main_menu.png)
>`Press-1` for navigate to EC2 Menu. 
 
> `Press-2` for navigate to EBS Menu.

> `Press-3` for navigate to S3 Menu.

> `Press-4` for navigate to Monitoring Menu.

> `Press-5` for navigate to Setting Menu.

> `Press-6` for Logout.

> `Press-7` for Exit.

#### 1. EC2 Menu
![enter image description here](https://raw.githubusercontent.com/GitPointer/aws_boto3/main/ec2_menu.png)
 >`Press-1` List all instances for the AWS account. 
 
> `Press-2` Start a specific(stopped) instance.

> `Press-3` Stop a specific(running) instance.

> `Press-4` Create an AMI from an existing(running or stopped) instance.

> `Press-5` Launch a new `Windows` or `Linux` instance from an existing (free tier) AMI(AMI-ID is predefined in `config.py`).

> `Press-6` Go Back.

#### 2. EBS Menu
![enter image description here](https://raw.githubusercontent.com/GitPointer/aws_boto3/main/ebs_menu.png)
 >`Press-1`  List all volumes. 
 
> `Press-2`  Attach an existing volume to an instance(running or stopped).

> `Press-3`  Detach a existing volume from an instance(running or stopped).

> `Press-4`  Take a snapshot of a specific volume.

> `Press-5`  Create a volume from a snapshot.

> `Press-6` Go Back.

#### 3. S3 Menu
![enter image description here](https://raw.githubusercontent.com/GitPointer/aws_boto3/main/s3_menu.png)
 >`Press-1`  List all buckets. 
 
> `Press-2`  List all objects in a bucket.

> `Press-3`  Upload an object in specific bucket.

> `Press-4`  Download an object from a specific bucket.

> `Press-5`  Delete an object from a specific bucket.

> `Press-6` Go Back.

#### 4. Monitoring Menu
![enter image description here](https://raw.githubusercontent.com/GitPointer/aws_boto3/main/monitoring_menu.png)
 >`Press-1`  Display `CPUUtilization` and `MemoryUtilization` metrics, averaged over the last 10 minutes for a specific instance. 
 
> `Press-2`  Set an Alarm for a specific instance if CPU utilization is less than equal to 28%.

> `Press-3`  Boto3 examples of Relational DB Service.

> `Press-4`  Go Back.

#### 5. Setting Menu
![enter image description here](https://raw.githubusercontent.com/GitPointer/aws_boto3/main/setting_menu.png)

> `Press-1` for disabling the color menu. **(default `enable`)**

>  `Press-2` for enable color menu after disabling.

> `Press-3` for display "Attachment Data"  of Volumes in EBS Menu.

> `Press-4`for hiding "Attachment Data"  of  Volumes in EBS Menu **(default `hide`)**

> `Press-5` for setting local upload dir path for S3 .From this path files will be display for upload.

>  `Press-6` for setting local download dir path for S3 .Files from S3 will be download in this dir.

>  `Press-7` Go Back.

## Notes
> 1. **Waiter** is used in `Start` and `Stop` instance operation in EC2 Menu.
> 2. **Waiter** is used in `Attach` and `Detach` Volume operation in EBS Menu.


