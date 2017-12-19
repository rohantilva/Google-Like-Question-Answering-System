from preprocess import Preprocess


def test_build_dataset(datapath, pickle_name):
    p = Preprocess()
    p.process_dataset(datapath, pickle_name)


def main():
    test_build_dataset("../data/WikiQA/WikiQA-train.tsv.gz", "processed_train")


if __name__ == '__main__':
    main()