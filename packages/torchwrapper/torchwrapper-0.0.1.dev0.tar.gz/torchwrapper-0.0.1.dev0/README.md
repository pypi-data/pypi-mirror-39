# TorchWrapper

A wrapper class for a PyTorhc Model using fit and predict functions that are
familiar to those who use Keras and Sklearn.

Reduces the need to write fit and evaluation functions for basic models.

## Quick Start

```python
# import the module
from torchwrapper import Wrapper

# create your module, optimizer, and criterion function
model = Model()
optimizer = torch.optim.Adam(model.parameters())
criterion = torch.nn.MSELos()

# wrap the model
model = Wrapper(model)

# train the network
model.fit(dataloader, optimizer, criterion, epochs=50)

```