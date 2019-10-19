import threading
import time

from keras_bert import load_trained_model_from_checkpoint

from solvers import tokenization


class PunctuationBert(threading.Thread):

    def __init__(self, model_path):
        threading.Thread.__init__(self)
        self.model = None

        self.model_path = model_path

        self.state = "busy"  # ready / waiting / busy
        self.input = None
        self.output = None

    def run(self):

        self.load()

        self.state = "ready"
        while self.input != -1:
            if self.input is not None and self.state == "ready":
                self.state = "busy"
                self.predict(self.input)
                self.input = None

            if self.state == "waiting" and self.output is None:
                self.state = "ready"

            if self.state == "ready":
                time.sleep(0.1)

    def load(self):
        config_path = self.model_path + '/bert_config.json'
        checkpoint_path = self.model_path + '/model.ckpt-35000'
        vocab_path = self.model_path + '/vocab.txt'

        self.tokenizer = tokenization.FullTokenizer(vocab_file=vocab_path, do_lower_case=False)
        self.model = load_trained_model_from_checkpoint(config_path, checkpoint_path, training=True)

    def predict(self, input: list):
        self.output = self.model.predict(input)
        self.state = "waiting"
