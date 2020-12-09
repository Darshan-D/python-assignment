import face_recognition
import pygame
from transitions import Machine

# Initialize pygame
pygame.init()
pygame.font.init()

# Setting up pygame
font = pygame.font.SysFont('Arial', 15)

# Width and height of the pygame window
X, Y = 400, 400

# Colors to be used in pygame display
black = (0, 0, 0)
white = (255, 255, 255)

# Setting up pygame window
display_surface = pygame.display.set_mode((X, Y))
pygame.display.set_caption('Face Recognition') 

# Since the webcam is not working, loading a bunch of images,
# and going throught them one by one
# It simulates the diffrent frame we would have gotten from
# an actual camera
IMAGES = [
'/home/darshan/Internship/images/om2.jpeg',
'/home/darshan/Internship/images/opm1.jpeg',
'/home/darshan/Internship/images/obama1.jpeg',
'/home/darshan/Internship/images/putin1.jpeg',
'/home/darshan/Internship/images/elon1.jpeg',
'/home/darshan/Internship/images/pm1.jpeg',
'/home/darshan/Internship/images/car3.jpeg',
'/home/darshan/Internship/images/obama4.jpeg',
'/home/darshan/Internship/images/car1.jpeg',
]



# Images processed
img_processed = 0

# Store the names of the found faces in this list
face_names = []


# Setting up the finite state machine
class FaceRecognitionMachine(object):
	
	# Defining the states of the machine
	states = ['MachineActive', 'MachineInactive']

	def __init__(self):

		# Initializing the machine
		self.machine = Machine(model = self, states=FaceRecognitionMachine.states, initial = 'MachineInactive')

		# Adding the transitions
		self.machine.add_transition(trigger='found', source='MachineInactive', dest='MachineActive')

		self.machine.add_transition(trigger='not_found', source='MachineActive', dest='MachineInactive')

# Used to render the text on the pygame window
def render_text(face_names, curr_state):

	# Coordinates for inital fonts to display
	x, y = 10, 275
	
	# If Current State is MachineInactive, 
	# display 'Application is Inactive'
	if curr_state == 'MachineInactive':
		state_render = 'Application is Inactive'
		state = font.render(state_render, True, white)
		display_surface.blit(state, [10, 350])
		pygame.display.update()

	# Else Display the name of the person
	for face in face_names:
		text = font.render(face, True, white)
		display_surface.blit(text, [x, y])
		pygame.display.update()
		y += 15	

# Initialize the state machine
statemachine = FaceRecognitionMachine()
curr_state = statemachine.state
print("\nState Machine Created***")
print("Current State: ", curr_state)

# Load the known faces
obama_image = face_recognition.load_image_file("/home/darshan/Internship/images/obama1.jpeg")
modi_image = face_recognition.load_image_file("/home/darshan/Internship/images/modi2.jpeg")

# Encode the known faces
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
modi_face_encoding = face_recognition.face_encodings(modi_image)[0]

# Store the known faces and encodings in a list
known_face_encodings = [obama_face_encoding, modi_face_encoding]
known_face_names = ["Barack Obama", "Narendra Modi"]


# If the input would have been an actual camera, the condition
# would have been True, and we would look out for QUIT event
# inorder to stop the infinite loop
# But since webcam is not working, we would loop till we have
# processed all the image
while img_processed < len(IMAGES):
	
	print('-----------------')
	print('Image Number: ', img_processed)
	# Loading the image in pygame
	image_pg = pygame.image.load(IMAGES[img_processed])

	# Filling the surface with black color, this will overlay
	# on any previous pygame renders, thus giving a clean black screen
	display_surface.fill(black)

	# Display the current image in pygame
	display_surface.blit(image_pg, (0,0))

	# Read the image for face recognition
	unknown_image = face_recognition.load_image_file(IMAGES[img_processed])
	
	# Figure out the location of the faces in the unknown image
	face_locations = face_recognition.face_locations(unknown_image)

	# Encode the face found from the unknown image
	face_encodings = face_recognition.face_encodings(unknown_image, face_locations)
	
	# Loop throught the encoded faces and compare it with encoding of knwon faces
	for face_encoding in face_encodings:
		matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
			
		# By Default set the name of the person to unknown
		name = "Unknown"

		# If a known person is found, figure out his name
		if True in matches:
			first_match_index = matches.index(True)
			name = known_face_names[first_match_index]

			# Since a match is found trigger the state machine
			if (statemachine.state != 'MachineActive'):
				statemachine.trigger('found')
				curr_state = statemachine.state

		face_names.append(name)


	# If no faces detected in the image, set the machine state to MachineInactive
	if not len(face_names):

		# Change State to Inactive only if it was Active Previously
		# Otherwise keep it as it is		
		if (statemachine.state != 'MachineInactive'):
			statemachine.trigger('not_found')
			curr_state = statemachine.state

	# Calling the text render function to render the identified faces and current machine state
	render_text(face_names, curr_state)
	
	# Looking out for the QUIT event
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			quit()

	# Updating the pygame display
	pygame.display.update()

	# Current State and Faces found
	print("Identified Faces: ", face_names)
	print("Current State: ", curr_state)

	# Delay to inspect the results, wont be there when using
	# stream from webcam
	pygame.time.delay(2000)
	img_processed += 1
	face_names = []

print("\nExecution Done***")
