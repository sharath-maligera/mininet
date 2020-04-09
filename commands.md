- SSH into mininet VM and use the following command to create you small network:<br/>
``` sudo mn --mac --controller=remote,ip=x.x.x.x,port=6633 ```<br/>
``` sudo``` – runs the command with root or superuser privileges<br/>
```--mac``` – makes the mac address of your hosts similar to the IP address. <br/>
```--controller=remote``` – tells mininet that the SDN controller is not on the local machine.<br/>
```ip=x.x.x.x ```– specify the IP Address of the SDN controller <br/>
```port=6633``` – This is the standard port number to connect to the controller.<br/>

- On the mininet prompt use the command dump to see the details of the network created.<br/>
``` mininet> dump```

- To shutdown controller which is running on port 6633 ``` $ sudo fuser -k 6633/tcp```<br/>




