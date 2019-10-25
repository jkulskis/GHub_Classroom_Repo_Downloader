import os
import requests
import git
import shutil
from getpass import getpass

ORG = 'EC327-Fall2019'

def parse_students():
	students = []
	student_count = 0
	while True:
		filename = input("Enter the path to your usernames file: ")
		if os.path.exists(filename):
			break
		print("Invalid file")
	with open(filename, 'r') as file:
		for line in file:
			if line.rstrip('\n'):
				student_count += 1
				students.append(line.rstrip('\n'))
	print(f'Succesfully parsed {student_count} student usernames')
	return students, student_count

def get_credentials():
	username = input("Enter either your GitHub username or email: ")
	password = getpass("Enter your GitHub password: ")
	return username, password

def download_assignments(students, username, password):
	assignment = input("Enter the assignment name (ex: PA1): ")
	assignment_path = input("Enter the directory to dump all the repos (leave blank to use assignment name): ")
	if not assignment_path.replace(' ', ''):
		assignment_path = assignment
	os.makedirs(assignment_path, exist_ok=True)
	success_count = 0
	fail_students = []
	for student in students:
		student_path = os.path.join(assignment_path, student)
		if (os.path.exists(student_path)):
			shutil.rmtree(student_path)
		os.makedirs(student_path)
		try:
			git.Git(student_path).clone(f"https://{username}:{password}@github.com/{ORG}/{assignment}-{student}.git", assignment)
			print(f"Cloned {assignment} repo of student {student} to {student_path}")
			success_count += 1
		except Exception as e:
			print(f"Failed to clone {assignment} repo of student {student}")
			print(f"Error: {e}")
			shutil.rmtree(student_path)
			fail_students.append(student)
	print(f"\nSuccesfully downloaded {success_count} repos")
	print(f"Failed to download {len(fail_students)} repos\n")
	if (len(fail_students)):
		print(f"Failed for students: {fail_students}\n")

if __name__ == '__main__':
	students, student_count = parse_students()
	username, password = get_credentials()
	download_assignments(students, username, password)
