# Setting up Docker on Jetstream

Source your virtual environment and openrc.sh file. Then run the following

```
export IMAGE=JS-API-Featured-CentOS7-Latest
export PROJECT_NAME=${OS_USERNAME}-docker-tutorial
openstack server create ${PROJECT_NAME} --flavor m1.tiny --image $IMAGE --key-name ${OS_USERNAME}-key --security-group global-ssh --nic net-id=${OS_USERNAME}-api-net
openstack floating ip create public
export IP_ADDRESS=...
openstack server add floating ip $PROJECT_NAME $IP_ADDRESS
```

If you don't have network setup use:

```
openstack network create ${OS_USERNAME}-api-net
openstack subnet create --network ${OS_USERNAME}-api-net --subnet-range 10.0.0.0/24 ${OS_USERNAME}-api-subnet1
openstack router create ${OS_USERNAME}-api-router
openstack router add subnet ${OS_USERNAME}-api-router ${OS_USERNAME}-api-subnet1
openstack router set --external-gateway public ${OS_USERNAME}-api-router
```

See <https://github.com/jlf599/JetstreamAPITutorial> for more details.

Once you have the VM running, SSH into and run the following:

```
sudo yum install -y yum-utils
sudo yum-config-manager     --add-repo     https://download.docker.com/linux/centos/docker-ce.repo
sudo yum install -y docker-ce docker-ce-cli containerd.io
sudo systemctl start docker
sudo systemctl enable docker
sudo docker run hello-world
sudo usermod -aG docker centos
```

Reboot:

```
openstack server reboot $PROJECT_NAME
```

Now from your local machine you should be able to do the following:

```
docker context create jetstream --docker host=ssh://centos@IP_ADDRESS
docker --context jetstream ps -a
docker context use jetstream
docker run hello-world
```

## Creating a user

```
sudo adduser training
sudo usermod -aG docker training
sudo su - training
```

As user:
```
# Create keypair without passphrase
ssh-keygen
cat .ssh/id_rsa.pub >> .ssh/authorized_keys
chmod 600 .ssh/authorized_keys
cp .ssh/id_rsa /tmp/
```

`config` file:
```
Host 149.165.170.99
  IdentityFile ~/.ssh/id_rsa
```

## Cleaning up

```
openstack server remove floating ip $PROJECT_NAME $IP_ADDRESS
openstack floating ip delete $IP_ADDRESS
openstack server delete $PROJECT_NAME
```

## TODO

- [x] setting up user accounts
