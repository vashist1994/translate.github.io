import keras as k
from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS,cross_origin
import logging as logger
# from model import NMT
from keras.models import Model,load_model
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.layers import LSTM, Input, Dense,Embedding
import pickle as pkl
import numpy as np
from keras.models import model_from_json
logger.basicConfig(level="DEBUG")

app = Flask(__name__)
logger.debug("flask instane is created")
api = Api(app)
logger.debug("API instance is created")
cors = CORS(app, resources={r"/*": {"origins": "*"}})
logger.debug("Cores it recure")

with open('tokenizer_input.pkl','rb') as f:
    tokenizer_input = pkl.load(f)
print("loaded the input toknizer")
with open('tokenizer_target.pkl','rb') as f:
    tokenizer_target = pkl.load(f)

class Translate(Resource):
    def get(self,sentance):
        # logger.debug("Model loading started")
        json_file = open('model_2.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        model = model_from_json(loaded_model_json)
        # load weights into new model
        model.load_weights("model_weight_5.h5")
        # logger.debug("Model loading done")
        # logger.debug("inside the get function")
        # print("sentance reached at NMT",sentance)
        # with open('tokenizer_input.pkl','rb') as f:
        #     tokenizer_input = pkl.load(f)
        # print("loaded the input toknizer")
        # with open('tokenizer_target.pkl','rb') as f:
        #     tokenizer_target = pkl.load(f)

        reverse_word_map_input = dict(map(reversed, tokenizer_input.word_index.items()))
        reverse_word_map_target = dict(map(reversed, tokenizer_target.word_index.items()))

        latent_dim = 50
        #inference encoder
        encoder_inputs_inf = model.input[0] #Trained encoder input layer
        encoder_outputs_inf, inf_state_h, inf_state_c = model.layers[4].output # retoring the encoder lstm output and states
        encoder_inf_states = [inf_state_h,inf_state_c]
        encoder = Model(encoder_inputs_inf,encoder_inf_states)
        print("encoder is loaded")

        #inference decoder
        # The following tensor will store the state of the previous timestep in the "starting the encoder final time step"
        decoder_state_h_input = Input(shape=(latent_dim,)) #becase during training we have set the lstm unit to be of 50
        decoder_state_c_input = Input(shape=(latent_dim,))
        decoder_state_input = [decoder_state_h_input,decoder_state_c_input]

        # # inference decoder input
        decoder_input_inf = model.input[1] #Trained decoder input layer
        # decoder_input_inf._name='decoder_input'
        decoder_emb_inf = model.layers[3](decoder_input_inf)
        decoder_lstm_inf = model.layers[5]
        decoder_output_inf, decoder_state_h_inf, decoder_state_c_inf = decoder_lstm_inf(decoder_emb_inf, initial_state =decoder_state_input)
        decoder_state_inf = [decoder_state_h_inf,decoder_state_c_inf]
        #inference dense layer
        dense_inf = model.layers[6]
        decoder_output_final = dense_inf(decoder_output_inf)# A dense softmax layer to generate prob dist. over the target vocabulary

        decoder = Model([decoder_input_inf]+decoder_state_input,[decoder_output_final]+decoder_state_inf)

        print("decoder is loaded")
        input_seq = tokenizer_input.texts_to_sequences([sentance])
        input_seq = pad_sequences(input_seq,maxlen=20, padding='post')
        # print("input_seq in sequence form=>",input_seq)
        state_values_encoder = encoder.predict(input_seq)
        # print("state_value: ",state_values_encoder)
        # intialize the target seq with start tag
        target_seq = np.zeros((1,1))
        target_seq[0, 0] = tokenizer_target.word_index['start']
        # print("target_seq in sequence form:=>",target_seq)
        stop_condition = False
        decoder_sentance = ''
        # print("Beforee the while loop")
        while not stop_condition:
            sample_word , decoder_h,decoder_c= decoder.predict([target_seq] + state_values_encoder)
            # print("sample_word: =>",sample_word)
            sample_word_index = np.argmax(sample_word[0,-1,:])
            # print("sample_word_index: ",sample_word_index)
            decoder_word = reverse_word_map_target[sample_word_index]
            decoder_sentance += ' '+ decoder_word
            # print("decoded word:=>",decoder_word)
            # print(len(decoder_sentance))
            # print("len(decoder_sentance) > 70: ",len(decoder_sentance) > 70)
            # print('decoder_word == "end"',decoder_word == 'end')
            # print(decoder_word == 'end' or len(decoder_sentance) > 70)
            # stop condition for the while loop
            if (decoder_word == 'end' or 
                len(decoder_sentance) > 50):
                stop_condition = True
                # print("from if condition")
            # target_seq = np.zeros((1,1))
            target_seq[0, 0] = sample_word_index
            # print(target_seq)
            state_values_encoder = [decoder_h,decoder_c]

        marathi_sentance = decoder_sentance[:-4]
        # logger.debug("Marathi sentance:",marathi_sentance)
        k.backend.clear_session()
        return{"original input":sentance, "Marathi Sentance": marathi_sentance},200


api.add_resource(Translate, '/<string:sentance>')

if __name__ == '__main__':
    app.run("0.0.0.0",port="5000",debug=True)
