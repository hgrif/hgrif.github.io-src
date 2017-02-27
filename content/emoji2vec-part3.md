Title: 💩2vec - Word2vec (3/4)
Date: 2017-01-09
Category: Blogs
Series: 💩2vec


Word2vec is an unsupervised algorithm that tries to learn the meaning of words.
It does this by constructing abstract concepts that link words to each other.
Concepts can, for instance, be cities, emotions or gender, but because learning is unsupervised we can't control what concepts are learned.
We can only look at the outcome and see it makes sense to us.

This blog shows a worked example of word2vec, some articles that conceptually explain word2vec are listed at the end.  


## Word2vec


Word2vec learns representations of words by constructing two matrices with word vectors: $\mathbf{W}_{\text{input}}$ and $\mathbf{W}'_{\text{out}}$. 
These matrices contain word representations for all words in the vocabulary and will allow use to investigate the concepts behind words.
Conceptually they are similar, but they are used for different concepts and contain different representations.
Even though we'll only use the representations of one matrix, we'll need to learn both.

Learning is done with either continuous bag-of-words (CBOW) or skip-gram (SG).
Both CBOW and SG consider a sequence of words and split a sequence in a target word and its context:


$$ \underbrace{\mathsf{happy}}_\text{context} \overbrace{\mathsf{panda}}^\text{target}\, \underbrace{\mathsf{laughs}}_\text{context} $$


CBOW predicts a target word given a context:

$$ P_{\mathsf{CBOW}}(\mathsf{target} | \mathsf{context}) = P_{\mathsf{CBOW}}(\mathsf{panda} | \mathsf{happy}, \mathsf{laughs}) $$

while SG predicts a context given a target word:

$$ P_{\mathsf{SG}}(\mathsf{context} | \mathsf{target}) = P_{\mathsf{SG}}(\mathsf{happy}, \mathsf{laughs} | \mathsf{panda}) $$

We'll train a neural network to make our predictions.
The architecture of our neural network for predicting a target from a one-word context is given below.
The network consists of an input layer, a hidden layer and an output layer.
For CBOW the input layer codes for the context, the hidden layer contains the abstract concepts and the output layer predicts the targets.
SG switches the context and the target.


<figure>
<p align="center">
<img src="{filename}/images/emoji2vec/one-word-cbow.png" alt="Drawing" style="width: 400px;"/>
<caption>
<p align='center'>
Neural network architecture (source: word2vec Parameter Learning Explained)
</p>
</caption>
</p>
</figure>

