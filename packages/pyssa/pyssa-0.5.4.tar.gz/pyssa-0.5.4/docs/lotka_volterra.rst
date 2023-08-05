==============
Model Building
==============


A predator prey system can be modeled by the Lotka Volterra system of differential equations:

.. math::

    \frac{dx}{dt} = \alpha x - \beta xy \\
    \frac{dy}{dt} = \delta xy - \gamma y

Here x represents the predator population and y represents the prey population. The corresponding 'chemical' equations are given by :

.. math::

    x \rightarrow x+1, y \rightarrow y : \alpha x \\
    x \rightarrow x-1, y \rightarrow y : \beta xy \\
    x \rightarrow x, y \rightarrow y+1 : \gamma xy \\
    x \rightarrow x, y \rightarrow y-1 : \delta y \\

Suppose we have

..math:: \alpha = 2/3,

\beta = 4/3, \gamma = 1 and \delta = 1. Then the model is built with the following lines::

    alpha, beta, gamma, delta = 2/3, 4/3, 1, 1
    V_r =


