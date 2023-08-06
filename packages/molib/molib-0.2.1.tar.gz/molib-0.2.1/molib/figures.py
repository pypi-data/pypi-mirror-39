from pathlib import Path
import matplotlib.pyplot as plt

def add_subfig_label(ax, label, size=14):
	''' Adds a subplot label to an axis.'''
	ax.text(-0.1, 1, label, transform=ax.transAxes,
      fontsize=size, fontweight='bold', va='top', ha='right')
	return ax

def gen_sub_label(lower=False, paren=False):
	'''Generates the next letter in the alphabet as a subfig label.
	   Label can be uppercase or lowercase, with optional parentheses.
	'''
	letters = 'A B C D E F G H I J K L M N O P Q R S T U V W X Y Z'
	labels = letters.lower().split(' ') if lower else letters.split(' ')
	for letter in labels:
		yield '('+letter+')' if paren else letter

def label_subplots(fig, size=14):
	'''Adds letter labels to all subplots in a figure.
	   Adjusts figure padding and left margin to make labels fit.
	'''
	allaxes = fig.get_axes()
	sub_labels = gen_sub_label(paren=True)
	for ax in allaxes:
		add_subfig_label(ax, next(sub_labels), size=size)
	# plt.tight_layout(rect=[l_mar,0,1,1], w_pad=w_pad)

def save_plot(output_filename, proj_dir=Path.cwd(), subdir=None, fig=None):
    ''' Function for saving plots and printing message.'''
    # make directory for plots, and save plot
    plots_dir = proj_dir/'plots'
    if subdir:
        plots_dir = plots_dir / str(subdir)
    plots_dir.mkdir(parents=True, exist_ok=True)
    output_file_path = plots_dir / (output_filename + '.png')
    if fig:
        fig.savefig(str(output_file_path), dpi=300)
    else:
        plt.savefig(str(output_file_path), dpi=300)
    print('Created plot: ' + str(output_file_path))
    plt.close()