So how are the two matrices with word vectors used by the neural network?
These implementations use $\mathbf{W}_{\text{input}}$ and $\mathbf{W}`_{\text{out}}$ in different ways.
For CBOW the input matrix $\mathbf{W}_{\text{input}}$ contains the representation of the words in the context and $\mathbf{W}'_{\text{out}}$ that of the target.
SG learns representations of target and context in respectively $\mathbf{W}_{\text{input}}$ and $\mathbf{W}'_{\text{out}}$.
The neural network constructs the word vectors to learn how to predict the target given a context (or vice versa).

Learning to predict is clearly supervised: we can penalize the algorithm if it doesn't predict the right target or context. 
Learning the representations is, however, unsupervised: we don't influence *what* concepts are learned.
Our precious matrices are a by-product of learning to predict a target from a context for CBOW (and vice versa for SG).


## Worked example

In this worked example we'll assume that our total vocabulary consist of three words: $\mathsf{happy}$, $\mathsf{panda}$ and $\mathsf{chair}$.
Their respective word vectors are $\mathbf{v}_0$, $\mathbf{v}_1$ and $\mathbf{v}_2$.
We'll learn representations using CBOW and a one-word context with a hidden layer of size 2.
In this example we won't consider $\mathsf{panda}$ to be one of the target words.

We start off not knowing what the representations are, so we take random values for the input and output matrices.

<figure>
<p align="center">
<img src="{filename}/images/emoji2vec/worked-example-w-start.png" alt="Drawing" style="width: 600px;"/>
</figure>

Words are represented with different colors, solid lines are used for input vectors and dashed lines for out vectors.
Our hidden layer has size 2 so we can conveniently plot the 2D vectors.
Unfortunately, we don't start with a good input matrix: $\mathsf{happy}$ is closer to $\mathsf{chair}$ than $\mathsf{panda}$.
Things look better in the output matrix where $ \mathsf{chair}$ is farther away from $ \mathsf{happy}$.

Better representations can be learned from data.
We encounter text with the following words that we feed into our neural network:

$$ \underbrace{\mathsf{happy}}_\text{context} \overbrace{\mathsf{panda}}^\text{target} $$

$\mathsf{happy}$ is the context and $\mathsf{pandas}$ is the target, so we'll try to adjust our word vectors by predicting $\mathsf{pandas}$ given $\mathsf{happy}$:

$$ P_{\mathsf{CBOW}}(\mathsf{target} | \mathsf{context}) = P_{\mathsf{CBOW}}(\mathsf{panda} | \mathsf{happy}) $$



### Predictions

Before optimizing our word vectors, we start by getting predictions from our current model.
We have to know how well we are doing before we can start improving.

Predictions are made using the similarities between the context and all possible target words in our vocabulary ($\mathsf{happy}$, $\mathsf{panda}$ and $\mathsf{chair}$).
For each possible target word $j$ get a similarity score $u_{j | i}$ by taking the dot product of its output vector $\mathbf{v'}_{\text{out}}^j$ with the input vector of the context $\mathbf{v}_{\text{in}}^i$:

$$ u_{j | i} = \mathbf{v'}_{\text{out}, j}^T \mathbf{v}_{\text{in}, i}^T $$

We'll get a high score if the vectors of the context and a word are close together.
 Conceptually similar words score high because they're close together. 

Scores are translated into probabilities by taking the soft-max, scaling the scores between 0 and 1:

$$ p(j | i) = \frac{\exp(u_{j | i})}{\sum_V \exp(u_{j | i})} $$

Similar words will result in high probabilities.

The probabilities of the targets $\mathsf{panda}$ and $\mathsf{chair}$ given the the context $\mathsf{happy}$ are given in the titles of the next figure:

<figure>
<p align="center">
<img src="{filename}/images/emoji2vec/worked-example-v-start.png" alt="Drawing" style="width: 600px;"/>
</figure>

The results aren't really good: $\mathsf{panda}$ gets a low probability while it's true label is 1, and $\mathsf{chair}$ gets a high probability while they didn't co-occur.
We clearly have to optimize our matrices so that our word vectors for $\mathsf{happy}$ and $\mathsf{panda}$ move to each other and away from $\mathsf{chair}$.


### Optimization

Optimization is done by backpropogating the errors through the neural networks in two steps.
The output vectors are adjusted using the difference between the probabilities and the labels and then the input vector of the context are adjusted.

New output vectors are computed with:

$$ \mathbf{v'}_{\text{out}, j}^{\mathsf{new}}  = \mathbf{v'}_{\text{out}, j}^{\mathsf{old}} - \eta e_j \mathbf{v}_{\text{in}, i}^T $$

This means that we take the new ougput vectors as the old output vector minus a scaled version of the input vector. 
There are two types of scaling: the learning parameter $\eta$ and the error $e_i$:

$$e_i = p(j |i) - t_i$$

The error moves relevant output vectors towards the input vector and irrelevant output vectors away.
The learning parameter $\eta$ determines how much the system is allowed to learn from one sample.

The new output vectors for a learning rate of $\eta = 1$ are shown in the figure below.
The black dashed line with the star is correction vector that's added to the old output vector.
The new output vectors are in dashed with a circle as marker.

<figure>
<p align="center">
<img src="{filename}/images/emoji2vec/worked-example-v-end.png" alt="Drawing" style="width: 600px;"/>
</figure>

The output vector for target $\mathsf{panda}$ has moved towards the input vector and the vector $\mathsf{chair}$ away from $\mathsf{happy}$, exactly how we wanted them to move!

The next step is to optimize the input vector of context $\mathsf{happy}$ by backpropagating the error further.
The input vector gets updated with:

$$ \mathbf{v}_{\text{in}, j}^{\mathsf{new}}  = \mathbf{v}_{\text{in}, j}^{\mathsf{old}} - \eta \text{EH}^T $$

where an element $i$ of $\text{EH}$ is given by:

$$ \text{EH}_i = \sum_V e_j {w'}_{ij} $$

All output vectors are added to the input vector weighted by their error and scaled by the learning rate.

The right panel in the figure below shows the original and updated output vectors, the left panel shows the original and updated input vectors.
The dotted lines are output vectors scaled by their error and the learning rate.
The new input vector is the result of the old vector plus these scaled output vectors.

<figure>
<p align="center">
<img src="{filename}/images/emoji2vec/worked-example-w-end.png" alt="Drawing" style="width: 600px;"/>
</figure>

The input vector for $\mathsf{happy}$ moved away from the output vector for $\mathsf{chair}$ and towards $\mathsf{pandas}$.
Input vectors $\mathsf{panda}$ and $\mathsf{chair}$ didn't change; input vectors are changed once they're considered the target.

By repeatedly doing predictions and optimizations for different pieces of text, the word vectors will (hopefully) converge to good representations.


## Related

* [Piotr Migdał](http://p.migdal.pl/2017/01/06/king-man-woman-queen-why.html) explains word vectors
* Chris McCormick's [tutorial](http://mccormickml.com/2016/04/19/word2vec-tutorial-the-skip-gram-model/) and [resources](http://mccormickml.com/2016/04/27/word2vec-resources/)
* [word2vec Parameter Learning Explained](https://arxiv.org/abs/1411.2738)
* [A word is worth a thousand vectors](http://multithreaded.stitchfix.com/blog/2015/03/11/word-is-worth-a-thousand-vectors/)
* [Quora thread](https://www.quora.com/How-does-word2vec-work) on how word2vec works
