import cv2
import mediapipe as mp
import pygame
import numpy as np

# Initialize MediaPipe BlazePose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, model_complexity=2, enable_segmentation=False)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Load character sprites
goku_body = pygame.image.load('goku.png').convert_alpha()  # Goku's body


# Function to draw the character based on pose keypoints
def draw_character(keypoints):
    # Example mapping - you'll need to adjust based on your sprites
    head_x, head_y = int(keypoints[0][0] * 800), int(keypoints[0][1] * 600)
    shoulder_x, shoulder_y = int(keypoints[11][0] * 800), int(keypoints[11][1] * 600)
    hip_x, hip_y = int(keypoints[23][0] * 800), int(keypoints[23][1] * 600)

    # Blit the body at the hip position
    screen.blit(goku_body, (hip_x - goku_body.get_width() // 2, hip_y - goku_body.get_height() // 2))

    

def main():
    cap = cv2.VideoCapture(0)  # Use the webcam

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ret, frame = cap.read()
        if not ret:
            break

        # Convert the image to RGB
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform pose detection
        results = pose.process(image_rgb)

        # Clear Pygame screen
        screen.fill((255, 255, 255))

        # Draw the character on the Pygame screen
        if results.pose_landmarks:
            keypoints = [(lm.x, lm.y) for lm in results.pose_landmarks.landmark]
            draw_character(keypoints)

        # Update the display
        pygame.display.flip()
        clock.tick(30)

    cap.release()
    pygame.quit()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
