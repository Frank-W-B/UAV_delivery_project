# UAV Delivery Capstone Project for DSI

Amazon, Google, and UPS continue to investigate unmanned aerial vehicles (UAVs)
for home package delivery. NASA and the FAA are attempting to develop the
technological and regulatory infrastructure needed for UAVs in many
industries, including package delivery. However, decisions are being made by
both agencies that would affect delivery service without a public model to
evaluate the effects of their decisions. For instance, should heliports at
hospitals, police departments, and news agencies continue to require 5 mile
radius no-fly zones? Should schools, government buildings, major shopping
areas and parks also be protected by no-fly zones, and if so how large? How
should flying over roads and highways be managed? And for delivery services and
potential customers, how will package delivery time and UAV requirements be
affected by these decisions?

The first part of the project answers these questions by creating
package delivery models for Denver County. "As the crow flies" routes are compared
to more constrained routes that include no-fly zones for many locations.
Routing problems solved via graph theory using data aggregated from the US. Census,
the DenverOpenData catalog, Wikipedia, and Google Maps via the JavaScript API. 
Results are visualized on Google Maps and in matplotlib.

The second part of the project addresses the final step of delivery: package
drop-off at the customer's home. In Amazon's conception of this step, the
customer places a 1'x1' sign with the Amazon logo flat on the ground near their
home where they want the UAV to land. As the UAV nears the home it switches
from GPS navigation to an on-board camera that looks for the sign and positions
itself over it to land. This is too restrictive. It should be possible to classify
potential landing zones around a home using high resolution satellite images.
These landing zones could serve as default landing locations that would not require
the customer's presence for deliveries. This portion of the project demonstrates
proof-of-concept for one city block.  Analysis consisted of training and
testing a random forest classifier on aerial images.
