import sys, os
from collections import OrderedDict
import csv

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from helpers import *
from gen_artifacts_lib import *

# Current experiment files
from deep_learning import *


def case_study_2(output_dir):
    logging.info("Starting Experiment 2")

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
    plot_bdc(output_dir + "/cs-2-stages", hws[0].stages, eval_results, 2)
    plot_category_bdc(output_dir + "/cs-2-cats", hws[0].get_categories(), category_results)
    plot_category_bdc_bars(output_dir + "/cs-2-cats-bars", hws[0].get_categories(), category_results, 2)


def case_study_3(output_dir):
    logging.info("Starting Experiment 3")

    # Select hardware designs
    hws = [ TPU(),
            Tesla_NNA(),
            VTA(),
            #Eisenhower_Accel(),
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
    plot_bdc(output_dir + "/cs-3-stages", hws[0].stages, eval_results, 3)
    plot_category_bdc(output_dir + "/cs-3-cats", hws[0].get_categories(), category_results)
    plot_category_bdc_bars(output_dir + "/cs-3-cats-bars", hws[0].get_categories(), category_results, 3)



def process_user_study(user_study_input, output_dir):

    filename = user_study_input

    score_map = {"Strongly Agree".lower(): 5,
                 "Agree".lower(): 4, "Strong Agree".lower(): 1,
                 "Neutral".lower(): 3, "Netural".lower(): 3,
                 "Disagree".lower(): 2,
                 "Strongly Disagree".lower(): 1,
                 "l": 99}

    dataset = []

    with open(filename) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')

        # skip header
        next(readCSV)

        col = 4
        for row in readCSV:
            # print (row)
            row_score = []
            for cell in row[col:]:
                if cell is not '' and cell.lower() in score_map:
                    row_score.append(score_map[cell.lower()])
                # else:
                #     row_score.append("-")

            dataset.append(row_score)

    print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in dataset]))

    # Flip any negative questions
    # Remember to subtract initial questions
    flipped = [3]
    for participant in dataset:
        for f in flipped:
            participant[f] =  ((participant[f] - 3) * (-1)) + 3

    # Each row in dataset corresponds to a participant.
    ####
    print (dataset)

    #plot_user_study_bw(output_dir + "/us-box-whisker", dataset)
    plot_user_study_sb(output_dir + "/us-stack-bar", dataset)



if __name__ == "__main__":
    
    output_dir = os.path.dirname(os.path.abspath(__file__)) + "/output"
    logfile = output_dir + "/paper_artifacts"
    setup_logging(logfile)


    # Print the Deep Learning Feature Tree Template
    dl_ftt = DeepLearning_FT_Template()
    logging.info (dl_ftt.to_stdout() + "\n")

    gen_latex_table(dl_ftt, output_dir + "/util-table.tex")

    case_study_2(output_dir)
    case_study_3(output_dir)

    user_study_input = os.path.dirname(os.path.abspath(__file__)) + "/user_study_results.csv"
    process_user_study(user_study_input, output_dir)
    
