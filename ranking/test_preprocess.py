from preprocess import Preprocess


def build_dataset(datapath, pickle_name):
    p = Preprocess()
    p.process_dataset(datapath, pickle_name)


def main():
    build_dataset("../data/WikiQA/WikiQA-train.tsv.gz", "processed_train")
    build_dataset("../data/WikiQA/WikiQA-dev.tsv.gz", "processed_dev")
    build_dataset("../data/WikiQA/WikiQA-test.tsv.gz", "processed_test")

if __name__ == '__main__':
    main()