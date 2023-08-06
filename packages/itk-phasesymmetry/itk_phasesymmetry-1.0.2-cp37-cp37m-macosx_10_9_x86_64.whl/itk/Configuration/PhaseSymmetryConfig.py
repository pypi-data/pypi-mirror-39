depends = ('ITKPyBase', 'ITKImageSources', 'ITKImageIntensity', 'ITKFFT', 'ITKCommon', )
templates = (
  ('SinusoidSpatialFunction', 'itk::SinusoidSpatialFunction', 'itkSinusoidSpatialFunctionF2PD2', True, 'float,2,itk::Point< double,2 >'),
  ('SinusoidSpatialFunction', 'itk::SinusoidSpatialFunction', 'itkSinusoidSpatialFunctionF3PD3', True, 'float,3,itk::Point< double,3 >'),
  ('SinusoidImageSource', 'itk::SinusoidImageSource', 'itkSinusoidImageSourceIF2', True, 'itk::Image< float,2 >'),
  ('SinusoidImageSource', 'itk::SinusoidImageSource', 'itkSinusoidImageSourceIF3', True, 'itk::Image< float,3 >'),
  ('SteerableFilterFreqImageSource', 'itk::SteerableFilterFreqImageSource', 'itkSteerableFilterFreqImageSourceIF2', True, 'itk::Image< float,2 >'),
  ('SteerableFilterFreqImageSource', 'itk::SteerableFilterFreqImageSource', 'itkSteerableFilterFreqImageSourceIF3', True, 'itk::Image< float,3 >'),
  ('ButterworthFilterFreqImageSource', 'itk::ButterworthFilterFreqImageSource', 'itkButterworthFilterFreqImageSourceIF2', True, 'itk::Image< float,2 >'),
  ('ButterworthFilterFreqImageSource', 'itk::ButterworthFilterFreqImageSource', 'itkButterworthFilterFreqImageSourceIF3', True, 'itk::Image< float,3 >'),
  ('LogGaborFreqImageSource', 'itk::LogGaborFreqImageSource', 'itkLogGaborFreqImageSourceIF2', True, 'itk::Image< float,2 >'),
  ('LogGaborFreqImageSource', 'itk::LogGaborFreqImageSource', 'itkLogGaborFreqImageSourceIF3', True, 'itk::Image< float,3 >'),
  ('PhaseSymmetryImageFilter', 'itk::PhaseSymmetryImageFilter', 'itkPhaseSymmetryImageFilterIF2IF2', True, 'itk::Image< float,2 >, itk::Image< float,2 >'),
  ('PhaseSymmetryImageFilter', 'itk::PhaseSymmetryImageFilter', 'itkPhaseSymmetryImageFilterIF3IF3', True, 'itk::Image< float,3 >, itk::Image< float,3 >'),
)
snake_case_functions = ('steerable_filter_freq_image_source', 'log_gabor_freq_image_source', 'phase_symmetry_image_filter', 'butterworth_filter_freq_image_source', 'sinusoid_image_source', )
