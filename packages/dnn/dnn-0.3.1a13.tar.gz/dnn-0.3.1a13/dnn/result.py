import tensorflow as tf
import numpy as np
from . import predutil
from aquests.lib.termcolor import tc
        
class Result:
    train_dir = None
    labels = None
    name = None
    _accfunc = None
    _summaryfunc = None        
            
    def __init__ (self, x, y, is_validating, logit, cost, acc, epoch, ops = None, args = None):
        self.xs = self.x = x
        self.ys = self.y = y
        self.logits = self.logit = logit
        self.cost = cost        
        self.accuracy = acc
        self.epoch = epoch
        self.is_validating = is_validating
        self.ops = ops
        self.args = args
        
        # set by trainer
        self.is_cherry = False
        self.on_ftest = False
        self.is_overfit = False
        self.is_improved = False
        
        if acc is not None and self._accfunc: # no run within batch steps
            self.accuracy = self._accfunc (self)
        
    def __make_summary (self, d = {}):
        d  ["eval/cost"] = self.cost
        if isinstance (self.accuracy, (tuple, list)):
            if not self.labels:
                for i, acc in enumerate (self.accuracy [:-1]):
                    d ["eval/acc/{}".format (i + 1)] = acc                                        
            else:
                for i in range (len (self.accuracy) - 1):
                    label = self.labels [i]
                    d ["eval/acc/" + label.name] = self.accuracy [i]
            d ["eval/acc/avg"] = self.accuracy [-1]                    
        elif self.accuracy:
            d ["eval/acc"] = self.accuracy
        
        d_ = {}
        for k, v in d.items ():
            if self.name:
                k = "{}:{}".format (self.name, k)
            if isinstance (v, (list, tuple)):
                if len (v) == 1: v = v [0]
                else: raise ValueError ("Required float, int or an array contains only one of them")
            d_ [k] = v        
        return d_
    
    def __get_phase_summary (self, kargs):
        output = []
        for k, v in self.__make_summary (kargs).items ():                            
            if isinstance (v, (float, np.float64, np.float32)):
                output.append ("{} {:.5f}".format (k, v))
            elif isinstance (v, (int, np.int64, np.int32)):
                output.append ("{} {:04d}".format (k, v))
            else:
                raise ValueError ("Required float, int type")
        output.sort ()
        
        if self.on_ftest:
            return " | ".join (output)            
        if self.phase != "saved":
            if self.is_overfit:
                output.append (tc.error ("overfitted"))
            if self.is_improved:
                output.append (tc.info ("improved"))
        return " | ".join (output)
            
    @property
    def phase (self):
        if self.on_ftest:
            return "final"
        elif self.is_cherry:
            return "saved"            
        return self.is_validating  and 'resub' or 'valid'
    
    def summary (self):
        self._summaryfunc (self.phase, self.__make_summary (self.args.get ("summary", {})))
        return self    
    
    # statistics helper methods -----------------------------------------    
    def log (self, msg = None, **kargs):
        coloring = False
        if not msg:
            msg = self.__get_phase_summary (kargs)
            coloring = True
        phase = self.phase
        if phase == "final":
            header = "[fin.:ftest]"
            color = tc.fail              
        else:    
            header = "[{:04d}:{}]".format (self.epoch, self.phase)                                  
            color = phase == "saved" and tc.warn or tc.debug                   
        print ("{} {}".format ((coloring and color or tc.critical) (header), msg))
        return self
    
    def get_confusion_matrix (self, num_label = 0, label_index = 0):
        if num_label <= 0:
            if not self.labels:
                raise ValueError ("num_label required")
            num_label = len (self.labels [label_index])
            
        mat_ = predutil.confusion_matrix (
            np.argmax (self.logit [:, :num_label], 1), 
            np.argmax (self.y [:, :num_label], 1),
            num_label
        )
        return mat_
            
    def confusion_matrix (self, num_label = 0, label_index = 0, indent = 13, show_label = True):
        mat_ = self.get_confusion_matrix (num_label, label_index)        
        mat = str (mat_) [1:-1]
        self.log ("confusion matrix")
        if show_label and self.labels: 
            cur_label = self.labels [label_index]
            first_row_length = len (mat.split ("\n", 1) [0]) - 2
            label_width = (first_row_length - 1) // mat_.shape [-1]        
            print (tc.info ((" " * indent) + "[" + " ".join ([str (each) [:label_width].rjust (label_width) for each in cur_label.items ()]) + "]"))        
        if not indent:
            mat = mat.replace ("\n ", "\n")
        else:    
            mat = (" " * indent) + mat.replace ("\n", "\n" + (" " * (indent - 1)))
        print (mat)
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
    
