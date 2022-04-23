# AWS-Adventure

This is the first time I'm using all of these AWS services.. please bear that in mind when seeing the many best-practices I have likely trampled over. 

Adding cat picture for distraction. 

<pre>
    /\_____/\
   /  o   o  \
  ( ==  ^  == )
   )         (
  (           )
 ( (  )   (  ) )
(__(__)___(__)__)
</pre>

### **Repo Structure**

**code** - Contains the python code used in the lambda functions.\
**templates** - Contains the yaml templates for deploying cloudformation stack.

## **Project Overview**

### **1- Get Data**
* Driven by an EventBridge event that triggers daily (no time-of-day specified)
* This daily event will trigger a lambda function which runs **get_data.py**
* The script will pull JSON data containing a list of 250 films. Working on the assumption that the JSON will start at film rank 1 and increase incrementally, we can select the first 10 lines for the top 10 films.
* The 10 lines will be sent over to an SQS queue in their entirety.

### **2- Enrich & Store**
* Lambda triggered by a message arriving in SQS queue, which will run **enrich_and_store.py**
* We'll use the film data to pull some extra info from the omdbapi and do some simple data processing - I haven't been too robust with handling data inconsistencies as they were out of scope.
* Finally, we'll convert the film data into a single JSON and write it to an S3 bucket. Since the bucket has versioning, the filename is hardcoded.


### **Things I'd do differently if I had more time**
I've tried not to spend too long on this, so I've knowingly taken some shortcuts. I'll list them here so you know about the 'mistakes' that I'm aware of.

* Various code optimizations, e.g. **get_data.py** could remove unwanted fields from the top10 films before sending a message to reduce message size.
* Form a single CloudFormation template to cover the full flow. This was taking too long so I've got individual templates for each piece.
* Move things like queueUrl, bucket names & keys and API key to a config file so that the only manual step after creating a CloudFormation would be to edit this single file. 
* Include role/permission specifications in the CloudFormation template - currently pointing to my arn which is likely inaccessible to you. I have created custom policies for my roles, using the principle of least privilege. 
* Wasn't sure about the "Private key handling" bonus point. I have placed some restrictions on bucket access, but I'm not convinced this is what you're looking for.
* Didn't look too much into how code should be stored for Lambda CloudFormation templates. Dumped them into an S3 bucket for now.