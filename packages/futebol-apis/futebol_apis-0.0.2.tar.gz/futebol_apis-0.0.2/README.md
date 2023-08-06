FUTEBOL API Definitions
==========

This repository contains the definition of all schemas used by the FUTEBOL services. The schemas are define using the protobuf DSL. The DSL description can be compiled to generate code in almost any programming language. In order to use that generated code you need to know the conventions for your language of choice:
  - [Javascript/ NodeJS](https://developers.google.com/protocol-buffers/docs/reference/javascript-generated)
  - [Python](https://developers.google.com/protocol-buffers/docs/reference/python-generated)

## Installing the protobuf compiler
To generate messages the protobuf compiler is necessary. To download and install it run the following commands:

```bash
wget https://github.com/protocolbuffers/protobuf/releases/download/v3.6.1/protoc-3.6.1-linux-x86_64.zip
unzip protoc-3.6.1-linux-x86_64.zip
sudo cp -rf bin/ /usr/local/
sudo cp -rf include/ /usr/local/
sudo chown -R $USER /usr/local/include/google
```

## *Python*

### Easy install

```bash
pip install --user futebol-apis
```

### From source

Generate the python source code:
```bash
protoc --python_out=. src/nerds/futebol/*.proto
```

Install the package:
```bash
pip install --user -e .
```

Using the library:
```python
from nerds.futebol.api_pb2 import StationStatus
status = StationStatus()
status.snr = 0.53434 # dBm
status.channel_frequency = 2.4262 # Ghz
print(status)
```

## *Javascript / NodeJS*

Install build dependencies and compile .proto schemas to .js files:
```shell
npm install # to get build dependencies
npm run generate # to generate js files
```

Now to use it on server side (nodejs) simply import and use the generated files, i.e:
```js
const apis = require("./api_pb.js");

let status =  new apis.StationStatus()
status.setSnr(0.53434) // dBm
status.setChannelFrequency(2.4262) // Ghz
console.log(status.toObject());
// ...
```

To use it on the browser, browserify the files by running:
```shell
npm run browserify 
```

Now to use it on the browser, include the browserified bundle, i.e:
```html
<script src="apis.js"></script>
<script>
  var status = new proto.nerds.futebol.StationStatus()
  status.setSnr(0.53434) // dBm
  status.setChannelFrequency(2.4262) // Ghz
  console.log(status.toObject());
</script>
// ...
```

## Services

### Vertical VM Austoscaler
Allow VM's / VNF's in an experiment to be automatically scaled in a vertical way, that is, increase or decrease their resources based on user specified policies. 

#### :arrows_counterclockwise: VerticalVMAutoscaler.Update: [VerticalScalerUpdateRequest](docs/README.md#nerds.futebol.VerticalScalerUpdateRequest) ⇒ [VerticalScalerUpdateReply](docs/README.md#nerds.futebol.VerticalScalerUpdateReply)

Update the scaler policies for one or more VM's.

#### :arrows_counterclockwise: VerticalVMAutoscaler.Delete: [VerticalScalerDeleteRequest](docs/README.md#nerds.futebol.VerticalScalerDeleteRequest) ⇒  [VerticalScalerDeleteReply](docs/README.md#nerds.futebol.VerticalScalerDeleteReply)

Remove one or more VM from the group of VM's being auto-scaled.

#### :arrow_right: VerticalVMAutoscaler.Status: ⇒  [VerticalScalerStatus](docs/README.md#nerds.futebol.VerticalScalerStatus)

Periodically published information about the VMs being auto-scaled.


### [Handover Controller](https://github.com/nerds-ufes/futebol-wifi/)
Controls where the wireless traffic should be routed based on some algorithm. 

#### :arrows_counterclockwise: HandoverCtl.Update: [HandoverUpdateRequest](docs/README.md#nerds.futebol.HandoverUpdateRequest) ⇒ [HandoverUpdateReply](docs/README.md#nerds.futebol.HandoverUpdateReply)

Configure the parameters of the handover controller algorithm. 


### [Station](https://github.com/nerds-ufes/futebol-wifi/)

#### :arrows_counterclockwise: Station.ID.Update: [StationUpdateRequest](docs/README.md#nerds.futebol.StationUpdateRequest) ⇒ [StationUpdateReply](docs/README.md#nerds.futebol.StationUpdateReply)

Configure the station broadcast parameters. The station uses beacon frames to configure the AP in the robot.

#### :arrow_right: Station.ID.Status: ⇒ [StationStatus](docs/README.md#nerds.futebol.StationStatus)

Periodically publishes information about the STA's.


### [Experiment Frontend](https://github.com/nerds-ufes/futebol-robot-frontend/)

#### :arrows_counterclockwise: ExperimentFrontend.Update: [ExperimentUpdateRequest](docs/README.md#nerds.futebol.ExperimentUpdateRequest) ⇒ [ExperimentUpdateReply](docs/README.md#nerds.futebol.ExperimentUpdateReply)

Configure the experiment parameters, e.g: the task the robot should perform. If a task is already being executed it will be overridden by the new task.

#### :arrow_right: ExperimentFrontend.Health: ⇒ [ServiceHealthInfo](docs/README.md#nerds.futebol.ServiceHealthInfo)

Periodically publishes information about the healthy of the experiment services.


### Robot Controller

#### :arrow_right: RobotController.ID.Status: ⇒ [RobotControllerProgress](docs/README.md#nerds.futebol.RobotControllerProgress)

Periodically publishes information about the control task.


### [Camera Gateway](https://github.com/labviros/is-cameras)

#### :arrow_right: CameraGateway.ID.Frame: ⇒ [Image](docs/README.md#nerds.futebol.Image)

Periodically publishes the latest frame captured by the camera.