import xanity
import matplotlib.pyplot as plt

xanity.associated_experiments([
        'experiment1',
        #'experiment2',
        'experiment3',
        ])

def main(data_dir):
    
    data, paths = xanity.load_variable('fakevar')

    plt.figure()
    for d in data:
        plt.hist(d)
    
    plt.show()
    
if __name__=='__main__':
    xanity.run_hook()