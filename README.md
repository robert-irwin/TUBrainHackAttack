# TUBrainHackAttack

Our repository for all code used to develop our GetRekt Car during the 2016 IEEE Brain Hackathon at Temple University.

### Members
- James Kollmer

  Built and configured Spikers. This included writing a large portion of the bare metal C code that runs on a Arduino UNO development board to acquire the EMG samples.
  
- Robert Irwin 

  Wrote the bare metal, embedded software to control the car’s Arduino UNO. With James, also responsible for acquiring EMG samples with UNO paired with the two Spikers.

- Andrew Powell

  Created C Python / classes for wirelessly communicating between host computer and car’s UNO, and host computer and Spiker’s UNO. Wrote Python application for running system from a host computer.

- Christian Ward

  Developed Python Class for interfacing with / getting data from Emotiv Insight. This included testing and determining how to best interpret the data ( power averages ) from the Emotiv.
