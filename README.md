# Virtual Paint
Turn your webcam into a digital canvas! Using Python and OpenCV, you can draw in mid air just by waving colorful markers in front of your camera.

## Key Features
### 1. Smooth Air Painting
Draw lines in real-time using marker tracking logic.
* **Persistent Canvas Logic:** <br>
Uses a separate canvas layer designed to keep frame rendering lighter. *(Note: Performance and smoothness may vary depending on your webcam quality and room lighting conditions).* <br><br>
* **Anti-Teleportation:** <br>
Automatically detects when the marker is lifted or hidden to minimize accidental messy lines cutting across the screen. <br><br>
<img src="output/01_output.gif" width="380">
<br><br>

---

## Upcoming Features
I am having fun and actively developing this project! Here are the features planned for the next updates:

- [ ] **Smart Eraser Tool:** Easily wipe out specific mistakes by toggling an eraser mode.
- [ ] **Clear Screen Button:** Clear the entire canvas instantly with a single action.
- [ ] **↩ Undo / Redo System:** Go back and forth between your brush strokes.