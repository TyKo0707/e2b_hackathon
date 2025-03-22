# AI Agent for Slide Animation

---
We developed an **AI agent** capable of generating animated versions of slides provided as input.  
The pipeline consists of **three main steps**:

1. **Slide Processing & Description**  
   The input file is analyzed and converted into a detailed textual description of its content.

2. **Scene Generation**  
   Based on the extracted description, scenes are generated to visually represent the information.

3. **Code Generation & Execution**  
   Using Anthropic's **Claude** model, we generate Manim-compatible code for each scene.  
   The resulting code is executed in an **e2b.Sandbox** environment based on a Docker template.

---

You can see a visual representation of the pipeline in the image below.
<p align="center">
  <img src="https://github.com/user-attachments/assets/1b22dccd-5e0d-427a-8a2d-f1448cef252c" width="400" title="Figure 1">
</p>
<p align="center">Figure 1: Visualization of the pipeline</p>

---

A video demonstration of the system in action is shown below.
[backprop](https://raw.githubusercontent.com/TyKo0707/e2b_hackathon/blob/main/output/BACKPROP.mp4)


