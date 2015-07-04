PYTHON_VERSION = 2.7
PYTHON_INCLUDE = /usr/include/python$(PYTHON_VERSION)

BOOST_INC = /usr/local/include
BOOST_LIB = /usr/local/lib
OPENCV_LIB = $$(pkg-config --libs opencv)
OPENCV_INC = $$(pkg-config --cflags opencv)

TARGET = cropText
HELPER = TextDetection

DIR = ./

$(TARGET).so: $(TARGET).o
		g++ -shared -Wl,--export-dynamic \
		$(TARGET).o $(HELPER).o -L$(BOOST_LIB) \
		$(OPENCV_LIB) -L/usr/lib/python$(PYTHON_VERSION)/config \
		-lboost_python -lpython$(PYTHON_VERSION) \
		-o $(TARGET).so

$(TARGET).o: $(TARGET).cpp
		g++ -I$(PYTHON_INCLUDE) $(OPENCV_TAGS) -I$(BOOST_INC) -fPIC -c $(TARGET).cpp $(HELPER).cpp -I$(DIR)