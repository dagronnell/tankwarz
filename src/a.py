import math

def calculate_angle(pos1, pos2):
    dx = pos2[0] - pos1[0]
    dy = pos1[1] - pos2[1]  # Inverterad eftersom y-axeln är omvänd
    angle_radians = math.atan2(dy, dx)
    angle_degrees = math.degrees(angle_radians)
    # Justera så att 0 grader är uppåt och öka medurs
    return (90 - angle_degrees) % 360

# Testa koden
pos1 = (100, 100)
pos2 = (100, 110)
print("Vinkel mellan pos1 och pos2:", calculate_angle(pos1, pos2))
