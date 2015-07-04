
/*
    Copyright 2012 Andrew Perrault and Saurav Kumar.

    This file is part of DetectText.

    DetectText is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    DetectText is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with DetectText.  If not, see <http://www.gnu.org/licenses/>.
*/
#include <boost/python/module.hpp>
#include <boost/python/def.hpp>
    
#include <cassert>
#include <fstream>
#include "TextDetection.h"
#include <opencv/highgui.h>
#include <exception>

using namespace boost::python;

void convertToFloatImage ( IplImage * byteImage, IplImage * floatImage )
{
  cvConvertScale ( byteImage, floatImage, 1 / 255., 0 );
}

class FeatureError : public std::exception
{
std::string message;
public:
FeatureError ( const std::string & msg, const std::string & file )
{
  std::stringstream ss;

  ss << msg << " " << file;
  message = msg.c_str ();
}
~FeatureError () throw ( )
{
}
};

IplImage * loadByteImage ( const char * name )
{
  IplImage * image = cvLoadImage ( name );

  if ( !image )
  {
    return 0;
  }
  cvCvtColor ( image, image, CV_BGR2RGB );
  return image;
}

IplImage * loadFloatImage ( const char * name )
{
  IplImage * image = cvLoadImage ( name );

  if ( !image )
  {
    return 0;
  }
  cvCvtColor ( image, image, CV_BGR2RGB );
  IplImage * floatingImage = cvCreateImage ( cvGetSize ( image ),
                                             IPL_DEPTH_32F, 3 );
  cvConvertScale ( image, floatingImage, 1 / 255., 0 );
  cvReleaseImage ( &image );
  return floatingImage;
}

void mainTextDetection ( char * filename, char * filenameO )
{
  IplImage * byteQueryImage = loadByteImage ( filename );
  if ( !byteQueryImage )
  {
    printf ( "couldn't load query image\n" );
    return;
  }

  // Detect text in the image
  // Take as black on white background, aka 1
  IplImage * output = textDetection ( byteQueryImage, 1 );
  cvReleaseImage ( &byteQueryImage );
  cvSaveImage ( filenameO, output );
  cvReleaseImage ( &output );
  return;
}

BOOST_PYTHON_MODULE(cropText)
{
  def("mainTextDetection", mainTextDetection);
}