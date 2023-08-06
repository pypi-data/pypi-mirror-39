# TPUColab

Unlike GPU, to make code work in TPU, code needs to be changed.

TPUColab is a library to make TPU working in Colab Google with **less code modification**.

In most cases, only 2 lines code change is enough *(not count the line of importing tpucolab)*.

## Install

    pip install tpucolab

In Colab Google Jupyter, for auto install and ensure using latest version of TPUColab, please add "!pip install -U tpucolab" at the first line of Jupyter cell

## Requirements

    Tensorflow

## Import

    from tpucolab import *

## Initialization

    tpucolab = TPUColab()

After initialization, text "Found TPU" will be shown in Colab Google Jupyter output

PS: If Initialization failed, please retry later. Google Colab, unfortunately, has TPU memory allocation issue occasionally.

## Turn ordinal compiled Keras model to TPU model

    tpucolab.compiled_model_to_tpu_model(model)
    
Now model is compatible with TPU

## Train TPU model

Just as the same as ordinal Keras model, e.g.:

    model.fit(X_train,Y_train,validation_data=(X_test,Y_test),epochs=9999)
    
Other Keras model functions can also be invoked in TPU model as usual.

## Important Note
The following keras object (include but not all) should not be imported from keras.* . Should be imported from tensorflow.keras.*

Sequential, Model, Dense, Dropout, Flatten, Conv2D, MaxPooling2D

e.g. (wrong)

    from keras.models import Sequential, Model
    from keras.layers import Dense, Dropout, Flatten
    from keras.layers import Conv2D, MaxPooling2D

e.g. (correct)

    from tensorflow.keras.models import Sequential, Model
    from tensorflow.keras.layers import Dense, Dropout, Flatten
    from tensorflow.keras.layers import Conv2D, MaxPooling2D


## Thanks

Google
