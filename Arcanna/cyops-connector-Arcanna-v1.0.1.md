## About the connector
Arcanna.ai is a platform for delivering decision intelligence. 
It augments Security Operation Center analysts in dealing with incoming threats by increasing analyst efficiency in decision-making.

More information is available at https://arcanna.ai
<p>This document provides information about the ArcannaAi Connector, which facilitates automated interactions, with a ArcannaAi server using FortiSOAR&trade; playbooks. Add the ArcannaAi Connector as a step in FortiSOAR&trade; playbooks and perform automated operations with ArcannaAi.</p>
### Version information

Connector Version: 1.0.1


Authored By: Arcanna.ai

Certified: No
## Installing the connector
<p>From FortiSOAR&trade; 5.0.0 onwards, use the <strong>Connector Store</strong> to install the connector. For the detailed procedure to install a connector, click <a href="https://docs.fortinet.com/document/fortisoar/0.0.0/installing-a-connector/1/installing-a-connector" target="_top">here</a>.<br>You can also use the following <code>yum</code> command as a root user to install connectors from an SSH session:</p>
`yum install cyops-connector-Arcanna`

## Prerequisites to configuring the connector
- You must have the URL of ArcannaAi server to which you will connect and perform automated operations and credentials to access that server.
- The FortiSOAR&trade; server should have outbound connectivity to port 443 on the ArcannaAi server.

## Minimum Permissions Required
- N/A

## Configuring the connector
For the procedure to configure a connector, click [here](https://docs.fortinet.com/document/fortisoar/0.0.0/configuring-a-connector/1/configuring-a-connector)
### Configuration parameters
<p>In FortiSOAR&trade;, on the Connectors page, click the <strong>ArcannaAi</strong> connector row (if you are in the <strong>Grid</strong> view on the Connectors page) and in the <strong>Configurations&nbsp;</strong> tab enter the required configuration details:&nbsp;</p>
<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>Server Address<br></td><td><br>
<tr><td>Server Port<br></td><td><br>
<tr><td>ApiKey<br></td><td><br>
<tr><td>Protocol<br></td><td><br>
<tr><td>Verify SSL<br></td><td>Specifies whether the SSL certificate for the server is to be verified or not. <br/>By default, this option is set as True.<br></td></tr>
</tbody></table>
## Actions supported by the connector
The following automated operations can be included in playbooks and you can also use the annotations to access operations from FortiSOAR&trade; release 4.10.0 and onwards:
<table border=1><thead><tr><th>Function<br></th><th>Description<br></th><th>Annotation and Category<br></th></tr></thead><tbody><tr><td>GET Arcanna RESPONSE<br></td><td><br></td><td> <br/>Utilities<br></td></tr>
<tr><td>Send Feedback<br></td><td><br></td><td> <br/>Utilities<br></td></tr>
<tr><td>Get Jobs<br></td><td><br></td><td> <br/>Utilities<br></td></tr>
<tr><td>Send To Arcanna<br></td><td><br></td><td> <br/>Utilities<br></td></tr>
</tbody></table>
### operation: GET Arcanna RESPONSE
#### Input parameters
<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>JobId<br></td><td><br>
</td></tr><tr><td>EventId<br></td><td><br>
</td></tr></tbody></table>
#### Output

 No output schema is available at this time.
### operation: Send Feedback
#### Input parameters
<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>user<br></td><td><br>
</td></tr><tr><td>JobId<br></td><td><br>
</td></tr><tr><td>EventId<br></td><td><br>
</td></tr><tr><td>closingStatus<br></td><td><br>
</td></tr></tbody></table>
#### Output

 No output schema is available at this time.
### operation: Get Jobs
#### Input parameters
None.
#### Output

 No output schema is available at this time.
### operation: Send To Arcanna
#### Input parameters
<table border=1><thead><tr><th>Parameter<br></th><th>Description<br></th></tr></thead><tbody><tr><td>JobId<br></td><td><br>
</td></tr><tr><td>title<br></td><td>Alert Title<br>
</td></tr><tr><td>caseId<br></td><td><br>
</td></tr><tr><td>body<br></td><td><br>
</td></tr></tbody></table>
#### Output

 No output schema is available at this time.
## Included playbooks
The `Sample - Arcanna - 1.0.1` playbook collection comes bundled with the ArcannaAi connector. These playbooks contain steps using which you can perform all supported actions. You can see bundled playbooks in the **Automation** > **Playbooks** section in FortiSOAR<sup>TM</sup> after importing the ArcannaAi connector.

- GET Arcanna RESPONSE
- Send Feedback
- Get Jobs
- Send To Arcanna

**Note**: If you are planning to use any of the sample playbooks in your environment, ensure that you clone those playbooks and move them to a different collection, since the sample playbook collection gets deleted during connector upgrade and delete.
