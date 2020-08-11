# pufattack
Code to attack PUFs through BCH ECC bits

There was once a paper from a major semiconductor manufacturer, describing a PUF.
It could be seen that the entropy leaked through the chosen BCH scheme was greater than the size of the PUF

This code is a proof of concept to show a PUF made with that BCH scheme allows the PUF value to be retrieved from the check bits alone.

Why is this possible? The errors in a BCH used on a communication channel can occur in the data or the check bits. In a PUF the check bits are usually reliable (E.G. stored in fuses or flash memory) and the errors only occur in the PUF cells. So if the size of the the BCH table is bug enough, each row in the BCH table uniquely identifies a PUF value.

This is what the code shows. It makes a random PUF value. Builds the check bits. Then uses only the check bits to compute the PUF value.

The vendor was told and they changed the algorithm.
