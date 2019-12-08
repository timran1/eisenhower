from helpers import *
from plot import *
from illustrator import *
from collections import OrderedDict

# Current experiment files
from deep_learning import *


def experiment_1(output_dir):
    logging.info("Starting Experiment 1")

    # Select hardware designs
    hws = [ CPU(),
            Intel_Xeon_Skylake_CPU(),
            NVIDIA_Fermi_GPU(),
            NVIDIA_Turing_GPU()]

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

def experiment_2(output_dir):
    logging.info("Starting Experiment 2")

    # Select hardware designs
    hws = [ TPU(),
            Tesla_NNA(),
            VTA(),
            #Ada_Accel(),
            Simba(),
            Intel_SpringHill()]

    eval_results = OrderedDict()
    category_results = OrderedDict()

    for hw in hws:
        # Evaluate BDC
        hw.eval()
        logging.info (hw.to_stdout() + "\n\n")

        eval_results[hw.name] = hw.get_bdc()
        category_results[hw.name] = hw.get_category_bdc()

    # Plot results
    plot_experiment(output_dir + "/exp-2", hws[0].stages, eval_results,
                                            hws[0].get_categories(), category_results)


if __name__ == "__main__":
    output_dir = os.path.dirname(os.path.abspath(__file__)) + "/output"
    logfile = output_dir + "/illustrate"
    setup_logging(logfile)


    # Print the Deep Learning Feature Tree Template
    dl_ftt = DeepLearning_FT_Template()
    logging.info (dl_ftt.to_stdout() + "\n")
    gen_markdown_readme(dl_ftt, get_class_dir(dl_ftt))

    experiment_1(output_dir)
    experiment_2(output_dir)
