from os import system; import time

def ask_user_for_time_intervals():
	global desired_loop_time, desired_average_time, desired_upload_time
	print "HOWDY. Welcome to the Met Station."
	while True:
		desired_loop_time=int(raw_input("Enter the number of seconds between looping: "))
		desired_average_time=int(raw_input("Enter the number of seconds between averaging: "))
		desired_upload_time=int(raw_input("Enter the number of seconds between uploading: "))
		if desired_loop_time < desired_average_time and desired_average_time < desired_upload_time:
			return desired_loop_time, desired_average_time, desired_upload_time
			break
		else:
			print "Remember: The upload time > averaging time > looping time."
			print "Try again."
	raw_input("Press enter when ready and wait.")

def zero_loop_timer(): #Start/reset the looping timer
	loop_time = time.time() + desired_loop_time 
	return loop_time

def zero_average_timer(): #Start/reset the averaging timer
	average_time = time.time() + desired_average_time
	return average_time

def zero_upload_timer(): #Start/reset the time between uploads
	upload_time = time.time() + desired_upload_time  
	return upload_time

def print_to_display(loops, averages, uploads):
        system('clear')
        print '%s\nTotal Loops Ran: %s\nAverages Completed: %s\nUploads Completed: %s' \
              % (time.strftime('%H:%M:%S', time.gmtime()), loops, averages, uploads)
