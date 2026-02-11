import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Evaluate recommendation result using Accuracy@K, Precision@K, and AP@K.')
parser.add_argument('ypred', type=str, help='Path to the prediction file.')
parser.add_argument('ytrue', type=str, help='Path to the ground truth file.')
parser.add_argument('--k', type=int,
                    help='the number of epochs to train', default=10)
parser.add_argument('--output_path', type=str,
                    help='path to output file.', default="result.csv")
args = parser.parse_args()

def read_input_file(filepath):
    """ Read input file for evaluation

    Args:
    ---
    - `filepath`: str
        Path to input file.
    
    Return:
    List[List[str]]
        The list of samples to evaluate.
    """
    res = []
    with open(filepath, 'r') as infile:
        for line in infile.readlines():
            line = line.split(",")[1:args.k+1]
            res.append(line)
    return res

if __name__ == "__main__":
    pred = read_input_file(args.ypred)
    true = read_input_file(args.ytrue)

    result = []

    accuracy, precision, average_precision = 0, 0, 0

    for (y_pred, y_true) in zip(pred, true):
        # count relevant recommendations
        rec = [1 if a in y_true else 0 for a in y_pred]
        # calculate accuracy at every level until k
        acc_k = [sum(rec[:i+1])/args.k for i in range(args.k)]
        # calculate precision at every level until k
        pre_k = [sum(rec[:i+1])/(i+1) for i in range(args.k)]
        # calculate average precision at k
        ap_k = sum([pre_k[i] * rec[i] for i in range(args.k)]) / min(args.k, len(y_true))

        accuracy += acc_k[-1]
        precision += pre_k[-1]
        average_precision += ap_k

    accuracy /= len(pred)
    precision /= len(pred)
    average_precision /= len(pred)

    df = pd.DataFrame({
        f"accuracy@{args.k}": [accuracy],
        f"precision@{args.k}": [precision],
        f"ap@{args.k}": [average_precision],
    })

    # save result to a csv file
    df.to_csv(args.output_path, index=False)