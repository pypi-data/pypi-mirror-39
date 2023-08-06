import keras
import keras.backend as K
from keras.models import Model
from keras.layers import Input,TimeDistributed,Flatten,Dropout,Dense,BatchNormalization,ReLU,Lambda
from keras.applications import VGG16,VGG19,Xception,ResNet50,InceptionV3,InceptionResNetV2,DenseNet121,DenseNet169,DenseNet201

def cnn(i_cnn_architecture = 'VGG19',
       i_input_shape       = (224,224,3),
       i_sequence_size     = 1,
       i_dropout           = 0.5,
       i_num_class         = 2,
       i_num_neurons       = 4096,
       i_combine_method    = 'Concatenate'):
    _new_input_shape = tuple([i_sequence_size]) + i_input_shape
    _input_sequences = Input(shape=_new_input_shape)
    if i_cnn_architecture == 'VGG16':
        _cnn_model = VGG16(include_top=False, weights='imagenet', pooling='avg', input_shape=i_input_shape)
    elif i_cnn_architecture == 'Xception':
        _cnn_model = Xception(include_top=False, weights='imagenet', pooling='avg', input_shape=i_input_shape)
    elif i_cnn_architecture == 'Resnet':
        _cnn_model = ResNet50(include_top=False,weights='imagenet',pooling='avg', input_shape=i_input_shape)
    elif i_cnn_architecture == 'Inception':
        _cnn_model = InceptionV3(include_top=False,weights='imagenet',pooling='avg', input_shape=i_input_shape)
    elif i_cnn_architecture == 'Inception_resnet':
        _cnn_model = InceptionResNetV2(include_top=False,weights='imagenet',pooling='avg', input_shape=i_input_shape)
    elif i_cnn_architecture == 'Densenet_121':
        _cnn_model = DenseNet121(include_top=False,weights='imagenet',pooling='avg', input_shape=i_input_shape)
    elif i_cnn_architecture == 'Densenet_169':
        _cnn_model = DenseNet169(include_top=False, weights='imagenet', pooling='avg', input_shape=i_input_shape)
    elif i_cnn_architecture == 'Densenet_201':
        _cnn_model = DenseNet201(include_top=False, weights='imagenet', pooling='avg', input_shape=i_input_shape)
    else:
        _cnn_model = VGG19(include_top=False, weights='imagenet', pooling='avg', input_shape=i_input_shape)
    """-----------------------------------------------------------------------------------------------------------------
                                              Extract texture features for our model.
    -----------------------------------------------------------------------------------------------------------------"""
    _cnn_feature_maps = TimeDistributed(_cnn_model,input_shape=_new_input_shape)(_input_sequences)
    _cnn_feature_maps = TimeDistributed(Flatten())(_cnn_feature_maps)
    _cnn_feature_maps = TimeDistributed(Dense(units=i_num_neurons))(_cnn_feature_maps)
    _cnn_feature_maps = TimeDistributed(BatchNormalization())(_cnn_feature_maps)
    _cnn_feature_maps = TimeDistributed(ReLU())(_cnn_feature_maps)
    if i_combine_method == 'Multiply':
        _combined_features = Lambda(time_distributed_mul,name='Features')(_cnn_feature_maps)
    elif i_combine_method == 'Add':
        _combined_features = Lambda(time_distributed_add,name='Features')(_cnn_feature_maps)
    elif i_combine_method == 'Subtract':
        _combined_features = Lambda(time_distributed_sub,name='Features')(_cnn_feature_maps)
    elif i_combine_method == 'Maximum':
        _combined_features = Lambda(time_distributed_max,name='Features')(_cnn_feature_maps)
    else:
        _combined_features = Flatten(name='Features')(_cnn_feature_maps)
    #_combined_features = Dropout(rate=i_dropout)(_combined_features)
    #_combined_features = Dense(units=i_num_neurons,activation='relu')(_combined_features)
    _combined_features = Dropout(rate=i_dropout)(_combined_features)
    _combined_features = Dense(units=i_num_class, activation='softmax', name='Output')(_combined_features)
    _model = Model(inputs=[_input_sequences], outputs=[_combined_features])
    _optimizer = keras.optimizers.Adam(lr=0.00001)
    #_optimizer = keras.optimizers.SGD(lr=0.001)
    _model.compile(optimizer=_optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
    return _model

def time_distributed_mul(x):
    """
    :param x: in shape of [None, time_step, feature_dims]
    :return: addition of all features at time_steps
    """
    _x_shape = x.shape
    _num_dims = len(_x_shape)
    assert _num_dims == 3
    _time_step,_feature_dims = x.shape[1],x.shape[2]
    if _time_step == 1:
        _output = x[:, 0, :]
    else:
        _output = x[:,0,:]
        for _index in range(1, _time_step):
            _output *= x[:,_index,:]
    return _output

def time_distributed_add(x):
    """
    :param x: in shape of [None, time_step, feature_dims]
    :return: addition of all features at time_steps
    """
    _x_shape = x.shape
    _num_dims = len(_x_shape)
    assert _num_dims == 3
    _time_step,_feature_dims = x.shape[1],x.shape[2]
    if _time_step == 1:
        _output = x[:,0,:]
    else:
        _output = x[:,0,:]
        for _index in range(1, _time_step):
            _output += x[:,_index,:]
    return _output

def time_distributed_sub(x):
    """
    :param x: in shape of [None, time_step, feature_dims]
    :return: addition of all features at time_steps
    """
    _x_shape = x.shape
    _num_dims = len(_x_shape)
    assert _num_dims == 3
    _time_step,_feature_dims = x.shape[1],x.shape[2]
    if _time_step == 1:
        _output = x[:, 0, :]
    else:
        _output = x[:,0,:]
        for _index in range(1, _time_step):
            _output -= x[:,_index,:]
    return _output

def time_distributed_max(x):
    """
    :param x: in shape of [None, time_step, feature_dims]
    :return: addition of all features at time_steps
    """
    _x_shape = x.shape
    _num_dims = len(_x_shape)
    assert _num_dims == 3
    _time_step,_feature_dims = x.shape[1],x.shape[2]
    if _time_step == 1:
        _output = x[:, 0, :]
    else:
        _output = x[:,0,:]
        for _index in range(1, _time_step):
            _output = K.maximum(_output,x[:,_index,:])
    return _output

if __name__ == '__main__':
    model = cnn()
    model.summary()