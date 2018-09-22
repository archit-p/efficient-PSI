## Secure Multi-Party Computation Protocols
Repository for IEEE year-long project. Look into the wiki for the learning outcomes.

### What is SMPC?
Secure multi-party computation is a method of securely computing the value of a function f for inputs (x1, x2, x3 … xn) when the inputs are distributed over multiple parties. Security here implies the function has to be computed when no two parties trust each other i.e. the values of any one party can’t be revealed to the other participating parties.

The security constraints that need to be fulfilled while computing the function are:
1. Privacy: no party should learn more than their prescribed output
2. Correctness: each parties output should be correct
3. Independence of Inputs: each party should choose their inputs independent of other parties inputs.
4. Guaranteed Output Delivery: adversary should not be able to execute a Denial of Service attack.
5. Fairness: corrupted parties should receive their output if and only if the honest parties receive their outputs.

### Interesting SMPC Problems
One good example of a function that can be computed in a multi-party setting is described by the Yao’s Millionaire Problem. Other example functions can be set intersection, matching problem, etc.

#### Yao's Millionaire Problem
The problem discusses two millionaires, Alice and Bob, who are interested in knowing which of them is richer without revealing their actual wealth. 

#### Set Intersection Problem
Each party has a dataset, and they want to find the intersection of the sets. 

#### Matching Problem
Each party has a bit, and they want to find the product of the bits.

### Weekly Plan
#### Weeks 1-2
1. Study number theory basics needed to understand cryptography.
2. Create GitHub repo with wiki.

#### Weeks 3-4
1. Study cryptography constructions - hash functions, symmetric encryption, asymmetric encrpytion.
2. Update wiki with cryptography section.
