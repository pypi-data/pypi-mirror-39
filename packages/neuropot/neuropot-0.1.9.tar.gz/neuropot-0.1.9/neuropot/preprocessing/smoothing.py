import subprocess, os

def smoothing(input_filename,workdir="/workdir",output_filename="image_N4_acpc_ss03_seg_01_registered_smooth"):

	os.chdir(os.path.dirname(__file__))
	path = os.getcwd()

	workdir = path + workdir
	output_filename = workdir + "/" + output_filename

	process = None
	args = (input_filename,output_filename)
	res = output_filename

	try:
		process = subprocess.Popen('fslmaths %s -s 3.3972872011520763 %s > /dev/null'%args, shell=True)
		process.wait()
	except Exception as e:
		print("We got an Exception in smoothing")
		print(e)

	return res+".nii.gz"