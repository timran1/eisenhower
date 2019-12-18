from helpers import *
from plot import *
from illustrator import *
from collections import OrderedDict

# Current experiment files
from spiking_nn import *


def experiment_1(output_dir):
    logging.info("Starting Experiment 1")

    # Select hardware designs
    hws = [ CPU(),
            Intel_Xeon_Skylake_CPU(),
            Loihi()]

    eval_results = OrderedDict()
    category_results = OrderedDict()

    for hw in hws:
        # Evaluate BDC
        hw.eval()
        logging.info (hw.to_stdout() + "\n\n")

        eval_results[hw.name] = hw.get_bdc()
        category_results[hw.name] = hw.get_category_bdc()

    # Plot results
    plot_experiment(output_dir + "/exp-1", hws[0].stages, eval_results,
                                            hws[0].get_categories(), category_results)

if __name__ == "__main__":
    output_dir = os.path.dirname(os.path.abspath(__file__)) + "/output"
    logfile = output_dir + "/main"
    setup_logging(logfile)


    # Print the Spiking Neural Nework Feature Tree Template
    snn_ftt = SpikingNN_FT_Template()
    logging.info (snn_ftt.to_stdout() + "\n")
    gen_markdown_readme(snn_ftt, get_class_dir(snn_ftt))

    experiment_1(output_dir)
