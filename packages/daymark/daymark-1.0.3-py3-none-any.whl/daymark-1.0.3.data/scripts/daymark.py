#import psutil
import requests
import time
import os,sys
from redis import Redis
#import boto
#from boto.s3.key import Key

#Global instances

#Timestamp converter

r = time.ctime(time.time())

#redis connection instance

rmaster = 0

class daymark():
	
	#Function to initialize basic configuration

	def init():
		#Connects to redis master running inside the same kubernetes cluster in 'default' namespace
		rmaster = Redis(host ="redis-master.default.svc.cluster.local")
	
	
	
	#function logs string to stdout in red & exits the code

	def logError(errorMsg):
		print("\033[1;31;40m %s: %s \n " % (r, errorMsg) + "\n > Unfortunately Exiting the system!")
		sys.exit(1)
	
	
	
	#function logs string to stdout in green & exits the code

	def logSuccessful(successMsg):
		print("\033[1;32;40m %s: %s \n" % (r, successMsg) + "> Successfully Exiting the system!")
		sys.exit(0)
	
	
	
	#function logs string to stdout in yellow

	def logWarning(warningMsg):
		print("\033[1;33;40m %s time = %s \n" % (warningMsg, r))
	
	
	
	#function returns the progress percentage

	def getProgress(file_processed_count, total_file_count):
		per = (float(file_processed_count)/float(total_file_count))*100
		return per	
	
	
	
	#function shows the progress

	def showProgress(self, file_processed_count):
		
		prog = '%d files (%.2f%%)' % (file_processed_count, self.percentDone())
		return prog

	
	'''
	#Resource Monitor

	def showResourceUsage(self):
		#CPU frequency usage

		print(psutil.cpu_freq() + "-> current frequency usage")
		#CPU memory usage
		
		print(psutil.virtual_memory() + "-> current memory usage")
	'''
	
	
	#function to push data to s3 bucket

	'''def pushToS3(url):
		#Credentials of AWS
		AWS_ACCESS_KEY_ID = ''
		AWS_SECRET_ACCESS_KEY = ''
		
		bucket_name = AWS_ACCESS_KEY_ID.lower() + '-dump'
		
		filename = ''

		#Connecting
		conn = boto.connect_s3(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
		bucket = conn.create_bucket(bucket_name, location=boto.s3.connection.Location.DEFAULT)

		print('Uploading %s to Amazon S3 bucket %s' % (filename, bucket_name))

		def percent_cb(complete, total):
    		sys.stdout.write('')	
    		sys.stdout.flush()
		
		k = Key(bucket)
		k.key = 'my test file'
		k.set_contents_from_filename(testfile, cb=percent_cb, num_cb=10)
	'''
	
	
	#function to get environment variable

	def getEnvVar(name):
		#Function to get environment variable named jobId 
		
		id = os.environ[name]
		return id

	
	
	#Set progress in redis-master

	def setProgress(key, value):
		#Setting progress in redis-master
		
		rmaster.set(key, value)
		#print(redisClient.get(key))

	
	
	#Function to download a file from a given url

	def downloader(self, Url):
		
		if Url:
			try:
				req = requests.get(url, allow_redirects=True)
        		size = int(req.headers['content-length'])
        		total = size/chunk_size
       	 		count = 0
        		filename = url.split('/')[-1]
        		with open(filename, 'wb') as f:
            		for data in tqdm( iterable = req.iter_content(chunk_size = chunk_size), total = size/chunk_size, unit = 'B'):
                		f.write(data)
                		count += 1
                		'''#id = self.getJobId()
                		#per = self.percentDone(count, total)
                		#self.createKey(id, per)'''
        		if(count == size):
            		self.logSuccessful("Download complete")
       			else:
            		raise Exception('The file could not be downloaded') 
    		except Exception as e:
        		self.logError(e)
		else:
    		self.logError("URL Unavailable")