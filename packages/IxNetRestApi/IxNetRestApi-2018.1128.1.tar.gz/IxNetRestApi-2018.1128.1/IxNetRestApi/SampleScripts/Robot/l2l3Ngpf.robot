# Description
#    Configure IxNetwork basic L2L3 in NGPF from scratch.
#
# Notes
#    This script is the same script as ../SampleScripts/l2l3Ngpf.py.
#
#    This script uses object oriented programming techniques.  The first thing you see in the *** Test Case *** is 
#    that it will extend the main ${ixnObj} object to all the instantiated classes.
#    The reason is because all the common functions like GET, POST, PATCH, and many more are located in IxNetRestApi.Connect.

*** Settings ***
Documentation  Configure IxNetwork basic L2L3 in NGPF
Metadata  Script_Author  Hubert Gee
Metadata  Script_Date    3/10/2018
 
Library  BuiltIn
Library  Collections

# Must add the ../../Modules path to PYTHONPATH.
Library  IxNetRestApi.IxNetRestApi.Connect  ${apiServerIp}  ${apiServerPort}  ${apiServerOs}  robotFrameworkStdout=True  WITH NAME  ixnObj
Library  IxNetRestApi.IxNetRestApiPortMgmt.PortMgmt      WITH NAME  portMgmtObj  
Library  IxNetRestApi.IxNetRestApiTraffic.Traffic        WITH NAME  trafficObj
Library  IxNetRestApi.IxNetRestApiProtocol.Protocol      WITH NAME  protocolObj
Library  IxNetRestApi.IxNetRestApiStatistics.Statistics  WITH NAME  statisticObj

*** Variables ***
${apiServerIp} =  192.168.70.3
${apiServerPort} =  11009
${apiServerOs} =  windows
${forceTakePortOwnership} =  True
${releasePortsWhenDone} =  False
${deleteSessionAfterTest} =  True
${licenseIsInChassis} =  False
@{licenseServerIp} =  192.168.70.3
${licenseModel} =  subscription
${licenseTier} =  tier3  

${ixChassisIp} =  192.168.70.120

# Creating a list and nested list for the way how the API needs them to be
@{port_1_1} =  ${ixChassisIp}  1  1
@{port_2_1} =  ${ixChassisIp}  1  2
@{portList} =  ${port_1_1}  ${port_2_1}
@{topology1Port} =  ${port_1_1}
@{topology2Port} =  ${port_2_1}
@{trackBy} =  flowGroup0  

# Defining dictionary for NGPF
&{ethMacAddr1} =  start=00:01:01:00:00:01  direction=increment  step=00:00:00:00:00:01
&{ethMacAddr2} =  start=00:02:01:00:00:01  direction=increment  step=00:00:00:00:00:01
&{ipv41} =        start=1.1.1.1  direction=increment  step=0.0.0.1
&{ipv42} =        start=1.1.1.2  direction=increment  step=0.0.0.1
&{ipv4Gateway1} =  start=1.1.1.2  direction=increment  step=0.0.0.1
&{ipv4Gateway2} =  start=1.1.1.1  direction=increment  step=0.0.0.1

# Traffic Item dictionary
&{trafficItem1} =  name=Topo1-to-Topo2  trafficType=ipv4  biDirectional=True  srcDestMesh=one-to-one routeMesh=oneToOne
...  allowSelfDestined=False  trackBy=${trackBy}

# Example settings for continuous traffic
#&{configElements} =  transmissionType=continuous  frameRate=88  frameRateType=percentLineRate  frameSize=128

# Example settings for fixed frame count
&{configElements} =  transmissionType=fixedFrameCount  frameCount=50000  frameRate=88  frameRateType=percentLineRate  frameSize=128


