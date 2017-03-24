"""
    Calls output of pretrained tensorflow model to make prediction of top k genres for user inputed album art
"""

import numpy as np
import tensorflow as tf
import argparse
import sys

def create_graph(modelFullPath):
    """Creates a graph from saved GraphDef file and returns a saver."""
    # Creates graph from saved graph_def.pb.
    with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def run_inference_on_image(imagePath, labelsFullPath, modelFullPath):
    answer = None

    if not tf.gfile.Exists(imagePath):
        tf.logging.fatal('File does not exist %s', imagePath)
        return answer

    image_data = tf.gfile.FastGFile(imagePath, 'rb').read()

    # Creates graph from saved GraphDef.
    create_graph(modelFullPath)

    with tf.Session() as sess:

        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)

        top_k = predictions.argsort()[-5:][::-1]  # Getting top 5 predictions
        f = open(labelsFullPath, 'rb')
        lines = f.readlines()
        labels = np.array([str(w).replace("\n", "") for w in lines])
        for node_id in top_k:
            human_string = labels[node_id]
            score = predictions[node_id]
            print('%s (score = %.5f)' % (human_string, score))

        answer = labels[top_k]
        return answer

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Fit a Text Classifier model and save the results.')
    parser.add_argument('--image', help='A jpg file to make predictions on.')
    parser.add_argument('--labels', help='A txt file with the genre labels, also produced as a tensorflow output.')
    parser.add_argument('--model', help='A pb file with the final layer tensorflow outputs.')
    args = parser.parse_args()

    with open('prediction.out', 'w') as f:
        sys.stdout = f
        run_inference_on_image(args.image, args.labels, args.model)
