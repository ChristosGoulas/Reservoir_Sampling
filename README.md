# Pseudocode

* K = sample size constant
* N = flow size

Store the first k elements of the Flow in K.
(Let's assume we already have a manager of n – 1 elements of the Flow. Our sample (K) includes exactly K of them randomly and uniformly with a probability of 1/(n -1)).

* When the nth element (n > K) of the Flow appears.
* With a probability of K/n, select the nth element to be added to the sample K, otherwise discard it.
* IF the nth element is selected to be added to K.
* THEN the nth element replaces one of the k elements already in the sample K. The one to be replaced is randomly and uniformly chosen.

# Logic

Essentially, we calculate each time the probability of an element being in our sample (in the code, this probability is p1= K / N), and then we use another randomly selected probability that "corresponds" to the probability of the nth element of the flow that just appeared (in the code, this is the probability p2). By comparing these two probabilities, we add the newly appeared element to our sample only if p2 ≤ p1. This check ensures that any element appearing in our sample will have a probability less than or equal to K / N. This is the desired property for our sample to be representative (uniformly random).

# Proof by mathematical induction

Base: For N ≤ K elements so far, the sample K has the desired property:

Each element of the flow is included in the sample with a probability of: n / n = 1.

Assumption: Suppose that after the appearance of n ≥ k elements, the sample K includes each element that has appeared so far with a probability of: k/n.

Step: We will show that even after the appearance of the (n + 1)th element of the flow, the sample K includes each of the first n + 1 elements of the flow with a probability of:

k/(n + 1)

Assumption: Suppose that after the appearance of n ≥ k elements, the sample K includes each element that has appeared so far with a probability of: k / n.

Step:

* The (n + 1)th element of the flow already has a probability of selection for the sample K exactly: k / (n + 1).
* Given that it was in K, the probability that one of the first n elements (let it be x) remains in K at time n+1 is:
(1 – k/(n+1)) + (k/(n + 1)) * ((k – 1)/k) = 1 – k/(n+1) + (k – 1)/(n + 1) = n/(n + 1)

Where:

* (1 – k/(n+1)) = "The n + 1 is not selected."
* k/(n + 1) = "The n + 1 is selected."
* (k – 1)/k = "x is not selected for replacement."

The total probability of one of the first n elements being in the sample K at time n + 1 is:

(k/n) * (n/(n + 1)) = k/(n + 1)

# Language
Python 3
