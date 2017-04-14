from flask import Flask, render_template, request
from werkzeug import secure_filename
import sys
import web_plot_prediction as wp
import web_predict as p

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    print "in index"
    return render_template('index.html')

@app.route('/more-artwork', methods = ['GET'])
def more():
    print "in more"
    return render_template('more-artwork.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    print 'in upload file'
    if request.method == 'POST':
        print 'these are your request files: ', request.files
        f = request.files['pic']
        print 'this is f:', f
        img_name = secure_filename(f.filename)
        photo_name = 'tmp/' + img_name
        photo = 'static/'+photo_name

        f.save(photo)
        #plot_name = photo_name[:-4]+'_plot'
        #plot = 'app/static/'+plot_name
        #print "\n plot will be saved to", plot

        #result = wp.primary(photo, session, tensor)
        #img_name_sin_ext = photo_name.split('.')[0]
        img_name_sin_ext = img_name.split('.')[0]
        img_path = 'static/tmp/{}'.format(img_name)
        labels_path = 'model/output_labels.txt'
        model_path = 'model/output_graph.pb'

        output_name = 'static/tmp/prediction{}.out'.format(img_name_sin_ext)
        with open(output_name, 'w') as f:
            sys.stdout = f
            p.run_inference_on_image(img_path, labels_path, model_path)

        top_prediction, results = wp.get_results(output_name)
        plot_name = 'static/tmp/{}_plt'.format(img_name_sin_ext)
        #print 'PLOT NAME: ', plot_name
        plt_name = photo_name[:-4]+'_plt'
        wp.plot_pred(top_prediction, results, save_as= plot_name)


        return render_template('results.html', photo= photo_name, plot= plt_name+'.png')

# set session and tensor globally to save overhead
#session, tensor = wp.setup()


@app.route('/predict', methods=['POST'])
def predict():
    """Recieve the image to be classified, use the model to classify, and
    then return the top 5 predictions
    """
    return " ".join(lines)


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=8081, debug=True)
