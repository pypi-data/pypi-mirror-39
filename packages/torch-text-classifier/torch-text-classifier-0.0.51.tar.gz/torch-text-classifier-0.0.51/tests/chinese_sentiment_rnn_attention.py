import os
import pickle
import tempfile
import uuid
from collections import Counter

from sklearn.model_selection import train_test_split
from torch_text_classifier import TextClassifier
from torch_text_classifier.utils import json_reader


def main():
    print('read data')
    x_data, y_data = json_reader('/tmp/chinese_sentiment.json')
    x_train, x_val, y_train, y_val = train_test_split(
        x_data, y_data, test_size=0.2, random_state=222)
    x_val, x_test, y_val, y_test = train_test_split(
        x_val, y_val, test_size=0.5, random_state=222)

    tag_best_path = os.path.join(tempfile.gettempdir(),
                                 str(uuid.uuid4()) + '.pkl')

    print('train', Counter(y_train))
    print('test', Counter(y_test))
    print('build model')
    tc = TextClassifier(
        verbose=1,
        device='auto',
        batch_size=32,
        epochs=200,
        embedding_dropout_p=0.1,
        encoder_dropout_p=0.1,
        encoder='rnn_attention',
        optimizer='adam')
    print('fit model')
    tc.fit(
        x_train,
        y_train,
        x_val,
        y_val,
        patient_dev=20,
        save_best=tag_best_path)

    tc = pickle.load(open(tag_best_path, 'rb'))
    print(tc.score(x_test, y_test, detail=True))


if __name__ == '__main__':
    main()
