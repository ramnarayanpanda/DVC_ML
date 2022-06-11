# here our file stage_02.py read artifacts01.txt file which will be generated only when stage_01.py is run

-> pip --default-timeout=1000 install dvc
-> git init 
-> dvc init 
# it will run all the dependencies one by one, and will generate a lock file 
-> dvc repro (reproduce) 

# again if you run dvc repro it will not generate lock file again, cause we have already reproduced our code 
-> dvc repro 

# in lock file it will create a hash value stored in md5: cef7ccd89dacf1ced6f5ec91d759953f, this hash value is specific to every dependency 

# below will show you the dag in a nice format 
-> dvc dag