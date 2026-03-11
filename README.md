# pufattack
Code to attack PUFs through BCH ECC bits

There was once a paper from a major semiconductor manufacturer, describing a PUF.
It could be seen that the entropy leaked through the chosen BCH scheme was greater than the size of the PUF

This code is a proof of concept to show a PUF made with that BCH scheme allows the PUF value to be retrieved from the check bits alone.

Why is this possible? The errors in a BCH used on a communication channel can occur in the data or the check bits. In a PUF the check bits are usually reliable (E.G. stored in fuses or flash memory) and the errors only occur in the PUF cells. So if the size of the the BCH table is big enough, each row in the BCH table uniquely identifies a PUF value.

This is what the code shows. It makes a random PUF value. Builds the check bits. Then uses only the check bits to compute the PUF value.

The vendor was told and they changed the algorithm.

It requires bchlib. If you don't have that a venv seems to be the best path.

```
git clone https://github.com/dj-on-github/pufattack
cd pufattack
python3 -m venv venv
source venv/bin/activate
pip install bchlib
python3 pufattack
```


An example run:

```
 % python3 attack.py         
0
1000000
2000000
3000000
4000000
5000000
6000000
7000000
8000000
9000000
10000000
11000000
12000000
13000000
14000000
15000000
16000000
PUF c0f4d7  ECC aaf60230f9
PUF bf9eae  ECC d069156453
PUF 712ba0  ECC 9c08272205
PUF bc9905  ECC 0c709238c0
PUF 49980f  ECC 4061f3f908
PUF fe3e68  ECC da413c072c
PUF ab5e1a  ECC 00bc5639d2
PUF 67b5ee  ECC 5c7affaaf0
PUF 993b66  ECC 20099116d8
PUF 80df82  ECC 0cd155a28a
 Found ECC aaf60230f9 ==> PUF c0f4d7
 Found ECC d069156453 ==> PUF bf9eae
 Found ECC 9c08272205 ==> PUF 712ba0
 Found ECC 0c709238c0 ==> PUF bc9905
 Found ECC 4061f3f908 ==> PUF 49980f
 Found ECC da413c072c ==> PUF fe3e68
 Found ECC 00bc5639d2 ==> PUF ab5e1a
 Found ECC 5c7affaaf0 ==> PUF 67b5ee
 Found ECC 20099116d8 ==> PUF 993b66
 Found ECC 0cd155a28a ==> PUF 80df82
```
