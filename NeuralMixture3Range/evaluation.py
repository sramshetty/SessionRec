import numpy as np
import torch
import dataset
from metric import *

class Evaluation(object):
	def __init__(self, model, loss_func, use_cuda, k=20):
		self.model = model
		self.loss_func = loss_func

		self.topk = k
		self.device = torch.device('cuda' if use_cuda else 'cpu')

	def eval(self, eval_data, batch_size):
		self.model.eval()

		losses = []
		recalls = []
		mrrs = []

		dataloader = eval_data

		eval_iter = 0

		def reset_hidden(hidden, mask):
			if len(mask) != 0:
				hidden[:, mask, :] = 0

			return hidden

		with torch.no_grad():
			hidden = self.model.init_hidden()
			total_test_num = []
			for input_idx, input, target, mask in dataloader:
				input = input.to(self.device)
				target = target.to(self.device)

				hidden = reset_hidden(hidden, mask).detach()

				logit, hidden = self.model(input, hidden)
				# print("preds", logit)
				logit_sampled = logit[:, target.view(-1)]
				loss = self.loss_func(logit_sampled)

				# print("input", input, input.size())
				# print("target", target, target.size())

				recall, mrr = evaluate(logit, target, k=self.topk)

				eval_iter += 1

				losses.append(loss.item())
				recalls.append(recall)
				mrrs.append(mrr.item())

				total_test_num.append(target.view(-1).size(0))

		# print("mrrs", mrrs)

		mean_losses = np.mean(losses)
		mean_recall = np.mean(recalls)
		mean_mrr = np.mean(mrrs)

		print("total test num", np.sum(total_test_num))
		# mean_losses = losses/eval_iter
		# mean_recall = recalls/eval_iter
		# mean_mrr = mrrs/eval_iter

		return mean_losses, mean_recall, mean_mrr

