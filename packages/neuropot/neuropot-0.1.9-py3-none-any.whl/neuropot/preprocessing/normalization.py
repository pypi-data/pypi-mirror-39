import subprocess, os

def normalization(input_filename,workdir="/workdir",output_filename="image_N4_acpc_ss03_seg_01_registered",template_filename="vbm_template.nii",mat_filename="mat_N4_acpc.mat"):

	os.chdir(os.path.dirname(__file__))
	path = os.getcwd()

	workdir = path + workdir
	template_filename = path + "/template/" + template_filename
	output_filename = workdir + "/" + output_filename
	mat_filename = workdir + "/" + mat_filename

	process = None
	args = (input_filename,template_filename,output_filename,mat_filename)
	res = output_filename

	try:
		process = subprocess.Popen('flirt -in %s -ref %s -out %s -omat %s -bins 256 -cost corratio -searchrx -90 90 -searchry -90 90 -searchrz -90 90 -dof 12  -interp trilinear > /dev/null'%args, shell=True)
		process.wait()
	except Exception as e:
		print("We got an Exception in normalization")
		print(e)

	return res