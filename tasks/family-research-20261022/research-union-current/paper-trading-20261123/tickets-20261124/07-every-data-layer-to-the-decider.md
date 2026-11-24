# 07: Every data layer to the decider, finished

**What to build:** The packet a decider is given holds every data layer known at the signal's moment, whole; what is known only afterwards is kept beside it for learning; a decider is written that uses the two lines and the depth.

**Blocked by:** None for the packet; 03 for the new decider

**Status:** ready-for-agent

- [ ] ROOT's stored planes known by the moment are in the packet, layer by layer; a layer that cannot be placed is named with the reason
- [ ] The whole state and every layer are written beside the brief; a decision may rest on any id of any layer
- [ ] The after-the-fact file is written and can never reach a decider or pass as a ground
- [ ] Each decision's line records the layers its packet held and the layers it named
- [ ] A second decider that reads the dipole and exhaustion lines and the depth goes through ticket 03's door
- [ ] Missing pieces covered: F38, F39
