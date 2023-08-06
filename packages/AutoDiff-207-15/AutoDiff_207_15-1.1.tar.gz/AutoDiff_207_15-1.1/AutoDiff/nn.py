from AutoDiff.ad import DiffObj, Variable
from AutoDiff.ad import MathOps as mo
import numpy as np

class NeuralNet(object):
    def __init__(self, input_dim, hidden_dim, out_dim, lr=0.1):
        self.in_var, self.in_val = self.DeclareVariables('x', (1, input_dim+1))
        self.hid_wt_var, self.hid_wt_val = self.DeclareVariables('w', (hidden_dim, input_dim+1))
        self.hid_function = self.AffineLayer(self.in_var[0].values(), self.hid_wt_var, \
                                             activation=True)
        self.hid_var, self.hid_val = self.DeclareVariables('h', (1, hidden_dim))
        self.out_wt_var, self.out_wt_val = self.DeclareVariables('v', (out_dim, hidden_dim))
        self.out_function = self.AffineLayer(self.hid_var[0].values(), self.out_wt_var)
        self.out_var, self.out_val = self.DeclareVariables('z', (1, out_dim))
        self.out_true_var, self.out_true_val = self.DeclareVariables('y', (out_dim, 1))
        self.loss = self.GetLoss('l2')
        self.lr = lr
    
    @classmethod
    def Sigmoid(cls, x):
        return 1/(1 + mo.exp(-x))
    
    def DeclareVariables(self, base_name, dim):
        var = [{base_name + '_' + str(i+1) + ('_' + str(j+1) if dim[1] > 1 else '') : \
               Variable(base_name + '_' + str(i+1) + ('_' + str(j+1) if dim[1] > 1 else '')) \
               for j in range(dim[1])} for i in range(dim[0])]
        val_dict = [{base_name + '_' + str(i+1) + ('_' + str(j+1) if dim[1] > 1 else '') : np.random.randn()\
               for j in range(dim[1])} for i in range(dim[0])]
        return var, val_dict
    
    def AffineLayer(self, in_obj, wt_var, activation=False):
        layer_out = [None]*len(wt_var)
        for idx, node_wt in enumerate(wt_var):
            layer_out[idx] = sum(a*b for a,b in zip(in_obj, node_wt.values()))
            if activation:
                layer_out[idx] = NeuralNet.Sigmoid(layer_out[idx])
        return layer_out
    
    def UpdateParams(self, wt_val, grad):
        for w, dw in zip(wt_val, grad):
            new_w = np.asarray(list(w.values())) - self.lr*np.asarray(dw)
            w.update(zip(w.keys(), new_w))
    
    def GetLoss(self, loss_fn='l2'):
        loss_obj = None
        if loss_fn == 'l2':
            loss_obj = sum((a - b)**2 for a,b in zip(self.out_true_var[0].values(), \
                                              self.out_var[0].values()))
        return loss_obj
    
    def forward(self, X, y):
        X_with_bias = np.array([1] + list(X))
        self.in_val[0].update(zip(self.in_val[0].keys(), X_with_bias))
        hid_vals = []
        for idx, hid_wt in enumerate(self.hid_wt_val):
            val_dict = {**self.in_val[0], **hid_wt}
            hid_vals += [self.hid_function[idx].get_val(val_dict)]
        self.hid_val[0].update(zip(self.hid_val[0].keys(), hid_vals))
        out_vals = []
        for idx, out_wt in enumerate(self.out_wt_val):
            val_dict = {**self.hid_val[0], **out_wt}
            out_vals += [self.out_function[idx].get_val(val_dict)]
        self.out_val[0].update(zip(self.out_val[0].keys(), out_vals))
        self.out_true_val[0].update(zip(self.out_true_val[0].keys(), [y]))
        val_dict = {**self.out_val[0], **self.out_true_val[0]}
        loss = self.loss.get_val(val_dict)
        return loss, self.out_val[0].values()
        
    def backward(self):
        val_dict = {**self.out_val[0], **self.out_true_val[0]}
        dLdz = self.loss.get_der(val_dict, with_respect_to=self.out_val[0].keys())
        dzdv, dzdh = [], []
        for idx, out_wt in enumerate(self.out_wt_val):
            val_dict = {**self.hid_val[0], **out_wt}
            dzdv += [self.out_function[idx].get_der(val_dict, \
                                                 with_respect_to=out_wt.keys())]
            dzdh += [self.out_function[idx].get_der(val_dict, \
                                                 with_respect_to=self.hid_val[0].keys())]
        dLdv =  [list(dLdz.values())[0]*np.asarray(list(dzdv[0].values()))]
        dLdh =  list(dLdz.values())[0]*np.asarray(list(dzdh[0].values()))[:, np.newaxis]
        dhdw = []
        for idx, hid_wt in enumerate(self.hid_wt_val):
            val_dict = {**self.in_val[0], **hid_wt}
            dhdw += [list(self.hid_function[idx].get_der(val_dict, \
                                                   with_respect_to=hid_wt.keys()).values())]
        dhdw = np.asarray(dhdw)
        dLdw = dLdh*dhdw
        self.UpdateParams(self.out_wt_val, dLdv)
        self.UpdateParams(self.hid_wt_val, dLdw)
