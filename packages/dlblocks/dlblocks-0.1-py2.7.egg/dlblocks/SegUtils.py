import numpy as np

# https://github.com/wkentaro/pytorch-fcn/blob/master/torchfcn/utils.py

def _fast_hist(label_true, label_pred, n_class):
    mask = (label_true >= 0) & (label_true < n_class)
    hist = np.bincount(
        n_class * label_true[mask].astype(int) +
        label_pred[mask], minlength=n_class**2).reshape(n_class, n_class)
    return hist


def label_accuracy_score(label_trues, label_preds, n_class):
    """Returns accuracy score evaluation result.
      - overall accuracy
      - mean accuracy
      - mean IU
      - fwavacc
      - label_trues, label_preds both ( batch , w , h ) or ( batch , ch , w , h )
    """

    if len(label_preds.shape) == 4:
    	label_preds = np.argmax( label_preds , axis=1 )

    if len(label_trues.shape) == 4:
    	label_trues = np.argmax( label_trues , axis=1 )

    hist = np.zeros((n_class, n_class))
    for lt, lp in zip(label_trues, label_preds):
        hist += _fast_hist(lt.flatten(), lp.flatten(), n_class)
    acc = np.diag(hist).sum() / hist.sum()
    acc_cls = np.diag(hist) / hist.sum(axis=1)
    acc_cls = np.nanmean(acc_cls)
    iu = np.diag(hist) / (hist.sum(axis=1) + hist.sum(axis=0) - np.diag(hist))
    mean_iu = np.nanmean(iu)
    freq = hist.sum(axis=1) / hist.sum()
    fwavacc = (freq[freq > 0] * iu[freq > 0]).sum()
    return { "acc":acc , "acc_cls":acc_cls, "mean_iu":mean_iu, "fwavacc":fwavacc }

def get_label_accuracy_score_fn( n_class ):
	def fn( label_trues, label_preds):
		return label_accuracy_score(label_trues, label_preds, n_class)
	return fn