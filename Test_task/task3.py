import sys
import numpy as np
import pandas as pd

HEAD = "H"
TAIL = "T"

# Probabilities to obtain head for each coin to be chosen
HEAD_PROBS = {"m1": 0.1, "m2": 0.2, "m3": 0.4, "m4": 0.8, "m5": 0.9}


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python task3.py observations.txt")

    # Load observations array from text file
    try:
        observations = load_data(sys.argv[1])
    except FileNotFoundError:
        sys.exit(f"Error! There is no such file '{sys.argv[1]}'.")
    except ValueError as e:
        sys.exit(f"Error! {e}.")

    # Probability distributions for head and tail for each coin to be chosen
    coin = pd.DataFrame()
    coin[HEAD] = HEAD_PROBS
    coin[TAIL] = 1 - coin[HEAD]  # Each probability of tail equals 1 - [probability of head]

    # Prior probabilities to choose a certain coin is equal for all coins
    choose = pd.Series({c: 1 for c in HEAD_PROBS.keys()})
    choose = normalize(choose)  # Each prior probability equals 1 / [number of coins]

    heads = []  # Contains probabilies to obtain head in next observation
    for observation in observations:

        # Calculate posterior probabilities using Bayes' theorem and update prior probabilities
        choose = normalize(choose * coin[observation])

        # Calculate new probability to obtain head based on previous observations (law of total probability)
        h = np.sum(choose * coin[HEAD])
        heads.append(round(h, 2))  # Probability is rounded to 2 decimal digits

    print(
        f"For {len(observations)} sequensive coin tosses "
        f"probabilities to obtain head ('{HEAD}') in next observation: {heads}."
    )


def load_data(filename):
    """
    Loads observations data from the text file `filename`.

    Returns a NumPy `ndarray` which contains all observations as strings.
    """

    # Use built-in NumPy function to load the array with string type
    data = np.loadtxt(filename, dtype=str)

    if data.ndim != 1:
        raise ValueError("All observations must be placed in one row")
    if not np.all((data == HEAD)^(data == TAIL)):
        raise ValueError(f"All observations must be heads ('{HEAD}') or tails ('{TAIL}')")

    return data


def normalize(probabilities):
    """
    Normalizes the probability distribution `probabilities`
    (Pandas `Series`) such that all probabilities sum to 1.

    Returns a normalized probability distribution as Pandas `Series`.
    """

    # Normalize by dividing probabilities by their sum
    return probabilities / np.sum(probabilities)


if __name__ == "__main__":
    main()