*** Test Cases ***
Configuring basic L2L3 in NGPF

    # Object oriented:  Extending the main ${ixnObj} object to all the instantiated classes
    ${ixnObj} =  ixnObj.getSelfObject
    portMgmtObj.setMainObject    ${ixnObj}
    protocolObj.setMainObject    ${ixnObj}
    trafficObj.setMainObject     ${ixnObj}   
    statisticObj.setMainObject   ${ixnObj}

    Log To Console  Connecting to chassis ...
    portMgmtObj.ConnectIxChassis  ${ixChassisIp}

    # Verify if ports are available. Take over ports if forceTakePortOwnership == True
    ${result} =  portMgmtObj.Are Ports Available  portList=${portList}  raiseException=${False}
    Log To Console  arePortsAvailable: ${result}
    Run Keyword If  ("${result}"!=0) and ("${forceTakePortOwnership}"=="True")  Run Keywords
    ...  Log To Console  Taking over ports ...
    ...  portMgmtObj.Release Ports  ${portList}
    ...  AND  portMgmtObj.Clear Port Ownership  ${portList}
    ...  ELSE  Fail  Ports are still owned


    Log To Console  Creating new blank config
    ixnObj.newBlankConfig

    Run Keyword If  "${licenseIsInChassis}"=="False"  Run Keywords
    ...  Log To Console  Configuring licenses ...
    ...  portMgmtObj.Release Ports  portList=${portList}
    ...  AND  ixnObj.Config License Server Details  ${licenseServerIp}  ${licenseModel}  ${licenseTier}

    Log To Console  Assigning ports ...
    portMgmtObj.Assign Ports  ${portList}

    Log To Console  Creating NGPF protocol stacks ...
    ${topology1Obj} =  protocolObj.Create Topology Ngpf  portList=${topology1Port}  topologyName=Topo1
    ${topology2Obj} =  protocolObj.Create Topology Ngpf  portList=${topology2Port}  topologyName=Topo2
    ${deviceGroup1Obj} =  protocolObj.Create Device Group Ngpf  ${topology1Obj}  multiplier=1  deviceGroupName=DG1  
    ${deviceGroup2Obj} =  protocolObj.Create Device Group Ngpf  ${topology2Obj}  multiplier=1  deviceGroupName=DG2  
    ${ethernet1Obj} =  protocolObj.Create Ethernet Ngpf  ${deviceGroup1Obj}  ethernetName=Eth1  macAddress=${ethMacAddr1}
    ${ethernet2Obj} =  protocolObj.Create Ethernet Ngpf  ${deviceGroup2Obj}  ethernetName=Eth2  macAddress=${ethMacAddr2}
    ${ipv41Obj} =  protocolObj.Create Ipv4 Ngpf  ${ethernet1Obj}  ipv4Address=${ipv41}  gateway=${ipv4Gateway1}  prefix=24
    ${ipv42Obj} =  protocolObj.Create Ipv4 Ngpf  ${ethernet2Obj}  ipv4Address=${ipv42}  gateway=${ipv4Gateway2}  prefix=24

    Log To Console  Starting all protocols ...
    protocolObj.Start All Protocols

    Log To Console  Verifying protocol sessions ...
    protocolObj.Verify Protocol Sessions Up

    @{sourceEndpointObjects}  Create List  ${topology1Obj}
    @{destEndpointObjects}  Create List  ${topology2Obj}
    &{endpoint1}  Create Dictionary  name=Flow Group 1  sources=${sourceEndpointObjects}  destinations=${destEndpointObjects}
    @{endpoint1}  Create List  ${endpoint1}
    @{configElements}  Create List  ${configElements}

    Log To Console  Configure Traffic Item
    ${trafficItemStatus} =  trafficObj.Config Traffic Item  mode=create  trafficItem=${trafficItem1}  endpoints=${endpoint1}
    ...  configElements=${configElements}
    trafficObj.Regenerate Traffic Items  
    trafficObj.Start Traffic  

    # Get the Traffic Item and ConfigElement objects to use for making modifications
    ${trafficItemObj} =  Get From List  ${trafficItemStatus}  0
    ${configElementObj} =  Get From List  ${trafficItemStatus}  2
    ${configElementObj} =  Get From List  ${configElementObj}  0
    
    # Check the traffic state before checking stats
    ${result} =  trafficObj.Get Transmission Type  ${configElementObj}
    @{expectedTrafficState}  Create List  stopped
    Run Keyword If  ('${result}' == "fixedFrameCount")  RunKeyword
    ...  trafficObj.Check Traffic State  expectedState=${expectedTrafficState}

    Log To Console  Getting stats
    ${stats} =  statisticObj.Get Stats  viewName=Flow Statistics
    
    Log To Console  ${stats}
    
