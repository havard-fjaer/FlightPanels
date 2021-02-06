# High level device driver for Logitech / Saitek Flight Panels
Based on the documentation compiled by Björn Andersson (https://github.com/bjanders/fpanels)

## Status
- Work in progress. The base communication is established, but needs more work before it works fully in a flight simulator.
- I only own the Radio Panel, so for now there are no implementation of the Multi Panel or Switch Panel.
## Components
The driver consists of:
- **PanelBase**, that handles USB device connection and starts a thread per device that listens for changes.
- **RadioPanel**, that contains logic specific for the Radio Panel, such as mapping bits to buttons, and updating LCD displays, aided by some supporting classes and fuctions.
- **Controller** loads and starts the panels, and triggers termination of threads (listens for Ctrl-C).
- **panel_mapping** - a demo implementation on how to connect the device to actions in a flight simulator. A dictionary maps button events to functions, separating the driver from whatever logic you may want to implement yourself.

- **Main** starts the demo of the radio panels.
## Typical usage
- Load panels into the controller - or handle running yourself.
- Create a action map, connecting button events defined in **RadioPanelFlag** to functions that you implement yourself. I.e. use the SimConnect library (https://github.com/odwdinc/Python-SimConnect) to connect the radio panels to your simulator.
