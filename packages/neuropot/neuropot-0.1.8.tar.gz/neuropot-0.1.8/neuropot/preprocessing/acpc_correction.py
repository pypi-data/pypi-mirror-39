import subprocess, os

def acpc_correction(input_filename,workdir="/workdir",output_filename="image_N4_acpc.nii",template_filename="vbm_template.nii",mat_filename="mat_N4_acpc.mat"):

	os.chdir(os.path.dirname(__file__))
	path = os.getcwd()

	workdir = path + workdir
	template_filename = path + "/template/" + template_filename
	output_filename = workdir + "/" + output_filename
	mat_filename = workdir + "/" + mat_filename

	process = None
	args = (workdir,input_filename,template_filename,output_filename,mat_filename)
	res = output_filename

	try:
		process = subprocess.Popen('ACPCAlignment.sh --workingdir=%s --in=%s --ref=%s --out=%s --omat=%s > /dev/null'%args, shell=True)
		process.wait()
	except Exception as e:
		print("We got an Exception")
		print(e)

	return res