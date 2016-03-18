# if not self.room.isPositionInRoom(temp_position):
#     if temp_position.getY() > self.room.height:
#         if 0 <= self.direction <= 90:
#             self.direction = abs(self.direction - 360)
#         elif 90 <= self.direction <= 180:
#             self.direction = self.direction + 90
#     if temp_position.getY() < 0:
#         if 180 <= self.direction <= 270:
#             self.direction = self.direction - 90
#         elif 270 <= self.direction <= 360:
#             self.direction = (self.direction + 90) % 360
#     if temp_position.getX() > self.room.width:
#         if 0 <= self.direction <= 90:
#             self.direction += 90
#         elif 270 <= self.direction <= 360:
#             self.direction = self.direction - 90
#     if temp_position.getX() < 0:
#         if 180 <= self.direction <= 270:
#             self.direction += 90
#         elif 90 <= self.direction <= 180:
#             self.direction -= 90
#     print temp_position, "angle", self.direction
# if 0 <= self.direction <= 180:
#     self.direction = random.randrange(181, 360)
# elif 181 <= self.direction <= 359:
#     self.direction = random.randrange(0, 180)
# #print self.robot_position
# self.direction = (self.direction + 60) % 360
# self.speed = -self.speed