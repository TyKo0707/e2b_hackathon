# TTA: Text-to-Animation Model

---
We developed an **AI agent** capable of generating animated videos from textual data provided as an input.  
The pipeline consists of **three main steps**:

1. **Input Processing & Description**  
   The input data is analyzed and converted into a detailed textual description of its content.

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
[Directory with demonstrations of work.](https://github.com/TyKo0707/e2b_hackathon/tree/main/demos)


## Usage

To generate animation run the below command.
```bash
python script.py --query "Your animation description here" [--pdf path/to/document.pdf] [--output-dir output_folder]
```

For example, if you want to animate backpropagation, run: `python script.py --query "Create an animation showing backpropagation in neural networks"`.

Or, if you want to feed it PDF to generate animation that would explain you probability distribution, you might run 

```bash
python3 generate_animation_cli.py --query "Generate a very short Manim animationthat would explain probability distributions in the attached PDF. Keep the animation short, the length of the scene should not exceed 100 lines." --pdf=./assets/example2.pdf
```