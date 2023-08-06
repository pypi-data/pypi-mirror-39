import tensorflow as tf
import numpy as np
from . import predutil
from aquests.lib.termcolor import tc
        
class Result:
    train_dir = None
    labels = None
    _accfunc = None
    _summaryfunc = None        
            
    def __init__ (self, x, y, is_validating, logit, cost, acc, epoch, ops = None, args = None):
        self.x = x
        self.y = y
        self.logit = logit
        self.cost = cost        
        self.accuracy = acc
        if acc is not None and self._accfunc: # no run within batch steps
            self.accuracy = self._accfunc (self)
        self.epoch = epoch
        self.is_validating = is_validating
        self.is_cherry = False
               
        self.ops = ops
        self.args = args
        
    def __make_summary (self, d):
        d  ["eval/cost"] = self.cost
        if isinstance (self.accuracy, (tuple, list)):
            if not self.labels:
                for i, acc in enumerate (self.accuracy [:-1]):
                    d ["eval/acc/{}".format (i + 1)] = acc                                        
            else:
                for i in range (len (self.accuracy) - 1):
                    label = self.labels [i]
                    d ["eval/acc/" + label.name] = self.accuracy [i]
            d ["eval/acc/average"] = self.accuracy [-1]                    
        else:
            d ["eval/acc"] = self.accuracy
        d ["epoch"] = self.epoch    
        return d
        
    @property
    def phase (self):
        return self.is_cherry and "saved" or (self.is_validating  and 'resub' or 'valid')
    
    def pipe (self):
        self._summaryfunc (self.phase, self.__make_summary (self.args.get ("summary", {})), True)
        return self
    update = pipe
    
    # statistics helper methods -----------------------------------------    
    def confusion_matrix (self, num_label = 0, label_index = 0, indent = 0, show_label = True):
        if num_label <= 0:
            if not self.labels:
                raise ValueError ("num_label required")
            num_label = len (self.labels [label_index])
            
        mat_ = predutil.confusion_matrix (
            np.argmax (self.logit [:, :num_label], 1), 
            np.argmax (self.y [:, :num_label], 1),
            num_label
        )
        
        mat = str (mat_) [1:-1]
        
        if show_label and self.labels: 
            cur_label = self.labels [label_index]
        
            first_row_length = len (mat.split ("\n", 1) [0]) - 2
            label_width = (first_row_length - 1) // mat_.shape [-1]        
            print (tc.info ((" " * indent) + "[" + " ".join ([str (each) [:label_width].rjust (label_width) for each in cur_label.items ()]) + "]"))
        
        if not indent:
            mat = mat.replace ("\n ", "\n")
        else:    
            mat = (" " * indent) + mat.replace ("\n", "\n" + (" " * (indent - 1)))
        return mat

    def logit_range (self):
        output_range = [self.logit.min (), self.logit.max (), np.mean (self.logit), np.std (self.logit)]
        quant_range = {}
        for idx, m in enumerate (self.logit [:,:29].argsort (1)[:,-2]):
            sec = int (self.logit [idx, m])
            try: quant_range [sec] += 1
            except KeyError: quant_range [sec] = 1
        quant_range = quant_range
        if quant_range:           
            stats = sorted (quant_range.items ())
            # output range for top1: {} ~ {}, logit range: {:.3f} ~ {:.3f}, mean: {:.3f} std: {:.3f}
            return stats [0][0] - 1, stats [-1][0] + 1, output_range [0], output_range [1], output_range [2], output_range [3]                                
        
    def confidence_level (self, label_index = 0):
        label = self.labels [label_index]
        stat = {}
        for idx in range (len (self.y)):
            logit = self.logit [idx][:len (label)]
            y = self.y [idx][:len (label)]
            probs = predutil.softmax (logit)
            prob = "{:.5f}".format (probs [np.argmax (probs)])
            if prob not in stat:
                stat [prob] = [0, 0]
            if np.argmax (probs) == np.argmax (y):    
                stat [prob][0] += 1
            stat [prob][1] += 1
            
        ordered = [] 
        accum = 0        
        accum_t = 0
        total = len (self.y)
        for lev, (c, t) in sorted (stat.items (), reverse = True):            
            accum += c            
            accum_t += t
            accuracy = accum / accum_t * 100
            ordered.append ((
                lev, 
                accum, accum_t, accuracy, 
                accum / total * 100 
            ))
            if len (ordered) >= 10 and accuracy < 100.:
                break
        return ordered    
    
