# Random Number Generation Using Boson Sampling -- ORCA-Computing
## Team and members
* **Team**: al-Khwarizmi
* **Members**:
    1. Yousof Mardoukhi
        * GitHub ID: [ymardoukhi](https://github.com/ymardoukhi)
        * Discord ID: Yousof#1948, 902571449041174598
        * Email: ymardoukhi@gmail.com
* **Challenge**: Random Number Generation Using Boson Sampling -- ORCA Computing
---
## Summary
__NOTE: for in-depth analysis of the results refer to <u>analysis.ipynb</u> file. This readme contains information on how to use this repository__

This repository contains necessary scripts and libraries to simulate a Boson Sampler using [Strawberry Fields](https://strawberryfields.ai/) library developed by [Xanadu](https://www.xanadu.ai/). The aim is to encode, post-process or extract entropy out of the outcomes (Fock states) of a Boson Sampler (BS) such that we could get __True Uniform Random Binary Sequences__. The stress is put more on the post-processing of the BS outputs. We address three approaches here to generate random binary sequences
1. Von Neumann debiasing [[1]](https://mcnp.lanl.gov/pdf_files/nbs_vonneumann.pdf) [[2]](https://arxiv.org/pdf/2206.02292.pdf)
2. Huffman Encoding [[3]](https://link.springer.com/book/9780387947044)
3. Permutation Symmetry

We use NIST SP800-22 test suit [[4]](https://csrc.nist.gov/publications/detail/sp/800-22/rev-1a/final) to evaluate the randomness of the binary sequences.

---
## Repository Structure
```
.
├── analysis.ipynb              -> Analyses of the results
├── binstrs2binstream.py        -> Convert list of binary strings to a binary stream
├── borealis_cloud.py           -> Submit job to Xanadu Borealis device on cloud
├── borealis_local.py           -> Simulate the Borealis BS using Gaussian backend
├── data                        -> Main simulation data storage
│   ├── borealis                -> Borealis cloud and local simulation results
│   └── n4_m4_nparam5_v0        -> BS simulation results using fock backend
│       └── nist                -> Stores the output results of the NIST SP800-22 tests
├── figs                        -> Figures for README.md and analysis.ipynb file
├── full_sim.sh                 -> Script than runs a full simulation for multimode linear BS
├── main_exact.py               -> Calculate the exact probabilities of the Fock states
├── main_hufmann.py             -> Post-processing of BS Fock states using Huffman Encoding
├── main_permutation.py         -> Post-processing of BS Fock states using permutation symmetry
├── main_sim.py                 -> Simulate BS using fock backend
├── main_tf.py                  -> Experimental: tune the BSGates to yield higher entropy
├── nist_extractor.sh           -> Bash script that extracts results of different test from NIST STS output
├── papers                      -> Folder where relevant papers are stored for further reading
├── README.md                   -> This readme file
├── requirements.txt            -> pip requirements for initialising the python environment
└── src                         -> Libraries
    ├── Architecture.py         -> Initialise the architecture of a BS
    ├── Borealis.py             -> Initialise the Borealis device on Xanadu cloud
    ├── BosonSamplingStat.py    -> Tools to analyse the disribution of Fock states
    ├── NIST.py                 -> Source for plotting NIST results
    ├── PostAnalysis.py         -> Tools to analyse a set of binary stream 
    └── PostProcessing.py       -> Post-processing methods Von Neumann, Huffman and Permutation Symmetry
```
---
## Local simulation multimode linear interferometer using the `fock` backend
To simulate a BS with a specific set of modes and gates using the `fock` backend, the user first needs to define the architecture in `src/Architecture.py`. In this file, the user can defines the number of input photons, the number of `BSGate`s and their transmittivity angle $\theta$. All the $\theta$'s are hard-coded to $\pi/4$ currently. This will change in favour of passing the angles in a `json` file.

The components mentioned above are understood as the free parameters of the architecture. Note that the phase angle $\phi$ is set to zero for all of them. The user must then takes note of the total number of photons, modes and the number of `BSGate`s. Once the architecture is set, the user can simulate the BS using the following command
```bash
python main_sim.py 4 4 5 0 1000000
```
where the arguments are
```bash
$ python main_sim.py -h
usage: main_sim.py [-h] n m n_param v N

positional arguments:
  n           number of photos
  m           number of modes
  n_param     number of beam-spliters
  v           version of the architecture
  N           total number of runs

optional arguments:
  -h, --help  show this help message and exit
```
The argument `v` let the user to consider variation of the architecture when the number of photons, modes and `BSGate`'s remain unaltered.

The results of the simulation are stored in `data/n4_m4_nparam5_v0/`. The name of the directory signifies the arguments of `main_sim.py`. Two files are generated,

1. `samples_N1000000.npy`
2. `vonneumann_strs_N1000000.json`

The first file contains all the Fock states that the BS sampled. The second contains all the results of the post-processing of the sampled Fock states according to the protocol described in Ref.[[2]](https://arxiv.org/pdf/2206.02292.pdf)

The user can try other encoding of the Fock states implemented in this repository. They are _Huffman encoding scheme_ and _permutation encoding scheme_. To do so, it is sufficient to execute the followings
```bash
$ python main_huffman.py 4 4 5 0 1000000
$ python main_permutation.py 4 4 5 0 1000000
```
The results of the two scripts above are stored as `huffman_strs_N1000000.json` and `permutation_strs_N1000000.json` in `data/n4_m4_nparam5_v0`. Note that for the Huffman encoding protocol, the user must initially calculate the full probability distribution of the Fock states by executing 
```bash
$ python main_exact.py 4 4 5 0
```
which generates the `exact_result.json` in `data/n4_m4_nparam5_v0` directory. Moreover, the _permutation protocol_ is in its early stages is only works with the default architecture defined in `src/Architecture.py`.

Once the output binary strings are generated, e.g. `vonnoumann_strs_N10000000.json`, the user can generate a binary file of the whole stream by using `binstrs2binstream.py` script. The script receives a `json` file of binary strings and outputs a binary file of the concatenation of all of them. This output binary file then can be used as the input of NIST SP800-22 statistical test suit for Random Number Generators to assess the randomness in the binary strings. For instance
```bash
$ python binstrs2binstream.py data/n4_m4_nparam5_v0/vonneumann_strs_N1000000.json data/n4_m4_nparam5_v0/vonneumann.bin
```

To simply the whole procedure the user can execute the bash script `full_sim.sh` by providing the necessary arguments for the python scripts mentioned above i.e.
```bash
$ bash full_sim.sh 4 4 5 0 1000000
```
---
## Xanadu Cloud and local Gaussian simulation of time-domain multiplexing Borealis device
In order to test Quantum Random Number Generation with real quantum hardware, we used Borealis time-domain multiplexing interferometer designed by Xanadu. To get more information about how to programme this device refer to this [link](https://strawberryfields.ai/photonics/demos/tutorial_borealis_quickstart.html).

Initially the user must register in [Xanadu Cloud](https://cloud.xanadu.ai/) platform and acquire an API key. Then set the environment according to this [documentation](https://strawberryfields.ai/photonics/demos/tutorial_X8.html#configuring-your-credentials).

To submit a programme to the Borealis device on Xanadu cloud execute the following
```bash
$ python borealis_cloud.py 4 1000000
```
where the first argument is the number of modes and the second is the total number of shots.
```bash
$ python borealis_cloud.py -h
usage: borealis_cloud.py [-h] m N

positional arguments:
  m           number of modes
  N           total number of runs

optional arguments:
  -h, --help  show this help message and exit
```
This submits the job to Xanadu Cloud and stores the sampled Fock states in `data/borealis/samples_cloud_N1000000.npy`. Subsequently, it post-processes those samples using the von Neumann debiasing protocol and stores those strings in `data/borealis/output_strs_cloud_N1000000.json`. Other two protocols, namely Huffman encoding and permutation symmetry are not yet implemented for the Borealis device.

The user can also simulate Borealis BS using local `gaussian` engine by executing
```bash
$ python borealis_local.py 4 1000000
```
which produces `samples_local_N1000000.npy` and `output_strs_local_N1000000.json` in `data/borealis` directory.

Similarly to the previous section, the in order to produce a binary file of all the binary strings produced by the post-processing procedure, it sufficient to execute for instance
```bash
$ python binstrs2binstream.py data/borealis/output_strs_local.json data/borealis/vonneumann.bin
```
The output binary file than can be passed to the NIST statistical test suit and analyse the result.

---
## NIST Statistical Test Suit (STS)
First grab a copy of the Statistical Test Suit from [here](https://csrc.nist.gov/CSRC/media/Projects/Random-Bit-Generation/documents/sts-2_1_2.zip). Also refer to the website [here](https://csrc.nist.gov/projects/random-bit-generation/documentation-and-software) and the latest publication [here](https://csrc.nist.gov/publications/detail/sp/800-22/rev-1a/final).

First unzip and navigate to unzipped folder. Therein, execute `make` to compile the source. This produces a binary executable called `assess`. To initiate the test execute
```bash
$ ./assess 16384
```
where the number is the length of the binary strings. What happens here is that `assess` partitions a binary file of ascii `0`'s and `1`s into binary strings of length 16384.

The following shows how to proceed with the test suit. Parts that we have to provide an input are indicated by `<- <comment in uppercase letters>`
```
           G E N E R A T O R    S E L E C T I O N 
           ______________________________________

    [0] Input File                 [1] Linear Congruential
    [2] Quadratic Congruential I   [3] Quadratic Congruential II
    [4] Cubic Congruential         [5] XOR
    [6] Modular Exponentiation     [7] Blum-Blum-Shub
    [8] Micali-Schnorr             [9] G Using SHA-1

   Enter Choice: 0 <- HERE WE PASS 0 TO INDICATE THAT WE WANT TO ANALYSE A BINARY INPUT FILE


		User Prescribed Input File: ../boson-sampling/data/n4_m4_nparam5_v0/vonneumann.bin <- INPUT FILE

                S T A T I S T I C A L   T E S T S
                _________________________________

    [01] Frequency                       [02] Block Frequency
    [03] Cumulative Sums                 [04] Runs
    [05] Longest Run of Ones             [06] Rank
    [07] Discrete Fourier Transform      [08] Nonperiodic Template Matchings
    [09] Overlapping Template Matchings  [10] Universal Statistical
    [11] Approximate Entropy             [12] Random Excursions
    [13] Random Excursions Variant       [14] Serial
    [15] Linear Complexity

         INSTRUCTIONS
            Enter 0 if you DO NOT want to apply all of the
            statistical tests to each sequence and 1 if you DO.

   Enter Choice: 1 <- HERE WE CHOOSE 1 TO INDICATE THAT WE WANT TO PERFORM ALL THE STATISTICAL TESTS             

        P a r a m e t e r   A d j u s t m e n t s
        -----------------------------------------
    [1] Block Frequency Test - block length(M):         128
    [2] NonOverlapping Template Test - block length(m): 9
    [3] Overlapping Template Test - block length(m):    9
    [4] Approximate Entropy Test - block length(m):     10
    [5] Serial Test - block length(m):                  16
    [6] Linear Complexity Test - block length(M):       500

   Select Test (0 to continue): 0 <- PASS 0 TO LEAVE THE PARAMETERS UNCHANGED

   How many bitstreams? 110 <- NUMBER OF BINARY STRINGS OF LENGTH 16384

      Input File Format:
    [0] ASCII - A sequence of ASCII 0's and 1's
    [1] Binary - Each byte in data file contains 8 bits of data

   Select input mode:  0 <- OUR FILE IS AN ASCII OF 0 AND 1
```
This will perform all the statistical tests on the binary file. The result gets stored in `<path to STA suit>/experiments/AlgorithmTesting/finalAnalysisReport.txt`. The content of a sample report may look like the following

```
------------------------------------------------------------------------------
RESULTS FOR THE UNIFORMITY OF P-VALUES AND THE PROPORTION OF PASSING SEQUENCES
------------------------------------------------------------------------------
   generator is <../boson-sampling/data/n4_m4_nparam5_v0/vonneumann.bin>
------------------------------------------------------------------------------
 C1  C2  C3  C4  C5  C6  C7  C8  C9 C10  P-VALUE  PROPORTION  STATISTICAL TEST
------------------------------------------------------------------------------
  0   0   0   0   0   0   0   0   0 110  0.000000 *  110/110     Frequency
  0   0   0   0   0   0   0   0   0 110  0.000000 *  110/110     BlockFrequency
  0   0   0   0   0   0   0   0   0 110  0.000000 *  110/110     CumulativeSums
  0   0   0   0   0   0   0   0   0 110  0.000000 *  110/110     CumulativeSums
110   0   0   0   0   0   0   0   0   0  0.000000 *    0/110  *  Runs
110   0   0   0   0   0   0   0   0   0  0.000000 *    0/110  *  LongestRun
 13  12  14  15   7  10  10  13   7   9  0.684327    109/110     Rank
110   0   0   0   0   0   0   0   0   0  0.000000 *    0/110  *  FFT
110   0   0   0   0   0   0   0   0   0  0.000000 *   30/110  *  NonOverlappingTemplate
 10  10  10   9   9  14  17  11  12   8  0.739918    107/110     NonOverlappingTemplate
 79  22   6   2   0   0   1   0   0   0  0.000000 *   98/110  *  NonOverlappingTemplate
110   0   0   0   0   0   0   0   0   0  0.000000 *    0/110  *  OverlappingTemplate
110   0   0   0   0   0   0   0   0   0  0.000000 *    0/110  *  Universal
110   0   0   0   0   0   0   0   0   0  0.000000 *    0/110  *  ApproximateEntropy
110   0   0   0   0   0   0   0   0   0  0.000000 *    0/110  *  RandomExcursions
  0   0   0   0   0   0   0   0   0   0     ----     ------     RandomExcursionsVariant
 24   1   2   1   0   0   0   0   0   0  0.000000 *   22/28   *  RandomExcursionsVariant
110   0   0   0   0   0   0   0   0   0  0.000000 *    0/110  *  Serial
110   0   0   0   0   0   0   0   0   0  0.000000 *    0/110  *  Serial
 17   7   6  12  11  15  10   6  10  16  0.150649    107/110     LinearComplexity


- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
The minimum pass rate for each statistical test with the exception of the
random excursion (variant) test is approximately = 105 for a
sample size = 110 binary sequences.

The minimum pass rate for the random excursion (variant) test is undefined.

For further guidelines construct a probability table using the MAPLE program
provided in the addendum section of the documentation.
- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
```
There are two important columns, _P-VALUE_ and _PROPORTION_. At the bottom of the file it is seen that a test is passed if out of 110 binary strings, at least 105 of them must fulfil the test. Otherwise, the test gets failed. If the proportion is for instance $104/110$ then this is indicated by a *. The same applies to the _P-VALUE_ column. The _p-value_ of a test must be $>0.01$ in order for the test to get passed. If the _p-value_ is smaller than this value, then an asterisk * appears near the test. Thus, for a test to get passed, both of these must fulfil their criteria.

The output file is then moved to `data/n4_m4_nparam5_v0/nist_vonneuman.txt`. Similar results for the Huffman encoding scheme and the permutation encoding are stored under the names `nist_huffman.txt` and `nist_permutation.txt` respectively.

*__hint on choosing the length and the number of bitstreams:__* when running the NIST test suit, the user must choose the length of the binary strings and how many of those are there in a binary file. We want to chose a length at which the binary string has an equal number of `0` bits and `1` bits i.e. the digit `0` and the digit `1` appear equally. This can be done by counting the number of zeros and ones at different lengths and choose the smallest value (for instance have a look at `analysis.ipynb` file to see at which length scales the ration between zeros and one asymptotically reaches unity). Let us call this $L$. Then we turn back to your binary file, let's say `vonneuman.bin`. We count the total number of bits in this file and denote it by $T$. Then the total number of binary strings is given by 

$$
  n = \left\lfloor\frac{T}{L}\right\rfloor
$$