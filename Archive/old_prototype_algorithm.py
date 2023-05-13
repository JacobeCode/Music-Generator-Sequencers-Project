# Old prototype model
# if note_highness < 28:
#     if points_to_use < 2:
#         self.music_info.index = 0
#     elif points_to_use < 3:
#         self.music_info.index = random.randint(0, 1)
#     elif points_to_use < 4:
#         self.music_info.index = random.randint(0, 2)
#     elif self.music_info.metrum > 1:
#         if points_to_use < 5:
#             self.music_info.index = random.randint(0, 3)
#         elif points_to_use < 7:
#             self.music_info.index = random.randint(0, 4)
#         elif points_to_use < 8:
#             self.music_info.index = random.randint(0, 5)
#         elif points_to_use < 9:
#             self.music_info.index = random.randint(0, 6)
#     elif points_to_use < 13 and self.music_info.metrum > 2:
#         self.music_info.index = random.randint(0, 7)
#     elif self.music_info.metrum > 3:
#         if points_to_use < 15:
#             self.music_info.index = random.randint(0, 8)
#         elif points_to_use < 17:
#             self.music_info.index = random.randint(0, 9)
#     elif points_to_use < 25 and self.music_info.metrum > 4:
#         self.music_info.index = random.randint(0, 10)
#     elif self.music_info.metrum > 5:
#         self.music_info.index = random.randint(0, 11)
#     elif self.music_info.metrum > 4:
#         self.music_info.index = random.randint(0, 10)
#     elif self.music_info.metrum > 3:
#         self.music_info.index = random.randint(0, 9)
#     elif self.music_info.metrum > 2:
#         self.music_info.index = random.randint(0, 7)
#     elif self.music_info.metrum > 1:
#         self.music_info.index = random.randint(0, 6)
#     else:
#         self.music_info.index = random.randint(0, 2)
#     self.music_info.melody.append(self.music_info.full_scale[note_highness] + self.music_info.durations[self.music_info.index])
#     points_to_use -= self.music_info.durations_weights[self.music_info.index]
# elif note_highness >= 28:
#     if points_to_use < 2:
#         self.music_info.index = 0
#     elif points_to_use < 3:
#         self.music_info.index = random.randint(0, 1)
#     elif points_to_use < 5:
#         self.music_info.index = random.randint(0, 2)
#     elif points_to_use < 9 and self.music_info.metrum > 1:
#         self.music_info.index = random.randint(0, 3)
#     elif points_to_use < 17 and self.music_info.metrum > 3:
#         self.music_info.index = random.randint(0, 4)
#     elif self.music_info.metrum > 3:
#         self.music_info.index = random.randint(0, 4)
#     elif self.music_info.metrum > 1:
#         self.music_info.index = random.randint(0, 3)
#     else:
#         self.music_info.index = random.randint(0, 2)
#     self.music_info.melody.append(self.music_info.full_scale[28] + self.music_info.rest_durations[self.music_info.index])
#     points_to_use -= self.music_info.rest_durations_weights[self.music_info.index]