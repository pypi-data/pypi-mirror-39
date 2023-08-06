import xanity
import numpy as np

xanity.analyze_this()

# register parameters
xanity.experiment_parameters({
    'n_trials': [100,150,200],
    'train_frac': [0.9, 0.5, 0.1],
    'scale': [1,2,3,]
})

def main(
        n_trials=200,
        scale =5,
        train_frac=0.8,
        ):
    
    """ do experiment 1 """
    
    fakevar = scale * np.random.rand(n_trials)**2
    xanity.log("here is a print from experiment 1")
    xanity.save_variable(fakevar)

if __name__=='__main__':
    xanity.run_hook()