import subprocess, os

def skull_stripping(input_filename,workdir="/workdir",output_filename="image_N4_acpc_ss03.nii"):

	os.chdir(os.path.dirname(__file__))
	path = os.getcwd()

	workdir = path + workdir
	output_filename = workdir + "/" + output_filename

	process = None
	args = (input_filename,output_filename)
	res = output_filename

	try:
		process = subprocess.Popen('/usr/local/fsl/bin/bet %s %s -B -f 0.3 -g 0 > /dev/null'%args, shell=True)
		process.wait()
	except Exception as e:
		print("We got an Exception in ss03")
		print(e)

	return res