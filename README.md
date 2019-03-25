# Private Set Intersection based on Simplest Oblivious Transfer

This project contains code for an application that can compute the Set Intersection of two distributed sets in a privacy preserving manner. Our code is based on the PSI approach by Pinkas et al.<sup>[[1]](https://www.usenix.org/conference/usenixsecurity14/technical-sessions/presentation/pinkas)</sup> and the SimplestOT by Chou et al.<sup>[[2]](https://link.springer.com/chapter/10.1007/978-3-319-22174-8_3)</sup>.

## Background
### What is Private Set Intersection?
Private Set Intersection involves computing the intersection of two sets - S<sub>A</sub> held with Alice and S<sub>B</sub> held with Bob without leaking any extra information to either of the users. It has several practical uses, including private incident sharing, private contact discovery etc. 
### Approach
An equality test involves testing whether two elements X and Y are equal. Oblivious transfer has been shown to be used for efficiently performing private equality test. Equality tests can be extended to perform set inclusion tests which can further be extended to set intersection computation.
### Results
We are able to achieve intersection computation of two 2<sup>10</sup> element sets in under 100 seconds. Considering the performance overhead of Python websockets, we believe we have achieved good performance with the desired accuracy. The protocol scales with O(nlogn) complexity wrt set size n. We have obtained results confirming this.

## Getting Started
### Prerequisites
The code is written in Python3, get it from [here](https://www.python.org/downloads/). We utilize [fastecdsa](https://github.com/AntonKueltz/fastecdsa) for elliptic curve operations.
### Usage
Some test datasets have been included in the repository. A quick way to test the code is using the included datasets. 
Run these commands in two seperate terminals.
```bash
python3 ot_receiver_test.py ../test/data2_1 100
```
```bash
python3 ot_sender_test.py ../test/data2_2 100
```
## License 
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments
This project was carried out as a part of [IEEE NITK](https://ieee.nitk.ac.in).
