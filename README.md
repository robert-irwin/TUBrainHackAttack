# IEEE/TU Brain Hackathon: 2016 September 23-25

Our repository for all code used to develop our Team GetRekt Car during the 2016 IEEE Brain Hackathon at Temple University in Philadelphia, PA. This was the first year of competition which was organized to be held in three cities throughout the year: San Diego, CA; Philadelphia, PA; Budapest, HU.

### Members
We're all graduate students at Temple University pursuing different areas of research. The team was organized by Andrew who felt the hackathon would bring together all of our unique skills. A slightly more detailed review of our work can be found at Andrew's [HACKADAY](https://hackaday.io/project/15310-getrekts-emg-eeg-controlled-rc-car) page.
  
- James Kollmer, MS

  Built and configured Spikers. This included writing a large portion of the bare metal C code that runs on a Arduino UNO development board to acquire the EMG samples.
  
- Robert Irwin, MS

  Wrote the bare metal, embedded software to control the car’s Arduino UNO. With James, also responsible for acquiring EMG samples with UNO paired with the two Spikers.

- Andrew Powell, PhD

  Created C Python / classes for wirelessly communicating between host computer and car’s UNO, and host computer and Spiker’s UNO. Wrote Python application for running system from a host computer.

- Christian Ward, PhD

  Developed Python Class for interfacing with / getting data from Emotiv Insight. This included testing and determining how to best interpret the data ( power averages ) from the Emotiv.
 
### Project
Prior to the start of the hackathon, it was clear that all groups would be given some form of EEG headset, an [Emotiv Insight](https://www.emotiv.com/insight/) or an [OpenBCI headset](http://openbci.com/), along with a [muscle spiker kit](https://backyardbrains.com/products/muscleSpikerShield). Andrew's original concept was to enable a user to paint without needing to use the mouse which was a well received idea within the group. However, as the hackathon approached the group shifted towards what they thought would be a more impressive demo of using a remote controlled car as the final goal.

The general idea we had for the car was to first get the car working as a regular RC car, something we knew we could do during the event, and then figure out how to apply the data we would get from the other devices to control the car. Our car was on loan from a professor at Temple (Thanks Dr. Helferty) and we gathered up [Xbees](https://www.digi.com/lp/xbee) for communicationg between the car and our computer. A number of [Arduinos](https://www.arduino.cc/) were used to support the car and the muscle spikers.

Below is a cartoon showing the overall system setup.

![alt text][cartoon]

As the cartoon indicates, we wrote all of our code in either C or Python. We couldn't avoid the C for using the Arduino or the Xbees, but we chose Python as it was supported by [Emotiv](http://emotiv.github.io/community-sdk/). Setting up the framework to control the car was developed in parallel with building, testing and development of code to gather data from the Insight and the muscle spikers. Thankfully all of these tasks came together at the same time allowing the group to work together on addressing integrating them to complete the overall system.

The major breakthrough came late at night as the first integration of the muscle spikers and car proved to be very effective for turn control. The following morning we were able to pair the Insight with the car as a means to control the on/off state of the car. Unfortunately the most distinct signal we could pick up with the Emotiv was a jaw clench and not a pure brainwave. Still pretty neat in the end and something everyone enjoyed working on over the weekend.

[cartoon]: https://lh4.googleusercontent.com/wn-DLa25Y4AIKMP5CTGxjDemtEV5gTdGs2OuQylRLMhcJc6kLHzN1UJvvL1Eflbk6R-n0pCqPUmHXKRQBBQE0m_z4Kycf8A6JLg2kZmkvlSEW7HPpefzeN-7bn4AlLXdxqvSTozx "GetRekt Project Layout"

