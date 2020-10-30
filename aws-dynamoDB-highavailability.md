# Create table in Singapore region

$ aws dynamodb create-table --table-name Employee \
>     --attribute-definitions \
>         AttributeName=Ename,AttributeType=S \
>         AttributeName=Dname,AttributeType=S \
>     --key-schema \
>         AttributeName=Ename,KeyType=HASH \
>         AttributeName=Dname,KeyType=RANGE \
>     --provisioned-throughput \
>         ReadCapacityUnits=1,WriteCapacityUnits=1 \
>     --stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES \
>     --region ap-southeast-1

# Output:
{"TableDescription":{"AttributeDefinitions":[{"AttributeName":"Ename","AttributeType":"S"},{"AttributeName":"Dname","AttributeType":"S"}],"TableName":"Employee",
"KeySchema":[{"AttributeName":"Ename","KeyType":"HASH"},{"AttributeName":"Dname","KeyType":"RANGE"}],
"TableStatus":"CREATING","CreationDateTime":1602518202.673,
"ProvisionedThroughput":{"NumberOfDecreasesToday":0,"ReadCapacityUnits":1,"WriteCapacityUnits":1},"TableSizeBytes":0,"ItemCount":0,
"TableArn":"arn:aws:dynamodb:ap-southeast-1:830346331862:table/Employee","TableId":"9746d640-f354-4531-91a4-315efb02b7c8"
,"StreamSpecification":{"StreamEnabled":true,"StreamViewType":"NEW_AND_OLD_IMAGES"},"LatestStreamLabel":"2020-10-12T15:56:42.673",
"LatestStreamArn":"arn:aws:dynamodb:ap-southeast-1:830346331862:table/Employee/stream/2020-10-12T15:56:42.673"}}


# create same table in N-virgina
$ aws dynamodb create-table --table-name Employee \
    --attribute-definitions \
        AttributeName=Ename,AttributeType=S \
        AttributeName=Dname,AttributeType=S \
    --key-schema \
        AttributeName=Ename,KeyType=HASH \
        AttributeName=Dname,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=1,WriteCapacityUnits=1 \
    --stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES \
    --region us-east-1

# create global table with replication enabled
$ aws dynamodb create-global-table --global-table-name Employee \
    --replication-group RegionName=ap-southeast-1 RegionName=us-east-1 \
    --region ap-southeast-1

# Output:
{"GlobalTableDescription":{"ReplicationGroup":[{"RegionName":"ap-southeast-1"},
{"RegionName":"us-east-1"}],"GlobalTableArn":"arn:aws:dynamodb::830346331862:global-table/Employee","CreationDateTime":1602518405.712,"GlobalTableStatus":"CREATING",
"GlobalTableName":"Employee"}}

# Create another table in Ireland region

$ aws dynamodb create-table --table-name Employee \
    --attribute-definitions \
        AttributeName=Ename,AttributeType=S \
        AttributeName=Dname,AttributeType=S \
    --key-schema \
        AttributeName=Ename,KeyType=HASH \
        AttributeName=Dname,KeyType=RANGE \
    --provisioned-throughput \
        ReadCapacityUnits=1,WriteCapacityUnits=1 \
    --stream-specification StreamEnabled=true,StreamViewType=NEW_AND_OLD_IMAGES \
    --region eu-west-1

# add this new table to the Employee global table

$ aws dynamodb update-global-table --global-table-name Employee \
    --replica-updates 'Create={RegionName=eu-west-1}' \
    --region ap-southeast-1
    
    
###########################################                  Verify Global Replication

# add data into table in Singapore region
aws dynamodb put-item --table-name Employee \
    --item '{"Ename": {"S":"Scott"},"Dname": {"S":"Marketing"}}' \
    --region ap-southeast-1

#check if its replicated in other regions

aws dynamodb get-item --table-name Employee \
    --key '{"Ename": {"S":"Scott"},"Dname": {"S":"Marketing"}}' \
    --region us-east-1

# Output:
{"Item":{"aws:rep:deleting":{"BOOL":false},"aws:rep:updateregion":{"S":"ap-southeast-1"},"aws:rep:updatetime":{"N":"1602518560.314001"}
,"Ename":{"S":"Scott"},"Dname":{"S":"Marketing"}}}


$ aws dynamodb get-item --table-name Employee \
>     --key '{"Ename": {"S":"Scott"},"Dname": {"S":"Marketing"}}' \
>     --region eu-west-1

# Output: {"Item":{"aws:rep:deleting":{"BOOL":false},"aws:rep:updateregion":{"S":"ap-southeast-1"},"aws:rep:updatetime":{"N":"1602518560.314001"},
"Ename":{"S":"Scott"},"Dname":{"S":"Marketing"}}}



# Check CRUD Operations

# Check CRUD Ops
for i in {2..10}
	do val=${RANDOM}
  t=2
  # Insert Items
	echo -e "\n\n-=-=- Inserting Employees:Scotty_${i} and Retrieving after ${t} Seconds -=-=-"
  aws dynamodb put-item --table-name Employee --item '{"Ename": {"S":"Scotty_'${i}'"},"Dname": {"S":"Marketing - '${val}'"}}' --region ap-southeast-1
  sleep ${t}
 # Read Items
  time aws dynamodb get-item --table-name Employee --key '{"Ename": {"S":"Scotty_'${i}'"},"Dname": {"S":"Marketing - '${val}'"}}' --region eu-west-1
  done

###### Output

-=-=- Inserting Employees:Scotty_2 and Retrieving after 2 Seconds -=-=-
{"Item":{"aws:rep:deleting":{"BOOL":false},"aws:rep:updateregion":{"S":"ap-southeast-1"},"aws:rep:updatetime":{"N":"1602518693.387001"},
"Ename":{"S":"Scotty_2"},"Dname":{"S":"Marketing -  32421"}}}

real    0m1.103s
user    0m0.368s
sys     0m0.051s
