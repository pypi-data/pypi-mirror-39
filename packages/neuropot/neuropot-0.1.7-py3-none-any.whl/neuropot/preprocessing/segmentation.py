import subprocess, os

def gm_segmentation(input_filename,workdir="/workdir"):

	os.chdir(os.path.dirname(__file__))
	path = os.getcwd()

	workdir = path + workdir
	output_basename = workdir + "/" + input_filename.split("/")[-1].split(".")[0]

	process = None
	args = (output_basename,input_filename)
	res = output_basename + "_seg_1"

	try:
		process = subprocess.Popen('/usr/local/fsl/bin/fast -t 1 -n 3 -g -o %s %s > /dev/null'%args, shell=True)
		process.wait()
	except Exception as e:
		print("We got an Exception in segmentation")
		print(e)

	return res

def wm_segmentation(input_filename,workdir="/workdir"):

	os.chdir(os.path.dirname(__file__))
	path = os.getcwd()

	workdir = path + workdir
	output_basename = workdir + "/" + input_filename.split("/")[-1].split(".")[0]

	process = None
	args = (output_basename,input_filename)
	res = output_basename + "_seg_0"

	try:
		process = subprocess.Popen('/usr/local/fsl/bin/fast -t 1 -n 3 -g -o %s %s > /dev/null'%args, shell=True)
		process.wait()
	except Exception as e:
		print("We got an Exception in segmentation")
		print(e)

	return res