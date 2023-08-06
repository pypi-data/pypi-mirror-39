from Dotua.rautodiff import rAutoDiff as rad
from Dotua.roperator import rOperator as op
import random

ad = rad()

class NeuralNetwork():
	def __init__(self, input_vals, input_bias, hidden_bias, num_hidden, output, learning_rate = 0.1):
		self.input_vals = input_vals
		self.input_bias = input_bias
		self.hidden_bias = hidden_bias
		self.num_hidden = num_hidden
		self.output = output
		self.learning_rate = learning_rate

		# To initialize the weights from input layer to hidden layer
		self.weights_tohidden = [None] * num_hidden
		for i in range(num_hidden):
			self.weights_tohidden[i] = []
			for j in range(len(input_vals)):
				w = ad.create_rscalar(random.random())
				self.weights_tohidden[i].append(w)

		# To initialize the weights from hidden layer to output layer
		self.weights_tooutput = [None] * len(output)
		for i in range(len(output)):
			self.weights_tooutput[i] = []
			w = ad.create_rscalar(random.random())
			for j in range(num_hidden):
				self.weights_tooutput[i].append(w)

	def train(self, input_vals, output_vals):
		self.input_vals = input_vals
		self.output = output_vals

		# To calculate the hidden layer neurons
		self.hidden_layer = []
		for i in range(self.num_hidden):
			h = 0
			for j in range(len(self.weights_tohidden[i])):
				h = h + self.weights_tohidden[i][j] * self.input_vals[j]
			h = h + self.input_bias
			self.hidden_layer.append(1/(1+op.exp(-h)))

		# To calculate the output layer neurons and error
		error = 0
		for i in range(len(self.output)):
			o = 0
			for j in range(len(self.weights_tooutput[i])):
				o = o + self.weights_tooutput[i][j] * self.hidden_layer[j]
			o = o + self.hidden_bias
			o = 1/(1+op.exp(-o))
			error = error + (o - self.output[i]) ** 2

		# To update weights from hidden layer to output layer
		for i in range(len(self.weights_tooutput)):
			for j in range(len(self.weights_tooutput[i])):
				d = ad.partial(error, self.weights_tooutput[i][j])
				self.weights_tooutput[i][j] = self.weights_tooutput[i][j] - d * self.learning_rate

		# To update weights from input layer to hidden layer
		for i in range(len(self.weights_tohidden)):
			for j in range(len(self.weights_tooutput[i])):
				d = ad.partial(error, self.weights_tohidden[i][j])
				self.weights_tohidden[i][j] = self.weights_tohidden[i][j] - d * self.learning_rate

	def predict(self, input_vals, output_vals):
		self.input_vals = input_vals
		self.output = output_vals

		# To calculate the hidden layer neurons using the current model
		self.hidden_layer = []
		for i in range(self.num_hidden):
			h = 0
			for j in range(len(self.weights_tohidden[i])):
				h = h + self.weights_tohidden[i][j] * self.input_vals[j]
			h = h + self.input_bias
			self.hidden_layer.append(1/(1+op.exp(-h)))

		# To calculate the output layer neurons using the current model and calculate the error
		error = 0
		output_layer = []
		for i in range(len(self.output)):
			o = 0
			for j in range(len(self.weights_tooutput[i])):
				o = o + self.weights_tooutput[i][j] * self.hidden_layer[j]
			o = o + self.hidden_bias
			o = 1/(1+op.exp(-o))
			output_layer.append(o.val)
			error = error + (o - self.output[i]) ** 2
		error = error / len(self.output)
		return (output_layer, error.val)

nn = NeuralNetwork([0.05,0.1],0.35,0.6,2,[0.01,0.09])
for i in range(100):
	nn.train([0.05,0.1],[0.01,0.09])
output, e = nn.predict([0.05,0.1],[0.01,0.09])
print('Final prediction given by the Neural Network is ', output)
print('The mean squared error is ', e)