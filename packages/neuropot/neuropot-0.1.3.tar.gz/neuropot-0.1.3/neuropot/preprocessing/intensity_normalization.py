from __future__ import print_function
import SimpleITK as sitk
import subprocess, sys, os

def n4_normalization(input_filename,workdir="workdir",output_filename="image_N4.nii"):
	os.chdir(os.path.dirname(__file__))
	path = os.getcwd()
	res = path + "/" + workdir + "/" + output_filename
	try:
		inputImage = sitk.ReadImage( input_filename )

		# if len ( argv ) > 4:
		#     maskImage = sitk.ReadImage( argv[4] )
		# else:
		#     maskImage = sitk.OtsuThreshold( inputImage, 0, 1, 200 )

		# if len ( argv ) > 3:
		#     inputImage = sitk.Shrink( inputImage, [ int(argv[3]) ] * inputImage.GetDimension() )
		#     maskImage = sitk.Shrink( maskImage, [ int(argv[3]) ] * inputImage.GetDimension() )

		inputImage = sitk.Cast( inputImage, sitk.sitkFloat32 )
		corrector = sitk.N4BiasFieldCorrectionImageFilter();
		numberFittingLevels = 4

		# if len ( argv ) > 6:
		#     numberFittingLevels = int( argv[6] )

		# if len ( argv ) > 5:
		#     corrector.SetMaximumNumberOfIterations( [ int( argv[5] ) ] *numberFittingLevels  )

		output = corrector.Execute( inputImage )
		sitk.WriteImage( output, res )
	except Exception as e:
		print("We got an Exception in n4")
		print(e)
		res = False;

	return res